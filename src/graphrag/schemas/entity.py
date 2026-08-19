"""Entity schema."""
from __future__ import annotations

from pydantic import BaseModel


class Entity(BaseModel):
    entity_id: str
    name: str
    type: str                       # Person | Organization | Location | …
    description: str | None = None
    aliases: list[str] = []
    source_chunk_ids: list[str] = []
    confidence: float = 1.0
