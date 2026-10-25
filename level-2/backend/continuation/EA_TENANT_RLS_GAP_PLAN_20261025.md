# EA Cross-Platform Sync — Tenant Isolation Gap and Synthetic Acceptance Plan — 23:56, 25.10.2026

**Work ID:** `EA-SYNC` · **Decision:** A1 source-only documentation preparation · **Status:** PREPARED_FOR_OWNING_ENGINEERING_REVIEW; NOT IMPLEMENTED / NOT ACCEPTED.
**Owner:** EA Personal Assistant. **Operator authorization:** Control Tower v2.2 exact 11-disposition confirmation on 25.10.2026, restricted to this document on a nonprotected feature branch. No schema/code changes, CI dispatch, database modification, tenant ingestion, OAuth, Azure deployment, real account synchronization, merge or release are authorized by this document.
**Canonical operational log:** [EA-SYNC work ledger](../../../docs/session-logs/EA-SYNC-WORKLEDGER-20261025.md).

## 1. Sources and existing acceptance boundary

| Authority/evidence | Exact current reference | Evidentiary meaning |
|---|---|---|
| Owning engineering continuation | [EA_CROSS_PLATFORM_SYNC_PENDING_20261011.md](EA_CROSS_PLATFORM_SYNC_PENDING_20261011.md), blob `5aa65205b69a9c1a0fba850ac1563efd8fa8fc26` | Engineering resumed 13 October; no live synchronization, production release or authorized paid infrastructure |
| Applied source migration definition | [005_tenant_rls.sql](../sql/005_tenant_rls.sql), blob `2f9c9736df45fff97a3e9c6c0424bd5aa36aa1d5` | Explicit FORCE RLS for projections, links, sync runs and source cursors; missing tenant scope must deny |
| Legacy schema | [001_initial_schema.sql](../sql/001_initial_schema.sql), blob `9a57030b09ba43e004f299046147213c93d687fc` | Original tables predate tenant-wide isolation; schema review is not runtime verification |
| Existing source tests | PR #41, PR #50 and [PR #51](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/51) | Offline/disposable-PostgreSQL tests and Calendar pipeline, not a live multi-tenant acceptance |
| EA staging | [EA issue #84](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/issues/84) | No accepted Azure staging deployment or all-in EUR20 assurance |

Source authority remains the latest approved EA project policy and exact owner instructions. This plan creates no new scope or operational mandate.

## 2. Verified gap inventory

Migration 005 explicitly **does not** secure these legacy tables in mixed-tenant use:

| Legacy table | Required review before shared runtime | Proposed isolation decision |
|---|---|---|
| `ea_cases` | Case ownership, email/calendar linkage, suppression and case reads | Require a tenant key or isolated single-tenant database; no inferred backfill |
| `ea_actions` | Case-linked actions and cross-tenant joins | Enforce same-tenant reference integrity plus default-deny RLS |
| `ea_approvals` | Approval principal and action binding | Deny cross-tenant approval reuse, replay or unauthorized visibility |
| `ea_audit` | Auditing privileges and retention, tenant-scoped reporting | Separate append-only audit rights from application DML; redact payloads |
| `ea_watch_registrations` | Account-specific provider cursor/watch metadata | Tenant/source/account-scoped isolation and revocation |
| `ea_ingest_events` | Raw incoming-event isolation and deduplication | Tenant-scoped keys, quarantine of unattributed events, no private payload exposure |

**Verified implemented boundary:** `ea_unified_items`, `ea_unified_links`, `ea_sync_runs`, and `ea_source_cursors` have FORCE RLS policies in migration 005. Superuser, table owner and BYPASSRLS access must never be the runtime execution identity. Migration 005 treats earlier NULL-scope cursor rows as invisible to restricted workers until explicitly reconciled or retired.

**Not verified:** deployed PostgreSQL roles, existing legacy record distribution, owner/custodian approval, actual tenant column names for a future migration, provider OAuth scope or cloud isolation. Do not invent those facts.

## 3. Recommended engineering decisions (proposals, not approvals)

**Path S — single-tenant isolation:** For an initial synthetic/nonproduction application, use one isolated dedicated tenant/database and restricted runtime role. No mixed-private/customer datasets. This is the safest interim candidate while source, migration and cost authority are unresolved.

**Path M — explicitly scoped multi-tenant migration:** An owning EA engineering change proposal must (a) inventory keys and references for each legacy table, (b) define stable tenant identity derived from authenticated principal, never untrusted UI fields, (c) determine approved existing-row migration/quarantine strategy, (d) stage tenant-aware constraints/foreign keys and FORCE RLS, (e) test default deny for missing/wrong tenant in a disposable PostgreSQL database, (f) independently inspect `pg_policies`, restricted DB grants and application role flags, and (g) prepare rollback/recovery using sanitized snapshots. No UPDATE/backfill or migration SQL is included here.

**STOP:** No production customer, personal, email, calendar or account records may be moved from one tenancy model to another on this proposal alone.

## 4. Synthetic acceptance test matrix — for future owning engineering

All test fixtures must use generated `synthetic-tenant-alpha` / `synthetic-tenant-beta` records, a real disposable PostgreSQL test instance and a **nonowner, non-superuser, non-BYPASSRLS** runtime role. Establish an approved test environment independently; this document runs no tests.

| ID | Negative/positive case | Required independently verifiable outcome |
|---|---|---|
| RLS-01 | No `ea.tenant_scope` transaction setting | 0 reads; INSERT/UPDATE/DELETE denied across guarded tables |
| RLS-02 | Tenant alpha role reads own synthetic case/actions | Own authorized records only; expected audit evidence |
| RLS-03 | Alpha reads/writes beta synthetic records | Denied/0 rows; no mutation of beta records |
| RLS-04 | Attempt to connect alpha action to beta case | Same-tenant FK/constraint or policy rejects |
| RLS-05 | Alpha approval references beta action | Rejected with no protected execution permit |
| RLS-06 | Invalid/unattributed provider watch registration | Fail closed; no active account subscription |
| RLS-07 | Beta-scoped source event deduped under alpha | No cross-tenant dedupe collision or visibility |
| RLS-08 | Audit writes/reads from ordinary app role | Only approved metadata append; no cross-tenant enumeration or audit modification |
| RLS-09 | Legacy NULL-tenant rows after migration | Quarantined/invisible; no automatic arbitrary assignment |
| RLS-10 | Missing scope after connection reuse/commit | Scope absent in subsequent transaction; fail closed |
| RLS-11 | Invalid/revoked tenant identity | Denial before source read, projection or cursor commit |
| RLS-12 | Permission check for runtime role | Role not owner, superuser or BYPASSRLS; grants minimized |
| RLS-13 | `pg_policies` and `relforcerowsecurity` inspection | Expected policies and FORCE RLS on every chosen table |
| RLS-14 | Retry/replay after rejected cursor/event | No duplicate or cross-tenant effect; idempotent negative result |
| RLS-15 | Rollback and restore in disposable environment | Expected sanitized prior state independently read back, no private data |

**Failure rule:** Any cross-tenant access, missing DENY, ambiguous DB commit, policy bypass, unmatched source identity, orphaned legacy row, failed recovery or leaked data blocks promotion; never weaken RLS to pass a test.

## 5. Engineering execution and acceptance handoff

1. **R0 audit:** Owning EA engineer records a verified table/column/FK inventory from `001`–`005`, current applicable policy, approved tenancy model, permission limits and migration risks.
2. **Design review:** Choose Path S or M explicitly; classify existing records, retention, data locality, audit handling and rollback; obtain project approvals for any changed tenant/data scope.
3. **Isolated source implementation (separate authorization):** Create a reviewed migration/tests in a dedicated owning engineering branch; no schema mutation in this Control Tower scope.
4. **Test and assure:** Run RLS-01..RLS-15 plus existing regression suites in isolated disposable PostgreSQL; preserve CI run IDs, source SHA, nonowner role evidence and negative-path results. AI self-review does not provide independent acceptance.
5. **Release gate:** Independently verify infrastructure privacy/security and cost requirements under EA #84. Keep Level 2B/2C, live synchronization, Gmail/Calendar/Drive account collectors and production promotion on HOLD pending exact authority.

**Completion criteria for this A1 documentation unit:** Exact file present on the feature branch; work-ID ledger and GitHub content readback recorded; no substantive code/provider changes; acceptance remains `PENDING_ENGINEERING_REVIEW`. This is **not** a claim that tenant RLS, EA synchronization or staging has been completed.
