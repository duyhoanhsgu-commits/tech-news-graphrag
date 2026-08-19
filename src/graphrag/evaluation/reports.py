"""Evaluation report generator."""
from __future__ import annotations

import json
from pathlib import Path

from graphrag.evaluation.evaluator import EvalResult


class ReportGenerator:
    def save_jsonl(self, results: list[EvalResult], path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with Path(path).open("w") as fh:
            for r in results:
                fh.write(json.dumps({
                    "question": r.question,
                    "ground_truth": r.ground_truth,
                    "prediction": r.prediction,
                    "exact_match": r.em,
                    "token_f1": r.f1,
                    "latency_ms": r.latency_ms,
                }) + "\n")

    def print_summary(self, summary: dict) -> None:
        print("\n=== Evaluation Summary ===")
        for k, v in summary.items():
            print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")
