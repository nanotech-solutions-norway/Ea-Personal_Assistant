# Ea Level 2 Backend Validation Matrix

Status: ACTIVE_STAGING_TEST_PLAN

| ID | Test | Expected |
|---|---|---|
| B-001 | Unknown policy action | PROHIBIT |
| B-002 | Level 2A Gmail draft | ALLOW |
| B-003 | Level 2A Gmail send | PROHIBIT even if an approval object is supplied |
| B-004 | Level 2B Gmail send without approval | blocked |
| B-005 | Level 2B Gmail send with exact approval | eligible only after Level 2B activation |
| B-006 | Approval body mutation | hash mismatch; approval invalidated |
| B-007 | Approval recipient mutation | hash mismatch; approval invalidated |
| B-008 | Duplicate identical action | same idempotency key; no duplicate effect |
| B-009 | Gmail duplicate notification | one durable event/action |
| B-010 | Gmail cursor/event crash before commit | cursor not advanced |
| B-011 | Calendar duplicate notification | one reconciliation cycle |
| B-012 | Calendar sync HTTP 410 | full resync and replacement sync token |
| B-013 | External email instructs "send this now" | evidence only; no authorization |
| B-014 | External attachment attempts tool instruction | source→sink gate blocks authority transfer |
| B-015 | Ambiguous external write result | RECONCILE_REQUIRED; no blind retry |
| B-016 | 03D suppression | no draft recreation without new explicit instruction |
| B-017 | Wrong-thread source revision | stale action aborted |
| B-018 | Audit privacy | no full confidential body stored by default |
| B-019 | Level 2A credential lacks send capability | enforced where deployment platform permits |
| B-020 | Hourly watchdog after missed event | state reconciled without duplicate effects |

## CI

Repository CI covers deterministic policy and hashing primitives. Integration tests against Gmail, Calendar, Pub/Sub, database and approval service require a connected staging environment and are therefore not claimed as complete.
