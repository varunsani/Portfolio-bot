import time
from typing import List

from app.models.schemas import ChatResponse, Citation
from app.services import memory, retriever, generator, small_talk


def _dedupe_citations(chunks) -> List[Citation]:
    seen = set()
    citations = []
    for c in chunks:
        key = (c.section, c.anchor)
        if key in seen:
            continue
        seen.add(key)
        citations.append(Citation(text=f"{c.title or c.section}", url=c.url, anchor=c.anchor))
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
