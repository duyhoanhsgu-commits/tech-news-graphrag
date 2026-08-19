"""Unit tests for chunking."""
from __future__ import annotations

import pytest

from graphrag.chunking.recursive import RecursiveChunker
from graphrag.schemas.article import Article


def test_chunker_produces_chunks(sample_article: Article) -> None:
    chunker = RecursiveChunker(chunk_size=200, chunk_overlap=20)
    chunks = chunker.chunk(sample_article)
    assert len(chunks) > 0


def test_chunk_ids_are_unique(sample_article: Article) -> None:
    chunker = RecursiveChunker(chunk_size=200, chunk_overlap=20)
    chunks = chunker.chunk(sample_article)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))


def test_all_chunks_reference_article(sample_article: Article) -> None:
    chunker = RecursiveChunker(chunk_size=200, chunk_overlap=20)
    chunks = chunker.chunk(sample_article)
    assert all(c.article_id == sample_article.article_id for c in chunks)
