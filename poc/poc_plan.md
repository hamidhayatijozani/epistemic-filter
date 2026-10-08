# Epistemic Filter POC Plan (Two Weeks)

## Goal
Measure whether a small, deterministic rule set helps reviewers prioritize epistemically risky agent claims. This is not a claim that the tool verifies truth.

## Week 1: implementation and frozen evaluation
- Freeze the current 200-event JSONL fixture and its checksum in the run record.
- Label at least 50 events with two independent reviewers; adjudicate disagreements.
- Keep labels separate from the rule implementation to reduce leakage.
- Run unit tests and inspect false positives/false negatives.
- Record Python version, commit SHA, command, raw output and fixture hash.

## Week 2: evaluation and decision
- Evaluate precision, recall, F1 and confusion matrix per category.
- Report latency p50/p95 only from measured repeated runs; do not present target values as results.
- Test deterministic replay: same event and same version must produce the same verdict/categories (timestamp excluded).
- Compare against a simple keyword baseline.
- Decide SURVIVE / REVISE / KILL using pre-registered thresholds.

## Exit gates
- At least 200 fixture events are available.
- At least 50 have adjudicated labels.
- Metrics and latency have raw, reproducible evidence.
- Known limitations and all failed cases are published.

## Current status
PLAN ONLY. No human-labelled evaluation set, measured precision/recall, latency benchmark, or replay-rate result is asserted by this document.
