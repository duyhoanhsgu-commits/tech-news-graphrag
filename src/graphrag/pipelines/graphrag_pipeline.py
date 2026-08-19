"""GraphRAG query pipeline — hybrid retrieval + rerank + generate."""
from __future__ import annotations

import time

from graphrag.generation.answer_generator import AnswerGenerator
from graphrag.generation.citation_builder import CitationBuilder
from graphrag.retrieval.context_builder import ContextBuilder
from graphrag.retrieval.hybrid_retriever import HybridRetriever
from graphrag.retrieval.reranker import Reranker
from graphrag.schemas.query import QueryRequest, QueryResponse


class GraphRAGPipeline:
    def __init__(
        self,
        retriever: HybridRetriever,
        reranker: Reranker,
        context_builder: ContextBuilder,
        generator: AnswerGenerator,
        citation_builder: CitationBuilder,
        top_k: int = 5,
    ) -> None:
        self._retriever = retriever
        self._reranker = reranker
        self._context_builder = context_builder
        self._generator = generator
        self._citation_builder = citation_builder
        self._top_k = top_k

    async def run(self, request: QueryRequest) -> QueryResponse:
        t0 = time.perf_counter()
        candidates = await self._retriever.retrieve(request.query, top_k=request.top_k * 4)
        reranked = self._reranker.rerank(request.query, candidates, top_k=request.top_k)
        context = self._context_builder.build(reranked)
        answer = await self._generator.generate(request.query, context)
        citations = self._citation_builder.extract(answer, reranked) if request.include_sources else []
        latency_ms = (time.perf_counter() - t0) * 1000
        return QueryResponse(
            query=request.query,
            answer=answer,
            citations=citations,
            mode="graphrag",
            latency_ms=round(latency_ms, 2),
        )
