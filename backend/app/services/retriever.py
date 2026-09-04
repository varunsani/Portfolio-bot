"""
Retrieval strategy
------------------
1. Vector search (pgvector, cosine) over the 'active' partition — top ~25 candidates.
2. BM25 keyword scoring over those same candidates. Each chunk's BM25
   document is its own text PLUS its anchor's plain-English aliases (see
   app.constants) — so a literal query like "what's his tech stack" gets a
   keyword hit against a #skills chunk even if the word "skills" never
   appears in the chunk's own wording. The aliases are never embedded into
   the vector and never shown to the user — purely a BM25-side boost.
3. Acceptance: a candidate clears the bar if its RAW vector cosine clears
   VECTOR_MIN_THRESHOLD, OR its normalized BM25 score clears
   BM25_MIN_THRESHOLD. Using an "either" gate (rather than one blended
   score with a single cutoff) matters specifically for queries that share
   no vocabulary with the source text — e.g. "university" when the
   portfolio only ever says "Institute of Technology". A blended score
   drags a genuinely strong semantic match down by an empty BM25 term,
   pushing it under a single threshold. Splitting the gate lets either
   signal carry a candidate through on its own strength.
4. A weighted hybrid score (vector_weight/bm25_weight) is still computed
   for ranking/MMR purposes among accepted candidates.
5. Maximum Marginal Relevance (MMR) re-ranking on the accepted, hybrid-
   scored shortlist, so near-duplicate chunks (e.g. the same project
   described in the portfolio AND the resume) don't crowd out distinct
   information.
6. Contextual compression: each surviving chunk is trimmed down to the
   sentences most relevant to the query, so the LLM's context window
   carries signal, not padding.
"""
import re
from dataclasses import dataclass
from typing import List

from rank_bm25 import BM25Okapi
import numpy as np

from app.config import settings
from app.constants import bm25_alias_tokens
from app.db.connection import get_pool
from app.services.embedder import embed_query



@dataclass
class RetrievedChunk:
    content: str
    embedding: List[float]
    source: str
    section: str
    anchor: str | None
    url: str
    title: str
    score: float
    vector_score: float = 0.0
    bm25_score: float = 0.0


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


async def _fetch_candidates(query_embedding: List[float], limit: int = 25) -> List[RetrievedChunk]:
    pool = await get_pool()
    vec_literal = "[" + ",".join(str(x) for x in query_embedding) + "]"
    rows = await pool.fetch(
        """
        SELECT content, embedding, source, section, anchor, url, title,
               1 - (embedding <=> $1::vector) AS cosine_sim
        FROM knowledge_base
        WHERE status = 'active'
        ORDER BY embedding <=> $1::vector
        LIMIT $2
        """,
        vec_literal,
        limit,
    )
    return [
        RetrievedChunk(
            content=r["content"],
            embedding=list(r["embedding"]),
            source=r["source"],
            section=r["section"],
            anchor=r["anchor"],
            url=r["url"],
            title=r["title"],
            score=float(r["cosine_sim"]),
            vector_score=float(r["cosine_sim"]),
        )
        for r in rows
    ]


def _bm25_scores(query: str, chunks: List[RetrievedChunk]) -> List[float]:
    if not chunks:
        return []
    corpus = [_tokenize(c.content) + bm25_alias_tokens(c.anchor) for c in chunks]
    bm25 = BM25Okapi(corpus)
    raw = bm25.get_scores(_tokenize(query))
    max_score = max(raw) or 1.0
    return [s / max_score for s in raw]  # normalize to [0, 1]


def _mmr(query_embedding: List[float], chunks: List[RetrievedChunk], k: int, lambda_mult: float) -> List[RetrievedChunk]:
    if not chunks:
        return []
    q = np.array(query_embedding)
    doc_vecs = [np.array(c.embedding) for c in chunks]

    def cos(a, b):
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-9
        return float(np.dot(a, b) / denom)

    selected: List[int] = []
    candidates = list(range(len(chunks)))
    relevance = [cos(q, v) for v in doc_vecs]

    while candidates and len(selected) < k:
        if not selected:
            best = max(candidates, key=lambda i: relevance[i])
        else:
            def mmr_score(i):
                diversity_penalty = max(cos(doc_vecs[i], doc_vecs[j]) for j in selected)
                return lambda_mult * relevance[i] - (1 - lambda_mult) * diversity_penalty

            best = max(candidates, key=mmr_score)
        selected.append(best)
        candidates.remove(best)

    return [chunks[i] for i in selected]


def _compress(query: str, content: str, max_sentences: int = 3) -> str:
    """Contextual compression: keep only the sentences most relevant to the query."""
    sentences = re.split(r"(?<=[.!?])\s+", content.strip())
    if len(sentences) <= max_sentences:
        return content.strip()

    q_tokens = set(_tokenize(query))
    scored = []
    for s in sentences:
        overlap = len(q_tokens & set(_tokenize(s)))
        scored.append((overlap, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for _, s in scored[:max_sentences]]
    ordered = [s for s in sentences if s in top]
    return " ".join(ordered)


async def retrieve(query: str) -> List[RetrievedChunk]:
    query_embedding = embed_query(query)
    candidates = await _fetch_candidates(query_embedding, limit=settings.top_k*settings.candidate_pool_multiplier)
    if not candidates:
        return []

    bm25_norm = _bm25_scores(query, candidates)
    for c, b in zip(candidates, bm25_norm):
        c.bm25_score = b
        c.score = settings.vector_weight * c.vector_score + settings.bm25_weight * b

    # "Either" gate: a candidate survives on vector strength alone, or BM25
    # strength alone — a weak showing on one axis never disqualifies a
    # strong showing on the other.
    accepted = [
        c for c in candidates
        if c.vector_score >= settings.vector_min_threshold
        or c.bm25_score >= settings.bm25_min_threshold
    ]
    if not accepted:
        return []

    accepted.sort(key=lambda c: c.score, reverse=True)
    shortlist = accepted[: max(settings.top_k * 5, settings.top_k)]

    diversified = _mmr(query_embedding, shortlist, k=settings.top_k, lambda_mult=settings.mmr_lambda)

    for c in diversified:
        c.content = _compress(query, c.content)

    return diversified
