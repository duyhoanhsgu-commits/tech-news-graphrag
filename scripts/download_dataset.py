#!/usr/bin/env python
"""Download and cache the cc_news dataset from HuggingFace."""
from __future__ import annotations

import typer
from datasets import load_dataset

app = typer.Typer()


@app.command()
def main(
    dataset: str = typer.Option("cc_news", help="HuggingFace dataset name"),
    split: str = typer.Option("train", help="Dataset split"),
    cache_dir: str = typer.Option("data/raw", help="Local cache directory"),
) -> None:
    typer.echo(f"Downloading {dataset} ({split}) → {cache_dir}")
    load_dataset(dataset, split=split, cache_dir=cache_dir)
    typer.echo("Done.")


if __name__ == "__main__":
    app()
