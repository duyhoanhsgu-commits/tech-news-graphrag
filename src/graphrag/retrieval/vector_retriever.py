"""Vector-only retriever."""
from __future__ import annotations

from graphrag.embeddings.base import BaseEmbedder
from graphrag.schemas.retrieval import VectorSearchResult
from graphrag.vectorstore.repository import VectorRepository


class VectorRetriever:
    def __init__(self, repository: VectorRepository, embedder: BaseEmbedder) -> None:
        self._repository = repository
        self._embedder = embedder

    async def retrieve(
        self,
        query: str,
        top_k: int = 20,
    ) -> list[VectorSearchResult]:
        query_vector = await self._embedder.embed_one(query)
        return await self._repository.similarity_search(query_vector, top_k=top_k)
