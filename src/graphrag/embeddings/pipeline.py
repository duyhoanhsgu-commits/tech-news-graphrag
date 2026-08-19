"""Embedding pipeline — batches chunks through an embedder."""
from __future__ import annotations

from typing import Iterator

from graphrag.embeddings.base import BaseEmbedder
from graphrag.schemas.chunk import Chunk


class EmbeddingPipeline:
    def __init__(self, embedder: BaseEmbedder, batch_size: int = 512) -> None:
        self._embedder = embedder
        self._batch_size = batch_size

    async def run(self, chunks: list[Chunk]) -> list[Chunk]:
        embedded: list[Chunk] = []
        for batch in self._batches(chunks):
            texts = [c.content for c in batch]
            vectors = await self._embedder.embed(texts)
            for chunk, vector in zip(batch, vectors):
                embedded.append(chunk.model_copy(update={"embedding": vector}))
        return embedded

    def _batches(self, chunks: list[Chunk]) -> Iterator[list[Chunk]]:
        for i in range(0, len(chunks), self._batch_size):
            yield chunks[i : i + self._batch_size]
