"""Shared pytest fixtures."""
from __future__ import annotations

import pytest

from graphrag.schemas.article import Article
from graphrag.schemas.chunk import Chunk


@pytest.fixture
def sample_article() -> Article:
    return Article(
        article_id="art-001",
        title="OpenAI releases GPT-5",
        content="OpenAI announced GPT-5 today, a major leap in AI capabilities. " * 20,
    )


@pytest.fixture
def sample_chunk(sample_article: Article) -> Chunk:
    return Chunk(
        chunk_id="chunk-001",
        article_id=sample_article.article_id,
        content=sample_article.content[:512],
        chunk_index=0,
        start_char=0,
        end_char=512,
    )
