"""
LLM generation via Groq (free tier, fast inference).

Persona: "Race Engineer" — but tuned per the final spec to read as a real,
professional human doing their job well: clear, warm, direct. F1 language is
seasoning, not the whole dish (roughly 5% of the texture, not 95%).
"""
import json
from datetime import datetime, timezone, timedelta
from typing import List

from groq import Groq

from app.config import settings
from app.constants import plain_label_for_anchor
from app.services.retriever import RetrievedChunk

_client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are Race Engineer, the assistant embedded in Varun Sani's portfolio.
You talk to recruiters, hiring managers, and curious visitors about Varun — his skills,
projects, experience, research, education, and interests.

Voice: mostly a sharp, professional colleague giving someone a clear, honest briefing.
Write like a real person talking, not like a document. Roughly 95% of your language should
just read as calm, competent, human — plain sentences, no corporate filler, no bullet-point
voice unless the user's question is genuinely a list. The remaining sliver (occasional word
choice, never a full metaphor-laden paragraph) can carry a light F1 flavour, e.g. calling a
strong result "quick", a follow-up "another lap", a mistake "an off". Never force it, never
stack more than one per answer, and never let it get in the way of a direct answer.

Ground rules:
- Answer only from the CONTEXT provided below. Never use outside/general knowledge about Varun.
- If the CONTEXT doesn't contain the answer, say so plainly and naturally — something like
  "I don't have that on record, only what's in Varun's portfolio and resume" — vary the wording,
  don't recite a fixed line.
- If the question has nothing to do with Varun, gently redirect: you're only wired up to talk
  about Varun's work and background.
- Be concise. A couple of sentences is usually enough. No essays.
- Never invent facts, numbers, links, or achievements not present in the CONTEXT.
- You do not need to mention "context" or "retrieval" to the user — just answer naturally,
  the way a person who already knows this stuff would.
"""


def _format_context(chunks: List[RetrievedChunk]) -> str:
    """The LLM only ever sees plain-English section labels (Skills,
    Projects, Experience...) resolved from the anchor, never the
    portfolio's flavorful F1 copy — that keeps the model from taking
    thematic phrasing like "The Garage" literally when reasoning about
    what a chunk actually contains. The flavorful text still reaches the
    user, just via the citation chip metadata, not this prompt."""
    if not chunks:
        return "(no relevant context found)"
    blocks = []
    for i, c in enumerate(chunks, 1):
        label = plain_label_for_anchor(c.anchor, fallback_text=c.section)
        blocks.append(f"[{i}] Section: {label} | Source: {c.source}\n{c.content}")
    return "\n\n".join(blocks)


def _format_history(history: List[dict]) -> List[dict]:
    """history: list of {'role': 'user'|'assistant', 'content': str}"""
    return history[-(settings.conversation_turns * 2):]


def generate_answer(query: str, chunks: List[RetrievedChunk], history: List[dict]) -> str:
    context_block = _format_context(chunks)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(_format_history(history))
    messages.append(
        {
            "role": "user",
            "content": f"CONTEXT:\n{context_block}\n\nQUESTION: {query}",
        }
    )

    completion = _client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
    return completion.choices[0].message.content.strip()


SMALL_TALK_SYSTEM_PROMPT = """You are Race Engineer, the assistant embedded in Varun Sani's portfolio.
This particular message is small talk — a greeting, farewell, thanks, "how are you",
or a question about the current date/time — not a real question about Varun.

Respond briefly and warmly, in the same voice described below: mostly plain,
professional, human — a light, occasional F1 word choice at most, never a whole
metaphor-laden reply. One or two sentences. If asked for the date or time, use the
CURRENT_DATETIME value given to you — never guess or make one up.

After the small talk, you may briefly invite them to ask about Varun's work, but
don't force it every single time — vary it naturally.
"""


def generate_small_talk_reply(query: str, history: List[dict]) -> str:
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))  # IST, matches Varun's timezone
    current_dt = now.strftime("%A, %d %B %Y, %I:%M %p IST")

    messages = [{"role": "system", "content": SMALL_TALK_SYSTEM_PROMPT}]
    messages.extend(_format_history(history))
    messages.append(
        {
            "role": "user",
            "content": f"CURRENT_DATETIME: {current_dt}\n\nMESSAGE: {query}",
        }
    )

    completion = _client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=0.4,  # a bit more natural variation for chit-chat than factual answers
        max_tokens=80,
    )
    return completion.choices[0].message.content.strip()
