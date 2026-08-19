"""End-to-end evaluator."""
from __future__ import annotations

from graphrag.evaluation.dataset import EvalDataset, EvalSample
from graphrag.evaluation.metrics import exact_match, token_f1
from graphrag.schemas.query import QueryRequest, QueryResponse


class EvalResult:
    def __init__(self, sample: EvalSample, response: QueryResponse) -> None:
        self.question = sample.question
        self.ground_truth = sample.ground_truth
        self.prediction = response.answer
        self.em = exact_match(response.answer, sample.ground_truth)
        self.f1 = token_f1(response.answer, sample.ground_truth)
        self.latency_ms = response.latency_ms


class Evaluator:
    def __init__(self, pipeline) -> None:
        self._pipeline = pipeline

    async def evaluate(self, samples: list[EvalSample]) -> list[EvalResult]:
        results: list[EvalResult] = []
        for sample in samples:
            request = QueryRequest(query=sample.question)
            response = await self._pipeline.run(request)
            results.append(EvalResult(sample, response))
        return results

    def summary(self, results: list[EvalResult]) -> dict:
        if not results:
            return {}
        avg_em = sum(r.em for r in results) / len(results)
        avg_f1 = sum(r.f1 for r in results) / len(results)
        avg_latency = sum(r.latency_ms or 0 for r in results) / len(results)
        return {"n": len(results), "exact_match": avg_em, "token_f1": avg_f1, "avg_latency_ms": avg_latency}
