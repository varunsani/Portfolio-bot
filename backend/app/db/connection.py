"""
asyncpg + pgvector connection pool and schema bootstrap.

Zero-downtime re-indexing strategy:
  - New chunks are inserted with status='pending'
  - Once the full batch is verified, we atomically flip status='active'
    for the new batch and delete everything that was previously active,
    inside a single transaction.
  - The retriever only ever queries WHERE status = 'active', so there is
    no window where the bot serves an empty or half-written index.
"""
import asyncpg
from app.config import settings

_pool: asyncpg.Pool | None = None

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_base (
    id          SERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    embedding   vector(384),
    source      VARCHAR(100),
    section     VARCHAR(100),
    anchor      VARCHAR(100),
    url         TEXT,
    title       VARCHAR(200),
    status      VARCHAR(20) DEFAULT 'active',
    batch_id    UUID,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Added after the initial release: which real-world project (if any) a
-- chunk is about, tagged at indexing time from GitHub repo names/
-- descriptions. ADD COLUMN IF NOT EXISTS is idempotent, so this runs
-- safely on both a brand-new database and an existing one that predates
-- this column.
ALTER TABLE knowledge_base ADD COLUMN IF NOT EXISTS project_id VARCHAR(150);

CREATE INDEX IF NOT EXISTS knowledge_base_embedding_hnsw
ON knowledge_base
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS knowledge_base_status_idx ON knowledge_base (status);
CREATE INDEX IF NOT EXISTS knowledge_base_content_trgm ON knowledge_base
USING gin (to_tsvector('english', content));
"""


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=10)
    return _pool


async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA_SQL)


async def close_db():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
