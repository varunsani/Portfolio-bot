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
import hashlib
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
from app.services import memory as memory_service  # noqa: E402

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

    heading_re = re.compile(r"^##\s*\[(.+?)\]\s*(.+?)\s*$")
    buffer_by_section: dict[tuple[str, str, str], list[str]] = {}
    current_subheading = ""

    for raw_line in text.splitlines():
        line = raw_line.strip()
        h = heading_re.match(line)
        if h:
            current_subheading = h.group(2)
            continue
        m = tag_re.match(line)
        if not m:
            continue
        section, anchor, content = m.groups()
        buffer_by_section.setdefault((section, anchor, current_subheading), []).append(content)

    for (section, anchor, subheading), lines in buffer_by_section.items():
        full_text = " ".join(lines)
        display_section = f"{section} — {subheading}" if subheading and subheading != section else section
        for piece in recursive_char_split(full_text, chunk_size=400, overlap=80):
            content_piece = f"{subheading}: {piece}" if subheading and subheading != section else piece
            chunks.append({
                "content": content_piece,
                "source": "portfolio",
                "section": display_section,
                "anchor": anchor,
                "url": f"https://varunsani.vercel.app/{anchor}",
                "title": display_section,
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


_BOILERPLATE_PATTERNS = [
    re.compile(r"corresponding author", re.I),
    re.compile(r"contributed equally", re.I),
    re.compile(r"\borcid\b", re.I),
    re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dXx]"),  # an ORCID id itself, e.g. 0000-0002-1234-567X
    re.compile(r"©|copyright", re.I),
    re.compile(r"ceur-ws\.org", re.I),
    re.compile(r"\bissn\b", re.I),
    re.compile(r"\bdoi\s*:", re.I),
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),  # a bare email/footnote line
    re.compile(r"this work is licen", re.I),
]


def _strip_boilerplate_lines(text: str) -> tuple[str, int]:
    """Removes only the noisy lines - ORCID strings, 'corresponding
    author'/'contributed equally' footnote markers, copyright/license
    lines, ISSN/DOI lines, bare email-footer lines - and keeps every other
    line of the document untouched. Returns (cleaned_text, lines_removed).

    Line-level, not paragraph-level: extract_pdf_text() joins pages (and
    pypdf joins a page's own lines) with single "\\n"s, never a blank-line
    "\\n\\n" - so paragraph_split() on the raw PDF text hands back the
    *entire document* as one paragraph. Checking that one giant blob for
    "does this contain a boilerplate pattern anywhere" meant a single
    ORCID id or email buried anywhere in an 8-page paper flagged the whole
    paper as boilerplate and dropped every real sentence in it, which is
    exactly what happened before this fix. Stripping line-by-line removes
    only the actual noisy lines, wherever they fall, and leaves everything
    else - including all the real page content - to be chunked normally
    afterward."""
    kept, removed = [], 0
    for line in text.splitlines():
        s = line.strip()
        if s and len(s) < 300 and any(pat.search(s) for pat in _BOILERPLATE_PATTERNS):
            removed += 1
            continue
        kept.append(line)
    return "\n".join(kept), removed


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

    cleaned_text, removed = _strip_boilerplate_lines(full_text)
    if removed:
        print(f"NOTE: stripped {removed} boilerplate line(s) from the research paper "
              f"(ORCID/copyright/footnote noise) — the rest of the document is indexed normally.")

    chunks = []
    for para in paragraph_split(cleaned_text):
        for piece in recursive_char_split(para, chunk_size=400, overlap=80):
            chunks.append({
                "content": piece,
                "source": "research_paper",
                "section": "The Wind Tunnel (Research) — Multipacking in Hypercubes",
                "anchor": "#research",
                "url": RESEARCH_PAPER_URL,
                "title": "Multipacking in Hypercubes (ICTCS 2025)",
            })
    if skipped:
        print(f"NOTE: skipped {skipped} boilerplate paragraph(s) from the research paper "
              f"(ORCID/copyright/footnote noise) — not indexed.")
    chunks.append({
        "content": (
            "The title of Varun's research paper, published at ICTCS 2025 "
            "(International Conference on Theoretical Computer Science) in "
            "CEUR Workshop Proceedings Vol-4039, is 'Multipacking in "
            "Hypercubes'. This is Varun's academic publication / research paper."
        ),
        "source": "research_paper",
        "section": "The Wind Tunnel (Research) — Multipacking in Hypercubes",
        "anchor": "#research",
        "url": RESEARCH_PAPER_URL,
        "title": "Multipacking in Hypercubes (ICTCS 2025) — Title",
    })

    chunks.append({
        "content": (
            "Authors of Varun's ICTCS 2025 publication paper 'Multipacking in Hypercubes': "
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
    """Tries JSON-LD, meta description, AND visible body text, and keeps
    whichever one actually returned the most content - not just whichever
    came back non-empty first.

    Previously this stopped at the first non-empty result: JSON-LD or a
    one-line meta description ("Contribute to X development by creating
    an account on GitHub.", "ORCID · Please enable JavaScript...") almost
    always exists and almost always "succeeds", so the much richer body
    text was silently never even attempted for the vast majority of
    static pages (Wikipedia, IMDb, chessgames.com, museum sites, poetry
    pages) where it would have returned a real paragraph or more. That's
    why external_links.md ended up so bare. JSON-LD/meta description are
    still needed as the fallback for genuinely JS-rendered pages where
    body text comes back empty - but "found something" and "found the
    best available something" aren't the same, so all three are now
    attempted and scored by length instead of by whichever ran first."""
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"WARNING: could not fetch external link {url} ({e})")
        return []

    candidates = []

    try:
        jsonld_text = _extract_json_ld_text(soup)
        if jsonld_text:
            candidates.append(jsonld_text)
    except Exception as e:
        print(f"NOTE: JSON-LD extraction failed for {url} ({e}).")

    try:
        meta_text = _extract_meta_description(soup)
        if meta_text:
            candidates.append(meta_text)
    except Exception as e:
        print(f"NOTE: meta description extraction failed for {url} ({e}).")

    # Body text extraction mutates `soup` (decompose()), so it always runs
    # last - after JSON-LD/meta description have already read what they
    # need from the untouched soup.
    try:
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()
        body_text = soup.get_text(" ", strip=True)
        if body_text:
            candidates.append(body_text)
    except Exception as e:
        print(f"WARNING: body text extraction failed for {url} ({e}).")

    if not candidates:
        print(f"NOTE: no extractable text found at all for {url} (likely a fully JS-rendered page).")
        return []

    text = max(candidates, key=len)

    # 3000 chars was cutting off the actual useful content on long/JS-heavy
    # pages (IMDb-style pages routinely bury the plot/bio text well past
    # that point once nav/boilerplate text is counted). 12000 gives the
    # body-text fallback enough room without this becoming a full page
    # mirror; JSON-LD and meta-description are already short and
    # unaffected by this.
    text = text[:12000]

    chunks = []
    # Was [:5] paragraphs, tuned for the old 3000-char cap. With more text
    # available there are more paragraphs to consider, so this is widened
    # to match rather than silently dropping the back half of the page.
    for para in paragraph_split(text)[:20]:
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

def write_chunks_markdown(name: str, chunks: list[dict]) -> None:
    """
    Writes scraped and chunked content to backend/content/<name>.md.

    Each chunk gets a numbered heading with its section and title,
    followed by metadata and full content, so you can scroll through
    and see exactly what got indexed and how it was split.

    Calling with name='master' writes all_chunks combined — every source
    in index order — giving a single file to audit the full index at once.
    """
    # content_dir = CONTENT_DIR  # already points to backend/content
    # content_dir.mkdir(parents=True, exist_ok=True)

    filename = "master.md" if name == "master" else f"{name}.md"
    path     = CONTENT_DIR / filename

    if not chunks:
        path.write_text(f"# {name}\n\n(no chunks extracted this run)\n")
        print(f"  {filename} — 0 chunks")
        return

    label = "All Sources Combined" if name == "master" else name
    lines = [
        f"# {label}  ({len(chunks)} chunks)\n",
        f"Generated by index_knowledge.py.\n",
    ]

    for i, chunk in enumerate(chunks):
        lines += [
            f"\n---\n",
            f"### Chunk {i + 1}  —  {chunk.get('section', '')}",
            f"**Title:** {chunk.get('title', '')}",
            f"**Source:** {chunk.get('source', '')}  |  "
            f"**Anchor:** {chunk.get('anchor', '')}",
            f"**URL:** {chunk.get('url', '')}  |  "
            f"**Project ID:** {chunk.get('project_id', 'none')}",
            "",
            chunk.get("content", "").strip(),
        ]

    path.write_text("\n".join(lines))
    print(f"  {filename} — {len(chunks)} chunks → {path}")

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
        elif url == RESEARCH_PAPER_URL:
            continue  # already indexed properly by chunk_research_paper()
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


def _content_hash(chunks: list[dict]) -> str:
    """Deterministic fingerprint of everything about to be indexed, so a
    reindex run that produced byte-identical content can be told apart
    from one that actually changed something. This is what lets index_all()
    skip the Redis session flush on the hourly safety-net run when nothing
    about Varun's site/resume/repos actually changed that hour."""
    joined = "\n".join(c["content"] for c in chunks)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


# ---------- main indexing flow ----------

async def index_all():
    await init_db()
    pool = await get_pool()

    repos = discover_github_repos(GITHUB_USERNAME)
    known_projects = _project_keyword_sets(repos)

    portfolio_chunks   = chunk_portfolio()
    resume_chunks      = chunk_resume()
    research_chunks    = chunk_research_paper()
    github_chunks      = chunk_github_repos(repos)
    external_chunks    = chunk_external_links()

    all_chunks = (
        portfolio_chunks
        + resume_chunks
        + research_chunks
        + github_chunks
        + external_chunks
    )

    write_chunks_markdown("portfolio_debug",      portfolio_chunks)
    write_chunks_markdown("resume",         resume_chunks)
    write_chunks_markdown("research_paper", research_chunks)
    write_chunks_markdown("github_repos",   github_chunks)
    write_chunks_markdown("external_links", external_chunks)
    write_chunks_markdown("master",         all_chunks)
 

    if not all_chunks:
        print("ERROR: no chunks produced, aborting reindex (leaving old index in place).")
        sys.exit(1)

    new_content_hash = _content_hash(all_chunks)

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

    # "The script ran" and "the content actually changed" are different
    # things — the hourly cron safety-net run re-embeds and swaps every
    # single hour regardless of whether Varun's site/resume/repos changed
    # at all (see reindex.yml's comment on why there's no diffing at the
    # workflow level). Only flush sessions when this run's content
    # genuinely differs from last run's, so an in-flight conversation
    # isn't reset by a no-op hourly reindex.
    previous_hash = await memory_service.get_last_content_hash()
    if new_content_hash != previous_hash:
        cleared = await memory_service.flush_all_sessions()
        print(f"Content changed since last reindex — cleared {cleared} "
              f"in-flight conversation session(s) from Redis.")
    else:
        print("Content unchanged since last reindex — leaving active sessions alone.")
    await memory_service.set_last_content_hash(new_content_hash)
    await memory_service.get_redis().aclose()


if __name__ == "__main__":
    asyncio.run(index_all())
