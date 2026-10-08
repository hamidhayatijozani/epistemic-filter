# Epistemic Filter

**Status:** executable research prototype (v0.1.0)  
**Canonical integration lineage:** HHJ-CSG / AgentRQ  
**License:** MIT (see `LICENSE`)

## English

Epistemic Filter is a deterministic, explainable screening layer for claims emitted by agents. It flags configured patterns such as absolute guarantees, category errors, missing evidence, missing scope, and missing provenance.

**Important boundary:** it is a heuristic triage tool, not an LLM, fact checker, truth oracle, security boundary, or substitute for human review. `VALID` means only that no configured heuristic fired; it does **not** mean the claim is true. Confidence is a rule-status indicator, not a calibrated probability.

### Quick start

Requires Python 3.10+; runtime has no third-party dependencies.

```bash
python -m unittest discover -s tests -v
python - <<'PY'
from epistemic_filter import evaluate_claim
print(evaluate_claim(
    "This system is guaranteed never to fail.",
    evidence=None,
    scope="local test",
    source_id="demo-1",
))
PY
```

### Layout

- `epistemic_filter.py`: deterministic screening functions.
- `tests/`: unit and integration-contract tests.
- `rfc/`: RFC specifications and machine-readable AgentRQ boundary.
- `poc/sample_events.jsonl`: 200-line event fixture.
- `poc/sample_events.json`: JSON-array representation of the same 200 events.
- `poc/mock_hhj_de.py`: local integration mock; not a real HHJ-DE service.
- `poc/poc_plan.md`: two-week evaluation plan. Metrics are targets until measured.

### Decision semantics

- `INVALID`: a configured category-error pattern, or absolute guarantee without evidence.
- `WEAK`: missing scope/provenance/evidence or another configured concern.
- `VALID`: no configured heuristic fired and basic evidence/scope/source metadata was supplied. Not proof of truth.

The output includes categories, rationale, scope, source identifier, timestamp, and explicit limitations. The prototype does not expose an HTTP API; the RFC's `POST /events` and `POST /decide` are integration proposals, not implemented endpoints.

## فارسی

Epistemic Filter یک لایهٔ غربال‌گری قطعی و قابل‌توضیح برای ادعاهای تولیدشده توسط Agentها است. این ابزار الگوهایی مانند تضمین مطلق، خطای مقوله‌ای، نبود شواهد، نبود دامنهٔ ادعا و نبود منشأ داده را علامت‌گذاری می‌کند.

**مرز مهم:** این ابزار نمونهٔ پژوهشی مبتنی بر قواعد است؛ حقیقت‌سنج، مدل زبانی، مرز امنیتی یا جایگزین بازبینی انسانی نیست. وضعیت `VALID` فقط یعنی هیچ قاعدهٔ تعریف‌شده‌ای فعال نشده است، نه اینکه ادعا حقیقت دارد. مقدار confidence نیز احتمال کالیبره‌شده نیست.

### اجرای سریع

به Python 3.10 یا بالاتر نیاز دارد و در زمان اجرا به وابستگی خارجی نیاز ندارد.

```bash
python -m unittest discover -s tests -v
```

### وضعیت شواهد

- وجود ۲۰۰ رویداد نمونه: دادهٔ fixture موجود است.
- تست‌های واحد و قرارداد ادغام: در CI اجرا می‌شوند؛ نتیجهٔ واقعی فقط پس از اجرای workflow اعلام می‌شود.
- دقت، recall، F1، تأخیر و نرخ replay: **هنوز اندازه‌گیری و تأیید نشده‌اند**.
- سرویس HTTP، احراز هویت شبکه‌ای و اتصال عملیاتی به HHJ-DE: **پیاده‌سازی نشده‌اند**.

## RFC lineage

- RFC-0000.5 — AgentRQ integration boundary.
- RFC-0001 — Runtime event model.
- RFC-0002 — Decision object schema.
- RFC-0003 — Metrics specification.

The RFCs define intended integration contracts. They do not establish that the corresponding network services or security controls are deployed.
