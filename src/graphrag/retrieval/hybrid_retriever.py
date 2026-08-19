"""Hybrid retriever — Reciprocal Rank Fusion of vector + graph results."""
from __future__ import annotations

from graphrag.retrieval.graph_retriever import GraphRetriever
from graphrag.retrieval.vector_retriever import VectorRetriever
from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult


class HybridRetriever:
    def __init__(
        self,
        vector_retriever: VectorRetriever,
        graph_retriever: GraphRetriever,
        vector_weight: float = 0.6,
        graph_weight: float = 0.4,
        k: int = 60,
    ) -> None:
        self._vector_retriever = vector_retriever
        self._graph_retriever = graph_retriever
        self._vector_weight = vector_weight
        self._graph_weight = graph_weight
        self._k = k

    async def retrieve(self, query: str, top_k: int = 10) -> list[VectorSearchResult]:
        vector_results = await self._vector_retriever.retrieve(query, top_k=top_k * 2)
        graph_results = await self._graph_retriever.expand(vector_results, top_k=top_k * 2)

        scores: dict[str, float] = {}
        for rank, r in enumerate(vector_results, 1):
            scores[r.chunk.chunk_id] = scores.get(r.chunk.chunk_id, 0.0) + self._vector_weight / (self._k + rank)
        for rank, r in enumerate(graph_results, 1):
            scores[r.chunk.chunk_id] = scores.get(r.chunk.chunk_id, 0.0) + self._graph_weight / (self._k + rank)

        chunk_map: dict[str, Chunk] = {r.chunk.chunk_id: r.chunk for r in vector_results}
        chunk_map.update({r.chunk.chunk_id: r.chunk for r in graph_results})

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [VectorSearchResult(chunk=chunk_map[cid], score=score) for cid, score in ranked]
