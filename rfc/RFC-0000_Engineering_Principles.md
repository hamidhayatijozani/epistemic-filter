# RFC-0000: Engineering Principles

**Status:** Draft  
**Version:** 0.1.0

## Purpose

Define the constraints for an epistemic-claim screening component that is explainable, replayable, and explicit about uncertainty.

## Principles

1. **Screening is not truth verification.** A rule-based result cannot establish that a claim is true or false in the world.
2. **Evidence must be referenced, not implied.** Store source identifiers and evidence references separately from the claim text.
3. **Scope is part of the claim.** Environment, time window, subject, and tested conditions constrain what the evidence supports.
4. **Unknown is not valid.** Missing evidence, missing provenance, or missing scope must remain visible.
5. **Fail conservatively at consequential boundaries.** The filter may recommend review or hold, but the protected system owns final authorization and execution.
6. **Determinism before sophistication.** Given the same event, rule version, and configuration, verdict/categories should remain stable. Volatile fields such as evaluation timestamps are excluded from replay comparisons.
7. **No uncalibrated probability claims.** A confidence field is not a calibrated probability unless a separate calibration study proves it.
8. **Measure before marketing.** Precision, recall, F1, latency, replay rate, and reviewer utility require raw reproducible runs.
9. **Human review remains available.** A rule hit is a triage signal, not a substitute for domain expertise.
10. **Version every decision.** Record filter version, schema version, source event identifier, and evidence references.

## Prototype boundary

The current implementation is a dependency-free Python heuristic library. It does not include a hosted API, authentication, transport security, continuous telemetry collection, or a production HHJ-DE/AgentRQ service.

## Acceptance evidence

Any claim of measured quality must include:
- dataset and label provenance;
- frozen test fixture and checksum;
- exact source commit and runtime version;
- command, raw output, and failed cases;
- metric definitions and uncertainty;
- reproducible replay instructions.

The presence of this RFC is a design statement, not evidence that every principle is fully implemented.
