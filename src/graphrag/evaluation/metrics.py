"""Evaluation metrics — faithfulness, answer relevance, context precision."""
from __future__ import annotations

import re


def exact_match(prediction: str, ground_truth: str) -> float:
    return 1.0 if prediction.strip().lower() == ground_truth.strip().lower() else 0.0


def token_f1(prediction: str, ground_truth: str) -> float:
    pred_tokens = set(re.findall(r"\w+", prediction.lower()))
    truth_tokens = set(re.findall(r"\w+", ground_truth.lower()))
    if not pred_tokens or not truth_tokens:
        return 0.0
    common = pred_tokens & truth_tokens
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def citation_coverage(answer: str, expected_citations: int) -> float:
    found = len(re.findall(r"\[\d+\]", answer))
    return min(found / max(expected_citations, 1), 1.0)
