"""Article normalizer — field standardisation and type coercion."""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime

from graphrag.schemas.article import Article


class ArticleNormalizer:
    def normalize(self, article: Article) -> Article:
        return article.model_copy(
            update={
                "title": self._clean_text(article.title),
                "content": self._clean_text(article.content),
                "published_at": self._parse_date(article.published_at),
            }
        )

    def _clean_text(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _parse_date(self, value: datetime | str | None) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            return None
