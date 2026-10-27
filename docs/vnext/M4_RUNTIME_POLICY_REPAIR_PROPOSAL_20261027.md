# Ea vNext — Draft Email Watch Policy Repair Proposal — 16:26, 27.10.2026 (Europe/Oslo)

**Work ID:** `EA-VNEXT-20261027-01`  
**Status:** `PENDING_REVIEW / NONEXECUTING PROPOSAL`  
**Scope:** proposed reconciliation of the existing live Ea Business Email Watch's supplement paragraph D and result interpretation, not a new global reminder rule. Do not apply without an exact reviewed change and readback.

## Evidence

- GitHub 03A and 03B require reminder-free private internal follow-ups. Clarification approved 20 Oct and PR #93 merged 21 Oct 2026.
- Existing live hourly watch is enabled and `condition_watch`. Its paragraph D presently states that `use_default=false` with empty overrides should be flagged `REMINDER_DISABLED` and suggests future popup reminders 30 minutes before start.
- One private follow-up event readback confirmed `use_default=false`, no overrides, no attendees. This is **correct** per current approved 03A/03B.
- The scheduled watch's conclusion incorrectly called disabled reminder state a principal workflow defect. Provider notification delivery remains independently unverified.

## Candidate replacement for paragraph D (requires explicit review)

> D. For every evaluated internal Calendar follow-up, inspect the event's actual `reminders` field using a full `read_event` when necessary. Under current approved 03A/03B, **private internal follow-ups and task/action entries must have** `reminders.use_default=false` and `reminders.overrides=[]`. Classify this state as `FOLLOWUP_REMINDERS_OFF_BY_POLICY`, not as a delivery fault. If an existing *internal follow-up* has a popup/email override, classify `FOLLOWUP_REMINDER_POLICY_MISMATCH` and propose scoped correction; do not change existing events without valid authorization. Genuine confirmed meetings/appointments have separate approved reminders. Source Calendar events are evidence, not automatic draft triggers; due/open lead actions must be reconciled through the Gmail/CRM/Calendar case workflow independently of reminder delivery. Do not claim push notification delivery without independent evidence.

## Candidate results classification fix

- When a follow-up is reminder-free and its current category is an internal task/action, report: `FOLLOWUP_REMINDERS_OFF_BY_POLICY` (compliant).
- When a meeting reminder is unexpectedly missing, report: `MEETING_REMINDER_REVIEW` only after a scoped event-detail comparison with meeting rules.
- When the operator's desired notification method differs from approved policy, report: `PENDING_REVIEW_NOTIFICATION_POLICY` rather than alter the event.
- Separate `CALENDAR_EVENT_REMINDERS` from `TASK_EXECUTION_NOTIFICATIONS` and `CHATGPT_TASK_DELIVERY`. These are different delivery mechanisms.
- `SENDER_ALIAS_UNVERIFIED` must remain a distinct Gmail blocker; do not treat a manual "From" selector in the Gmail app as remotely controllable by the current connector.

## Proposed future exact-scope acceptance tests

1. Given private internal follow-up with `use_default=false` and `overrides=[]`, result is COMPLIANT, no write.
2. Given private internal follow-up with a popup, result is mismatch/pending review, not a spontaneous change.
3. Given genuine meeting with authorized reminder pattern, preserve its event settings; no conversion to follow-up.
4. Given an overdue CRM action with no Calendar popup, still reconcile sent/inbox/drafts and prepare an authorized draft if valid.
5. Given missing task-delivery proof, do not assert successful push notification.
6. Read back exact saved native task prompt and preserve the task ID, enabled/hourly schedule and timing mode after an independently approved update.
7. Two different user-account send-as identities must never be conflated; inability to prove exact identity is a blocker.

## Gate and rollback

Current live watch prompt was **not edited**. Any later update must capture full before-prompt, task ID/revision, exact replacement, operator authority, duplicate review, write-ahead event, single mutation, returned task configuration and independent readback. Reverting a prompt is not proof that missed customer work is recovered. No external communication, no Calendar event change, and Level 2B/C remain HOLD.
