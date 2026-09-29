# 11 — Ea Implementation Blueprint

Status: ACTIVE_BLUEPRINT  
Authority: Active-source framework

## Build order

1. Maintain approved Level 1 baseline and active-source authority.
2. Apply Level 1.1 transactional hardening to business-email/Calendar workflows.
3. Add stable case identity/state, idempotency semantics, freshness checks, typed failures, readback verification and audit metadata where technically supported.
4. Preserve 03D manual-draft-deletion suppression as approved; treat proposed thread/case scoping as PENDING_REVIEW until explicitly approved.
5. Add Level 1.2 observability: incremental change detection where managed integrations support it, plus hourly reconciliation/watchdog.
6. Run extended Level 1 hardening regression and production validation.
7. Demonstrate least privilege, including no-send capability for Level 1/Level 2A where technically feasible.
8. Operate Level 2A controlled internal autonomy under least-privilege and readback controls.
9. Continue production validation of Level 2A internal actions and failure isolation.
10. Design and validate Level 2B approval-bound external execution separately; keep HOLD.
11. Consider Level 2C narrow autonomous external execution only after sustained Level 2A/2B evidence and separate approval.

## Level 1.1 minimum hardening

- stable case identity/state or deterministic equivalent;
- exactly one current draft per actionable thread;
- stable Gmail draft identity;
- idempotency/deduplication;
- pre-write freshness/concurrency guard;
- typed error/retry/reconciliation handling;
- Calendar duplicate-safe private follow-up semantics;
- attachment manifest/readback;
- post-write verification;
- operator notification only on material state change;
- audit/action metadata.

## Level 1.2 observability

- incremental Gmail/Calendar change ingestion where supported;
- hourly reconciliation retained as safety watchdog;
- regression suite for duplicates, stale writes, wrong thread/recipient, 03D, attachment mismatch, Calendar duplicate, partial failure and unsupported claims;
- metrics for verification/failure isolation.

## Level 2 staged rule

- **Level 2A:** ACTIVE — controlled internal autonomy only; no autonomous external communication.
- **Level 2B:** approval-gated external execution bound to an exact action revision.
- **Level 2C:** narrowly defined low-risk autonomous external execution, future separate decision.

Level 2A is ACTIVE by explicit operator instruction. Level 2B and Level 2C remain HOLD and require separate promotion. Level 2 must not be activated as one monolithic autonomy tier.
