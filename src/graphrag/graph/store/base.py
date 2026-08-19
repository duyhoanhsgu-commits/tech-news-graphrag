"""Abstract graph store interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

from graphrag.schemas.entity import Entity
from graphrag.schemas.relationship import Relationship


class BaseGraphStore(ABC):
    @abstractmethod
    async def upsert_entities(self, entities: list[Entity]) -> None:
        ...

    @abstractmethod
    async def upsert_relationships(self, relationships: list[Relationship]) -> None:
        ...

    @abstractmethod
    async def get_neighbors(
        self,
        entity_ids: list[str],
        max_hops: int = 1,
    ) -> list[dict]:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...
