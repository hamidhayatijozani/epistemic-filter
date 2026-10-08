import unittest

from epistemic_filter import evaluate_claim, evaluate_event


class EpistemicFilterTests(unittest.TestCase):
    def test_empty_claim_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_claim(" ")

    def test_absolute_guarantee_without_evidence_is_invalid(self):
        result = evaluate_claim("This system is guaranteed to never fail.")
        self.assertEqual(result["verdict"], "INVALID")
        self.assertIn("OVERCLAIM", result["categories"])
        self.assertIn("INSUFFICIENT_EVIDENCE", result["categories"])

    def test_category_error_flagged(self):
        result = evaluate_claim("The model knows the operator's intention.", evidence={"test": "x"}, scope="one test", source_id="run-1")
        self.assertEqual(result["verdict"], "INVALID")
        self.assertIn("CATEGORY_ERROR", result["categories"])

    def test_missing_scope_and_provenance_are_weak(self):
        result = evaluate_claim("The latency was 120 ms.", evidence={"measurement": 120})
        self.assertEqual(result["verdict"], "WEAK")
        self.assertIn("MISSING_SCOPE", result["categories"])
        self.assertIn("MISSING_PROVENANCE", result["categories"])

    def test_fully_scoped_claim_only_means_no_rule_fired(self):
        result = evaluate_claim(
            "In test run R-17, observed latency was 120 ms.",
            evidence={"artifact": "sha256:example"},
            scope="local fixture, 20 requests",
            source_id="R-17",
        )
        self.assertEqual(result["verdict"], "VALID")
        self.assertIn("not verified", result["rationale"])

    def test_event_adapter_reads_prompt(self):
        result = evaluate_event({
            "event_id": "evt-1",
            "workspace_id": "test",
            "tool_params": {"prompt": "This always works."},
        })
        self.assertEqual(result["verdict"], "INVALID")
        self.assertEqual(result["source_id"], "evt-1")


if __name__ == "__main__":
    unittest.main()
