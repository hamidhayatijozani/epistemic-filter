# Integration contract test matrix

**Status:** local mock contract only. This is not a live AgentRQ or HHJ-DE integration test.

| Case | Input condition | Mock action | Expected behavior |
|---|---|---|---|
| invalid | configured category error or unsupported absolute guarantee | `HOLD` | Preserve event ID and return the epistemic result |
| weak | evidence, scope, or provenance is incomplete | `ASK` | Request review rather than silently accepting |
| valid | no configured heuristic fires and metadata is supplied | `REVIEW` | Do not convert `VALID` into automatic permission |
| malformed | no supported claim/text field | exception | Reject explicitly; caller must handle the error |

## What these tests establish

- The local Python mock maps the current filter's three verdicts to the documented suggestion labels.
- The mock preserves the input event identifier.
- Missing claim content raises an explicit error.

## What these tests do not establish

- HTTP endpoints, network reachability, TLS/mTLS, bearer-token authentication, timeout handling, retries, or idempotency.
- A real AgentRQ/HHJ-DE service exists at a configured endpoint or accepts this contract.
- An action suggestion is enforced by a protected execution boundary.
- Any live integration is available in the current environment.

## Required next step for live integration

A service owner must provide a real base URL, versioned API contract, non-production credentials via secret storage, and a test tenant. Then add opt-in tests that are skipped unless explicit environment variables are present. Never put tokens in fixtures, commit logs, or CI output. Verify successful and unauthorized requests, timeout behavior, duplicate event IDs, malformed responses, and the chosen fail-closed/fail-open policy against that real service.

Until that test has run against a configured endpoint, live integration status remains **UNKNOWN**.
