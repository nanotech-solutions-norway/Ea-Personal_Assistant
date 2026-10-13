# Ea Level 2 Managed Runtime Deployment Runbook

Status: STAGING_READY / INFRASTRUCTURE_PENDING  
Level 2A: ACTIVE  
Level 2B: HOLD  
Level 2C: HOLD

## Verified connector baseline — 30.09.2026

The connected NTSN Gmail and Google Calendar surfaces authenticate successfully to the same business profile.

Verified Level 2A read surfaces:
- Gmail profile lookup;
- Gmail message-ID search;
- Gmail draft listing;
- Calendar profile lookup;
- Calendar listing;
- bounded Calendar event search;
- Google Drive read/list access to the Level 2 staging folder.

No send, forward, invitation, attendee mutation, Drive sharing, permission mutation or destructive action was exercised.

## What the connected app surfaces do not provision

The current Gmail/Calendar connectors used by Ea do not expose infrastructure provisioning for:
- Gmail `users.watch`;
- Google Cloud Pub/Sub topic/subscription creation;
- Calendar watch-channel creation;
- HTTPS webhook hosting;
- PostgreSQL provisioning;
- secret-store/managed-identity provisioning.

Those remain deployment dependencies rather than failed Level 2A connector tests.

## Deployment order

1. Provision a managed PostgreSQL-compatible database.
2. Apply `sql/001_initial_schema.sql`.
3. Provision an HTTPS service endpoint with TLS.
4. Provision secret storage and a Level 2A execution identity.
5. Provision Google Cloud Pub/Sub for Gmail push.
6. Register Gmail `users.watch` and persist history/expiration.
7. Register Calendar watch channels and persist channel/resource/expiration.
8. Implement Gmail-history and Calendar-sync-token processors.
9. Wire deterministic policy evaluation before every tool sink.
10. Append readback/audit results after every write.
11. Run the integration validation matrix in staging.
12. Keep the hourly Ea Business Email Watch as reconciliation watchdog.

## Required environment

See `staging.env.example`.

Production secrets must never be committed to GitHub or copied into Drive.

## Promotion rule

Completing deployment does not activate Level 2B. Level 2B.1 remains HOLD until its promotion gate is separately satisfied and the operator explicitly promotes it.


## Runtime scaffold checkpoint

Implemented in repository:
- deterministic Gmail Pub/Sub notification parser;
- deterministic Calendar notification-header parser;
- stable event identifiers for duplicate delivery handling;
- durable ingestion-event SQL migration;
- WSGI `/healthz`, `/readyz`, `/hooks/gmail`, and `/hooks/calendar` surface;
- fail-closed webhook behavior when durable storage is unavailable;
- container scaffold;
- unit tests for malformed notifications, duplicate Gmail delivery, Calendar notification persistence, health/readiness separation and no-store rejection.

Important: `server.py` deliberately starts without a durable store adapter, so `/readyz` remains 503 and webhook POSTs remain unavailable until the managed PostgreSQL adapter is connected. This is an intentional safety state, not a production configuration.


## Delivery authentication requirement

Before any cloud watch/channel is registered, implement an authenticated-delivery adapter appropriate to the deployed Google push configuration.

The runtime now treats delivery authentication as a mandatory readiness dependency. Test-only allow-all authentication is not production-safe.

Recommended production control:
- Gmail Pub/Sub push: validate authenticated push identity/token at the ingress/gateway or runtime adapter;
- Calendar channels: validate the channel identity/token and expected stored watch registration before event acceptance;
- reject unexpected source/channel/resource combinations;
- do not persist authentication secrets in event metadata or audit bodies.

`EA_WEBHOOK_AUTH_MODE` must identify the configured mechanism; the staging example uses `google_verified_delivery`.


## Durable adapter checkpoint

Repository adapters now exist for:
- PostgreSQL event persistence;
- Gmail authenticated Pub/Sub OIDC delivery;
- Calendar channel-token authentication.

Additional required environment:
- `GMAIL_PUSH_AUDIENCE`;
- `GMAIL_PUSH_SERVICE_ACCOUNT_EMAIL`;
- `CALENDAR_CHANNEL_TOKEN`.

The container installs `psycopg[binary]`, `google-auth` and `requests` from `requirements-runtime.txt`.

Production sequence is now:
1. provision database;
2. apply `001_initial_schema.sql` and `002_ingestion_events.sql`;
3. provision HTTPS runtime and secrets;
4. set the Google delivery-auth values;
5. confirm `/readyz` is 200;
6. only then register Gmail/Calendar watches.

Do not register watches while readiness is 503.


## Cross-platform atomic staging checkpoint — 11.10.2026

Operator confirmed merged PR #37. Follow-up PR #38 stages:
- `src/ea_backend/projection_sink.py`: PostgreSQL transactional projection and cursor write with optimistic expected-cursor check, per-collection advisory lock, rollback and in-transaction readback.
- `src/ea_backend/provider_paging.py`: bounded complete-page collector; missing/cyclic page tokens or missing terminal source cursor fail closed.
- `sql/004_collection_scoped_projection.sql`: collection identity for secondary calendars, Google accounts and provider resource scopes; apply **after 001, 002 and 003**.
- tests for duplicate replay, cursor drift, incomplete pagination, tenant/collection separation and rollback.

The change is **not a deployed worker**. It does not register Google watches, deploy cloud resources, configure OAuth or initiate a full data copy.

### Staging deployment gate, in order

1. Confirm intended owner, tenant/resource isolation, subscription, region and budget for a **separate private EA** environment; do not silently reuse AtlasOrbit or family credentials or infrastructure.
2. Provision private managed PostgreSQL and restricted service networking. Run and verify SQL migrations 001, 002, 003, 004; enable effective per-tenant DB row security before processing non-synthetic personal/customer records.
3. Deploy authenticated HTTPS service with durable EventStore and secret manager. Require 2A-only flags, TLS, denied public DB access, backups, retention, tracing and kill switch.
4. Register separate least-privilege Google OAuth grants for the managed service. The native ChatGPT Gmail/Calendar/Drive connections **do not confer** those provider API credentials on the backend. Provision Google Cloud Pub/Sub plus Gmail `users.watch`, Calendar `events.watch` and Drive change processing only after readiness and delivery signature/token verification pass.
5. Install GitHub App webhook only for authorized repositories, validate its signatures and replay IDs. Poll/reconcile to cover missed webhook deliveries.
6. Complete full *authorized resource-scoped* scans, exhaust page tokens and store source cursors atomically with items. Test HTTP 410 Calendar cursor reset, Gmail history expiry, Drive change-cursor recovery, duplicate GitHub webhook, process restart and rollback.
7. Perform independent post-commit readback against the application DB and original provider; validate 03B exclusions, 03D suppression, policy bypass negatives, tenant isolation, source freshness, revocation and data minimization.
8. Record provider-specific PASS evidence; request the operator's explicit production launch authorization. Level 2B/2C stay HOLD. Continuous sync must not be labelled live until recurring ingestion and reconciliation have actually succeeded.

### Known blockers

- No authenticated cloud subscription/resource-management connector is present in this ChatGPT runtime.
- No actual managed PostgreSQL database, HTTPS webhook deployment or backend OAuth credential has been verified in this session.
- Real provider-specific `events.list`, Gmail `history.list`, Drive `changes.list` and GitHub webhook workers remain to be integrated with the staging sink.
- No independent post-commit readback, database RLS proof or end-to-end staging test has yet been evidenced.
- Native ChatGPT Tasks/chats/Projects do not have a generally verified external synchronization API; treat as manual/operator-authorized snapshots where applicable.

Repository CI covers synthetic tests only. Treat anything beyond that as `PENDING_REVIEW` or `INFRASTRUCTURE_PENDING`, not production acceptance.

## Disposable PostgreSQL / Calendar source integration checkpoint — 11.10.2026

PR #39 adds a PostgreSQL 16 ephemeral GitHub Actions service and a real (non-mock) database integration test. The test applies migrations `001` through `004` and verifies item insert/revision, cursor advancement, duplicate no-op, cross-collection identity separation, explicit tombstone, stale cursor rollback and failed validation rollback. Synthetic records only; CI is **not** the EA live datastore.

New read-only `src/ea_backend/calendar_source.py` transforms `events.list` into resource-scoped `SourceItem` records and enforces all-pages-before-cursor behavior. Use `nextSyncToken` only from the last Calendar page; retain `showDeleted=true` and the same compatible parameters when making incremental `syncToken` calls. A Calendar HTTP 410 requires new full source reconciliation; do **not** delete prior state before a new complete scan and atomic commit. See Google's official Events.list API documentation for parameter limitations. No OAuth credential or HTTP transport was provisioned by this PR.

### Acceptance evidence required before next phase

- Evidence that a separate private EA staging subscription/resource group and cost ceiling have been approved.
- PostgreSQL private ingress, secrets in vault, tenant isolation / RLS, independent migration verification, backup and audit proof.
- A deployed, authenticated HTTPS receiver that answers `/readyz == 200` with actual durable DB and verified provider delivery identity.
- Independent backend OAuth grants: native ChatGPT connector authorization is not a usable backend token.
- A full resource-scoped Google Calendar sync, OAuth readback, persisted `nextSyncToken`, incremental follow-on run, and verified 410 recovery.
- Separately completed Gmail, Drive and GitHub incremental workers, source cursors, signed notifications and reconciliation.
- Privacy, exclusions, no-send, no-external-calendar-write, deduplication, kill switch and recovery tests passing before any promotion.

**No production deployment or cross-platform data replication is evidenced by this code.** Level 2B and 2C remain HOLD.

## Source-change adapter checkpoint — 11.10.2026

This follow-on review branch adds deterministic read-only adapters for:
- `src/ea_backend/gmail_history_source.py`: follows Gmail `users.history.list` until the terminal `historyId`, emits only dirty thread IDs, deduplicates change pointers, and propagates the documented 404 history-expiry condition. It **does not** retrieve or classify threads and is not initial mailbox-sync logic.
- `src/ea_backend/drive_changes_source.py`: exhausts `changes.list` pages and saves the terminal `newStartPageToken` only after complete capture, tracks IDs needing re-read, distinguishes potentially removed files, and refuses unsupported shared-drive events rather than silently discarding them. A file omitted from an incremental feed is NOT deleted. It **does not** yet establish approved Drive-folder membership, account access or a complete baseline.
- `src/ea_backend/github_delivery.py`: validates GitHub `X-Hub-Signature-256` against raw signed bytes using constant-time comparison, checks allowlisted repositories and installations, and emits minimal delivery metadata. It does **not** connect an HTTP listener or perform any GitHub mutations.

All adapters have synthetic unit regression tests. Source watch creation, provider OAuth, subscription renewal, reconnect/resync, credential revocation, error backoff/dead-letter queue and protected database write-through remain follow-up infrastructure and integration work.

### Required worker-to-database integration

1. Use account-/collection-specific least-privilege OAuth credentials stored in a dedicated secret manager, never these ChatGPT connector session credentials.
2. For Gmail changed thread IDs: retrieve authoritative current `threads.get` (including the latest draft/deletion suppression state), apply 03D before any approved internal draft action, produce minimal normalized records only after consent/scope classification.
3. For Drive changed file IDs: re-read `files.get` and relevant parents/permissions. Access loss and `removed` are potentially significant but require scope-specific reconciliation before tombstoning. Skip personal/private items in business namespace and never mirror raw file contents to public GitHub.
4. For GitHub: verify webhook delivery signature before JSON parsing, persist delivery IDs for replay protection, fetch current issue/PR/workflow state with a least-privileged installation token, and verify repository/installation allowlist on each worker cycle. Do not treat webhook payload as business instructions.
5. Atomically persist the vetted resource projections, completed source cursor, and audit metadata under an authorized tenant identity; prove real PostgreSQL row security and cross-tenant negative tests.
6. Observe a second incremental delivery, forced token expiry/reset, replay, provider revocation, and disconnect/restart before marking a source SYNCED.

Provider change notifications are triggers, not authoritative evidence. No user data or credentials were copied into this repository, and no continuous synchronization is active as a result of this change.

## Resumed engineering checkpoint — 13.10.2026 (staging only)

The operator expressly resumed the previously saved EA cross-platform synchronization project on 13 October 2026. The 11 October hold on engineering work is lifted **only for authorized development and synthetic testing**; no production launch, customer data migration, Azure expenditure or credential onboarding was authorized.

### New Calendar atomic-readback pilot

- `src/ea_backend/calendar_staging_worker.py` orchestrates **one authorized, bounded, read-only Google Calendar collection** using injected `events.list` transport. It refuses incremental mode without a trusted persisted cursor and propagates HTTP 410/partial-page failure without changing the datastore.
- `src/ea_backend/postcommit_readback.py` independently opens another PostgreSQL connection **after** the projection sink commits, sets its RLS tenant scope for the read transaction and compares the recorded run, cursor and item revisions. Its `CommittedStateUnverified` exception **does not imply rollback**, so never blindly replay after a readback error.
- `src/ea_backend/projection_sink.py` normalizes offset-qualified timestamps to a canonical UTC instant before comparing a provider observation with PostgreSQL `timestamptz`, preventing false source-revision drift when server and provider time zones differ. Ambiguous timestamp input fails closed.
- New tests cover staged full/incremental paging, incorrect/missing tokens, HTTP 410 failure, postcommit ambiguity and actual PostgreSQL nonowner-role readback/unchanged replay using synthetic Calendar fixtures.

### Deployment hard gates still open

1. Obtain **separate EA** staging subscription/resource group, region, monthly cost cap, account owner, tenant owner and safe data scope. The AtlasOrbit Azure environment is **not** interchangeable.
2. Provision via an actually authorized cloud administrator/connector. Use managed PostgreSQL with migrations 001–005, private networking, a nonowner/no-BYPASSRLS runtime identity, mandatory TLS, secrets vault, audit/backup/retention and independent readback identity. Legacy EA case/action/watch/audit tables are **not yet tenant-isolated**.
3. Provide a genuinely authorized **read-only** Google Calendar backend OAuth credential; native ChatGPT Google connector access cannot be exported as a backend OAuth grant.
4. Fetch an initial complete authorized Calendar collection and incremental token, reconcile 410 with a separately completed full scan, and verify provider/database state without inferring deletions from a partial or filtered scan.
5. Repeat for Gmail, Drive, GitHub with provider-specific starting cursor, replay guards, permissions/tenant boundaries and independent source readback. Do not claim a worker deployed just because a staging adapter passes unit tests.
6. Run real staging authorization/revocation, restart, duplicate, crash, wrong-tenant, provider 404/410, rollback, exclusion and no-external-write tests. Require the operator's explicit final production acceptance; Level 2B/2C stay HOLD.

**Important:** independent DB readback proves only DB persistence, not source/provider reconciliation. Do not call it full end-to-end synchronization. A verifier must run using a restricted database role, **not** the CI superuser. A tenant scope must come from trusted workload authorization, never webhook-supplied text. Raw credentials and customer event content must never be checked into this public repository.
