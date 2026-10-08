import unittest

from poc.mock_hhj_de import decide


class MockIntegrationContractTests(unittest.TestCase):
    def test_invalid_screening_maps_to_hold_and_preserves_event_id(self):
        result = decide({
            "event_id": "evt-invalid-001",
            "tool_params": {"claim": "This system is guaranteed never to fail."},
        })
        self.assertEqual(result["event_id"], "evt-invalid-001")
        self.assertEqual(result["action"], "HOLD")
        self.assertEqual(result["epistemic_result"]["verdict"], "INVALID")

    def test_missing_scope_maps_to_ask(self):
        result = decide({
            "event_id": "evt-weak-001",
            "claim": "The test measured 12 errors.",
            "evidence": {"log": "fixture"},
            "source_id": "run-12",
        })
        self.assertEqual(result["action"], "ASK")
        self.assertEqual(result["epistemic_result"]["verdict"], "WEAK")

    def test_scoped_observation_maps_to_review_not_automatic_allow(self):
        result = decide({
            "event_id": "evt-valid-001",
            "claim": "In run R-1, the endpoint returned HTTP 403.",
            "evidence": {"artifact": "sha256:fixture"},
            "scope": "isolated test, one request",
            "source_id": "R-1",
        })
        self.assertEqual(result["action"], "REVIEW")
        self.assertEqual(result["epistemic_result"]["verdict"], "VALID")

    def test_missing_claim_fails_explicitly(self):
        with self.assertRaises(ValueError):
            decide({"event_id": "evt-no-claim", "tool_params": {"action": "deploy"}})


if __name__ == "__main__":
    unittest.main()
