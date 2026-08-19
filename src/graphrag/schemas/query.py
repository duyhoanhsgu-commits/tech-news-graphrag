"""Query request/response schemas."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    mode: Literal["graphrag", "vector"] = "graphrag"
    top_k: int = Field(default=5, ge=1, le=20)
    include_sources: bool = True


class Citation(BaseModel):
    chunk_id: str
    article_id: str
    title: str | None = None
    url: str | None = None
    excerpt: str


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: list[Citation] = []
    mode: str
    latency_ms: float | None = None
