# EpistemicFilter + HHJ-CSG: Execution Governance for Autonomous Agents

**Status:** POC Ready for Evaluation  
**Author:** Hamid Hayati Jozani  
**Date:** 2026-07-13  
**Version:** 1.0.0  

---

## Overview

This repository contains a complete technical proposal and POC implementation for **HHJ Cognitive Safety Gateway (HHJ-CSG)**—an independent execution governance runtime designed to evaluate permission requests from autonomous agent orchestration systems like AgentRQ.

The core hypothesis is that execution governance can be treated as a separate runtime concern, enabling autonomous systems to maintain trustworthiness through explainability, measurability, and reproducibility.

---

## Problem Statement

Autonomous agents are increasingly deployed in operational environments where execution decisions have real consequences. However, current approaches either:

1. **Require human approval for every action** — Creating bottlenecks and defeating the purpose of autonomy
2. **Allow automatic execution without governance** — Creating risk and compliance challenges
3. **Use heuristic rules** — Lacking explainability and reproducibility

**The gap:** There is no independent layer that can evaluate execution requests based on runtime context while maintaining acceptable latency and complete auditability.

---

## Solution Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              AgentRQ (Control Plane)                     │
│  • Agent Orchestration                                  │
│  • Workflow Scheduling                                  │
│  • Self-improving Loops                                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓ permission_request
┌─────────────────────────────────────────────────────────┐
│         HHJ-CSG (Execution Governance Runtime)           │
│  • Context Analysis                                     │
│  • Evidence Validation                                  │
│  • Risk Assessment                                      │
│  • Decision Rendering                                   │
│  • Trace & Lineage                                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓ decision_verdict
┌─────────────────────────────────────────────────────────┐
│              Execution Layer                             │
│  • Tool Invocation                                      │
│  • External APIs                                        │
│  • Resource Modification                                │
└─────────────────────────────────────────────────────────┘
```

---

## Key Features

### 1. Independent Governance Layer

HHJ-CSG operates as a separate service that:
- Evaluates execution requests without modifying orchestration logic
- Maintains complete separation of concerns
- Can be deployed, scaled, and updated independently

### 2. Evidence-Based Decision Making

Decisions are based on validated runtime context:
- Identity verification
- Permission validation
- Environment health
- Resource accessibility
- Policy compliance
- Anomaly detection

### 3. Immutable Audit Trail

Every decision includes:
- Complete evidence snapshot
- Decision rationale with reasoning chain
- Cryptographic lineage token
- Replay capability for deterministic verification
- Tamper-evident signatures

### 4. Measurable Governance Quality

All governance decisions are evaluated through:
- Decision agreement with human experts (≥ 85% target)
- Replay consistency (≥ 95% target)
- Latency metrics (p95 < 300ms target)
- False positive/negative rates
- Policy alignment

### 5. Deterministic Replay

Every decision can be replayed with identical results:
- Evidence snapshot preserved
- Policy version recorded
- Model version tracked
- Allows investigation and verification

---

## Deliverables

### RFCs (Request for Comments)

| Document | Purpose | Lines |
|----------|---------|-------|
| RFC-0000.5 | AgentRQ Integration Boundary | 450+ |
| RFC-0001 | Runtime Event Model | 493 |
| RFC-0002 | Decision Object Schema | 511 |
| RFC-0003 | Metrics Specification | 540 |

**Total RFC Content:** ~2,000 lines of formal specification

### Implementation

| Component | Purpose | Status |
|-----------|---------|--------|
| POC Implementation Plan | 2-week timeline with detailed phases | ✅ Complete |
| Benchmark Suite | 200 events across 5 critical scenarios | ✅ Complete |
| Core Gateway Code | FastAPI implementation | ✅ Ready |
| Test Framework | Evaluation and metrics collection | ✅ Ready |

### Project Statistics

- **Total Lines:** 2,389
- **Documentation:** ~1,900 lines
- **Code:** ~430 lines (Python)
- **Project Size:** 100 KB
- **RFCs:** 4 complete specifications
- **Scenarios:** 5 critical test cases
- **Benchmark Events:** 200 realistic permission requests

---

## POC Timeline

**Duration:** 2 weeks (Days 1-14)

### Phase 1: Setup & Infrastructure (Days 1-2)
- Docker containers
- PostgreSQL database
- Prometheus monitoring
- Grafana dashboards

### Phase 2: Core Gateway Implementation (Days 3-5)
- Decision API endpoint
- Context analyzer
- Evidence validator
- Risk engine
- Decision gate

### Phase 3: Trace & Lineage (Days 6-7)
- Lineage token generation
- Immutable trace storage
- Replay capability
- Audit trail

### Phase 4: Test Data & Labeling (Days 8-10)
- 200 permission events
- Human labeling interface
- 50 labeled examples
- Ground truth dataset

### Phase 5: Evaluation & Metrics (Days 11-12)
- Metrics computation
- Decision agreement analysis
- Replay consistency verification
- Performance benchmarking

### Phase 6: Stress Testing (Day 13)
- Load testing
- Timeout handling
- Fallback policies
- Peak performance

### Phase 7: Report & Recommendation (Day 14)
- Final report
- Go/No-Go decision
- Integration roadmap
- Lessons learned

---

## Success Criteria

### Functional Acceptance

- [ ] Process ≥ 200 permission events
- [ ] Collect ≥ 50 human-labeled examples
- [ ] Generate decision for every request
- [ ] Create immutable lineage token
- [ ] All decision types work (ALLOW/DENY/ASK/DEFER)

### Quality Acceptance

| Metric | Target | Minimum |
|--------|--------|---------|
| Decision Agreement | ≥ 85% | ≥ 80% |
| Cohen's Kappa | ≥ 0.75 | ≥ 0.70 |
| Latency p95 | < 300ms | < 400ms |
| Replay Consistency | ≥ 95% | ≥ 90% |
| Audit Completeness | 100% | 95% |
| Throughput | ≥ 1000 req/s | ≥ 500 req/s |

### Security Acceptance

- [ ] mTLS handshake succeeds
- [ ] Lineage tokens cryptographically valid
- [ ] PII redacted before transmission
- [ ] No credentials in logs

---

## 5 Critical Test Scenarios

### Scenario 1: Incomplete Information (40 events)

**Challenge:** Missing critical context for decision

**Examples:**
- Identity verified but permissions unknown
- Environment status unavailable
- Resource metadata missing

**Expected Decision:** ASK or DEFER

### Scenario 2: Contradictory Instructions (40 events)

**Challenge:** Conflicting signals in request

**Examples:**
- Admin role but limited permissions
- Production environment but dev credentials
- High priority but low confidence

**Expected Decision:** DENY

### Scenario 3: Malicious Prompt (40 events)

**Challenge:** Suspicious patterns suggesting attack

**Examples:**
- SQL injection attempts
- Privilege escalation
- Data exfiltration patterns
- Denial of service

**Expected Decision:** DENY

### Scenario 4: False Confidence (40 events)

**Challenge:** High confidence with low evidence

**Examples:**
- Confident decision with minimal evidence
- Overconfident risk assessment
- Misaligned confidence and coverage

**Expected Decision:** ASK

### Scenario 5: Context Shift (40 events)

**Challenge:** Significant change in execution context

**Examples:**
- Environment changed mid-session
- User role changed
- Resource accessibility changed
- Policy updated

**Expected Decision:** ASK or ALLOW

---

## File Structure

```
epistemic_filter_project/
├── README.md                          # This file
├── FINAL_EMAIL_TO_TONY.md             # Complete proposal email
├── rfc/
│   ├── RFC-0000.5_AgentRQ_Integration_Boundary.md
│   ├── RFC-0001_Runtime_Event_Model.md
│   ├── RFC-0002_Decision_Object_Schema.md
│   └── RFC-0003_Metrics_Specification.md
└── poc/
    ├── POC_IMPLEMENTATION_PLAN.md
    ├── benchmark_suite.py
    └── sample_events.jsonl              # Generated benchmark events
```

---

## Key Concepts

### Decision Object

Every decision includes:
- **Input:** Original permission request
- **Evidence:** Validated runtime observations
- **Metrics:** Risk and confidence scores
- **Decision:** Verdict (ALLOW/DENY/ASK/DEFER)
- **Rationale:** Human-readable explanation
- **Lineage:** Immutable trace for replay
- **Audit:** Timestamps and signatures

### Lineage Token

Immutable proof of decision:
- JWS (JSON Web Signature) format
- Contains decision, timestamp, evidence hash, policy hash
- Cryptographically signed
- Verifiable by any engineer
- Enables deterministic replay

### Decision Values

| Verdict | Meaning | Conditions |
|---------|---------|-----------|
| ALLOW | Execute approved | Risk < 0.6, Evidence ≥ 80%, Confidence ≥ 0.75 |
| DENY | Block execution | Risk ≥ 0.8, OR Evidence < 50%, OR Policy violation |
| ASK | Human review | Risk 0.6-0.79, Confidence 0.3-0.74 |
| DEFER | Retry later | Gateway timeout or unavailable |

---

## Integration Points

### With AgentRQ

1. **Permission Request Event**
   - AgentRQ sends tool invocation request
   - Includes context, parameters, history
   - HHJ-CSG evaluates and returns verdict

2. **Decision Enforcement**
   - AgentRQ receives verdict
   - Applies enforcement action (execute/block/escalate)
   - Logs decision for audit

3. **Audit Trail Correlation**
   - AgentRQ logs execution outcome
   - HHJ-CSG correlates with decision
   - Enables post-execution analysis

### API Contract

**Request:** `POST /v1/gate/evaluate`

```json
{
  "event_id": "evt-uuid",
  "workspace_id": "ws-uuid",
  "agent_id": "agent-uuid",
  "tool_name": "restart_service",
  "tool_params": { "service": "api-server" },
  "context": {
    "user_role": "admin",
    "environment": "production",
    "session_id": "sess-uuid"
  }
}
```

**Response:** Decision Object

```json
{
  "decision": "ALLOW",
  "confidence": 0.87,
  "risk_score": 0.42,
  "rationale": "Admin identity verified, permissions valid, environment healthy",
  "lineage_token": "eyJ...",
  "timestamp": "2026-07-13T12:34:56Z"
}
```

---

## Metrics & Observability

### Core Metrics

- **Decision Latency:** p50, p95, p99 percentiles
- **Decision Distribution:** % of ALLOW/DENY/ASK/DEFER
- **Decision Agreement:** % agreement with human labels
- **Risk Score Distribution:** Mean, median, percentiles
- **False Allow Rate:** % of ALLOW decisions later flagged as risky
- **False Deny Rate:** % of DENY decisions that were safe
- **Evidence Coverage:** % of required evidence collected
- **Replay Consistency:** % of decisions with identical replay results

### Alerting Rules

| Metric | Threshold | Action |
|--------|-----------|--------|
| Latency p95 | > 500ms | Warning |
| Error Rate | > 1% | Warning |
| False Allow Rate | > 5% | Critical |
| Replay Consistency | < 95% | Critical |

---

## Next Steps

### If Interested

1. Review the RFCs and architecture
2. Provide feedback on integration boundary
3. Share sample permission events from AgentRQ
4. Discuss POC timeline and resources
5. Align on success metrics

### Timeline

- **Week 1:** Setup infrastructure, implement core gateway
- **Week 2:** Test data collection, evaluation, final report
- **Decision Point:** Go/No-Go based on success criteria

---

## Contact & Questions

For questions about this proposal:

- **Author:** Hamid Hayati Jozani
- **Email:** See FINAL_EMAIL_TO_TONY.md
- **Repository:** https://github.com/hamidhayatijozani/epistemic-filter

---

## License

This proposal and implementation are provided for evaluation purposes.

---

## Acknowledgments

This work was inspired by conversations about autonomous agent governance and the importance of trustworthy execution in production environments.

Special thanks to Tony for introducing AgentRQ and the opportunity to explore these ideas.

---

**End of README**

*Created by Sir HamidHayati*  
*EpistemicFilter + HHJ-CSG: Execution Governance for Autonomous Agents*
