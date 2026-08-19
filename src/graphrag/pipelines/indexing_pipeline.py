"""Indexing pipeline — ingest → chunk → embed → upsert → build graph."""
from __future__ import annotations

from graphrag.chunking.pipeline import ChunkingPipeline
from graphrag.embeddings.pipeline import EmbeddingPipeline
from graphrag.graph.builder import GraphBuilder
from graphrag.ingestion.pipeline import IngestionPipeline
from graphrag.vectorstore.repository import VectorRepository


class IndexingPipeline:
    def __init__(
        self,
        ingestion: IngestionPipeline,
        chunking: ChunkingPipeline,
        embedding: EmbeddingPipeline,
        vector_repository: VectorRepository,
        graph_builder: GraphBuilder,
        batch_size: int = 64,
    ) -> None:
        self._ingestion = ingestion
        self._chunking = chunking
        self._embedding = embedding
        self._vector_repository = vector_repository
        self._graph_builder = graph_builder
        self._batch_size = batch_size

    async def run(self, dataset_name: str, split: str = "train", limit: int = 0) -> None:
        articles = self._ingestion.run_from_huggingface(dataset_name, split, limit)
        chunk_iter = self._chunking.run(articles)

        batch: list = []
        for chunk in chunk_iter:
            batch.append(chunk)
            if len(batch) >= self._batch_size:
                await self._flush(batch)
                batch = []
        if batch:
            await self._flush(batch)

    async def _flush(self, chunks: list) -> None:
        embedded = await self._embedding.run(chunks)
        await self._vector_repository.add_chunks(embedded)
        await self._graph_builder.build_from_chunks(embedded)
