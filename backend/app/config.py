from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"   # <--- KEEP THIS

    portfolio_url: str = "https://varunsani.vercel.app"
    frontend_origin_prod: str = "https://varunsani.vercel.app"

    # Has been tuned back to current 15, while dialing in citation relevance/coverage.
    # If you change this, re-check candidate_pool_multiplier and
    # MAX_GUARANTEED_FRACTION in retriever.py together with it — both scale
    # off top_k, not off each other.
    
    top_k: int = 15
    candidate_pool_multiplier: int = 10

    # Primary-source content (portfolio/resume/research paper/GitHub) keeps
    # the original, looser floors - these chunks are already boosted toward
    # being genuinely about Varun (see retriever._PRIMARY_SOURCES /
    # _SOURCE_SCORE_BOOST), so a stricter gate here mostly drops legitimate
    # sparse content (e.g. the paper title/authors chunk) rather than noise.
    vector_min_threshold: float = 0.28
    bm25_min_threshold: float = 0.35
    SOURCE_SCORE_BOOST: float = 0.03
  
    vector_weight: float = 0.75
    bm25_weight: float = 0.25
    mmr_lambda: float = 0.65
    # How many rows the Postgres full-text-search fallback pulls in
    # alongside the vector-search candidate pool (see
    # retriever._fetch_keyword_candidates). Keeps an exact keyword hit -
    # e.g. "authors" - from being missed just because it didn't happen to
    # rank in the top vector-similarity candidates.
    keyword_candidate_limit: int = 15

    llm_temperature: float = 0.20
    llm_max_tokens: int = 500

    conversation_turns: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
