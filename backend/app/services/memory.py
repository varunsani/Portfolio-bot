"""
Conversation memory in Redis.
Keeps the last N turns (user+assistant pairs) per session_id so follow-up
questions like "tell me more about that project" resolve correctly.
"""
import json
from typing import List

import redis.asyncio as redis

from app.config import settings

_redis: redis.Redis | None = None
SESSION_TTL_SECONDS = 60 * 60 * 6  # 6 hours of inactivity clears the session
SESSION_KEY_PREFIX = "race_engineer:session:"


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(session_id: str) -> str:
    return f"{SESSION_KEY_PREFIX}{session_id}"


async def get_history(session_id: str) -> List[dict]:
    r = get_redis()
    raw = await r.get(_key(session_id))
    if not raw:
        return []
    return json.loads(raw)


async def append_turn(session_id: str, user_message: str, assistant_message: str):
    r = get_redis()
    history = await get_history(session_id)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_message})
    max_messages = settings.conversation_turns * 2
    history = history[-max_messages:]
    await r.set(_key(session_id), json.dumps(history), ex=SESSION_TTL_SECONDS)


async def flush_all_sessions() -> int:
    """Wipes every in-flight conversation's history — called by
    index_knowledge.py the moment a reindex actually ships new content
    (see index_all()), not on every reindex run or on a timer.

    Why this and not "just always wipe Redis": the KB itself (Postgres)
    already reindexes safely with zero downtime — the problem this solves
    is narrower. A session's Redis history holds the *assistant's own
    previous replies*, which get replayed verbatim into the next LLM call
    (see generator._format_history). If those replies were generated
    before a reindex changed the underlying facts, the model can end up
    half-anchored to a stale answer even though the fresh CONTEXT block
    for the new question is correct. Wiping only at the moment truth
    changes keeps memory intact for the common case (a session living
    entirely between two reindexes) while guaranteeing no session ever
    carries pre-reindex answers across a content change.

    Scoped to the "race_engineer:session:*" prefix (SCAN, not KEYS, so it
    doesn't block Redis on a large keyspace) rather than FLUSHDB — nothing
    else lives in this Redis instance today, but scoping by prefix means
    this stays correct even if that ever changes. Returns the number of
    sessions cleared, purely for the reindex script's own log line."""
    r = get_redis()
    keys = [key async for key in r.scan_iter(match=f"{SESSION_KEY_PREFIX}*", count=200)]
    if keys:
        await r.delete(*keys)
    return len(keys)
