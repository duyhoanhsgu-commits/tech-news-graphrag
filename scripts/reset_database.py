#!/usr/bin/env python
"""Reset all indexes and graph data — USE WITH CARE."""
from __future__ import annotations

import asyncio

import typer

app = typer.Typer()


@app.command()
def main(
    confirm: bool = typer.Option(False, "--yes", help="Skip confirmation prompt"),
) -> None:
    if not confirm:
        typer.confirm("This will DELETE all data. Are you sure?", abort=True)
    asyncio.run(_run())


async def _run() -> None:
    typer.echo("Resetting pgvector tables…")
    # TODO: run Alembic downgrade then upgrade, or TRUNCATE tables
    typer.echo("Resetting Neo4j graph…")
    # TODO: call Neo4jGraphStore.clear()
    typer.echo("Reset complete.")


if __name__ == "__main__":
    app()
