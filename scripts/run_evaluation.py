#!/usr/bin/env python
"""Run end-to-end retrieval / generation evaluation and save a report."""
from __future__ import annotations

import asyncio

import typer

from graphrag.core.config import get_settings
from graphrag.evaluation.dataset import EvalDataset
from graphrag.evaluation.evaluator import Evaluator
from graphrag.evaluation.reports import ReportGenerator

app = typer.Typer()


@app.command()
def main(
    questions: str = typer.Option("data/evaluation/questions.jsonl"),
    ground_truth: str = typer.Option("data/evaluation/ground_truth.jsonl"),
    output: str = typer.Option("data/evaluation/results.jsonl"),
    mode: str = typer.Option("graphrag", help="graphrag | vector"),
) -> None:
    asyncio.run(_run(questions, ground_truth, output, mode))


async def _run(questions: str, ground_truth: str, output: str, mode: str) -> None:
    settings = get_settings()
    dataset = EvalDataset()
    samples = dataset.load(questions, ground_truth)
    typer.echo(f"Loaded {len(samples)} eval samples. Running {mode} pipeline…")

    # TODO: build the correct pipeline from settings and inject into Evaluator
    pipeline = None  # placeholder
    evaluator = Evaluator(pipeline)
    results = await evaluator.evaluate(samples)

    reporter = ReportGenerator()
    reporter.save_jsonl(results, output)
    reporter.print_summary(evaluator.summary(results))
    typer.echo(f"Results saved to {output}")


if __name__ == "__main__":
    app()
