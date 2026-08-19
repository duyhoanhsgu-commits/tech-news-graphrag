"""Citation builder — extracts [N] references from LLM output."""
from __future__ import annotations

import re

from graphrag.schemas.query import Citation
from graphrag.schemas.retrieval import RerankedResult


class CitationBuilder:
    def extract(
        self,
        answer: str,
        results: list[RerankedResult],
    ) -> list[Citation]:
        indices = {int(m) for m in re.findall(r"\[(\d+)\]", answer)}
        citations: list[Citation] = []
        for idx in sorted(indices):
            if 1 <= idx <= len(results):
                chunk = results[idx - 1].chunk
                citations.append(
                    Citation(
                        chunk_id=chunk.chunk_id,
                        article_id=chunk.article_id,
                        excerpt=chunk.content[:200],
                    )
                )
        return citations
