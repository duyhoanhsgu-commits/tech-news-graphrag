"""Article schema."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Article(BaseModel):
    article_id: str
    title: str
    content: str
    url: str | None = None
    source: str | None = None
    published_at: datetime | None = None
    language: str = "en"
    metadata: dict = Field(default_factory=dict)
