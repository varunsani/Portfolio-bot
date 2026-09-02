from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: str = Field(..., min_length=1, max_length=128)


class Citation(BaseModel):
    text: str
    url: str
    anchor: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    latency_ms: int


class HealthResponse(BaseModel):
    status: str
    vectors_indexed: int


class KnowledgeChunk(BaseModel):
    """One retrievable unit in the knowledge base."""
    content: str
    source: str          # e.g. "portfolio", "resume", "research_paper", "github_readme", "external_link"
    section: str          # human readable section name, e.g. "The Garage"
    anchor: Optional[str] = None   # in-page anchor, e.g. "#projects"
    url: str
    title: str
