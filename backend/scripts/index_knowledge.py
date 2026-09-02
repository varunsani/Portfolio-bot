"""
Indexing pipeline. Run manually or via .github/workflows/reindex.yml.

Sources indexed:
  - content/portfolio.md   (scraped live site, chunked per-section)
  - resume PDF             (fetched fresh from Google Drive every run — see
                             RESUME_URL — semantic chunking at font-detected
                             section boundaries; content/resume.pdf is only a
                             last-known-good cache, not the source of truth)
  - research paper PDF     (chunked by paragraph, notation preserved)
  - GitHub READMEs         (chunked by heading)
  - external_links.json    (best-effort text extraction, chunked by paragraph)

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
from collections import Counter
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

try:
    import pdfplumber
    HAVE_PDFPLUMBER = True
except ImportError:
    HAVE_PDFPLUMBER = False

sys.path.append(str(Path(__file__).parent.parent))

from app.db.connection import get_pool, init_db  # noqa: E402
from app.services.embedder import embed_texts  # noqa: E402

CONTENT_DIR = Path(__file__).parent.parent / "content"
RESUME_URL = "https://drive.google.com/uc?export=download&id=1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn"
RESEARCH_PAPER_URL = "https://ceur-ws.org/Vol-4039/paper19.pdf"

GITHUB_REPOS = [
    "https://github.com/varunsani/weather-alert-platform",
    "https://github.com/varunsani/UrlShortener",
]


# ---------- generic helpers ----------

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

            # apply overlap
            overlapped = []
            for i, c in enumerate(chunks):
                if i > 0 and overlap > 0:
                    prev_tail = chunks[i - 1][-overlap:]
                    c = prev_tail + " " + c
                overlapped.append(c)
            return [c for c in overlapped if c.strip()]

    # fallback: hard cut
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]


def paragraph_split(text: str) -> list[str]:
    """Used for the research paper: preserve paragraph boundaries and
    mathematical notation instead of splitting mid-formula."""
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


def _looks_like_heading_text(line: str) -> bool:
    """Generic fallback heuristic — no keyword whitelist. A line reads as a
    resume section header if it's short, has no trailing sentence punctuation,
    isn't a bullet, and is Title Case or ALL CAPS (how resume headers are
    conventionally styled, regardless of what word they actually use)."""
    stripped = line.strip()
    if not stripped or len(stripped) > 40:
        return False
    if stripped[-1] in ".,;:":
        return False
    if stripped.startswith(("-", "*", "•", "◦")):
        return False
    words = stripped.split()
    if not (1 <= len(words) <= 5):
        return False
    letters_only = re.sub(r"[^A-Za-z]", "", stripped)
    if not letters_only:
        return False
    is_upper = letters_only.isupper()
    is_title = all(w[:1].isupper() for w in words if w[:1].isalpha())
    return is_upper or is_title


def _split_on_heading_lines(text: str, is_heading) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading, current_body = "Summary", []
    for line in lines:
        if is_heading(line):
            if current_body:
                sections.append((current_heading, "\n".join(current_body).strip()))
            current_heading = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections.append((current_heading, "\n".join(current_body).strip()))
    return [(h, b) for h, b in sections if b]


def _cluster_words_into_lines(words: list[dict], tolerance: float = 3.0) -> list[tuple[str, float, bool]]:
    """Group extracted words into visual lines by y-position (a resume line is
    often typeset with two runs at slightly different baselines — e.g. a bold
    institution name on the left and a plain date on the right — so a naive
    round(top, 1) bucket splits one line into two). Returns (text, max_size,
    is_bold) per line, left-to-right."""
    if not words:
        return []
    ordered = sorted(words, key=lambda w: w["top"])
    raw_lines: list[list[dict]] = []
    current: list[dict] = []
    ref_top = None
    for w in ordered:
        if ref_top is None or abs(w["top"] - ref_top) <= tolerance:
            current.append(w)
            ref_top = sum(x["top"] for x in current) / len(current)
        else:
            raw_lines.append(current)
            current = [w]
            ref_top = w["top"]
    if current:
        raw_lines.append(current)

    lines = []
    for line_words in raw_lines:
        line_words.sort(key=lambda w: w["x0"])
        text = " ".join(w["text"] for w in line_words)
        max_size = max(w["size"] for w in line_words)
        is_bold = any("bold" in w["fontname"].lower() for w in line_words)
        lines.append((text, max_size, is_bold))
    return lines


def detect_resume_sections_by_font(pdf_path: Path) -> list[tuple[str, str]] | None:
    """Detect section headers by font size/weight instead of wording, so any
    header the resume actually uses (Leadership, Volunteering, whatever) is
    picked up automatically. Returns None if pdfplumber isn't available or no
    reliable size signal is found, so the caller can fall back gracefully."""
    if not HAVE_PDFPLUMBER:
        return None

    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            all_lines: list[tuple[str, float, bool]] = []
            sizes = Counter()
            for page in pdf.pages:
                words = page.extract_words(extra_attrs=["size", "fontname"])
                page_lines = _cluster_words_into_lines(words)
                for text, size, _ in page_lines:
                    sizes[round(size)] += len(text)
                all_lines.extend(page_lines)

            if not sizes:
                return None
            body_size = sizes.most_common(1)[0][0]

            def is_heading(entry) -> bool:
                text, size, is_bold = entry
                stripped = text.strip()
                if not stripped or len(stripped) > 45 or len(stripped.split()) > 6:
                    return False
                bigger = size >= body_size + 1.5
                if bigger:
                    return True
                # Same-size bold is only trustworthy as a header signal when it's
                # ALSO all-caps — plenty of resumes bold sub-entries (job titles,
                # institution names, "Languages:") at body size too, and those
                # aren't section boundaries. ALL CAPS is the actual distinguishing
                # convention for top-level headers in that case. Compare rounded
                # sizes here (PDF font metrics rarely land on a clean integer —
                # "10pt" often extracts as 9.96 — so a strict >= against the
                # rounded body_size would spuriously reject same-size headers).
                letters_only = re.sub(r"[^A-Za-z]", "", stripped)
                return bool(is_bold and round(size) >= body_size and letters_only.isupper()
                            and len(letters_only) >= 3)

            heading_flags = [is_heading(l) for l in all_lines]
            if sum(heading_flags) < 2:
                return None  # not enough signal to trust font-based detection

            sections: list[tuple[str, str]] = []
            current_heading, current_body = "Summary", []
            for (text, *_), heading in zip(all_lines, heading_flags):
                if heading:
                    if current_body:
                        sections.append((current_heading, "\n".join(current_body).strip()))
                    current_heading = text.strip()
                    current_body = []
                else:
                    current_body.append(text)
            if current_body:
                sections.append((current_heading, "\n".join(current_body).strip()))
            return [(h, b) for h, b in sections if b]
    except Exception as e:
        print(f"WARNING: font-based resume section detection failed ({e}), falling back.")
        return None


def semantic_resume_split(text: str, pdf_path: Path | None = None) -> list[tuple[str, str]]:
    """Split resume text at section-header boundaries (Education, Experience,
    Projects, etc.) automatically — no hardcoded list of expected header words.

    Preferred: font-size/weight based detection (resume headers are visually
    distinct from body text). Falls back to a text-shape heuristic (short,
    Title Case / ALL CAPS line) if font metadata isn't available or isn't
    a reliable signal for this particular PDF."""
    if pdf_path is not None:
        by_font = detect_resume_sections_by_font(pdf_path)
        if by_font:
            return by_font
    return _split_on_heading_lines(text, _looks_like_heading_text)


# ---------- per-source chunk builders ----------

def chunk_portfolio() -> list[dict]:
    path = CONTENT_DIR / "portfolio.md"
    if not path.exists():
        print("WARNING: content/portfolio.md not found, skipping. Run scrape_portfolio.py first.")
        return []

    text = path.read_text()
    chunks = []
    # portfolio.md lines are pre-tagged like: [Section Name](#anchor) content...
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


def _download_gdrive_file(url: str, dest: Path) -> bool:
    """Download a Google Drive share link. Handles Drive's "can't scan this
    file for viruses" interstitial that kicks in for larger files (it serves
    an HTML confirmation page instead of the PDF unless you follow its
    confirm token)."""
    session = requests.Session()
    resp = session.get(url, timeout=30, stream=True)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "")
    if "text/html" in content_type:
        # Large-file interstitial — pull the confirm token out of the page
        # (either a cookie or an embedded confirm= param) and retry.
        token = None
        for key, value in resp.cookies.items():
            if key.startswith("download_warning"):
                token = value
        if not token:
            m = re.search(r"confirm=([0-9A-Za-z_-]+)", resp.text)
            if m:
                token = m.group(1)
        if not token:
            return False
        resp = session.get(url, params={"confirm": token}, timeout=30, stream=True)
        resp.raise_for_status()
        if "text/html" in resp.headers.get("Content-Type", ""):
            return False  # still didn't get a real file — give up cleanly

    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1 << 16):
            f.write(chunk)
    return dest.stat().st_size > 0


def chunk_resume() -> list[dict]:
    """Resume is fetched fresh from Google Drive (RESUME_URL) on every
    reindex run rather than relying on a manually-updated local file — update
    the resume on Drive and the next reindex just picks it up. content/resume.pdf
    is kept only as a last-known-good cache: if the Drive download fails
    (network blip, sharing settings changed, etc.) we fall back to whatever
    was cached from the last successful run instead of hard-failing the whole
    reindex, and log loudly either way so a broken share link doesn't fail
    silently."""
    resume_path = CONTENT_DIR / "resume.pdf"
    try:
        ok = _download_gdrive_file(RESUME_URL, resume_path)
        if not ok:
            raise RuntimeError("Drive returned an interstitial page instead of the PDF")
        print("Resume fetched from Google Drive.")
    except Exception as e:
        if resume_path.exists():
            print(f"WARNING: could not fetch resume from Google Drive ({e}); "
                  f"using last cached content/resume.pdf instead.")
        else:
            print(f"WARNING: could not fetch resume from Google Drive ({e}), "
                  f"and no cached copy exists — skipping resume indexing.")
            return []

    reader = PdfReader(str(resume_path))
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    chunks = []
    for heading, body in semantic_resume_split(full_text, pdf_path=resume_path):
        for piece in recursive_char_split(body, chunk_size=500, overlap=60):
            chunks.append({
                "content": f"{heading}: {piece}",
                "source": "resume",
                "section": f"Resume — {heading}",
                "anchor": None,
                "url": "https://drive.google.com/file/d/1JjJZtAeLVnRYEXLAK_Xa-_nOhYypzAFn/view",
                "title": f"Resume — {heading}",
            })
    return chunks


def chunk_research_paper() -> list[dict]:
    try:
        resp = requests.get(RESEARCH_PAPER_URL, timeout=30)
        resp.raise_for_status()
        tmp_path = CONTENT_DIR / "_paper.pdf"
        tmp_path.write_bytes(resp.content)
        reader = PdfReader(str(tmp_path))
        full_text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        tmp_path.unlink(missing_ok=True)
    except Exception as e:
        print(f"WARNING: could not fetch research paper ({e}), skipping.")
        return []

    chunks = []
    for para in paragraph_split(full_text):
        chunks.append({
            "content": para,
            "source": "research_paper",
            "section": "The Wind Tunnel (Research) — Multipacking in Hypercubes",
            "anchor": "#research",
            "url": RESEARCH_PAPER_URL,
            "title": "Multipacking in Hypercubes (ICTCS 2025)",
        })
    return chunks


def chunk_github_repos() -> list[dict]:
    chunks = []
    for repo_url in GITHUB_REPOS:
        repo_name = repo_url.rstrip("/").split("/")[-1]
        for branch in ("main", "master"):
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/README.md"
            try:
                resp = requests.get(raw_url, timeout=15)
                if resp.status_code == 200 and resp.text.strip():
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
                print(f"WARNING: could not fetch {raw_url} ({e})")
    return chunks


def chunk_external_links() -> list[dict]:
    links_path = CONTENT_DIR / "links.json"
    if not links_path.exists():
        return []

    links = json.loads(links_path.read_text())
    chunks = []
    for link in links:
        url = link["url"]
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav"]):
                tag.decompose()
            text = soup.get_text(" ", strip=True)
            text = text[:3000]  # cap — this is supplementary context, not the primary source
        except Exception as e:
            print(f"WARNING: could not fetch external link {url} ({e})")
            continue

        for para in paragraph_split(text)[:5]:  # keep only the first few paragraphs
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


# ---------- main indexing flow ----------

async def index_all():
    await init_db()
    pool = await get_pool()

    all_chunks = []
    all_chunks += chunk_portfolio()
    all_chunks += chunk_resume()
    all_chunks += chunk_research_paper()
    all_chunks += chunk_github_repos()
    all_chunks += chunk_external_links()

    if not all_chunks:
        print("ERROR: no chunks produced, aborting reindex (leaving old index in place).")
        sys.exit(1)

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
                        (content, embedding, source, section, anchor, url, title, status, batch_id)
                    VALUES ($1, $2::vector, $3, $4, $5, $6, $7, 'pending', $8)
                    """,
                    chunk["content"], vec_literal, chunk["source"], chunk["section"],
                    chunk.get("anchor"), chunk["url"], chunk["title"], batch_id,
                )

            pending_count = await conn.fetchval(
                "SELECT COUNT(*) FROM knowledge_base WHERE batch_id = $1 AND status = 'pending'",
                batch_id,
            )
            if pending_count != len(all_chunks):
                raise RuntimeError("Pending batch verification failed — rolling back reindex.")

            # atomic swap
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
