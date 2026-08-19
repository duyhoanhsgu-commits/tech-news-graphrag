"""Chunking pipeline — applies a chunker to a stream of articles."""
from __future__ import annotations

from typing import Iterator

from graphrag.chunking.base import BaseChunker
from graphrag.chunking.recursive import RecursiveChunker
from graphrag.schemas.article import Article
from graphrag.schemas.chunk import Chunk


class ChunkingPipeline:
    def __init__(self, chunker: BaseChunker | None = None) -> None:
        self._chunker = chunker or RecursiveChunker()

    def run(self, articles: Iterator[Article]) -> Iterator[Chunk]:
        for article in articles:
            yield from self._chunker.chunk(article)
