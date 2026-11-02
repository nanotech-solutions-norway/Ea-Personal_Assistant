# EA-SYNC Path S tenant-isolation decision — 14:35, 02.11.2026

**Work ID:** EA-SYNC  
**Status:** OWNER-SELECTED ARCHITECTURE / SOURCE-ONLY DESIGN RECORD  
**Decision:** Path S — isolated single-tenant foundation.  
**Authority:** The operator selected Path S in the W2 engineering continuation.  
**Scope:** Synthetic/nonproduction engineering design. This record does not authorize or perform a live database creation, migration, data movement, OAuth change, deployment, or customer synchronization.

## Decision

Use a dedicated database and restricted runtime identity for each tenant boundary. The application connection and provider credentials must be bound to one authenticated tenant context; tenant identity must not come from an untrusted request field. A shared database/runtime serving multiple tenants is not the selected initial architecture.

The six legacy tables `ea_cases`, `ea_actions`, `ea_approvals`, `ea_audit`, `ea_watch_registrations`, and `ea_ingest_events` remain isolated by the database boundary for this path. Preserve same-database foreign-key and approval-to-action/case integrity. Do not add an assumed tenant column or assign an existing row to a tenant without verified provenance. Existing `ea_unified_items`, `ea_unified_links`, `ea_sync_runs`, and `ea_source_cursors` RLS in migration 005 remains defense in depth; this decision does not weaken it or claim RLS for the six legacy tables.

## Source cursor and replay contract

Keep source-cursor ownership inside the tenant's dedicated database. Preserve current source and collection identifiers until a separately reviewed versioned key transition exists. Missing, unattributed, revoked, or mismatched tenant identity must deny before source reads, projection writes, cursor advancement, or approval use. Do not use a shared cross-tenant cursor store.

## Migration contract v1 disposition

The existing `EA_TENANT_MIGRATION_CONTRACT_V1_20261031.md` and `tenant_migration_contract.py` remain the executable readiness contract. For Path S, readiness still requires a complete six-table inventory, restricted-role and reference/replay/rollback/quarantine proofs, `shared_runtime=false`, and independently verified dedicated-database isolation. The contract's empty-blocker result is not deployment authority. Because dedicated-database evidence has not been read back, the current readiness result remains blocked by `single_tenant_database_isolation_required`.

## Required synthetic acceptance before any protected transition

1. Use two synthetic tenants with separate disposable databases and distinct restricted roles.
2. Prove each credential reaches only its assigned database; missing/wrong binding denies before query execution.
3. Exercise cases, actions, approvals, audit, watch registrations, ingest events and source cursors, including same-tenant references and replay denial.
4. Simulate connection reuse, interrupted transaction, restore and rollback; verify no cross-database connection or cursor advancement.
5. Inspect effective role grants and database identity independently. Never use owner, superuser or `BYPASSRLS` as the runtime role.
6. Record source SHA, test run, database identities and sanitized readback before changing the readiness contract.

## Unresolved implementation gates

Actual isolated database provisioning, database identity/readback, role grants, source/principal binding, rollback evidence and any live data migration remain unverified and outside this source-only W2 change. Existing production/customer data must not be moved or queried under this design record. The application must remain fail-closed until the stated evidence is independently supplied.

## Alternatives and rationale

Path M would require tenant-key changes, composite foreign keys and FORCE RLS across every legacy table, plus a reviewed classification/quarantine plan for existing rows. The source evidence shows those tables predate tenant-wide isolation and no verified row distribution or migration columns are available. Path S therefore limits initial isolation design to a dedicated database boundary and avoids speculative legacy-row backfill. A later move to M requires a separately versioned decision and migration plan.
