"""Abstract base chunker."""
from __future__ import annotations

from abc import ABC, abstractmethod

from graphrag.schemas.article import Article
from graphrag.schemas.chunk import Chunk


class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, article: Article) -> list[Chunk]:
        ...
