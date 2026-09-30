# 09 — Ea Level 2 Managed Backend

Status: LEVEL_2A_ACTIVE / LEVEL_2B_HOLD / LEVEL_2C_HOLD  
Authority: Operator instruction 29.09.2026 plus current active-source governance  
Activation: Level 2A explicitly approved 29.09.2026 for controlled internal autonomy; Level 2B/2C remain separately gated

## Hold rule

Level 2A controlled internal execution is **ACTIVE** by explicit operator instruction. Level 2B and Level 2C remain **HOLD**.

Level 2 must not be treated as “Level 1 with unrestricted autonomy.” It is a controlled execution layer built on the hardened Level 1 observer/decision/policy foundation.

## Target architecture

1. **Observer** — Gmail, Calendar, Drive, GitHub and other approved evidence sources.
2. **Case State** — stable case ID, source/thread IDs, suppression state, action history, next action, due date and verification state.
3. **Decision Engine** — classification, evidence retrieval, drafting/planning and factual dependencies.
4. **Policy Engine** — deterministic `ALLOW / REQUIRE_APPROVAL / PROHIBIT` decision wherever possible.
5. **Execution Engine** — performs only the action allowed by policy.
6. **Readback/Reconciliation** — verifies actual state and resolves ambiguous writes before retry.
7. **Audit Ledger** — append-only operational metadata for consequential/internal writes without indiscriminate storage of confidential message bodies.

## Level 2A — Controlled internal autonomy

**Status:** ACTIVE — controlled internal autonomy only.

Candidate permissions after validation:
- create/update verified Gmail drafts;
- create/update duplicate-safe internal Calendar follow-ups;
- meeting preparation;
- summaries/action extraction from explicitly supplied or authorized meeting content;
- internal action/state synchronization;
- controlled Drive/GitHub internal write-back where separately authorized;
- attachment preparation/validation;
- internal status reports;
- stale-case escalation;
- post-write verification and audit.

Level 2A does **not** authorize autonomous external email sending, invitations, external attendee changes, commercial commitments, financial actions, deletion or permission changes.

## Level 2B — Approval-gated external execution

**Status:** HOLD.

A proposed external action must be presented with:
- action type;
- recipient/attendees;
- final content;
- attachments;
- source/case;
- risk/authority classification;
- exact reason the action is required.

Operator approval must bind to the exact action revision. Any material change to recipient, body, attachments, time or commitment invalidates that approval and requires a new approval.

Candidate approved actions:
- send the specifically approved email;
- send the specifically approved invitation;
- perform the specifically approved meeting change;
- forward the specifically approved attachment.

Every execution requires readback verification and audit evidence.

## Level 2C — Narrow autonomous external execution

**Status:** HOLD / future separate decision.

May only be considered after sustained Level 2A/2B validation. Candidate scope must be tightly predefined, low-risk and reversible where possible. It must exclude new pricing/discounts, warranties, legal/regulatory claims, liability/exclusivity, payment/bank instructions, purchases/refunds, file sharing/permissions, confidential disclosure, new external attendees and other approval-controlled commitments.

No Level 2C activation is implied by this document.

## Permanent approval-gated categories

Keep approval gates for:
- new pricing or discounts;
- warranty;
- exclusivity;
- liability acceptance;
- contractual/legal/tax/regulatory commitments;
- payment instructions or bank details;
- purchases/refunds;
- external file sharing/permission changes;
- deletion of business evidence;
- mass email;
- sensitive/customer-confidential disclosure;
- adding new external attendees;
- irreversible Drive/GitHub actions.

## Meeting capture/transcription

Universal meeting capture is not a Level 2 core default.

Capture/transcription may be implemented only where:
- the operator explicitly enables it;
- required participant notice/consent is addressed;
- retention is defined;
- sensitive-material exclusions are defined;
- authorized storage is defined;
- deletion/retention controls exist.

Post-meeting automation may operate on an authorized transcript or notes set.

## Transactional and security requirements

- least privilege by tool/credential;
- separate external-send capability from Level 1/Level 2A toolsets where technically possible;
- idempotency/exactly-once controls;
- freshness/concurrency checks;
- typed failure handling;
- ambiguous-write reconciliation before retry;
- action preview for approval-gated operations;
- revision-bound approvals;
- readback verification;
- kill/hold capability;
- source-authority and 03D suppression enforcement;
- confidentiality boundaries;
- append-only audit metadata.

## Audit record

Each write/action should record, at minimum:

```text
timestamp
cycle_id
case_id
policy_version
source_ids
classification_before
classification_after
action
risk_class
approval_required
approval_id
tool_result
verification_result
error
retry_count
```

Do not persist full confidential email/transcript content unless separately authorized and necessary.

## Activation gates

Continuing Level 2A validation should demonstrate:
- Level 1.1 transactional hardening is implemented or equivalent controls are demonstrably enforced;
- Level 1.2 observability/regression controls are operational to the extent needed for the deployment;
- no Critical/Major approval, confidentiality, wrong-recipient, wrong-thread, duplicate or unsupported-commitment defects remain;
- post-write verification is demonstrated;
- failure isolation and reconciliation are demonstrated;
- audit metadata is demonstrated;
- external send remains unavailable to the Level 2A execution identity/toolset where technically feasible;

Recommended ongoing validation target for Level 2A:
- at least 100 consecutive actionable cases and at least 14 days of normal operation, whichever is longer;
- zero wrong-recipient drafts;
- zero autonomous sends;
- zero external Calendar writes;
- zero duplicate drafts/follow-ups;
- zero 03D violations;
- zero wrong-thread drafts;
- zero unsupported commercial claims;
- zero missed high-priority actionable threads in the validation sample;
- 100% mandatory post-write verification and audit capture.

A severe boundary violation resets the validation window.

Level 2B and Level 2C require separate validation and explicit promotion decisions.

## Current Level 2 scope status

- Level 2A: ACTIVE — controlled internal autonomy
- Level 2B: HOLD
- Level 2C: HOLD
- Universal live meeting capture: HOLD / separate privacy-security design
- 03:00 file-aware managed update: HOLD
- Autonomous external sending: HOLD
- External Calendar execution: HOLD except exact operator-approved Level 2B action after future activation


## 30.09.2026 managed-backend foundation implementation

Repository foundation is now **IMPLEMENTED_IN_REPOSITORY / NOT_DEPLOYED** under `level-2/backend/`.

Implemented artifacts:
- PostgreSQL-compatible durable case/action/approval/audit/watch/cursor schema;
- deterministic policy matrix and fail-closed evaluator;
- stable action revision and idempotency hashing primitives;
- source→sink control matrix for untrusted external content;
- JSON schemas for case, event, audit and approval envelopes;
- Gmail `users.watch` / history cursor ingestion contract;
- Calendar notification-channel / `syncToken` ingestion contract including HTTP 410 full-resync behavior;
- Level 2A vs Level 2B identity/least-privilege design;
- MCP 2026-07-28 gateway requirements;
- Level 2B.1 exact-approval Gmail send staging design;
- unit CI for policy/idempotency primitives;
- integration validation matrix.

This implementation does **not** activate Level 2B, deploy a managed database/webhook/Pub/Sub service, create send-capable credentials, or authorize external effects.

### Deployment prerequisites still open
1. managed PostgreSQL-compatible runtime store;
2. HTTPS webhook receiver;
3. Google Cloud project and Gmail Pub/Sub topic/watch;
4. Google Calendar watch channels;
5. secrets/identity store and separate Level 2A/Level 2B execution identities;
6. application runtime using Agents SDK/Responses or equivalent approved harness;
7. observability destination;
8. staging integration tests and operator promotion decision.

Canonical implementation root: `level-2/backend/README.md`.


## 30.09.2026 fail-closed event runtime scaffold

Status: **IMPLEMENTED_IN_REPOSITORY / NOT_CLOUD_DEPLOYED**.

The Level 2A managed-backend foundation now includes:
- `sql/002_ingestion_events.sql` for durable notification-event capture;
- deterministic Gmail Pub/Sub and Google Calendar notification parsing;
- stable event IDs for duplicate-delivery handling;
- an EventStore interface;
- a production-readiness requirement for durable storage;
- an authenticated-delivery interface;
- fail-closed `/healthz`, `/readyz`, `/hooks/gmail`, and `/hooks/calendar` runtime endpoints;
- a container scaffold;
- regression tests for malformed events, duplicates, readiness, missing durable storage and rejected authentication.

### Runtime safety rule

A non-test runtime must not report ready or acknowledge Gmail/Calendar notification POSTs unless:
1. deployment preflight passes;
2. a durable EventStore is attached;
3. a production-safe authenticated-delivery adapter is attached.

The bundled in-memory EventStore and allow-all authenticator are test-only and may satisfy readiness only under `EA_ENV=test`.

### Remaining infrastructure

- managed PostgreSQL-compatible deployment;
- PostgreSQL EventStore adapter;
- HTTPS runtime deployment;
- Google Cloud Pub/Sub + Gmail `users.watch`;
- Calendar watch-channel registration;
- production Google delivery authentication;
- managed secrets/identity separation;
- integration observability and crash/recovery tests.

Cloud watch/channel registration must occur only after durable storage and authenticated delivery are available.

This runtime scaffold changes infrastructure readiness only. Level 2A authority is unchanged; Level 2B and Level 2C remain HOLD.
