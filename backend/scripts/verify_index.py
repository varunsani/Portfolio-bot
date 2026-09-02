"""
Sanity check run right after index_knowledge.py in CI. Fails the workflow
(non-zero exit) if the active index looks broken, so a bad reindex never
silently ships.
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.connection import get_pool, init_db  # noqa: E402

MIN_EXPECTED_CHUNKS = 20
EXPECTED_SOURCES = {"portfolio", "resume"}


async def verify():
    await init_db()
    pool = await get_pool()

    total = await pool.fetchval("SELECT COUNT(*) FROM knowledge_base WHERE status = 'active'")
    print(f"Active chunks: {total}")
    if total < MIN_EXPECTED_CHUNKS:
        print(f"FAIL: expected at least {MIN_EXPECTED_CHUNKS} active chunks, got {total}")
        sys.exit(1)

    sources = await pool.fetch(
        "SELECT DISTINCT source FROM knowledge_base WHERE status = 'active'"
    )
    found_sources = {r["source"] for r in sources}
    missing = EXPECTED_SOURCES - found_sources
    if missing:
        print(f"FAIL: missing expected sources in active index: {missing}")
        sys.exit(1)

    stale = await pool.fetchval("SELECT COUNT(*) FROM knowledge_base WHERE status != 'active'")
    if stale:
        print(f"WARNING: {stale} stale/pending rows found (should be 0 after a clean swap).")

    print("Index verification passed.")


if __name__ == "__main__":
    asyncio.run(verify())
