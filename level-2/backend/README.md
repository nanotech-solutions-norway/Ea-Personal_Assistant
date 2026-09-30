# Ea Level 2 Backend Foundation

Status: IMPLEMENTED_IN_REPOSITORY / NOT_DEPLOYED  
Level 2A: ACTIVE  
Level 2B: HOLD  
Level 2C: HOLD

## Purpose

This directory implements the first managed-backend foundation for Ea without granting additional external autonomy.

The backend design enforces these boundaries:

1. durable case state and action/audit records;
2. deterministic policy decisions: ALLOW / REQUIRE_APPROVAL / PROHIBIT;
3. idempotency and revision binding;
4. source-to-sink controls for untrusted external content;
5. incremental Gmail/Calendar ingestion contracts;
6. least-privilege separation between Level 2A and future Level 2B;
7. readback/reconciliation requirements;
8. Level 2B.1 approval-bound Gmail send staging only.

## Repository implementation

- `sql/001_initial_schema.sql` — portable PostgreSQL schema for cases, actions, approvals, source cursors, watches and audit.
- `policy/policy-matrix.v1.json` — deterministic action authority matrix.
- `policy/source-sink.v1.json` — external-input/source and consequential-sink controls.
- `schemas/*.schema.json` — event, case, audit and approval envelopes.
- `src/ea_backend/policy.py` — deterministic policy evaluator.
- `src/ea_backend/idempotency.py` — stable action/revision hashing.
- `ingestion/GMAIL_INCREMENTAL.md` — Gmail watch/history contract.
- `ingestion/CALENDAR_INCREMENTAL.md` — Calendar watch/sync-token contract.
- `staging/LEVEL_2B1_SEND_DRAFT.md` — exact approval-bound send pilot design.
- `validation/TEST_MATRIX.md` — backend and promotion validation.
- `.github/workflows/ea-level2-backend-tests.yml` — standard-library CI checks.

## Runtime decision

Recommended runtime: application-owned backend using OpenAI Agents SDK/Responses with Ea-owned storage, tools and approval state. The backend policy gateway remains outside model discretion.

## Deployment prerequisites

NOT_DEPLOYED until all are available:

- managed PostgreSQL-compatible database;
- HTTPS webhook endpoint;
- Google Cloud project + Pub/Sub topic for Gmail push;
- Google Calendar watch callback endpoint;
- secrets/identity store;
- separate Level 2A and Level 2B credentials/scopes where technically possible;
- OpenAI runtime credential;
- observable tracing/logging destination;
- backup/retention configuration.

The native hourly Ea Business Email Watch remains the reconciliation/watchdog path even after event-driven ingestion is deployed.

## External references

- Gmail users.watch: https://developers.google.com/workspace/gmail/api/reference/rest/v1/users/watch
- Calendar push: https://developers.google.com/workspace/calendar/api/guides/push
- Calendar incremental sync: https://developers.google.com/workspace/calendar/api/guides/sync
- OpenAI Agents SDK: https://developers.openai.com/api/docs/guides/agents/sdk
- OpenAI guardrails/approvals: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- MCP 2026-07-28: https://blog.modelcontextprotocol.io/posts/2026-07-28/


## Live connector validation — 30.09.2026

Connected Level 2A application surfaces were validated against the NTSN business Gmail, Google Calendar and Drive accounts.

Passed:
- Gmail profile lookup, message-ID search and draft listing;
- Calendar profile lookup, calendar listing and bounded event search;
- Drive staging-folder read/list.

No external write was exercised.

The connected app surfaces do not provision Gmail `users.watch`, Calendar watch channels, Pub/Sub, managed PostgreSQL, webhook hosting or secret/identity infrastructure. Those remain `INFRASTRUCTURE_PENDING`.

Deployment artifacts:
- `runtime/DEPLOYMENT_RUNBOOK.md`
- `runtime/staging.env.example`
- `runtime/preflight.py`
- `validation/LIVE_CONNECTOR_VALIDATION_2026-09-30.md`


## Runtime scaffold — 30.09.2026

Repository staging now includes a fail-closed event receiver scaffold:
- `sql/002_ingestion_events.sql` — durable trigger-event table;
- `runtime/ea_runtime/events.py` — Gmail Pub/Sub and Calendar notification parsing;
- `runtime/ea_runtime/store.py` — EventStore contract plus test-only in-memory implementation;
- `runtime/ea_runtime/app.py` — WSGI health/readiness/webhook surface;
- `runtime/ea_runtime/server.py` — staging server entry point;
- `runtime/Dockerfile` — container scaffold;
- event/runtime regression tests.

The webhook surface intentionally returns **503** when the deployment preflight is not ready or when no durable EventStore is attached. This prevents notification acknowledgement before durable capture.

The included `InMemoryEventStore` is test-only and must never be used as a production acknowledgement sink.


### Webhook authentication hardening

Production readiness now also requires an authenticated-delivery adapter. The runtime will not report ready, and will not acknowledge Gmail/Calendar webhook traffic, unless:
- deployment preflight passes;
- a durable EventStore is attached;
- an authenticated-delivery adapter is attached.

The bundled allow-all authenticator and in-memory store are test-only and become readiness-eligible only when `EA_ENV=test`.
