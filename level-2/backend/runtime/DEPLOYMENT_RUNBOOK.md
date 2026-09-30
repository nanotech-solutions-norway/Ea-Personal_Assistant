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
