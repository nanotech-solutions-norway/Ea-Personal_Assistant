# 11 — Ea Implementation Blueprint

Status: ACTIVE_BLUEPRINT  
Authority: Active-source framework

## Build order

1. Maintain approved Level 1 baseline and active-source authority.
2. Apply Level 1.1 transactional hardening to business-email/Calendar workflows.
3. Repository implementation complete for stable case/action/audit schemas, idempotency primitives, policy gateway foundation and approval envelopes; provision the managed runtime/store next.
4. Preserve 03D manual-draft-deletion suppression as approved; treat proposed thread/case scoping as PENDING_REVIEW until explicitly approved.
5. Repository contracts complete for Gmail watch/history and Calendar watch/sync-token ingestion; deploy the webhook/Pub/Sub runtime next while retaining hourly reconciliation/watchdog.
6. Run extended Level 1 hardening regression and production validation.
7. Provision the specified separate Level 2A no-send identity and future Level 2B approval-gated execution identity; repository policy already fails Level 2A send closed.
8. Operate Level 2A controlled internal autonomy under least-privilege and readback controls.
9. Continue production validation of Level 2A internal actions and failure isolation.
10. Level 2B.1 approval-bound Gmail send design is implemented in staging files; validate against staging Gmail only after separate send-capable identity and approval store are provisioned; keep HOLD.
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


## Current implementation checkpoint — 30.09.2026

Completed in repository:
- durable data model;
- deterministic policy matrix/evaluator;
- idempotency and payload hashing;
- source→sink rules;
- incremental ingestion contracts;
- identity/scoping design;
- Level 2B.1 staging transaction;
- unit-test workflow.

Not deployed:
- database;
- Pub/Sub/webhook receivers;
- Gmail/Calendar watch registrations;
- separate OAuth/service identities;
- approval service;
- production agent runtime.


## 30.09.2026 integration-stage implementation

Implemented:
- live read-surface validation for connected NTSN Gmail/Calendar/Drive;
- managed-runtime deployment runbook;
- placeholder-only staging environment contract;
- fail-closed deployment preflight;
- CI tests for missing infrastructure and unsafe Level 2A flags.

Next executable phase requires infrastructure outside the current Gmail/Calendar/Drive connector surfaces:
1. provision managed PostgreSQL;
2. provision HTTPS runtime/webhook endpoint;
3. provision Google Cloud Pub/Sub and Gmail watch;
4. provision Calendar watch channels;
5. provision managed secret/identity separation;
6. run staging integration tests against those deployed components.

Level 2B/2C remain HOLD.


## Runtime scaffold progression — 30.09.2026

The repository now contains the event-receiver/container scaffold and ingestion-event SQL migration. The next implementation unit is the durable PostgreSQL EventStore adapter plus managed deployment. Until that adapter is connected, the staging server is intentionally not ready and will not acknowledge Gmail/Calendar notifications.

After durable storage is available:
1. deploy the container to an HTTPS endpoint;
2. attach PostgreSQL EventStore;
3. validate `/readyz`;
4. create Gmail Pub/Sub/watch;
5. create Calendar watch channels;
6. run duplicate, crash/restart and cursor-recovery integration tests;
7. preserve the hourly reconciliation watchdog.
