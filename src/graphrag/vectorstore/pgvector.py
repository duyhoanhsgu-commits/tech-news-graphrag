"""pgvector implementation of the vector store."""
from __future__ import annotations

from sqlalchemy import Column, Index, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from graphrag.core.config import Settings
from graphrag.schemas.chunk import Chunk
from graphrag.schemas.retrieval import VectorSearchResult
from graphrag.vectorstore.base import BaseVectorStore


class Base(DeclarativeBase):
    pass


class ChunkRow(Base):
    __tablename__ = "chunks"

    chunk_id = Column(String, primary_key=True)
    article_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    chunk_index = Column(String, nullable=False)
    # embedding stored as pgvector type — migration sets this column via Alembic
    __table_args__ = (
        Index("ix_chunks_article_id", "article_id"),
    )


class PgVectorStore(BaseVectorStore):
    def __init__(self, settings: Settings) -> None:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        self._session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def upsert(self, chunks: list[Chunk]) -> None:
        # TODO: implement bulk upsert with pgvector embeddings
        raise NotImplementedError

    async def search(
        self,
        query_vector: list[float],
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[VectorSearchResult]:
        # TODO: implement cosine similarity search via pgvector
        raise NotImplementedError

    async def delete(self, chunk_ids: list[str]) -> None:
        raise NotImplementedError
