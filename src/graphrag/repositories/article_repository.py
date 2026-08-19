"""Article repository — CRUD operations for articles in PostgreSQL."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from graphrag.schemas.article import Article


class ArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, article: Article) -> None:
        # TODO: upsert into articles table
        raise NotImplementedError

    async def get(self, article_id: str) -> Article | None:
        # TODO: SELECT from articles table
        raise NotImplementedError

    async def list(self, limit: int = 100, offset: int = 0) -> list[Article]:
        raise NotImplementedError
