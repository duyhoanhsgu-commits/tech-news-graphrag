"""Article loader — reads from HuggingFace datasets or local JSONL files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from graphrag.core.exceptions import DatasetNotFoundError
from graphrag.schemas.article import Article


class ArticleLoader:
    def load_jsonl(self, path: str | Path) -> Iterator[Article]:
        path = Path(path)
        if not path.exists():
            raise DatasetNotFoundError(f"File not found: {path}")
        with path.open() as fh:
            for line in fh:
                yield Article.model_validate(json.loads(line))

    def load_huggingface(
        self,
        dataset_name: str,
        split: str = "train",
        limit: int = 0,
    ) -> Iterator[Article]:
        try:
            from datasets import load_dataset  # type: ignore[import]
        except ImportError as exc:
            raise ImportError("Install 'datasets' to load from HuggingFace") from exc

        ds = load_dataset(dataset_name, split=split, streaming=True)
        for i, row in enumerate(ds):
            if limit and i >= limit:
                break
            title = row.get("title") or row.get("companyName") or row.get("headline") or ""
            content = row.get("text") or row.get("content") or row.get("description") or row.get("article") or ""
            yield Article(
                article_id=str(row.get("id", i)),
                title=title,
                content=content,
                url=row.get("url") or row.get("link"),
                source=row.get("domain") or row.get("source"),
                published_at=row.get("date") or row.get("published_at"),
            )
