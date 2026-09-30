# 10 — Ea Phase Validation Tracker

Status: LEVEL_1_APPROVED / HARDENING_ACTIVE / LEVEL_2A_ACTIVE  
Authority: Active-source framework

## Phase status

| Phase | Name | Status | Notes |
|---|---|---|---|
| 00 | Scope and architecture | APPROVED | Level 1 baseline confirmed; Level 2A active; Level 2B/2C HOLD |
| 01 | Folder skeleton and governance | APPROVED | GitHub and Drive skeleton created |
| 02 | Runtime core | APPROVED | Approval and confidentiality rules passed QA |
| 03 | Project learning and source authority | APPROVED | Source authority and dynamic skill tests passed |
| 04 | Email, calendar and meeting workflows | APPROVED / HARDENING | Level 1.1 transaction/state/idempotency/readback hardening adopted as implementation target |
| 05 | Due diligence, legal and financial | APPROVED | Custom GPT and Project QA prompts passed |
| 06 | Templates, registers and indexes | READY_FOR_CUSTOMIZATION | Needs real project/business data for production depth |
| 07 | Custom GPT build | APPROVED | Custom GPT QA prompts passed |
| 08 | Project setup and permissions | APPROVED | Project QA prompts passed |
| 09 | Scheduled tasks | ACTIVE / LEVEL_2A | Hourly Ea Business Email Watch enabled and synchronized to canonical `condition_watch`; prior timing-mode drift resolved |
| 10 | QA and release gate | APPROVED_BASELINE / EXTENDED_VALIDATION | Baseline Level 1 approved; new hardening controls require targeted evidence |
| 11 | Level 2 backend | LEVEL_2A_ACTIVE / 2B-2C_HOLD | Controlled internal autonomy active; external execution stages remain HOLD |

## Current release classification

Level 1 baseline: APPROVED and active.  
Level 1.1 transactional hardening: IMPLEMENTATION / ACTIVE_VALIDATION.  
Level 1.2 observability/incremental architecture: IMPLEMENTATION_TARGET / ACTIVE_VALIDATION.  
Level 2A: ACTIVE — controlled internal autonomy.  
Level 2B: HOLD.  
Level 2C: HOLD.

## Validation evidence

- `validation/LEVEL_1_VALIDATION_RESULTS.md`
- `validation/Ea_Scheduled_Function_Audit_1810_25082026.md`
- `active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`
- `active-source/09_EA_LEVEL_2_MANAGED_BACKEND.md`

## Level 1 hardening validation matrix

Required targeted tests:
1. persistent/stable case identity or equivalent deterministic case reconciliation;
2. exact one-draft-per-thread behavior;
3. stable `threadId + draftId` handling where supported;
4. stale-state/pre-write freshness test;
5. transient vs permanent vs conflict error handling;
6. ambiguous-write reconciliation before retry;
7. failure isolation across multiple candidate threads;
8. 03D suppression across hourly and recovery routines;
9. notification deduplication independent from execution;
10. deterministic Calendar duplicate detection and private/solo/no-Meet/no-reminder rules;
11. attachment version/fit/readback test;
12. product/commercial claim verification test;
13. wrong-recipient and wrong-thread negative tests;
14. post-write readback verification;
15. audit/action metadata capture;
16. Level 1/Level 2A no-send capability boundary where technically enforceable.

## Level 2A promotion target

Before promotion, accumulate at least 100 consecutive actionable cases and 14 days normal operation, whichever is longer, with:
- 0 wrong-recipient drafts;
- 0 autonomous sends;
- 0 unauthorized external Calendar writes;
- 0 duplicate drafts/follow-ups;
- 0 03D violations;
- 0 wrong-thread drafts;
- 0 unsupported commercial commitments;
- 0 missed high-priority actionable cases in the validation sample;
- 100% mandatory readback verification;
- 100% required audit capture;
- demonstrated failure isolation/reconciliation.

One severe boundary violation resets the validation window.

## PENDING_REVIEW / unresolved

- whether 03D should later become thread/case-scoped instead of current approved recipient-level suppression;
- managed backend design is now implemented in-repository under `level-2/backend/`, but deployment runtime/database/webhooks/Pub/Sub remain NOT_DEPLOYED;
- separate Level 2A/Level 2B credential architecture is specified but not yet provisioned;
- Level 2B and Level 2C remain separate future promotion decisions.

## Remaining actions

1. Continue Level 1 production validation under the hardened 07B protocol.
2. Provision the managed PostgreSQL-compatible case/audit store using `level-2/backend/sql/001_initial_schema.sql`.
3. Deploy Gmail watch/Pub/Sub and Calendar watch/sync-token ingestion using the repository contracts; retain hourly reconciliation as watchdog.
4. Provision least-privilege Level 2A identity and separate future Level 2B approval-gated execution identity.
5. Preserve 03D as currently approved until any scope change is explicitly approved.
6. Keep Level 2B and Level 2C on HOLD until their separate activation gates pass; continue Level 2A validation.


## Backend foundation evidence — 30.09.2026

Status: `IMPLEMENTED_IN_REPOSITORY / NOT_DEPLOYED`.

Validation now includes repository CI for deterministic policy and idempotency primitives. External integration tests require staging credentials/infrastructure and are not claimed as complete. Level 2B.1 remains `STAGING_DESIGN_ONLY / HOLD`.


## Live connector validation checkpoint — 30.09.2026

Status: `PASS_FOR_CONNECTED_LEVEL_2A_READ_SURFACES / INFRASTRUCTURE_PENDING`.

Verified:
- NTSN business Gmail authentication;
- recent Gmail message-ID search;
- Gmail draft listing;
- NTSN Calendar authentication;
- calendar discovery and bounded event retrieval;
- Drive Level 2 staging-folder visibility.

No send/forward, external Calendar mutation, Drive share/permission mutation, or destructive action was performed.

Remaining deployment blockers are infrastructure-level: managed PostgreSQL, HTTPS webhook runtime, Gmail Pub/Sub/watch, Calendar watch channels, managed secrets/identity, and observability.

Repository staging preflight now fails closed if required infrastructure variables are absent or if Level 2B/external-send/external-Calendar flags are enabled during a Level 2A deployment.


## Runtime scaffold checkpoint — 30.09.2026

Status: `IMPLEMENTED_IN_REPOSITORY / STORAGE_ADAPTER_AND_CLOUD_RUNTIME_PENDING`.

Completed:
- ingestion-event migration;
- Gmail/Calendar event validation/parsing;
- duplicate-stable event identity;
- fail-closed health/readiness/webhook app;
- container scaffold;
- automated runtime tests.

Safety invariant: notification POSTs are rejected with 503 until both deployment preflight passes and a durable EventStore is attached. No webhook may acknowledge external change notifications using the test-only in-memory store in production.

Remaining:
- PostgreSQL EventStore adapter;
- actual managed database;
- HTTPS deployment;
- Google Pub/Sub/watch registration;
- Calendar watch registration;
- secret/identity provisioning;
- tracing/observability integration.


Webhook security hardening is now implemented at the interface boundary: durable storage and authenticated delivery are both mandatory before readiness. Test-only storage/authentication cannot make a non-test deployment ready.
