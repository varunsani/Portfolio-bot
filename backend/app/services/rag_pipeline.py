import time
from typing import List

from app.constants import display_label_for_chunk
from app.models.schemas import ChatResponse, Citation
from app.services import memory, retriever, generator, small_talk


def _dedupe_citations(chunks) -> List[Citation]:
    """One citation chip per distinct URL - full stop. Previously this
    deduped on (label, url), which let the exact same link surface as
    multiple chips whenever two chunks that share a URL got different
    labels (e.g. the resume PDF chunked into "Education"/"Experience"/
    "Skills"/"Resume" sections all sharing one Drive URL - same link,
    shown 3-4 times). A link is either worth clicking or it isn't; it
    doesn't need to appear once per section that happens to live at that
    URL. Chunks arrive already sorted by retrieval relevance, so keeping
    the first-seen label per URL keeps the most relevant framing.

    Labels themselves come from display_label_for_chunk, the same helper
    generator.py uses for the LLM's grounding context, so what the model
    reasons about and what the user sees as a citation chip always agree
    - and GitHub repos in particular get their real repo name folded in
    instead of colliding on the generic "Projects" anchor label."""
    seen_urls = set()
    citations = []
    for c in chunks:
        if c.url in seen_urls:
            continue
        seen_urls.add(c.url)
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
