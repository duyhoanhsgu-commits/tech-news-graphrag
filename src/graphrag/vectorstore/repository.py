"""High-level vector store repository used by retrievers."""
from __future__ import annotations

from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult
from graphrag.vectorstore.base import BaseVectorStore


class VectorRepository:
    def __init__(self, store: BaseVectorStore) -> None:
        self._store = store

    async def add_chunks(self, chunks: list[Chunk]) -> None:
        await self._store.upsert(chunks)

    async def similarity_search(
        self,
        query_vector: list[float],
        top_k: int = 10,
    ) -> list[VectorSearchResult]:
        return await self._store.search(query_vector, top_k=top_k)

    async def remove_chunks(self, chunk_ids: list[str]) -> None:
        await self._store.delete(chunk_ids)
