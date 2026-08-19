"""LLM-based entity extractor."""
from __future__ import annotations

import json
import uuid

from graphrag.graph.extraction.prompts import (
    ENTITY_EXTRACTION_SYSTEM,
    ENTITY_EXTRACTION_USER,
)
from graphrag.schemas.chunk import Chunk
from graphrag.schemas.entity import Entity


class EntityExtractor:
    def __init__(self, llm_client, entity_types: list[str]) -> None:
        self._client = llm_client
        self._entity_types = entity_types

    async def extract(self, chunk: Chunk) -> list[Entity]:
        system = ENTITY_EXTRACTION_SYSTEM.format(entity_types=", ".join(self._entity_types))
        user = ENTITY_EXTRACTION_USER.format(text=chunk.content)
        raw = await self._client.complete(system=system, user=user)
        return self._parse(raw, chunk.chunk_id)

    def _parse(self, raw: str, chunk_id: str) -> list[Entity]:
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            return []
        entities = []
        for item in items:
            if not isinstance(item, dict):
                continue
            entities.append(
                Entity(
                    entity_id=str(uuid.uuid4()),
                    name=item.get("name", ""),
                    type=item.get("type", "Unknown"),
                    description=item.get("description"),
                    source_chunk_ids=[chunk_id],
                )
            )
        return entities
