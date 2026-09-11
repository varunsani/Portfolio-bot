from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"   # <--- KEEP THIS

    portfolio_url: str = "https://varunsani.vercel.app"
    frontend_origin_prod: str = "https://varunsani.vercel.app"

    # Lowered from 10 -> 5: at top_k=10 nearly every answer surfaced up to
    # 10 citation chips, several of them barely-relevant "either" gate
    # survivors. 5 is enough to back a 2-3 sentence answer without
    # flooding the chip row.
    top_k: int = 10
    candidate_pool_multiplier: int = 10

    # Primary-source content (portfolio/resume/research paper/GitHub) keeps
    # the original, looser floors - these chunks are already boosted toward
    # being genuinely about Varun (see retriever._PRIMARY_SOURCES /
    # _SOURCE_SCORE_BOOST), so a stricter gate here mostly drops legitimate
    # sparse content (e.g. the paper title/authors chunk) rather than noise.
    vector_min_threshold: float = 0.28
    bm25_min_threshold: float = 0.35

    # Stricter floors, scoped to external_link chunks only (see
    # retriever._passes_threshold) - this is where the noisy/unrelated
    # citations were actually coming from, so tightening only this pair
    # cuts the noise without also starving primary-source retrieval.
    vector_min_threshold_external: float = 0.32
    bm25_min_threshold_external: float = 0.42

    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    mmr_lambda: float = 0.7
    # How many rows the Postgres full-text-search fallback pulls in
    # alongside the vector-search candidate pool (see
    # retriever._fetch_keyword_candidates). Keeps an exact keyword hit -
    # e.g. "authors" - from being missed just because it didn't happen to
    # rank in the top vector-similarity candidates.
    keyword_candidate_limit: int = 15

    llm_temperature: float = 0.15
    llm_max_tokens: int = 300

    conversation_turns: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
