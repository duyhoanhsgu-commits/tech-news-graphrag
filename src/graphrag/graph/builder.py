"""Graph builder — orchestrates extraction, resolution, and storage."""
from __future__ import annotations

from graphrag.graph.extraction.entity_extractor import EntityExtractor
from graphrag.graph.extraction.relation_extractor import RelationExtractor
from graphrag.graph.resolution.deduplicator import EntityDeduplicator
from graphrag.graph.store.repository import GraphRepository
from graphrag.schemas.chunk import Chunk


class GraphBuilder:
    def __init__(
        self,
        entity_extractor: EntityExtractor,
        relation_extractor: RelationExtractor,
        deduplicator: EntityDeduplicator,
        repository: GraphRepository,
    ) -> None:
        self._entity_extractor = entity_extractor
        self._relation_extractor = relation_extractor
        self._deduplicator = deduplicator
        self._repository = repository

    async def build_from_chunks(self, chunks: list[Chunk]) -> None:
        all_entities = []
        all_relationships = []
        for chunk in chunks:
            entities = await self._entity_extractor.extract(chunk)
            if not entities:
                continue
            relationships = await self._relation_extractor.extract(
                entities, chunk.content, chunk.chunk_id
            )
            all_entities.extend(entities)
            all_relationships.extend(relationships)

        deduped_entities, deduped_rels = self._deduplicator.deduplicate(
            all_entities, all_relationships
        )
        await self._repository.save_entities(deduped_entities)
        await self._repository.save_relationships(deduped_rels)
