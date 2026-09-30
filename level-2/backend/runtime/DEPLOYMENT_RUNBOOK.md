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
