"""Ingestion pipeline — orchestrates loader → normalizer → cleaner."""
from __future__ import annotations

from typing import Iterator

from graphrag.ingestion.cleaner import ArticleCleaner
from graphrag.ingestion.loader import ArticleLoader
from graphrag.ingestion.normalizer import ArticleNormalizer
from graphrag.schemas.article import Article


class IngestionPipeline:
    def __init__(self) -> None:
        self._loader = ArticleLoader()
        self._normalizer = ArticleNormalizer()
        self._cleaner = ArticleCleaner()

    def run_from_huggingface(
        self,
        dataset_name: str,
        split: str = "train",
        limit: int = 0,
    ) -> Iterator[Article]:
        for article in self._loader.load_huggingface(dataset_name, split, limit):
            yield from self._process(article)

    def run_from_jsonl(self, path: str) -> Iterator[Article]:
        for article in self._loader.load_jsonl(path):
            yield from self._process(article)

    def _process(self, article: Article) -> Iterator[Article]:
        article = self._normalizer.normalize(article)
        cleaned = self._cleaner.clean(article)
        if cleaned is not None:
            yield cleaned
