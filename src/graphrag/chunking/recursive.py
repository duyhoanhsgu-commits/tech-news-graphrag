"""Recursive character text splitter chunker."""
from __future__ import annotations

import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter

from graphrag.chunking.base import BaseChunker
from graphrag.schemas.article import Article
from graphrag.schemas.chunk import Chunk


class RecursiveChunker(BaseChunker):
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def chunk(self, article: Article) -> list[Chunk]:
        texts = self._splitter.split_text(article.content)
        chunks: list[Chunk] = []
        pos = 0
        for idx, text in enumerate(texts):
            start = article.content.find(text, pos)
            end = start + len(text)
            chunk_id = hashlib.md5(f"{article.article_id}-{idx}".encode()).hexdigest()
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    article_id=article.article_id,
                    content=text,
                    chunk_index=idx,
                    start_char=start,
                    end_char=end,
                )
            )
            pos = start
        return chunks
