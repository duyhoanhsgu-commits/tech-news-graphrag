"""Unit tests for vector retriever (mock embedder + mock repository)."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from graphrag.retrieval.vector_retriever import VectorRetriever
from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult


@pytest.fixture
def mock_embedder():
    embedder = AsyncMock()
    embedder.embed_one.return_value = [0.1] * 1536
    return embedder


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    chunk = Chunk(chunk_id="c1", article_id="a1", content="text", chunk_index=0, start_char=0, end_char=4)
    repo.similarity_search.return_value = [VectorSearchResult(chunk=chunk, score=0.9)]
    return repo


@pytest.mark.asyncio
async def test_retrieve_returns_results(mock_embedder, mock_repo) -> None:
    retriever = VectorRetriever(mock_repo, mock_embedder)
    results = await retriever.retrieve("What is OpenAI?", top_k=5)
    assert len(results) == 1
    assert results[0].score == 0.9
