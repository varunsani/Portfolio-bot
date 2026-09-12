import time
from typing import List
from urllib.parse import urlparse

from app.constants import display_label_for_chunk
from app.models.schemas import ChatResponse, Citation
from app.services import memory, retriever, generator, small_talk


def _normalize_citation_url(url: str) -> str:
    """Canonical key for the citation dedup set: scheme, `www.`, trailing
    slash, query string, and #fragment are all stripped/normalized, so
    http vs https, www vs bare domain, a tracking query param, or a
    same-page anchor don't let an otherwise-identical URL slip past the
    set as "different" and produce a duplicate chip. Falls back to a
    plain strip/rstrip if the URL doesn't parse cleanly."""
    if not url:
        return ""
    try:
        p = urlparse(url.strip())
        netloc = p.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return f"{netloc}{p.path.rstrip('/')}".lower()
    except Exception:
        return url.strip().rstrip("/").lower()


def _dedupe_citations(chunks) -> List[Citation]:
    """One citation chip per distinct URL, and one chip per distinct
    visible label.

    Two independent dedup rules run together because each catches a
    different class of duplicate that the other misses:

    1. URL-level (via _normalize_citation_url): the same underlying link
       arriving as different strings - http vs https, www vs bare domain,
       trailing slash, tracking query param, or a same-page #fragment -
       must not produce a second chip. This is the resume-PDF case, where
       one Drive URL gets chunked into "Education"/"Experience"/"Skills"/
       "Resume" sections and would otherwise surface 3-4 times.

    2. Label-level: two *different* URLs can still render the exact same
       visible chip text (e.g. two portfolio anchors that both resolve to
       "Beyond"). Even though the links technically differ, they read as
       a duplicate chip to the user and, in practice, point at the same
       section of the same page - so one chip is enough. Dropping the
       second is the intended behavior here, not a loss.

    Chunks arrive already sorted by retrieval relevance, so keeping the
    first-seen entry per URL and per label keeps the most relevant
    framing. Labels come from display_label_for_chunk, the same helper
    generator.py uses for the LLM's grounding context, so what the model
    reasons about and what the user sees as a citation chip always agree
    - and GitHub repos in particular get their real repo name folded in
    instead of colliding on the generic "Projects" anchor label."""
    seen_urls: set[str] = set()
    seen_texts: set[str] = set()
    citations = []
    for c in chunks:
        url_key = _normalize_citation_url(c.url)
        label = display_label_for_chunk(c.source, c.anchor, c.section, c.title)
        text_key = label.strip().lower()

        # Two different URLs can still land on the exact same visible chip
        # label (e.g. two portfolio anchors that both resolve to "Beyond"),
        # which reads as a duplicate chip to the user even though the links
        # technically differ - so both sets have to be clear, not just the
        # URL one.
        if url_key in seen_urls or text_key in seen_texts:
            continue
        seen_urls.add(url_key)
        seen_texts.add(text_key)
        citations.append(Citation(text=label, url=c.url, anchor=c.anchor))
    return citations


async def answer_question(message: str, session_id: str) -> ChatResponse:
    start = time.perf_counter()

    history = await memory.get_history(session_id)

    # Small talk (greetings, farewells, thanks, date/time) bypasses
    # retrieval entirely — there's no portfolio chunk about "hello", so
    # without this check it would incorrectly hit the "no data" decline.
    if small_talk.is_small_talk(message):
        reply = generator.generate_small_talk_reply(message, history)
        await memory.append_turn(session_id, message, reply)
        latency_ms = int((time.perf_counter() - start) * 1000)
        return ChatResponse(answer=reply, citations=[], latency_ms=latency_ms)

    chunks = await retriever.retrieve(message)

    if not chunks:
        reply = (
            "I don't have anything on that in Varun's portfolio or resume — "
            "happy to help with something that's actually in his telemetry."
        )
        await memory.append_turn(session_id, message, reply)
        latency_ms = int((time.perf_counter() - start) * 1000)
        return ChatResponse(answer=reply, citations=[], latency_ms=latency_ms)

    reply = generator.generate_answer(message, chunks, history)
    await memory.append_turn(session_id, message, reply)

    citations = _dedupe_citations(chunks)
    latency_ms = int((time.perf_counter() - start) * 1000)
    return ChatResponse(answer=reply, citations=citations, latency_ms=latency_ms)
