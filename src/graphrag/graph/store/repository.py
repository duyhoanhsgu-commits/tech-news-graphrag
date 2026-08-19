"""Graph repository facade."""
from __future__ import annotations

from graphrag.graph.store.base import BaseGraphStore
from graphrag.schemas.entity import Entity
from graphrag.schemas.relationship import Relationship


class GraphRepository:
    def __init__(self, store: BaseGraphStore) -> None:
        self._store = store

    async def save_entities(self, entities: list[Entity]) -> None:
        await self._store.upsert_entities(entities)

    async def save_relationships(self, relationships: list[Relationship]) -> None:
        await self._store.upsert_relationships(relationships)

    async def get_neighbors(
        self,
        entity_ids: list[str],
        max_hops: int = 1,
    ) -> list[dict]:
        return await self._store.get_neighbors(entity_ids, max_hops)
