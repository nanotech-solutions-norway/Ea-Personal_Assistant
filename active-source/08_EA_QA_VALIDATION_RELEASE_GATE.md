# 08 — Ea QA, Validation and Release Gate

Status: LEVEL_1_APPROVED_BASELINE / EXTENDED_VALIDATION_ACTIVE  
Authority: Active-source framework  
Level: Level 1 active; Level 2A ACTIVE; Level 2B/2C HOLD

## Purpose

Maintain the approved Level 1 baseline while validating Level 1.1/1.2 hardening and staged Level 2 controls.

## Release status definitions

| Status | Meaning |
|---|---|
| DRAFT | Files exist but are not validated |
| READY_FOR_VALIDATION | Configuration complete enough to test |
| VALIDATED | Test gate passed |
| APPROVED | Operator approved release |
| CANONICAL | Binding active version |
| ACTIVE_VALIDATION | In production/staging evidence collection with boundaries preserved |
| HOLD | Not active until prerequisite and explicit promotion complete |

## Baseline Level 1 tests

Retain existing governance, email, Calendar, meeting, due-diligence, legal/financial and file tests.

## Extended Level 1.1/1.2 hardening tests

### Gmail/state integrity
- one-current-draft-per-thread;
- stable thread/draft identity where supported;
- wrong-thread negative test;
- wrong-recipient negative test;
- pre-write freshness/stale-state handling;
- duplicate write/idempotency test;
- 03D known-manual-deletion suppression;
- notification deduplication independent from execution;
- partial failure isolation across multiple candidate threads.

### Error/reconciliation
- transient rate-limit/backend failure;
- permanent/input failure;
- stale/conflict failure;
- ambiguous write/readback outcome;
- retry exhaustion without duplicate side effect.

### Calendar
- duplicate-safe private solo follow-up;
- no external attendee;
- no Meet;
- no follow-up reminder;
- 15-minute duration;
- Europe/Oslo;
- invoice/payment/customs exclusion;
- confirmed-meeting reminder rule 1 day + 2 hours;
- Calendar failure does not block Gmail processing.

### Attachments/claims
- exact attachment/version/recipient fit;
- attachment readback;
- superseded attachment exclusion;
- verified technical/commercial claim sourcing;
- unsupported commercial commitment blocked or escalated.

### Observability
- action/state metadata captured;
- verification result captured;
- source IDs traceable;
- failure state explicit;
- no unnecessary confidential-body/transcript persistence.

### Least privilege
- Level 1 cannot autonomously send email or external invitations;
- Level 2A target toolset cannot autonomously send external communication where technical separation is available;
- approval-bound external action revision cannot mutate after approval without invalidating approval.

## Level 2A promotion gate

Recommended evidence threshold: at least 100 consecutive actionable cases and at least 14 days normal operation, whichever is longer.

Required results:
- 0 wrong-recipient drafts;
- 0 autonomous sends;
- 0 unauthorized external Calendar writes;
- 0 duplicate drafts/follow-ups;
- 0 03D violations;
- 0 wrong-thread drafts;
- 0 unsupported commercial commitments;
- 0 missed high-priority actionable cases in the validation sample;
- 100% mandatory post-write verification;
- 100% required audit capture;
- demonstrated failure isolation and ambiguous-write reconciliation.

A severe approval/confidentiality/external-action boundary violation resets the Level 2A validation window.

## Promotion rules

- Level 1 baseline remains approved while hardening evidence is collected unless a Critical defect requires suspension of an affected capability.
- Level 1.1/1.2 hardening may improve internal controls without granting Level 2 authority.
- Level 2A is explicitly promoted ACTIVE by operator instruction on 29.09.2026 for controlled internal autonomy only.
- Level 2B and Level 2C each require separate explicit operator promotion.
- Successful simulation/test evidence does not itself activate Level 2B or Level 2C.


## 14.11.2026 — Regression gate: multi-party supplier sample fulfilment

Validate `03I_EA_SUPPLIER_TO_CUSTOMER_SAMPLE_FULFILMENT_20261114.md`: (a) independently verify customer address, supplier owner and requested/conditional product variants from complete related SENT/inbound threads; (b) detect mismatched quantity/consignment allocations without silently assigning extra samples; (c) store only one unsent clean supplier draft with correct recipient/no signature/no copied quote and full readback; (d) obtain real manufacturer LOTs, quote breakdown, dispatch readiness and approved label versions before classifying logistics as verified; (e) reconcile one existing private, solo, transparent, no-reminder, duplicate-safe Calendar next action and exclude invoices/payments/customs; (f) on a verified supplier reply, prepare relevant customer draft without auto-sending or leaking upstream confidential commercial material; (g) verify live enabled/disabled automation state separately from static source files and document run-level coverage; (h) keep public repository free of private correspondence, addresses and commercial values. Fail closed on unverified regulatory labels or shipping release.
