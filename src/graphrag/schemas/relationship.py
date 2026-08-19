"""Relationship schema."""
from __future__ import annotations

from pydantic import BaseModel


class Relationship(BaseModel):
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str          # MENTIONS | RELATED_TO | WORKS_FOR | …
    description: str | None = None
    source_chunk_id: str | None = None
    confidence: float = 1.0
    properties: dict = {}
