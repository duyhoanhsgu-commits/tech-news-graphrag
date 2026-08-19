"""Chunk schema."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    chunk_id: str
    article_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    token_count: int | None = None
    embedding: list[float] | None = None
    metadata: dict = Field(default_factory=dict)
