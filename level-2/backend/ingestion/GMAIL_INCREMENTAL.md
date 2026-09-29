# Gmail Incremental Ingestion Contract

Status: IMPLEMENTATION_SPEC / NOT_DEPLOYED

## Authoritative API behavior

Use Gmail `users.watch` to establish or renew mailbox push notification delivery. The response supplies a current `historyId` and an `expiration` timestamp. The watch must be renewed before expiration.

A production watch requires a Google Cloud Pub/Sub topic and appropriate Gmail publishing permission.

## Ea flow

1. Register/renew `users.watch`.
2. Persist returned `historyId` and `expiration` in `ea_source_cursors` / `ea_watch_registrations`.
3. Pub/Sub callback validates message provenance and decodes the mailbox notification.
4. Compare notification history ID with stored cursor.
5. Retrieve Gmail history from the stored point.
6. Convert changed thread/message IDs into Ea event envelopes.
7. Re-read the complete relevant thread before classification/action.
8. Advance the cursor only after the event batch is durably recorded.
9. If history cannot be reconciled, perform a bounded mailbox reconciliation and reset the cursor from current state.
10. The hourly Ea Business Email Watch remains the safety reconciliation path.

## Invariants

- Push notification content is a trigger, not sufficient evidence for a business decision.
- Do not execute actions from notification payload alone.
- Do not advance a cursor before durable event capture.
- Duplicate Pub/Sub deliveries must be harmless.
- One thread failure must not block unrelated changed threads.
- Level 2A cannot send mail.

Reference: https://developers.google.com/workspace/gmail/api/reference/rest/v1/users/watch
