# EA tenant migration contract v1 — 02:08, 31.10.2026

Work ID EA-SYNC. Status PENDING_REVIEW; S/M architecture UNDECIDED. This proposal adds offline executable contract evaluation and disposable PostgreSQL regression cases. It neither applies a legacy migration nor chooses a tenancy architecture.

`tenant_migration_contract.py` evaluates both S and M with explicit owner decision provenance. S requires a verified dedicated database and rejects shared runtime. M requires FORCE RLS evidence for all six legacy tables. Both require inventory, restricted role, source cursor scope, same-tenant references, approval/case binding, replay denial, rollback readback and quarantine proofs. Inputs are evidence assertions, not independently authenticated proof; an empty blocker list never authorizes deployment. This module is not wired to the live application.

| Table/key | Current source | Required S/M review |
| --- | --- | --- |
| ea_cases | global case_id and gmail_thread unique | dedicated DB or tenant-qualified case/thread key |
| ea_actions | global action_id/idempotency_key; case FK | same-tenant case and scoped replay identity |
| ea_approvals | global approval_id; action/case FKs separately | same tenant AND matching action-to-case binding; immutable revision/hash |
| ea_audit | global audit_id; case/action labels | isolated append-only audit grants/retention |
| ea_watch_registrations | global watch_id; source/resource | tenant/account/source scope and revocation |
| ea_ingest_events | global event_id; source/cursor index | tenant-qualified event dedupe/quarantine |
| ea_source_cursors | global source PK stores hashed tenant/source/collection scope | preserve existing stable keys; NULL tenant rows remain invisible; no inferred backfill |

Synthetic PostgreSQL additions inspect role flags, owner separation, pg_policies and FORCE RLS; test missing/wrong-tenant reads/deletes and INSERT policy denials with temporary transactional DML grants; test scope removal after commit/rollback; and prove transaction rollback/readback with NULL legacy cursors. These cover the EXISTING projection/cursor boundary, not unimplemented legacy RLS. Legacy cross-case approval and migration rollback tests remain blocked until the owner chooses and reviews S/M schema design. The contract demands those future proofs without falsely claiming them implemented.

Reproduce: from `level-2/backend`, run `python -m unittest discover -s tests -v`. Existing `ea-level2-backend-tests.yml` runs the same suite and a PostgreSQL 16 integration job using a disposable synthetic database. PostgreSQL tests are skipped when EA_TEST_DATABASE_URL is absent; skips are not acceptance. No dependency or workflow changes.

Recovery: close unmerged feature PR to withdraw this proposal. Existing SQL 001–006 and runtime source are unchanged. No live migration needs reversal. Independent acceptance, source/CI readback and separate live privacy/infrastructure approvals remain outstanding; Level 2B/2C and production sync HOLD. Before/after overall progress N/A% independently unverified.
