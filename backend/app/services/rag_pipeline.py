import time
from typing import List
from urllib.parse import urlparse

from app.constants import display_label_for_chunk
from app.models.schemas import ChatResponse, Citation
from app.services import memory, retriever, generator, small_talk


def _normalize_citation_url(url: str) -> str:
    """Scheme/host/path key for dedup purposes - ignores case, a leading
    www., trailing slash, query string, and #fragment, so http vs https,
    www vs bare domain, a tracking query param, or an anchor on an
    otherwise-identical page don't slip past dedup as "different" URLs.
    Falls back to a plain strip/rstrip if the URL doesn't parse cleanly."""
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
    """One citation chip per distinct URL - full stop. Deduped via a set
    on a normalized URL key (see _normalize_citation_url), not just a raw
    strip/rstrip, so http vs https, www vs bare domain, a stray query
    param, or a #anchor fragment on the same page can't slip past as a
    "different" URL and produce a duplicate chip. Chunks arrive already
    sorted by retrieval relevance, so keeping the first-seen label per URL
    keeps the most relevant framing.

    Labels themselves come from display_label_for_chunk, the same helper
    generator.py uses for the LLM's grounding context, so what the model
    reasons about and what the user sees as a citation chip always agree
    - and GitHub repos in particular get their real repo name folded in
    instead of colliding on the generic "Projects" anchor label."""
    seen_urls: set[str] = set()
    citations = []
    for c in chunks:
        url_key = _normalize_citation_url(c.url)
        if url_key in seen_urls:
            continue
        seen_urls.add(url_key)
        label = display_label_for_chunk(c.source, c.anchor, c.section, c.title)
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
