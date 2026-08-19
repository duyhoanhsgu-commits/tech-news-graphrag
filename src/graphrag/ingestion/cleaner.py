"""Article content cleaner — strips HTML, boilerplate, and short articles."""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from graphrag.schemas.article import Article

MIN_CONTENT_LENGTH: int = 100


class ArticleCleaner:
    def clean(self, article: Article) -> Article | None:
        content = self._strip_html(article.content)
        content = self._remove_boilerplate(content)
        if len(content) < MIN_CONTENT_LENGTH:
            return None
        return article.model_copy(update={"content": content})

    def _strip_html(self, text: str) -> str:
        soup = BeautifulSoup(text, "lxml")
        return soup.get_text(separator=" ")

    def _remove_boilerplate(self, text: str) -> str:
        patterns = [
            r"Share this article.*?(?=\n)",
            r"Subscribe to.*?(?=\n)",
            r"Read more:.*?(?=\n)",
        ]
        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text.strip()
