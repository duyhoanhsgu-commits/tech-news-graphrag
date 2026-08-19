"""LLM-based relation extractor."""
from __future__ import annotations

import json
import uuid

from graphrag.graph.extraction.prompts import (
    RELATION_EXTRACTION_SYSTEM,
    RELATION_EXTRACTION_USER,
)
from graphrag.schemas.entity import Entity
from graphrag.schemas.relationship import Relationship


class RelationExtractor:
    def __init__(self, llm_client) -> None:
        self._client = llm_client

    async def extract(
        self,
        entities: list[Entity],
        chunk_text: str,
        chunk_id: str,
    ) -> list[Relationship]:
        entity_list = "\n".join(f"- {e.name} ({e.type})" for e in entities)
        user = RELATION_EXTRACTION_USER.format(entities=entity_list, text=chunk_text)
        raw = await self._client.complete(system=RELATION_EXTRACTION_SYSTEM, user=user)
        return self._parse(raw, entities, chunk_id)

    def _parse(
        self,
        raw: str,
        entities: list[Entity],
        chunk_id: str,
    ) -> list[Relationship]:
        name_to_id = {e.name.lower(): e.entity_id for e in entities}
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            return []
        relationships = []
        for item in items:
            src = name_to_id.get(item.get("source", "").lower())
            tgt = name_to_id.get(item.get("target", "").lower())
            if not src or not tgt:
                continue
            relationships.append(
                Relationship(
                    relationship_id=str(uuid.uuid4()),
                    source_entity_id=src,
                    target_entity_id=tgt,
                    relationship_type=item.get("relationship_type", "RELATED_TO"),
                    description=item.get("description"),
                    source_chunk_id=chunk_id,
                )
            )
        return relationships
