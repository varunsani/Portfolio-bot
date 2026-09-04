"""
Deterministic classification for messages that should bypass retrieval
entirely: greetings, farewells, thanks, "how are you", and date/time
questions. These are matched with plain regexes rather than left to the
LLM's judgment, so:

  - they never accidentally hit the "no data on that" decline (retrieval
    would find nothing for "hey" or "thanks" — there's no portfolio chunk
    about greetings — so without this check they'd get refused, which is
    wrong)
  - genuinely off-topic questions ("what's happening in Nepal", "best
    online code editor") are NOT matched here, so they still fall through
    to retrieval, find nothing, and get the deterministic decline — no LLM
    call, no hallucination risk.

Kept intentionally narrow: a message must be short (under ~8 words) to
match, so a longer sentence that happens to start with "hi" or contain the
word "thanks" isn't misclassified as pure small talk.
"""
import re

_MAX_WORDS = 8

_GREETING_RE = re.compile(
    r"^\s*(hi|hello+|hey+|yo|sup|good\s*(morning|afternoon|evening|night))\b(?!-)", re.I
)
_FAREWELL_RE = re.compile(
    r"^\s*(bye+|goodbye|see\s*(you|ya)|take\s*care|catch\s*you\s*later)\b", re.I
)
_THANKS_RE = re.compile(r"^\s*(thanks|thank\s*you|thx|ty|cheers|appreciate\s*it)\b", re.I)
_HOW_ARE_YOU_RE = re.compile(r"how\s*(are|r)\s*(you|u|ya)\b", re.I)
_DATETIME_RE = re.compile(
    r"(what.?s|what\s+is)\s+(the\s+)?(current\s+)?(date|day|time)\b"
    r"|current\s+(date|time)\b"
    r"|today.?s\s+date\b"
    r"|what\s+time\s+is\s+it\b",
    re.I,
)

_PATTERNS = [_GREETING_RE, _FAREWELL_RE, _THANKS_RE, _HOW_ARE_YOU_RE, _DATETIME_RE]


def is_small_talk(message: str) -> bool:
    stripped = message.strip()
    if not stripped:
        return False
    if len(stripped.split()) > _MAX_WORDS:
        return False
    return any(p.search(stripped) for p in _PATTERNS)
