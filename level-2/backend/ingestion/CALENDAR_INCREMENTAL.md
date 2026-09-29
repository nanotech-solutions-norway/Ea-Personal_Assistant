# Google Calendar Incremental Ingestion Contract

Status: IMPLEMENTATION_SPEC / NOT_DEPLOYED

## Authoritative API behavior

Use Calendar notification channels to signal resource changes. Notifications do not contain complete changed event data; the receiver must call Calendar API to retrieve changes.

Maintain a persisted `syncToken` for incremental event synchronization. If Calendar returns HTTP 410 for an invalidated token, wipe the local Calendar event projection for that cursor scope and perform a full synchronization to obtain a new token.

## Ea flow

1. Create/renew an Events watch channel with an HTTPS callback.
2. Persist channel ID, resource ID and expiration.
3. On notification, validate channel metadata.
4. Load the stored Calendar sync token.
5. Perform incremental `events.list` using the same compatible query parameters as the initial sync.
6. Store changed events and the returned next sync token atomically.
7. On HTTP 410, invalidate cursor, clear the affected local projection, full-sync, then store the replacement sync token.
8. Feed only material changes into Ea case reconciliation.
9. The hourly Ea Business Email Watch remains the reconciliation watchdog.

## Invariants

- Calendar notification body absence must never be treated as "no change".
- No external attendee or invitation action is authorized by ingestion.
- Internal Ea follow-up writes remain duplicate-safe and Level 2A-only.
- Watch channel expiration/renewal is monitored explicitly.

References:
- https://developers.google.com/workspace/calendar/api/guides/push
- https://developers.google.com/workspace/calendar/api/guides/sync
