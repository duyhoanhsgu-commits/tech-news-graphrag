#!/usr/bin/env python
"""Ingest articles through the normalisation + cleaning pipeline and save to JSONL."""
from __future__ import annotations

import json
from pathlib import Path

import typer

from graphrag.core.config import get_settings
from graphrag.ingestion.pipeline import IngestionPipeline

app = typer.Typer()


@app.command()
def main(
    limit: int = typer.Option(0, help="Max articles to ingest (0 = all)"),
    output: str = typer.Option("data/processed/articles/articles.jsonl"),
) -> None:
    settings = get_settings()
    pipeline = IngestionPipeline()
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with Path(output).open("w") as fh:
        for article in pipeline.run_from_huggingface(
            settings.dataset_name, settings.dataset_split, limit or settings.articles_limit
        ):
            fh.write(article.model_dump_json() + "\n")
            count += 1
            if count % 500 == 0:
                typer.echo(f"  {count} articles ingested…")
    typer.echo(f"Done — {count} articles written to {output}")


if __name__ == "__main__":
    app()
