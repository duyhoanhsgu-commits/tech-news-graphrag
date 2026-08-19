"""Entity deduplicator — merges matched entities into canonical records."""
from __future__ import annotations

from graphrag.graph.resolution.entity_matcher import EntityMatcher
from graphrag.schemas.entity import Entity
from graphrag.schemas.relationship import Relationship


class EntityDeduplicator:
    def __init__(self, matcher: EntityMatcher | None = None) -> None:
        self._matcher = matcher or EntityMatcher()

    def deduplicate(
        self,
        entities: list[Entity],
        relationships: list[Relationship],
    ) -> tuple[list[Entity], list[Relationship]]:
        id_map = self._matcher.match(entities)
        seen: dict[str, Entity] = {}
        for entity in entities:
            canonical_id = id_map[entity.entity_id]
            if canonical_id not in seen:
                seen[canonical_id] = entity.model_copy(update={"entity_id": canonical_id})
            else:
                # merge source_chunk_ids
                existing = seen[canonical_id]
                merged_chunks = list(set(existing.source_chunk_ids + entity.source_chunk_ids))
                seen[canonical_id] = existing.model_copy(update={"source_chunk_ids": merged_chunks})

        deduped_entities = list(seen.values())
        deduped_rels = [
            r.model_copy(
                update={
                    "source_entity_id": id_map.get(r.source_entity_id, r.source_entity_id),
                    "target_entity_id": id_map.get(r.target_entity_id, r.target_entity_id),
                }
            )
            for r in relationships
        ]
        return deduped_entities, deduped_rels
