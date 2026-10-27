# Ea vNext M2 — Target Architecture, Migration and Acceptance Plan — 16:06, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Status:** `ARCHITECTURE_PROPOSED / SYNTHETIC_ONLY / PRODUCTION_CUTOVER_HOLD`  
**Source:** existing approved EA Level 1/2A and QA rules; proposals below do not create new provider authority.

## Operating architecture

1. **Assistant interface:** ChatGPT interprets requests, reviews source evidence, drafts recommendations and receives exact approvals. Must disclose unavailable tools and unverified outcomes.
2. **Effective rule resolver:** Load exact approved source/sha/scope, reject unsupported authority or unresolved conflicts; deny external effects outside active Level 2A permissions.
3. **Persistent case/action controller (target, NOT DEPLOYED):** Stable case ID, source revision, action ID, idempotency key, ownership, retry/reconciliation state, work cursor and overdue backlog. Store provider pointers minimally, not confidential bodies.
4. **Provider-specific adapters:** Gmail drafts, Google Calendar, approved CRM and Drive/GitHub only under granted permissions; provider writes require before/after reads and fail-closed handling. No external send or external invitations.
5. **Independent verification and monitoring:** Dispositions, limits, missed/blocked work, fairness, alias faults, notifications and output scores independently checked against provider state.
6. **Audit and recovery:** One append-only redacted ledger per owning workstream; stable reference to immutable code revision and source event. Derived Drive memory mirrors are separate and non-authoritative.

## M1 to M8 migration sequence and gates

| Stage | Owner and exact work | Gate/evidence | Effect |
| --- | --- | --- | --- |
| M1 — Baseline | EA vNext preparer: pin approved repo, Drive mirror metadata, live task states, conflicts and historical decision chain | Source SHAs, no duplicates, non-sensitive branch ledger and readback | Non-executing |
| M2 — Consolidate | EA rule owner: propose minimized effective rule manifest, no silent promotions or old rule deletion | CR register and targeted diff; operator review for changed authority | Non-executing proposal |
| M3 — Synthetic policy proof | Engineering: isolated rules evaluator, exhaustive negative fixtures, state machine model | Deterministic offline tests PASS; no provider interaction | Local/synthetic only |
| M4 — Adapter diagnosis | EA connector owner: bounded read-only capability probe and privacy/alias validation | Supported/unsupported provider action matrix, missing scopes named | Read-only unless separately approved |
| M5 — Level 2A canary | Explicit operator-approved internal-only test cohort | End-to-end draft/Calendar readback, no duplicate writers | Exact separate grant required |
| M6 — Shadow | New system in read-only shadow alongside existing Ea, no parallel outbound writer | Differences documented by stable case ID and outcome | Read-only |
| M7 — Endurance | Owner acceptance authority: 100 consecutive actionable cases and 14 days normal operation, whichever longer | Canonical zero-violation gates, 100% verification/audit; independent witness | No cutover |
| M8 — Cutover | Operator separately signs exact new release/rollback envelope | Single-writer switch, frozen source revision, independent before/after and recovery readiness | HOLD until separate approval |

## Transaction and case states

`DISCOVERED -> VALIDATING -> POLICY_EVALUATED -> ACTION_READY -> ATTEMPTED -> READBACK -> VERIFIED_COMPLETE`

Alternative terminal-for-run, but **nonterminal for case**: `PENDING_COVERAGE`, `BLOCKED_PERMISSION`, `BLOCKED_FACTUAL_DEPENDENCY`, `PENDING_REVIEW`, `PENDING_APPROVAL`, `SENDER_ALIAS_UNVERIFIED`, `DRAFT_QA_FAILED`, `WRITE_FAILED`, `AMBIGUOUS_WRITE`. `ALREADY_SENT`, `WAITING_EXTERNAL`, `WAITING_INTERNAL`, `OPERATOR_DELETED_SUPPRESS_RECREATE` and `CLOSED_NO_ACTION` require grounded, source-linked dispositions and periodic reconciliation as appropriate.

An unattended run may be `COMPLETED_WITH_BLOCKERS` while individual cases remain open. It may **not** claim all work complete merely because its time window ended.

## Reconciliation contract

- Discovery: union inbound changes, oldest due cases, existing drafts, sent state, registered next actions, applicable Calendar event states, and authorized CRM rows.
- Deduplicate by stable tenant/account + real-world case + provider thread/action type; never silently merge distinct legal entities.
- Before a provider write: check current source, suppressions, exact sender identity, duplicates, pending approvals, price/product claims, and source revision freshness.
- After a provider write: independently verify the actual stored provider object. If this fails after ambiguous success, do not repeat blindly; queue reconciliation.
- Fairness: reserve bounded capacity for oldest previously deferred cases; report exact skipped/blocked counts rather than inventing queue clearance.
- Do not create an external attendee, send/forward an email, modify permissions, release commercial terms or promote approved rules without the applicable independent approval.

## Synthetic rule tests (M3, offline)

The adjacent `synthetic_policy_guard.py` implements a bounded *illustrative* policy evaluator (not production authorization logic). Tests in `test_synthetic_policy_guard.py` assert:
- Level 2B/C external actions denied;
- 03D known recipient suppression and explicit specific reset;
- Espen chat-only path;
- wrong/unknown Gmail sender alias blocked;
- stale and duplicate draft blocked;
- no manually inserted Gmail signature;
- internal follow-up no-reminder policy (CR-01 unresolved);
- unresolved source conflict blocks new behavior;
- no unauthorized external Calendar attendee/Meet actions;
- self-contained deterministic output.

Passing these tests demonstrates only the synthetic fixture model, not actual connector capability or release acceptance.

## Acceptance targets and evidence grading

| Metric | Proposed target | Accepted evidence |
| --- | --- | --- |
| Required cases accounted for | 100% of observed bounded cohort | Complete source scan/queue dispositions |
| Mandatory write/readback | 100% | Provider object readback after mutation |
| Unauthorized external emails/invites | 0 | Provider audit + exact action logs |
| Duplicate drafts/follow-ups | 0 | Provider thread/event identity checks |
| 03D suppression violations | 0 | Known operator-deletion fixture and live readback where authorized |
| Wrong-thread or wrong-recipient drafts | 0 | Verified headers/thread IDs |
| Unexplained skipped cases | 0 | Queue with owner and disposition |
| Conflict promotions without approval | 0 | Exact source revision + approval event |
| Secrets and confidential data in public repo | 0 | Source diff and privacy scan |
| Production dual-writer window | 0 | Coordinated cutover with stop/start readback |

## Infrastructure/financial constraints

EA issue #84 retains `NO_DEPLOYMENT / ALL_IN_EUR20_HOLD / SYNTHETIC_ONLY`; Azure staging cost, dedicated tenant, protected identity, tenancy/isolation, teardown and provider OAuth remain individually gated. Do not infer cost eligibility from a sample price, free grant or passing GitHub CI. Use synthetic CI until owner-specific approval and security evidence are complete.

## Rollback and release decision

Source documentation branch may be abandoned without changing production. Once a later separately approved vNext runtime exists, rollback must include scoped single-writer fencing and independent per-provider reconciliation, not just a Git revert. Production cutover remains HOLD and requires a new explicit operator decision.

**Next engineering gate after this PR:** validate source consolidation and resolve CR-01 without silently changing the live reminder policy; then authorize connector-specific M4 reads or a bounded M5 canary separately.
