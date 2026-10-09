# 07C — Ea Unified Calendar and Daily Commitments Briefing

**Timestamp:** 01:48, 10.10.2026 Europe/Madrid
**Decision:** OPERATOR-INSTRUCTED — add a calendar-and-commitments review to the Ea daily scheduled run.
**Scope:** Native ChatGPT daily task and approved read-only/Level 2A personal assistant workflows.
**Production status:** Daily native task ACTIVATED. Unified sidebar/plugin calendar UI NOT IMPLEMENTED. Managed two-way synchronization NOT DEPLOYED. Level 2B/2C HOLD.
**Authority:** Current operator instruction; EA 02, 03A, 03B, 03D, 07/07B and existing Level 2A controls. This document does not grant new production connector authority.

## 1. Native task registration

- Title: `Ea Daily Calendar Briefing`.
- Native ChatGPT task ID: `6a9287f458048191ad59286eba6eea2d` (formerly `Ea Morning Briefing`).
- Schedule: daily, 07:00 Europe/Oslo; equivalent local clock in Europe/Madrid. First occurrence 10.10.2026 07:00.
- Task mode: `exact_schedule`; enabled after operator request 10.10.2026.
- Scope: one bounded run. No claims of continuous monitoring or automatic ingestion of all ChatGPT chats, Projects or tasks.
- The existing `Ea Business Email Watch` remains independent, hourly and `condition_watch`. Do not duplicate its schedule, override its prompt or reinstate the removed `Daily task review — morning priorities` Google Calendar series.
- The previously recorded enabled states for Morning and Mid-Day as of 29.09.2026 differed from the live disabled state observed on 10.10.2026. Morning was expressly reactivated by the latest operator request; Mid-Day stays disabled. Do not silently change other task states.

## 2. Calendar-first daily review

1. Read available authorized Google Calendars and today's chronological events, confirming time zones, locations and conferencing only where present.
2. Look ahead 7 days for meetings, commitments and material due dates, with 14/30-day horizon for preparation, travel, dependencies and risks.
3. Identify overlaps, unrealistic travel or preparation buffers, stale tentative holds and rescheduling proposals. Never invent availability or imply a proposed event is booked.
4. Reconcile Google Calendar business follow-ups against latest relevant Gmail history; an overdue Calendar entry alone is not evidence that a reply is still due.
5. Distinguish private/family, company and project contexts. Never disclose private items into company/project artifacts or logs.

## 3. Cross-source commitment review

- **Google Calendar:** Authority for actual scheduled event times and attendance.
- **Gmail:** Authority for correspondence, received requests and replies; check latest sent/received context before declaring a follow-up due.
- **GitHub:** Authority for issue, pull-request, workflow-run and repository milestone state.
- **Google Drive:** Evidence for project/action registers, schedules, briefs and milestone documents. Canonical approvals outrank historical evidence.
- **Ea approved action register/External Memory:** Cross-platform commitment identity, next action, owner, due date and evidence links, within permitted privacy boundary.
- **Native ChatGPT tasks/chats/Projects:** Inspect only where actual access is available for that particular run. Never assert universal task inventory or chat-project APIs. Mark absent access `UNAVAILABLE`.
- **Other connectors:** Optional explicitly authorized sources; do not infer data access or install integrations autonomously.

Each unified item should have stable `source_system`, `source_id`, `commitment_id`, `title`, `owner`, `due_at` and `timezone` (if known), `status`, `priority`, `linked_source_references`, `last_verified_at`, and `approval_state`. Do not put private event bodies or customer data in this public repository. De-duplicate by authoritative source IDs and correlated case identity; never merge ambiguously.

## 4. Execution and governance

- Native daily briefing is a reporting/reconciliation workflow, **not** authorization for arbitrary automatic event creation, external invitations or global two-way synchronization.
- Existing approved Level 2A internal operations may prepare/verify private Gmail drafts and duplicate-safe *internal* business follow-ups, subject to specific runtime connector affordances, previous-source freshness, 03D recipient-level deleted-draft suppression, explicit exclusion list, and authoritative post-write readback.
- Internal business follow-up standard (where permitted): private transparent 15-minute solo event, no attendees/Google Meet/reminders, Europe/Oslo time, `[Company/contact] - [urgency] - Follow-up`. Search for duplicates and retain only one active next action.
- Never create or maintain calendar entries for invoice, payment, collection, subscription/autopay failure, customs, Tolletaten or Altinn customs items. Report material risks separately with an exclusion note.
- External sends, external event changes/invites/attendee modifications, sharing/deletion/permissions, money movement, financial/legal/commercial commitments and production promotions require independent approval. Preserve approved meeting reminders 1 day and 2 hours before where configured.
- Level 2B/2C remain HOLD. Full managed Calendar webhooks, OAuth identities, durable storage and plugin sidebar interface remain separate engineering scope and require formal acceptance before promotion.

## 5. Daily report contract

Title format `Ea Daily Calendar & Commitments Briefing — HH:MM, DD.MM.YYYY`.

Sections: chronological Today; Calendar conflict/preparation; next 7 days; upcoming 14/30-day material deadlines; urgent Gmail; GitHub/Drive project deadlines/blockers; ChatGPT Tasks/Projects coverage status; overdue/awaiting external/awaiting internal/approval needed; top recommended actions; concise source and verification status bar.

For every material entry, include verified owner, due date/time and timezone if known, last source check, evidence link and next step. Separate verified facts from recommendations, PENDING_REVIEW and missing-access placeholders. Report tool/readback failures explicitly; never claim synchronization without independent source checks.

## 6. Acceptance and limitations

**Native schedule configuration:** verified by returned task-update response, enabled DAILY 07:00; first live run not yet observed.
**Connector execution:** not live-tested in the newly edited daily task.
**Google Calendar two-way synchronization:** not activated by this change.
**ChatGPT native Scheduled/tasks inventory:** no generally asserted API; use conditional access label.
**ChatGPT sidebar calendar:** separate UI build, not part of native scheduled-task change.
**Publication:** this source addition is staged in a GitHub review PR; do not treat an unmerged PR as canonical production code.
**Data protection:** no personal schedule details, email bodies, credentials or confidential documents in repository content.
