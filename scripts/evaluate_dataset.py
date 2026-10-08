"""Evaluate the rule-based filter against a versioned, labeled JSONL dataset.

Metrics measure agreement with the dataset's screening-policy labels only. They do
not measure factual truth detection or general-world accuracy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from epistemic_filter import evaluate_claim  # noqa: E402

LABELS = ("INVALID", "WEAK", "VALID")


def load_dataset(path: Path) -> tuple[list[dict[str, Any]], str]:
    raw = path.read_bytes()
    rows = []
    for line_number, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        required = {"id", "claim", "expected_verdict", "expected_flagged"}
        missing = required - row.keys()
        if missing:
            raise ValueError(f"{path}:{line_number}: missing fields {sorted(missing)}")
        if row["expected_verdict"] not in LABELS:
            raise ValueError(f"{path}:{line_number}: unsupported expected_verdict")
        if not isinstance(row["expected_flagged"], bool):
            raise ValueError(f"{path}:{line_number}: expected_flagged must be boolean")
        rows.append(row)
    if not rows:
        raise ValueError(f"Dataset is empty: {path}")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Dataset contains duplicate ids")
    return rows, hashlib.sha256(raw).hexdigest()


def stable_result(row: dict[str, Any]) -> dict[str, Any]:
    result = evaluate_claim(
        row["claim"],
        evidence=row.get("evidence"),
        scope=row.get("scope"),
        source_id=row.get("source_id"),
    )
    # evaluated_at is intentionally removed: this test compares decision semantics.
    result.pop("evaluated_at", None)
    return result


def classification_metrics(y_true: list[str], y_pred: list[str]) -> dict[str, Any]:
    matrix = {actual: {predicted: 0 for predicted in LABELS} for actual in LABELS}
    for actual, predicted in zip(y_true, y_pred):
        matrix[actual][predicted] += 1
    per_class = {}
    for label in LABELS:
        tp = matrix[label][label]
        fp = sum(matrix[actual][label] for actual in LABELS if actual != label)
        fn = sum(matrix[label][predicted] for predicted in LABELS if predicted != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = {
            "support": sum(matrix[label].values()),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }
    total = len(y_true)
    correct = sum(y == p for y, p in zip(y_true, y_pred))
    return {
        "accuracy": round(correct / total, 4) if total else 0.0,
        "confusion_matrix_rows_actual_columns_predicted": matrix,
        "per_class": per_class,
        "macro_f1": round(sum(per_class[label]["f1"] for label in LABELS) / len(LABELS), 4),
    }


def evaluate_dataset(path: Path) -> dict[str, Any]:
    rows, dataset_sha256 = load_dataset(path)
    results = [stable_result(row) for row in rows]
    by_id = {row["id"]: result for row, result in zip(rows, results)}
    expected = [row["expected_verdict"] for row in rows]
    predicted = [result["verdict"] for result in results]
    expected_flagged = [row["expected_flagged"] for row in rows]
    predicted_flagged = [result["verdict"] != "VALID" for result in results]
    tp = sum(a and p for a, p in zip(expected_flagged, predicted_flagged))
    fp = sum((not a) and p for a, p in zip(expected_flagged, predicted_flagged))
    fn = sum(a and (not p) for a, p in zip(expected_flagged, predicted_flagged))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    mismatches = [
        {
            "id": row["id"],
            "expected_verdict": row["expected_verdict"],
            "predicted_verdict": by_id[row["id"]]["verdict"],
        }
        for row in rows
        if row["expected_verdict"] != by_id[row["id"]]["verdict"]
    ]
    return {
        "evaluation_schema_version": "1.0",
        "dataset_path": str(path),
        "dataset_sha256": dataset_sha256,
        "dataset_size": len(rows),
        "runtime_version": "0.1.0",
        "git_commit": os.environ.get("GITHUB_SHA", "UNKNOWN"),
        "label_semantics": "agreement with curated screening-policy labels; not factual truth",
        "verdict_metrics": classification_metrics(expected, predicted),
        "flagged_vs_unflagged": {
            "positive_class": "expected_flagged=true",
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        },
        "mismatches": mismatches,
        "limitations": [
            "Small, manually curated synthetic smoke dataset; not representative of production traffic.",
            "Metrics quantify agreement with declared screening labels, not factual correctness.",
            "No latency benchmark or statistical confidence interval is computed.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=ROOT / "evaluation" / "labeled_claims.jsonl")
    parser.add_argument("--output", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args()
    report = evaluate_dataset(args.dataset)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report["mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
