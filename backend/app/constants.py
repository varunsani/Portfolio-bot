"""
Single source of truth for resolving a chunk's plain-English display label
- used for the LLM's grounding context AND for citation-chip text, so F1
theming never surfaces in either place.

Fully automatic: for portfolio chunks, the label is derived directly from
the section's real HTML id (e.g. id="projects" -> "Projects", id="work-
history" -> "Work History") - the same id that already powers the site's
own nav links, so it stays plain even when the visible copy above it gets
themed. Nothing here needs updating if the portfolio is redesigned, as
long as new sections keep a plain id. No manual per-anchor mapping to
maintain, and no BM25 "alias" word injection either - that approach was
tried and deliberately removed: it only covered anchors someone remembered
to add by hand, silently leaving newer/renamed sections uncovered, and it
worked against exactly the keyword-search mechanism it was trying to help
by feeding it words that never actually appear in the underlying content.

For chunks with no portfolio anchor (resume, research paper, GitHub
READMEs), normalize_free_text_label classifies by a handful of durable
substrings instead of an exact-match list.
"""


def plain_label_from_anchor_id(anchor: str | None) -> str | None:
    """'#work-history' -> 'Work History'. Returns None if there's no anchor
    to derive from (caller falls back to normalize_free_text_label)."""
    if not anchor:
        return None
    raw = anchor.lstrip("#").replace("-", " ").replace("_", " ").strip()
    return raw.title() if raw else None


def plain_label_for_anchor(anchor: str | None, fallback_text: str = "") -> str:
    """Best plain-English label for a chunk, given its anchor (if any)."""
    label = plain_label_from_anchor_id(anchor)
    if label:
        return label
    return normalize_free_text_label(fallback_text)


def display_label_for_chunk(source: str, anchor: str | None, section: str, title: str) -> str:
    """The one place both the LLM's grounding context AND citation chips
    resolve a chunk's label from - keeps the two perfectly consistent.

    GitHub-sourced chunks (source == "github_repo"/"github_readme") are
    given a repo-specific anchor "#projects" purely so retriever.py's
    generic anchor-based grounding still bucket them under "Projects" -
    but that meant every distinct repo collapsed to the identical label
    "Projects" for citation purposes, so three repos in one answer showed
    three identical-looking chips pointing at three different URLs. Repo
    chunks carry their real repo name in `title`, so use that instead:
    "Projects — reponame" stays in the same category but is distinguishable
    and correct per-repo, and downstream dedup-by-url no longer sees
    same-label collisions hiding genuinely different links."""
    if source in ("github_repo", "github_readme") and title:
        return f"Projects — {title}"
    return plain_label_for_anchor(anchor, fallback_text=section)


def normalize_free_text_label(text: str) -> str:
    """For chunks with no portfolio anchor (resume, research paper, GitHub
    READMEs) - classify by a handful of durable substrings instead of an
    exact-match list, so this doesn't need updating when wording changes."""
    s = (text or "").lower()
    if "educat" in s:
        return "Education"
    if "experien" in s or "intern" in s:
        return "Experience"
    if "project" in s or "garage" in s:
        return "Projects"
    if "skill" in s or "tech stack" in s:
        return "Skills"
    if "research" in s or "public" in s or "paper" in s or "wind tunnel" in s:
        return "Research"
    if "certif" in s:
        return "Certifications"
    if "interest" in s or "beyond" in s or "hobb" in s or "off track" in s:
        return "Interests"
    if "contact" in s or "debrief" in s:
        return "Contact"
    return text or "General"
