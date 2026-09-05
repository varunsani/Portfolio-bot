"""
Retrieval strategy
------------------
1. Vector search (pgvector, cosine) over the 'active' partition - candidate
   pool size is top_k * candidate_pool_multiplier (see app.config), not a
   fixed number, so it scales automatically if top_k ever changes.
2. BM25 keyword scoring over those same candidates, on their own text only
   - no injected "alias" words. (An earlier version folded each anchor's
   thematic label into BM25 tokens as a keyword-search boost; that only
   covered anchors someone remembered to hand-list, silently missed
   anything new/renamed, and worked against the very mechanism it was
   trying to help by feeding BM25 words that don't actually appear in the
   content. Removed - keyword search now only ever matches real text.)
3. Acceptance: a candidate clears the bar if its RAW vector cosine clears
   VECTOR_MIN_THRESHOLD, OR its normalized BM25 score clears
   BM25_MIN_THRESHOLD - an "either" gate rather than one blended score
   with a single cutoff, so a query with zero vocabulary overlap with the
   source text (e.g. "university" when the portfolio only ever says
   "Institute of Technology") isn't unfairly punished by an empty BM25 term.
4. A weighted hybrid score (vector_weight/bm25_weight) is still computed
   for ranking purposes among accepted candidates.
5. Project-diversity guarantee: every chunk is tagged (at indexing time)
   with a best-guess project_id, based on real GitHub repo names/
   descriptions - not on matching inconsistent titles across the
   portfolio/resume/README, which don't share a naming convention. Before
   final selection, at least one chunk per distinct project_id present in
   the accepted pool is guaranteed a slot, so a heavily-documented project
   (mentioned in portfolio + resume + README) can't silently crowd out one
   that's only mentioned once. This only ever acts on chunks that already
   passed the relevance gate above, so an unrelated query (e.g. about
   skills) is never polluted with an irrelevant project chunk just because
   one happened to sit in the wider candidate pool.
6. MMR (Maximum Marginal Relevance) fills any remaining slots after the
   guarantee, removing near-duplicate chunks among what's left.
7. Contextual compression trims each surviving chunk down to its most
   query-relevant sentences before it reaches the LLM.
"""
import re
import json
from dataclasses import dataclass
from typing import List

from rank_bm25 import BM25Okapi
import numpy as np

from app.config import settings
from app.db.connection import get_pool
from app.services.embedder import embed_query

MAX_GUARANTEED_FRACTION = 0.5


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
    project_id: str | None = None
    vector_score: float = 0.0
    bm25_score: float = 0.0


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _parse_embedding(raw) -> List[float]:
    """
    Safely convert whatever asyncpg returns for a pgvector column into
    a plain Python list of floats.

    asyncpg can return the vector column as:
      - a string  '[0.1,0.2,...]'   (most common without a codec registered)
      - a list/tuple of floats      (if a codec is registered)
      - a numpy array               (unlikely but handled)

    Calling list() on a string gives a list of characters, which is the
    root cause of the 'could not convert string to float' error in _mmr.
    """
    if isinstance(raw, (list, tuple)):
        return [float(x) for x in raw]
    if isinstance(raw, np.ndarray):
        return raw.astype(float).tolist()
    if isinstance(raw, str):
        # pgvector uses '[v1,v2,...]' format — json.loads handles it directly
        return [float(x) for x in json.loads(raw)]
    # fallback: try iterating whatever it is
    return [float(x) for x in raw]


async def _fetch_candidates(query_embedding: List[float], limit: int) -> List[RetrievedChunk]:
    pool = await get_pool()
    vec_literal = "[" + ",".join(str(x) for x in query_embedding) + "]"
    rows = await pool.fetch(
        """
        SELECT content, embedding, source, section, anchor, url, title, project_id,
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
            embedding=_parse_embedding(r["embedding"]),  # fixed: was list(r["embedding"])
            source=r["source"],
            section=r["section"],
            anchor=r["anchor"],
            url=r["url"],
            title=r["title"],
            project_id=r["project_id"],
            score=float(r["cosine_sim"]),
            vector_score=float(r["cosine_sim"]),
        )
        for r in rows
    ]


def _bm25_scores(query: str, chunks: List[RetrievedChunk]) -> List[float]:
    if not chunks:
        return []
    corpus = [_tokenize(c.content) for c in chunks]
    bm25 = BM25Okapi(corpus)
    raw = bm25.get_scores(_tokenize(query))
    max_score = max(raw) or 1.0
    return [s / max_score for s in raw]  # normalize to [0, 1]


def _mmr(query_embedding: List[float], chunks: List[RetrievedChunk], k: int, lambda_mult: float) -> List[RetrievedChunk]:
    if not chunks or k <= 0:
        return []
    q = np.array(query_embedding, dtype=float)
    doc_vecs = [np.array(c.embedding, dtype=float) for c in chunks]

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


def _diversify_by_project(accepted: List[RetrievedChunk]) -> List[RetrievedChunk]:
    """Reorders the already-relevance-sorted accepted list so the single
    best chunk for each distinct project_id comes first, followed by
    everything else in its original score order. This only reorders - it
    never adds a chunk that wasn't already accepted, so it can't inject an
    irrelevant project into an unrelated answer."""
    seen_projects: set[str] = set()
    guaranteed: List[RetrievedChunk] = []
    rest: List[RetrievedChunk] = []
    for c in accepted:
        if c.project_id and c.project_id not in seen_projects:
            seen_projects.add(c.project_id)
            guaranteed.append(c)
        else:
            rest.append(c)
    return guaranteed + rest


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
    pool_size = settings.top_k * settings.candidate_pool_multiplier
    candidates = await _fetch_candidates(query_embedding, limit=pool_size)
    if not candidates:
        return []

    bm25_norm = _bm25_scores(query, candidates)
    for c, b in zip(candidates, bm25_norm):
        c.bm25_score = b
        c.score = settings.vector_weight * c.vector_score + settings.bm25_weight * b

    # "Either" gate: a candidate survives on vector strength alone, or BM25
    # strength alone - a weak showing on one axis never disqualifies a
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

    diversified_order = _diversify_by_project(shortlist)

    max_guaranteed = max(1, int(settings.top_k * MAX_GUARANTEED_FRACTION))
    seen_projects: set[str] = set()
    guaranteed: List[RetrievedChunk] = []
    for c in diversified_order:
        if len(guaranteed) >= max_guaranteed:
            break
        if c.project_id and c.project_id not in seen_projects:
            seen_projects.add(c.project_id)
            guaranteed.append(c)

    remaining_slots = settings.top_k - len(guaranteed)
    final: List[RetrievedChunk] = list(guaranteed)
    if remaining_slots > 0:
        pool_for_mmr = [c for c in diversified_order if c not in guaranteed]
        final += _mmr(query_embedding, pool_for_mmr, k=remaining_slots, lambda_mult=settings.mmr_lambda)

    for c in final:
        c.content = _compress(query, c.content)

    return final