import unittest
from pathlib import Path

from scripts.evaluate_dataset import evaluate_dataset, load_dataset, stable_result

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evaluation" / "labeled_claims.jsonl"


class EvaluationHarnessTests(unittest.TestCase):
    def test_dataset_has_unique_ids_and_stable_hash(self):
        rows_a, hash_a = load_dataset(DATASET)
        rows_b, hash_b = load_dataset(DATASET)
        self.assertEqual(len(rows_a), 20)
        self.assertEqual(hash_a, hash_b)

    def test_replay_decision_is_deterministic(self):
        rows, _ = load_dataset(DATASET)
        for row in rows:
            self.assertEqual(stable_result(row), stable_result(row), row["id"])

    def test_curated_smoke_dataset_matches_declared_labels(self):
        report = evaluate_dataset(DATASET)
        self.assertEqual(report["dataset_size"], 20)
        self.assertEqual(report["mismatches"], [])
        self.assertEqual(report["verdict_metrics"]["accuracy"], 1.0)
        self.assertEqual(report["flagged_vs_unflagged"]["precision"], 1.0)
        self.assertEqual(report["flagged_vs_unflagged"]["recall"], 1.0)
        self.assertIn("not factual truth", report["label_semantics"])

    def test_metrics_report_warns_dataset_is_not_representative(self):
        report = evaluate_dataset(DATASET)
        self.assertTrue(any("not representative" in item for item in report["limitations"]))


if __name__ == "__main__":
    unittest.main()
