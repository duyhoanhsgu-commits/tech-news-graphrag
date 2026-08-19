"""Context builder — formats retrieved chunks into an LLM-ready context string."""
from __future__ import annotations

from graphrag.schemas.retrieval import RerankedResult


class ContextBuilder:
    def __init__(self, max_tokens: int = 4096) -> None:
        self._max_tokens = max_tokens

    def build(self, results: list[RerankedResult]) -> str:
        parts: list[str] = []
        total = 0
        for i, r in enumerate(results, 1):
            tokens = len(r.chunk.content.split())
            if total + tokens > self._max_tokens:
                break
            parts.append(f"[{i}] {r.chunk.content}")
            total += tokens
        return "\n\n".join(parts)
