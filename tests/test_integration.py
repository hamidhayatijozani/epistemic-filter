import unittest

from epistemic_filter import evaluate_event


class RuntimeEventIntegrationTests(unittest.TestCase):
    def test_event_decision_has_contract_fields(self):
        result = evaluate_event({
            "event_id": "evt-integration-001",
            "workspace_id": "ws-test",
            "tool_name": "deployment_tool",
            "tool_params": {"claim": "Deployment completed in the isolated test."},
            "evidence_refs": ["artifact://test-run/001"],
            "scope": "isolated test environment",
            "source_id": "test-run-001",
        })
        for field in (
            "schema_version", "filter_version", "verdict", "categories",
            "confidence", "rationale", "claim", "evaluated_at", "limitations",
        ):
            self.assertIn(field, result)
        self.assertIn(result["verdict"], {"VALID", "WEAK", "INVALID"})
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)


if __name__ == "__main__":
    unittest.main()
