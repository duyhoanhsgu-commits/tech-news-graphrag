"""Evaluation dataset loader."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator


class EvalSample:
    def __init__(self, question: str, ground_truth: str, metadata: dict | None = None) -> None:
        self.question = question
        self.ground_truth = ground_truth
        self.metadata = metadata or {}


class EvalDataset:
    def load(self, questions_path: str, ground_truth_path: str) -> list[EvalSample]:
        questions = list(self._read_jsonl(questions_path))
        truths = list(self._read_jsonl(ground_truth_path))
        return [
            EvalSample(
                question=q["question"],
                ground_truth=t["answer"],
                metadata=q.get("metadata"),
            )
            for q, t in zip(questions, truths)
        ]

    def _read_jsonl(self, path: str) -> Iterator[dict]:
        with Path(path).open() as fh:
            for line in fh:
                yield json.loads(line)
