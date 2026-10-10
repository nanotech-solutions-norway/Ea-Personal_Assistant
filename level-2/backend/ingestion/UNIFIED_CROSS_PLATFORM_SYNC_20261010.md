# Ea Cross-Platform Synchronization
Timestamp: 02:10, 10.10.2026 Europe/Madrid
Status: STAGING_IMPLEMENTATION / NOT_DEPLOYED

## Decision and authority
Operator requested initiation following merger of EA calendar PR #36. EA 03A, 03B, 03D, 07/07B/07C and Level 2A restrictions continue. Level 2B/2C remain HOLD. No new permission, secret, production deployment, invitation, email send or external event mutation is authorized by this source file.

## Provider boundaries
- Google Calendar: scoped initial full event scan, persisted syncToken, incremental events.list, channel-triggered refresh, handle 410 with scoped resync. Calendar remains authoritative for event time.
- Gmail: scoped initial review followed by verified users.watch / Pub/Sub / history.list with latest thread readback. Existing private-draft rules and recipient-level 03D suppression remain.
- GitHub: issues, pull requests, workflows and milestones through read API plus validated webhooks and periodic reconciliation.
- Google Drive: approved project folders and action documents, changes.getStartPageToken, changes.list and optional changes.watch with metadata/readback.
- ChatGPT Tasks/chats/Projects: native inventory or explicitly shared snapshots only where accessible; no blanket background API is assumed. Report MANUAL_ONLY/UNAVAILABLE otherwise.

## Deterministic projection
- Scope every source identity by tenant, provider, account and resource.
- Keep private event/commitment records in a protected application database, never the public EA repository.
- Source revision and explicit deletion/tombstones govern convergence. Never infer deletion from a partial, bounded or paginated listing.
- Merge cross-provider references only with verified case evidence; never with title similarity.
- Persist normalized changes and provider cursor atomically. Require independent database readback. Do not advance a cursor after an incomplete/failed scan.
- The Python planner and SQL migration added in this PR are staging infrastructure, not an active provider worker.

## Acceptance sequence
1. Verified: PR #36 merged; read-only Calendar/Gmail/GitHub/Drive connector check completed.
2. In progress: planner, SQL projection and synthetic regression tests.
3. Infrastructure pending: managed PostgreSQL, authenticated HTTPS webhook runtime, secret manager, Google Pub/Sub/watch registrations, Drive change-feed credentials, GitHub App webhooks.
4. Staging tests pending: duplicates, stale revisions, 410 reset, dropped pages, restart recovery, audit privacy, 03D/03B, tenant isolation and kill switch.
5. Production gate pending: provider-scoped permission approvals, independent readback and operator-authorized launch.

No source may be reported SYNCED until its full initial scan, durable cursor and independent readback have passed. Do not conflate ChatGPT's native scheduled briefing with a production continuous synchronization engine.
