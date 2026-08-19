"""Graph-aware retriever — expands results via entity neighborhood traversal."""
from __future__ import annotations

from graphrag.graph.store.repository import GraphRepository
from graphrag.schemas.retrieval import GraphSearchResult, VectorSearchResult


class GraphRetriever:
    def __init__(
        self,
        graph_repository: GraphRepository,
        max_hops: int = 2,
    ) -> None:
        self._graph_repository = graph_repository
        self._max_hops = max_hops

    async def expand(
        self,
        vector_results: list[VectorSearchResult],
        top_k: int = 10,
    ) -> list[GraphSearchResult]:
        # TODO: resolve entity IDs from chunks, then traverse the graph
        # For now return vector results wrapped as GraphSearchResult stubs
        return [
            GraphSearchResult(chunk=r.chunk, graph_score=r.score)
            for r in vector_results[:top_k]
        ]
