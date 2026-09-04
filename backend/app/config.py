from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"   # <--- KEEP THIS

    portfolio_url: str = "https://varunsani.vercel.app"
    frontend_origin_prod: str = "https://varunsani.vercel.app"

    top_k: int = 10
    candidate_pool_multiplier: int = 10
    vector_min_threshold: float = 0.28       # <--- NEW REQUIRED SETTING
    bm25_min_threshold: float = 0.35         # <--- NEW REQUIRED SETTING
    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    mmr_lambda: float = 0.7

    llm_temperature: float = 0.15
    llm_max_tokens: int = 300

    conversation_turns: int = 10

    class Config:
        env_file = ".env"


settings = Settings()