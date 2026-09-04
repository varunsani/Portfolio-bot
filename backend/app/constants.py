"""
Single source of truth for mapping a portfolio anchor to plain-English
labels. Used three ways:

1. generator.py resolves the LLM-facing "Section:" label from this instead
   of the site's flavorful eyebrow copy ("The Garage"), so F1 theming never
   leaks into the model's grounding context.
2. retriever.py appends these words (not the raw chunk text) into the BM25
   tokenization only, so a literal query like "what's his tech stack"
   lexically matches #skills chunks even though the word "skills" might not
   appear in that exact phrasing anywhere in the portfolio copy.
3. index_knowledge.py uses the resume-heading normalizer for the same
   plain-label purpose on resume chunks, which have no portfolio anchor.

The thematic title ("The Garage — Fresh off the lift") is still stored as
each chunk's `section` field for citation-chip display — this file never
touches that, it only supplies a second, LLM/BM25-facing signal alongside it.
"""

ANCHOR_LABELS: dict[str, list[str]] = {
    "#about": ["About", "Introduction", "Background", "Formation Lap", "Building race pace"],
    "#skills": ["Skills", "Tech Stack", "Technical Skills", "The Pit Crew", "Everything under the hood"],
    "#experience": ["Experience", "Work Experience", "Internship", "Race Stints", "Time on track"],
    "#projects": ["Projects", "The Garage", "Fresh off the lift"],
    "#research": ["Research", "Publications", "Paper", "The Wind Tunnel", "First podium"],
    "#beyond": ["Interests", "Hobbies", "Off Track", "Cool-down lap thoughts"],
    "#contact": ["Contact", "Post-Race Debrief", "Email", "Phone", "Box box box"],
}


def plain_label_for_anchor(anchor: str | None, fallback_text: str = "") -> str:
    """Best plain-English label for a chunk, given its anchor (if any)."""
    if anchor and anchor in ANCHOR_LABELS:
        return ANCHOR_LABELS[anchor][0]
    return normalize_free_text_label(fallback_text)


def normalize_free_text_label(text: str) -> str:
    """For chunks with no portfolio anchor (resume, research paper, GitHub
    READMEs) — classify by a handful of durable substrings instead of an
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


def bm25_alias_tokens(anchor: str | None) -> list[str]:
    """Extra words to fold into a chunk's BM25 document only (not the vector
    embedding, not the visible answer) so thematic section names don't cost
    a chunk its keyword-search recall."""
    if anchor and anchor in ANCHOR_LABELS:
        return ANCHOR_LABELS[anchor]
    return []
