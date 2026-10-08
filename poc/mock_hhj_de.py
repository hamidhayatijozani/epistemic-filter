"""Small deterministic mock for testing the AgentRQ/HHJ-DE boundary."""
from __future__ import annotations

from typing import Any, Mapping

from epistemic_filter import evaluate_event


def decide(event: Mapping[str, Any]) -> dict[str, Any]:
    result = evaluate_event(event)
    # This mock only maps epistemic screening to a conservative action suggestion.
    action = {"VALID": "REVIEW", "WEAK": "ASK", "INVALID": "HOLD"}[result["verdict"]]
    return {"event_id": event.get("event_id"), "action": action, "epistemic_result": result}


if __name__ == "__main__":
    sample = {
        "event_id": "mock-001",
        "workspace_id": "local-demo",
        "tool_name": "deploy",
        "tool_params": {"claim": "This deployment is guaranteed never to fail."},
    }
    import json
    print(json.dumps(decide(sample), indent=2))
