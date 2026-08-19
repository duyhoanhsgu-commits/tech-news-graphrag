"""Abstract vector store interface."""
from __future__ import annotations

from abc import ABC, abstractmethod

from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult


class BaseVectorStore(ABC):
    @abstractmethod
    async def upsert(self, chunks: list[Chunk]) -> None:
        ...

    @abstractmethod
    async def search(
        self,
        query_vector: list[float],
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[VectorSearchResult]:
        ...

    @abstractmethod
    async def delete(self, chunk_ids: list[str]) -> None:
        ...
