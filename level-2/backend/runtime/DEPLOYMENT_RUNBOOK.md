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
