"""Retrieval result schemas."""
from __future__ import annotations

from pydantic import BaseModel

from graphrag.schemas.chunk import Chunk


class VectorSearchResult(BaseModel):
    chunk: Chunk
    score: float


class GraphSearchResult(BaseModel):
    chunk: Chunk
    entity_names: list[str] = []
    relationship_types: list[str] = []
    graph_score: float = 0.0


class RerankedResult(BaseModel):
    chunk: Chunk
    rerank_score: float
    original_rank: int
