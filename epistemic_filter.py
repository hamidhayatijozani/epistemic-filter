"""Deterministic, explainable epistemic-claim screening prototype.

This module flags risky wording and missing evidence metadata. It does not verify
whether a claim is true, replace expert review, or infer facts from an LLM.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Mapping

VERSION = "0.1.0"

_ABSOLUTES = (
    r"\balways\b", r"\bnever\b", r"\bguaranteed?\b", r"\b100\s*%\b",
    r"\bzero risk\b", r"\bimpossible to fail\b", r"\ball (?:users|systems|cases)\b",
    r"\bproven (?:safe|secure|effective|to work)\b",
)
_CATEGORY_ERROR_PATTERNS = (
    (r"\bthe model (?:wants|believes|knows|intends)\b", "Anthropomorphic mental-state wording needs operational definition."),
    (r"\bcorrelation proves causation\b", "Correlation alone does not establish causation."),
)
_EVIDENCE_CUES = ("because", "according to", "measured", "observed", "test", "artifact", "source", "log", "dataset", "study")


def evaluate_claim(
    claim: str,
    *,
    evidence: Any = None,
    scope: str | None = None,
    source_id: str | None = None,
) -> dict[str, Any]:
    """Return a stable decision object for a single claim.

    Verdicts:
      INVALID: a known category-error pattern or unsupported absolute guarantee.
      WEAK: insufficient provenance/scope or high-risk wording.
      VALID: no configured heuristic fired and basic provenance is supplied.
    VALID means only 'no configured rule fired', not that the claim is true.
    """
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim must be a non-empty string")

    text = claim.strip()
    lower = text.lower()
    findings: list[dict[str, str]] = []

    for pattern, message in _CATEGORY_ERROR_PATTERNS:
        if re.search(pattern, lower):
            findings.append({"category": "CATEGORY_ERROR", "message": message})

    absolute_hits = [pattern for pattern in _ABSOLUTES if re.search(pattern, lower)]
    if absolute_hits:
        findings.append({
            "category": "OVERCLAIM",
            "message": "Absolute or guarantee language requires unusually strong, scoped evidence.",
        })

    evidence_present = evidence is not None and evidence != "" and evidence != [] and evidence != {}
    scope_present = isinstance(scope, str) and bool(scope.strip())
    source_present = isinstance(source_id, str) and bool(source_id.strip())
    if not evidence_present:
        findings.append({"category": "INSUFFICIENT_EVIDENCE", "message": "No explicit evidence object/reference was supplied."})
    if not scope_present:
        findings.append({"category": "MISSING_SCOPE", "message": "Claim scope is not specified."})
    if not source_present:
        findings.append({"category": "MISSING_PROVENANCE", "message": "No source identifier was supplied."})

    categories = {item["category"] for item in findings}
    if "CATEGORY_ERROR" in categories or ("OVERCLAIM" in categories and not evidence_present):
        verdict = "INVALID"
    elif findings:
        verdict = "WEAK"
    else:
        verdict = "VALID"

    rationale = (
        "No configured heuristic fired; truth is not verified."
        if not findings else " ".join(item["message"] for item in findings)
    )
    return {
        "schema_version": "1.0",
        "filter_version": VERSION,
        "verdict": verdict,
        "categories": sorted(categories),
        "confidence": round(0.5 if findings else 0.25, 2),
        "rationale": rationale,
        "claim": text,
        "evidence_present": evidence_present,
        "scope": scope.strip() if scope_present else None,
        "source_id": source_id.strip() if source_present else None,
        "evaluated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "limitations": [
            "Heuristic screening only; not a factuality verifier.",
            "A VALID verdict does not prove the claim true.",
            "Confidence is a rule-status indicator, not a calibrated probability.",
        ],
    }


def evaluate_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate a runtime event using common claim/text fields."""
    if not isinstance(event, Mapping):
        raise ValueError("event must be a mapping")
    claim = event.get("claim") or event.get("text")
    if not claim:
        params = event.get("tool_params")
        if isinstance(params, Mapping):
            claim = params.get("claim") or params.get("prompt") or params.get("body_snippet")
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("event must include claim, text, or a supported tool_params field")
    return evaluate_claim(
        claim,
        evidence=event.get("evidence") or event.get("evidence_refs"),
        scope=event.get("scope") or event.get("workspace_id"),
        source_id=event.get("source_id") or event.get("event_id"),
    )
