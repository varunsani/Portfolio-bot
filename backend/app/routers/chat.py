from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.rag_pipeline import answer_question
from app.db.connection import get_pool

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat(request: Request, body: ChatRequest):
    return await answer_question(body.message, body.session_id)


@router.get("/health", response_model=HealthResponse)
async def health():
    pool = await get_pool()
    count = await pool.fetchval("SELECT COUNT(*) FROM knowledge_base WHERE status = 'active'")
    return HealthResponse(status="ok", vectors_indexed=count or 0)
