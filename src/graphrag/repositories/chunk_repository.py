"""Chunk repository — CRUD operations for chunks in PostgreSQL."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from graphrag.schemas.chunk import Chunk


class ChunkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_batch(self, chunks: list[Chunk]) -> None:
        # TODO: bulk upsert into chunks table
        raise NotImplementedError

    async def get(self, chunk_id: str) -> Chunk | None:
        raise NotImplementedError

    async def get_by_article(self, article_id: str) -> list[Chunk]:
        raise NotImplementedError
