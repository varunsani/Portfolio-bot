from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"

    portfolio_url: str = "https://varunsani.vercel.app"
    frontend_origin_prod: str = "https://varunsani.vercel.app"

    top_k: int = 5
    similarity_threshold: float = 0.3
    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    mmr_lambda: float = 0.7

    llm_temperature: float = 0.15
    llm_max_tokens: int = 300

    conversation_turns: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
