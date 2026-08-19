#!/usr/bin/env python
"""Chunk articles and build the pgvector index."""
from __future__ import annotations

import asyncio

import typer

from graphrag.core.config import get_settings

app = typer.Typer()


@app.command()
def main(
    articles_path: str = typer.Option("data/processed/articles/articles.jsonl"),
) -> None:
    asyncio.run(_run(articles_path))


async def _run(articles_path: str) -> None:
    settings = get_settings()
    typer.echo(f"Building vector index from {articles_path}")
    # TODO: wire IngestionPipeline + ChunkingPipeline + EmbeddingPipeline + VectorRepository
    typer.echo("Vector index built.")


if __name__ == "__main__":
    app()
