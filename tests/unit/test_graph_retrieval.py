"""Unit tests for graph retriever (mock graph repository)."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from graphrag.retrieval.graph_retriever import GraphRetriever
from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult


@pytest.fixture
def mock_graph_repo():
    return AsyncMock()


@pytest.fixture
def vector_results() -> list[VectorSearchResult]:
    chunk = Chunk(chunk_id="c1", article_id="a1", content="text", chunk_index=0, start_char=0, end_char=4)
    return [VectorSearchResult(chunk=chunk, score=0.8)]


@pytest.mark.asyncio
async def test_expand_returns_graph_results(mock_graph_repo, vector_results) -> None:
    retriever = GraphRetriever(mock_graph_repo, max_hops=1)
    results = await retriever.expand(vector_results, top_k=5)
    assert len(results) == 1
    assert results[0].chunk.chunk_id == "c1"
