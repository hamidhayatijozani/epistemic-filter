# EpistemicFilter + HHJ-CSG: Execution Governance for Autonomous Agents

> **Repository status:** Research / POC specification lineage.
>
> The current canonical research and provenance record is **[HamidCognition-Unified](https://github.com/hamidhayatijozani/HamidCognition-Unified)**. This repository remains independently citable because it contains the RFC and POC lineage for HHJ-CSG / epistemic execution governance.
>
> Claims in this README are proposal/POC claims unless a corresponding execution result and evidence record is available. Targets are not results.

**Status:** POC / research record  
**Author:** Hamid Hayati Jozani  
**Date:** 2026-07-13  
**Version:** 1.0.0

---

## Citation and evidence boundary

For current project status, evidence levels, contradiction handling, canonicalization and repository roles, consult `RESEARCH/REPOSITORY_GOVERNANCE.md` in `HamidCognition-Unified`.

When citing this repository, identify the exact RFC, code path, benchmark artifact and commit where applicable. Do not present target metrics such as replay consistency, latency, throughput or agreement as achieved measurements unless an execution artifact supports them.

---

## Overview

This repository contains a technical proposal and POC implementation lineage for **HHJ Cognitive Safety Gateway (HHJ-CSG)**—an execution-governance runtime designed to evaluate permission requests from autonomous agent orchestration systems.

The core hypothesis is that execution governance can be treated as a separate runtime concern, enabling autonomous systems to evaluate execution requests with explicit evidence, measurable decisions and reproducible traces.

---

## Problem Statement

Autonomous agents may execute actions with operational consequences. This repository investigates a separate governance layer between orchestration and execution.

The repository's original proposal distinguishes three approaches:

1. Human approval for every action
2. Automatic execution without a separate governance layer
3. Heuristic rules without sufficient reproducibility

The proposed research question is whether an independent execution-governance runtime can evaluate runtime context while preserving useful latency and auditability.

---

## Solution Architecture

```text
Application Layer
        ↓
AgentRQ / Control Plane
        ↓ permission_request
HHJ-CSG / Execution Governance Runtime
        ↓ decision_verdict
Execution Layer
```

The detailed RFCs remain the authoritative specification for the version contained in this repository.

---

## Key research components

- Independent governance layer
- Evidence-based decision evaluation
- Decision Object / verdict rendering
- Trace and lineage
- Deterministic replay proposal
- Governance quality metrics
- Benchmark scenarios

---

## Important distinction

The repository contains a mixture of **implemented artifacts, specifications, targets, proposals and research assumptions**. These categories must not be collapsed.

In particular:

- target ≥85% agreement ≠ measured ≥85% agreement
- replay target ≥95% ≠ reproduced replay result
- p95 target <300ms ≠ measured latency
- POC-ready ≠ production-validated
- specification ≠ empirical evidence

---

## RFCs

The repository records RFC material including:

- RFC-0000.5 — AgentRQ Integration Boundary
- RFC-0001 — Runtime Event Model
- RFC-0002 — Decision Object Schema
- RFC-0003 — Metrics Specification

Use the exact file and commit when citing a specific rule or schema.

---

## Decision values

The proposal defines verdicts including `ALLOW`, `DENY`, `ASK`, and `DEFER`. Thresholds and conditions must be interpreted from the exact RFC version cited.

---

## Research continuation

Further validation belongs in the Unified research loop:

`claim → operationalization → experiment → observation → falsification/survival → reproduction → status transition`

**Canonical research record:** https://github.com/hamidhayatijozani/HamidCognition-Unified

**Originator:** Hamid Hayati Jozani
