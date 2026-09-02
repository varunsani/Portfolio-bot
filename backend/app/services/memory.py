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


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def _key(session_id: str) -> str:
    return f"race_engineer:session:{session_id}"


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
