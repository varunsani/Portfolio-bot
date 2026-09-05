"""
Indexing pipeline. Run manually or via .github/workflows/reindex.yml.

Sources indexed:
  - content/portfolio.md     (scraped live site, chunked per-section)
  - Varun's resume           (fetched live from Google Drive on every run -
                               never committed to the repo, so editing the
                               resume on Drive is the only step needed)
  - research paper PDF       (chunked by paragraph; extraction is per-page,
                               so an image/formula-heavy page that fails to
                               extract cleanly doesn't take the rest of the
                               document down with it)
  - ALL of Varun's public, non-fork GitHub repos (auto-discovered via the
                               GitHub API, not a hardcoded list - new repos
                               are picked up on the next scheduled run).
                               Every discovered repo gets at least one
                               chunk (name + language + description) even
                               if it has no README, so a repo never goes
                               completely unrepresented.
  - content/links.json       (every external link found on the portfolio,
                               dispatched to a source-appropriate fetcher -
                               see chunk_external_links)

Every chunk, from every source above, is also tagged with a best-guess
project_id (see assign_project_id) based on keyword overlap with a real
GitHub repo's name/description - not by matching titles across sources,
which don't share a naming convention. This powers retriever.py's
project-diversity guarantee.

Zero-downtime strategy:
  1. Insert everything for this run under a fresh batch_id with status='pending'.
  2. Verify the pending batch is non-empty and every row has an embedding.
  3. Single transaction: flip pending -> active, delete every row that isn't
     in this batch. The retriever only ever reads status='active', so readers
     never see a partial or empty table.
"""
import asyncio
import json
import re
import sys
import uuid
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

sys.path.append(str(Path(__file__).parent.parent))

from app.constants import normalize_free_text_label  # noqa: E402
from app.db.connection import get_pool, init_db  # noqa: E402
from app.services.embedder import embed_texts  # noqa: E402

CONTENT_DIR = Path(__file__).parent.parent / "content"

RESUME_DRIVE_VIEW_URL = "https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view?usp=sharing"
RESEARCH_PAPER_URL = "https://ceur-ws.org/Vol-4039/paper19.pdf"
GITHUB_USERNAME = "varunsani"

REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RaceEngineerBot/1.0)"}

_STOPWORDS = {
    "the", "and", "for", "with", "using", "app", "api", "system", "project",
    "based", "a", "an", "of", "to", "in", "on", "this", "that", "is", "are",
}


# ---------- generic text-splitting helpers ----------

def recursive_char_split(text: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """RecursiveCharacterTextSplitter-style splitting: try paragraph, then
    sentence, then hard character boundaries, respecting chunk_size/overlap."""
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    separators = ["\n\n", "\n", ". ", " "]
    for sep in separators:
        parts = text.split(sep)
        if len(parts) > 1:
            chunks, current = [], ""
            for part in parts:
                candidate = (current + sep + part) if current else part
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        chunks.append(current.strip())
                    current = part
            if current:
                chunks.append(current.strip())

            overlapped = []
            for i, c in enumerate(chunks):
                if i > 0 and overlap > 0:
                    prev_tail = chunks[i - 1][-overlap:]
                    c = prev_tail + " " + c
                overlapped.append(c)
            return [c for c in overlapped if c.strip()]

    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]


def paragraph_split(text: str) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paragraphs


def heading_split(text: str) -> list[tuple[str, str]]:
    """Used for READMEs: split by markdown heading, return (heading, body)."""
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading, current_body = "Overview", []
    for line in lines:
        if line.strip().startswith("#"):
            if current_body:
                sections.append((current_heading, "\n".join(current_body).strip()))
            current_heading = line.strip("# ").strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections.append((current_heading, "\n".join(current_body).strip()))
    return [(h, b) for h, b in sections if b]


def is_likely_section_header(line: str) -> bool:
    """Heuristic header detection for resumes - no fixed vocabulary to
    maintain. Section headers are reliably short, standalone lines that are
    either ALL CAPS ('EDUCATION') or every word capitalized ('Research &
    Publications'), contain no ':' or ',' (which show up in data lines like
    'Languages: Python, C++, C'), and carry no trailing sentence punctuation."""
    s = line.strip()
    if not s or len(s) > 40 or len(s) < 3:
        return False
    if s.endswith((".", ",", ";")):
        return False
    if ":" in s or "," in s:
        return False

    words = s.split()
    alpha_words = [w for w in words if any(c.isalpha() for c in w)]
    if not alpha_words:
        return False

    if s.upper() == s:
        return True
    if len(alpha_words) <= 4 and all(w[0].isupper() for w in alpha_words):
        return True
    return False


def semantic_resume_split(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading, current_body = "Summary", []
    for line in lines:
        if is_likely_section_header(line):
            if current_body:
                sections.append((current_heading, "\n".join(current_body).strip()))
            current_heading = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections.append((current_heading, "\n".join(current_body).strip()))
    return [(h, b) for h, b in sections if b]


# ---------- Google Drive fetch (resume + any other drive link) ----------

def _extract_drive_file_id(url: str) -> str | None:
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    return m.group(1) if m else None


def fetch_drive_pdf_bytes(view_url: str, timeout: int = 30) -> bytes | None:
    """Fetches a Google Drive file's raw bytes, handling the small-file
    direct-download case and the "can't scan this file for viruses" confirm
    page that appears for larger files. Returns None if it can't get a PDF."""
    file_id = _extract_drive_file_id(view_url)
    if not file_id:
        print(f"WARNING: could not extract a Drive file id from {view_url}")
        return None

    session = requests.Session()
    base = "https://drive.google.com/uc"

    try:
        resp = session.get(base, params={"id": file_id, "export": "download"},
                            headers=REQUEST_HEADERS, timeout=timeout)
    except Exception as e:
        print(f"WARNING: Drive fetch failed for {view_url} ({e})")
        return None

    if resp.content[:4] == b"%PDF":
        return resp.content

    token = None
    for k, v in resp.cookies.items():
        if k.startswith("download_warning"):
            token = v
    if not token:
        m = re.search(r'confirm=([0-9A-Za-z_-]+)', resp.text)
        if m:
            token = m.group(1)

    if token:
        try:
            resp2 = session.get(base, params={"id": file_id, "export": "download", "confirm": token},
                                 headers=REQUEST_HEADERS, timeout=timeout)
            if resp2.content[:4] == b"%PDF":
                return resp2.content
        except Exception as e:
            print(f"WARNING: Drive confirm-token fetch failed for {view_url} ({e})")

    print(f"WARNING: could not retrieve a PDF from {view_url} — got non-PDF content.")
    return None


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extracts text page by page. A single page that fails to extract
    cleanly (a scanned image, a heavily formula/Type3-font page some PDF
    libraries choke on) is skipped with a warning instead of aborting the
    whole document - every other page's text still makes it through."""
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as e:
        print(f"WARNING: could not open PDF at all ({e}) — 0 pages extracted.")
        return ""

    pages_text = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            print(f"WARNING: page {i + 1} failed to extract ({e}) — skipping just this page.")
            continue
        if text.strip():
            pages_text.append(text)
        else:
            print(f"NOTE: page {i + 1} produced no extractable text (likely an image/diagram) — skipping just this page.")

    return "\n".join(pages_text)


# ---------- per-source chunk builders ----------

def chunk_portfolio() -> list[dict]:
    path = CONTENT_DIR / "portfolio.md"
    if not path.exists():
        print("WARNING: content/portfolio.md not found, skipping. Run scrape_portfolio.py first.")
        return []

    text = path.read_text()
    chunks = []
    tag_re = re.compile(r"^\[(.+?)\]\((#.*?)\)\s?(.*)$")
    buffer_by_section: dict[tuple[str, str], list[str]] = {}

    for line in text.splitlines():
        m = tag_re.match(line.strip())
        if not m:
            continue
        section, anchor, content = m.groups()
        buffer_by_section.setdefault((section, anchor), []).append(content)

    for (section, anchor), lines in buffer_by_section.items():
        full_text = " ".join(lines)
        for piece in recursive_char_split(full_text, chunk_size=400, overlap=80):
            chunks.append({
                "content": piece,
                "source": "portfolio",
                "section": section,
                "anchor": anchor,
                "url": f"https://varunsani.vercel.app/{anchor}",
                "title": section,
            })
    return chunks


def chunk_resume() -> list[dict]:
    """Always fetched live from Google Drive - never a locally committed
    file. This is intentional: the resume gets updated on Drive only, and
    should never require a manual git commit to reach the bot."""
    print("Fetching resume from Google Drive...")
    pdf_bytes = fetch_drive_pdf_bytes(RESUME_DRIVE_VIEW_URL)
    if pdf_bytes is None:
        print("WARNING: resume could not be fetched from Drive — skipping resume indexing this run.")
        return []

    full_text = extract_pdf_text(pdf_bytes)
    if not full_text.strip():
        print("WARNING: resume PDF produced no extractable text at all — skipping.")
        return []

    chunks = []
    for heading, body in semantic_resume_split(full_text):
        label = normalize_free_text_label(heading)
        for piece in recursive_char_split(body, chunk_size=500, overlap=60):
            chunks.append({
                "content": f"{heading}: {piece}",
                "source": "resume",
                "section": f"Resume — {heading}",
                "anchor": None,
                "url": RESUME_DRIVE_VIEW_URL,
                "title": f"Resume — {label}",
            })

    # Explicit discoverability chunk: guarantees a query like "give me his
    # resume link" or "where's his resume" has something to literally match
    # on the word "resume", independent of how the surrounding prose is
    # phrased anywhere else.
    chunks.append({
        "content": "Varun's resume is available here as a PDF, kept up to date on Google Drive.",
        "source": "resume",
        "section": "Resume",
        "anchor": None,
        "url": RESUME_DRIVE_VIEW_URL,
        "title": "Resume",
    })
    return chunks


def chunk_research_paper() -> list[dict]:
    try:
        resp = requests.get(RESEARCH_PAPER_URL, headers=REQUEST_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"WARNING: could not fetch research paper ({e}), skipping.")
        return []

    full_text = extract_pdf_text(resp.content)
    if not full_text.strip():
        print("WARNING: research paper produced no extractable text at all — skipping.")
        return []

    chunks = []
    for para in paragraph_split(full_text):
        for piece in recursive_char_split(para, chunk_size=400, overlap=80):
            chunks.append({
                "content": piece,
                "source": "research_paper",
                "section": "The Wind Tunnel (Research) — Multipacking in Hypercubes",
                "anchor": "#research",
                "url": RESEARCH_PAPER_URL,
                "title": "Multipacking in Hypercubes (ICTCS 2025)",
            })

    chunks.append({
        "content": (
            "Co-authors of Varun's ICTCS 2025 paper 'Multipacking in Hypercubes': "
            "Deepak Rajendraprasad, Varun Sani, Birenjith Sasidharan, and Jishnu Sen, "
            "all affiliated with the Indian Institute of Technology Palakkad."
        ),
        "source": "research_paper",
        "section": "The Wind Tunnel (Research) — Multipacking in Hypercubes",
        "anchor": "#research",
        "url": RESEARCH_PAPER_URL,
        "title": "Multipacking in Hypercubes (ICTCS 2025) — Authors",
    })
    return chunks


def discover_github_repos(username: str) -> list[dict]:
    """Auto-discovers every public, non-fork repo for the user via the
    GitHub API instead of a hardcoded list, so new repos are picked up
    automatically on the next scheduled reindex."""
    try:
        resp = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "type": "owner", "sort": "updated"},
            headers=REQUEST_HEADERS, timeout=20,
        )
        resp.raise_for_status()
        repos = resp.json()
    except Exception as e:
        print(f"WARNING: GitHub repo discovery failed for {username} ({e})")
        return []

    return [r for r in repos if not r.get("fork")]


def chunk_github_repos(repos: list[dict]) -> list[dict]:
    """Every discovered repo gets at least one chunk - name, language, and
    description if present - even if it has no README at all. Previously,
    a repo with neither a description nor a README produced zero chunks
    and silently never showed up in any answer; this guarantees every repo
    is represented at minimum."""
    if not repos:
        print("WARNING: no GitHub repos discovered — skipping GitHub indexing this run.")
        return []

    chunks = []
    for repo in repos:
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        default_branch = repo.get("default_branch", "main")
        description = repo.get("description") or ""
        language = repo.get("language") or ""

        baseline = f"{repo_name}"
        if language:
            baseline += f" (written in {language})"
        if description:
            baseline += f": {description}"
        chunks.append({
            "content": baseline,
            "source": "github_repo",
            "section": f"The Garage (Projects) — {repo_name}",
            "anchor": "#projects",
            "url": repo_url,
            "title": repo_name,
        })

        got_readme = False
        for branch_candidate in {default_branch, "main", "master"}:
            raw_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repo_name}/{branch_candidate}/README.md"
            try:
                resp = requests.get(raw_url, headers=REQUEST_HEADERS, timeout=15)
                if resp.status_code == 200 and resp.text.strip():
                    got_readme = True
                    for heading, body in heading_split(resp.text):
                        for piece in recursive_char_split(body, chunk_size=400, overlap=80):
                            chunks.append({
                                "content": f"{repo_name} — {heading}: {piece}",
                                "source": "github_readme",
                                "section": f"The Garage (Projects) — {repo_name}",
                                "anchor": "#projects",
                                "url": repo_url,
                                "title": repo_name,
                            })
                    break
            except Exception as e:
                print(f"WARNING: could not fetch README for {repo_name} on {branch_candidate} ({e})")

        if not got_readme:
            print(f"NOTE: no README found for {repo_name} — indexed with baseline info only.")

    return chunks


# ---------- project_id tagging (used by every source, not just GitHub) ----------

def _project_keyword_sets(repos: list[dict]) -> list[dict]:
    """One durable keyword set per discovered repo, built from its name,
    description, and topics — real GitHub data, not guessed from
    inconsistently-worded titles across the portfolio/resume/README."""
    projects = []
    for repo in repos:
        name_words = re.findall(r"[a-zA-Z]+", repo["name"].replace("-", " ").replace("_", " "))
        desc_words = re.findall(r"[a-zA-Z]+", repo.get("description") or "")
        topic_words = []
        for t in repo.get("topics", []) or []:
            topic_words += re.findall(r"[a-zA-Z]+", t.replace("-", " "))
        words = {w.lower() for w in (name_words + desc_words + topic_words) if len(w) > 2}
        words -= _STOPWORDS
        projects.append({"id": repo["name"], "keywords": words})
    return projects


def assign_project_id(content: str, known_projects: list[dict]) -> str | None:
    tokens = set(re.findall(r"[a-z0-9]+", content.lower()))
    best_id, best_score = None, 0
    for proj in known_projects:
        overlap = len(tokens & proj["keywords"])
        if overlap > best_score:
            best_score = overlap
            best_id = proj["id"]
    return best_id if best_score >= 2 else None


# ---------- external link dispatch ----------

def _fetch_chess_com_stats(username: str, link: dict) -> list[dict]:
    """chess.com's profile page is JS-rendered — ratings never show up in a
    plain HTML fetch. Their public stats API returns them directly."""
    try:
        resp = requests.get(f"https://api.chess.com/pub/player/{username}/stats",
                             headers=REQUEST_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"WARNING: chess.com stats fetch failed for {username} ({e})")
        return []

    lines = []
    label_map = {
        "chess_rapid": "Rapid", "chess_blitz": "Blitz", "chess_bullet": "Bullet",
        "chess_daily": "Daily",
    }
    for key, label in label_map.items():
        block = data.get(key)
        if block and "last" in block:
            rating = block["last"].get("rating")
            best = block.get("best", {}).get("rating")
            if rating:
                text = f"{label} rating: {rating}"
                if best and best != rating:
                    text += f" (best: {best})"
                lines.append(text)

    if not lines:
        return []

    content = f"Varun's Chess.com ratings — {'; '.join(lines)}."
    return [{
        "content": content,
        "source": "external_link",
        "section": link["section"],
        "anchor": link.get("anchor"),
        "url": link["url"],
        "title": "Chess.com ratings",
    }]


def _fetch_youtube_oembed(url: str, link: dict) -> list[dict]:
    try:
        resp = requests.get("https://www.youtube.com/oembed",
                             params={"url": url, "format": "json"},
                             headers=REQUEST_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"WARNING: YouTube oEmbed fetch failed for {url} ({e})")
        return []

    title = data.get("title", "")
    author = data.get("author_name", "")
    if not title:
        return []

    content = f"(Referenced by Varun in '{link['section']}') YouTube video: \"{title}\""
    if author:
        content += f" by {author}"
    return [{
        "content": content,
        "source": "external_link",
        "section": link["section"],
        "anchor": link.get("anchor"),
        "url": url,
        "title": title,
    }]


def _fetch_drive_link(url: str, link: dict) -> list[dict]:
    pdf_bytes = fetch_drive_pdf_bytes(url)
    if pdf_bytes is None:
        return []
    text = extract_pdf_text(pdf_bytes)
    if not text.strip():
        return []
    chunks = []
    for para in paragraph_split(text)[:10]:
        for piece in recursive_char_split(para, chunk_size=400, overlap=80):
            chunks.append({
                "content": f"(Referenced by Varun in '{link['section']}') {link['label']}: {piece}",
                "source": "external_link",
                "section": link["section"],
                "anchor": link.get("anchor"),
                "url": url,
                "title": link["label"],
            })
    return chunks


def _extract_json_ld_text(soup) -> str:
    """Many JS-heavy sites (IMDb included) still embed a full JSON-LD
    <script type="application/ld+json"> block for search-engine rich
    snippets - this is server-rendered, present regardless of what the
    visible page needs JavaScript to display. A malformed block on one
    site is caught per-block, so it can't block extraction on any other
    site or block."""
    pieces = []
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or "")
        except Exception:
            continue
        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or ""
            description = item.get("description") or ""
            if name or description:
                pieces.append(f"{name}: {description}" if name else description)
    return " ".join(pieces).strip()


def _extract_meta_description(soup) -> str:
    """og:description / meta description - also server-rendered for social
    previews, so it survives even when the main body needs JS to render."""
    for attrs in ({"property": "og:description"}, {"name": "description"}):
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def _fetch_generic_page(url: str, link: dict) -> list[dict]:
    """Tries JSON-LD, then meta description, then visible body text, in
    that order of reliability for JS-rendered pages - each attempt is
    independent, so a page that fails one extraction method still gets a
    chance at the next rather than the whole link coming back empty."""
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"WARNING: could not fetch external link {url} ({e})")
        return []

    text = ""
    try:
        text = _extract_json_ld_text(soup)
    except Exception as e:
        print(f"NOTE: JSON-LD extraction failed for {url} ({e}) — trying meta description next.")

    if not text:
        try:
            text = _extract_meta_description(soup)
        except Exception as e:
            print(f"NOTE: meta description extraction failed for {url} ({e}) — trying body text next.")

    if not text:
        try:
            for tag in soup(["script", "style", "nav"]):
                tag.decompose()
            text = soup.get_text(" ", strip=True)
        except Exception as e:
            print(f"WARNING: body text extraction also failed for {url} ({e}) — giving up on this link.")
            return []

    text = text[:3000]
    if not text.strip():
        print(f"NOTE: no extractable text found at all for {url} (likely a fully JS-rendered page).")
        return []

    chunks = []
    for para in paragraph_split(text)[:5]:
        for piece in recursive_char_split(para, chunk_size=400, overlap=80):
            chunks.append({
                "content": f"(Referenced by Varun in '{link['section']}') {link['label']}: {piece}",
                "source": "external_link",
                "section": link["section"],
                "anchor": link.get("anchor"),
                "url": url,
                "title": link["label"],
            })
    return chunks

def write_external_links_markdown(chunks: list[dict]) -> None:
    """Writes the actual extracted content for every external link (from
    chunk_external_links) to a human-readable markdown file, mirroring
    portfolio.md's format: a heading per link, tagged body lines underneath.

    This is separate from links.json (which only holds link metadata) -
    this file holds the real scraped/fetched text so it's easy to eyeball
    what actually got indexed for each link.
    """
    external_links_path = CONTENT_DIR / "scraped_external_links.md"

    if not chunks:
        external_links_path.write_text(
            "# Scraped External Link Content\n\n(no external link content extracted this run)\n"
        )
        print("NOTE: no external link chunks to write to scraped_external_links.md")
        return

    # Group by (url, title) preserving first-seen order, so every distinct
    # link gets exactly one heading with all its extracted content lines
    # underneath, in the order they were produced.
    grouped: dict[tuple[str, str], list[dict]] = {}
    for chunk in chunks:
        key = (chunk["url"], chunk["title"])
        grouped.setdefault(key, []).append(chunk)

    lines = ["# Scraped External Link Content\n"]
    lines.append("Extracted content for every external link referenced in content/links.json.\n")

    for (url, title), group_chunks in grouped.items():
        section = group_chunks[0]["section"]
        anchor = group_chunks[0].get("anchor") or ""
        lines.append(f"\n## [{section}] {title}\n")
        lines.append(f"Source: {url}\n")
        for chunk in group_chunks:
            content = chunk["content"].strip()
            if content:
                lines.append(f"[{section}]({anchor}) {content}")

    external_links_path.write_text("\n".join(lines))
    print(f"Wrote {len(grouped)} external links' content to {external_links_path}")

def chunk_external_links() -> list[dict]:
    """Every external link gets rendered — dispatched to a source-specific
    fetcher where a plain HTML scrape would fail (chess.com, YouTube,
    Drive), and the generic scraper otherwise."""
    links_path = CONTENT_DIR / "links.json"
    if not links_path.exists():
        return []

    links = json.loads(links_path.read_text())
    chunks = []

    for link in links:
        url = link["url"]
        if not url.startswith("http"):
            continue

        if "chess.com/member/" in url:
            username = url.rstrip("/").split("/")[-1]
            chunks += _fetch_chess_com_stats(username, link)
        elif "youtube.com/watch" in url or "youtu.be/" in url:
            chunks += _fetch_youtube_oembed(url, link)
        elif "drive.google.com" in url:
            # Skip if this is the same file as the resume - chunk_resume()
            # already indexes it properly with semantic section splitting;
            # routing it through here too would just double the content
            # with a lower-quality generic paragraph split.
            if _extract_drive_file_id(url) == _extract_drive_file_id(RESUME_DRIVE_VIEW_URL):
                continue
            chunks += _fetch_drive_link(url, link)
        elif re.match(r"https?://github\.com/[^/]+/?$", url):
            continue  # profile link itself — repos are discovered separately
        else:
            chunks += _fetch_generic_page(url, link)

    return chunks


# ---------- main indexing flow ----------

async def index_all():
    await init_db()
    pool = await get_pool()

    repos = discover_github_repos(GITHUB_USERNAME)
    known_projects = _project_keyword_sets(repos)

    all_chunks = []
    all_chunks += chunk_portfolio()
    all_chunks += chunk_resume()
    all_chunks += chunk_research_paper()
    all_chunks += chunk_github_repos(repos)
    external_chunks = chunk_external_links()
    write_external_links_markdown(external_chunks)
    all_chunks += external_chunks

    

    if not all_chunks:
        print("ERROR: no chunks produced, aborting reindex (leaving old index in place).")
        sys.exit(1)

    for chunk in all_chunks:
        chunk["project_id"] = assign_project_id(chunk["content"], known_projects)

    print(f"Embedding {len(all_chunks)} chunks...")

    
    embeddings = embed_texts([c["content"] for c in all_chunks])

    batch_id = str(uuid.uuid4())
    async with pool.acquire() as conn:
        async with conn.transaction():
            for chunk, embedding in zip(all_chunks, embeddings):
                vec_literal = "[" + ",".join(str(x) for x in embedding) + "]"
                await conn.execute(
                    """
                    INSERT INTO knowledge_base
                        (content, embedding, source, section, anchor, url, title, project_id, status, batch_id)
                    VALUES ($1, $2::vector, $3, $4, $5, $6, $7, $8, 'pending', $9)
                    """,
                    chunk["content"], vec_literal, chunk["source"], chunk["section"],
                    chunk.get("anchor"), chunk["url"], chunk["title"], chunk.get("project_id"), batch_id,
                )

            pending_count = await conn.fetchval(
                "SELECT COUNT(*) FROM knowledge_base WHERE batch_id = $1 AND status = 'pending'",
                batch_id,
            )
            if pending_count != len(all_chunks):
                raise RuntimeError("Pending batch verification failed — rolling back reindex.")

            await conn.execute(
                "UPDATE knowledge_base SET status = 'active' WHERE batch_id = $1",
                batch_id,
            )
            await conn.execute(
                "DELETE FROM knowledge_base WHERE batch_id != $1 OR batch_id IS NULL",
                batch_id,
            )

    print(f"Reindex complete. {len(all_chunks)} chunks now active (batch {batch_id}).")


if __name__ == "__main__":
    asyncio.run(index_all())