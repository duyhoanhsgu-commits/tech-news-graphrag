"""Cross-encoder reranker."""
from __future__ import annotations

from graphrag.schemas.retrieval import RerankedResult, VectorSearchResult


class Reranker:
    def __init__(self, model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        from sentence_transformers import CrossEncoder  # type: ignore[import]
        self._model = CrossEncoder(model)

    def rerank(
        self,
        query: str,
        results: list[VectorSearchResult],
        top_k: int = 5,
    ) -> list[RerankedResult]:
        pairs = [(query, r.chunk.content) for r in results]
        scores: list[float] = self._model.predict(pairs).tolist()
        ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            RerankedResult(chunk=r.chunk, rerank_score=score, original_rank=i)
            for i, (r, score) in enumerate(ranked)
        ]
