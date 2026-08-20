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
    dataset: str = typer.Option("vencortex/TechNews", help="HuggingFace dataset name"),
    limit: int = typer.Option(0, help="Max articles to ingest (0 = download all / unlimited)"),
    output: str = typer.Option("data/processed/articles/articles.jsonl"),
    append: bool = typer.Option(False, "--append", help="Append to output instead of overwrite"),
) -> None:
    settings = get_settings()
    pipeline = IngestionPipeline()
    dataset_name = dataset or settings.dataset_name
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    count = 0
    typer.echo(f"Starting ingestion from '{dataset_name}' (limit={'ALL' if limit == 0 else limit})...")
    with Path(output).open(mode) as fh:
        for article in pipeline.run_from_huggingface(
            dataset_name, settings.dataset_split, limit=limit
        ):
            fh.write(article.model_dump_json() + "\n")
            count += 1
            if count % 1000 == 0:
                typer.echo(f"  {count} articles ingested…")
    typer.echo(f"Done — {count} articles written to {output}")


if __name__ == "__main__":
    app()
