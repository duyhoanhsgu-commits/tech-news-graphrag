#!/usr/bin/env python
"""Extract entities and relations from chunks and load them into Neo4j."""
from __future__ import annotations

import asyncio

import typer

app = typer.Typer()


@app.command()
def main(
    chunks_path: str = typer.Option("data/processed/chunks"),
    batch_size: int = typer.Option(16),
) -> None:
    asyncio.run(_run(chunks_path, batch_size))


async def _run(chunks_path: str, batch_size: int) -> None:
    typer.echo(f"Building knowledge graph from chunks in {chunks_path}")
    # TODO: wire GraphBuilder with EntityExtractor + RelationExtractor + Neo4jGraphStore
    typer.echo("Knowledge graph built.")


if __name__ == "__main__":
    app()
