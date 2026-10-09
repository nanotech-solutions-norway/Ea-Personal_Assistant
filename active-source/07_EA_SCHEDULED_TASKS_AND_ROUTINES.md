# 07 — Ea Scheduled Tasks and Routines

Status: ACTIVE / LEVEL_2A_CONTROLLED_INTERNAL  
Authority: Active-source framework with approved operator overrides  
Level: Level 1 baseline active; Level 2A controlled internal autonomy ACTIVE; Level 2B/2C HOLD

## Purpose

Define Ea's native scheduled routines, current Level 2A internal-autonomy scope, and the boundary to approval-gated or external Level 2 functions.

## Native scheduled-task rule

Each native task performs one bounded cycle per run. Native tasks may use connected evidence, create/update verified Gmail drafts, create/update duplicate-safe private internal Calendar follow-ups, prepare meetings, validate attachments and perform post-write verification within Level 2A. They may not claim continuous/unbounded monitoring, universal recording, unrestricted file/governance write-back, or autonomous external execution.

## Active hourly email task

**Task ID:** `6a6336e9994c8191b25966dc451c2db0`  
**Task title:** `Ea Business Email Watch`  
**Canonical timing mode:** `condition_watch`  
**Live timing mode:** `condition_watch` — verified 29.09.2026; prior `exact_schedule` drift resolved  
**Schedule:** hourly  
**State:** ENABLED  
**Level:** Level 2A controlled internal autonomy

Current controlling runtime source:

`07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`

The hourly task may search/read connected sources, create or update private Gmail drafts, and create or update duplicate-safe private internal Calendar follow-ups exactly as authorized by the current runtime. Required private write-back must not be suppressed merely because a case was previously reported. Notification deduplication and execution deduplication are separate controls.

Gmail is the default drafting channel for all business contacts. The former standing chat-only exception for Inster, Grupo Oesía and Tecnobit is superseded. Chat-only/no-Gmail handling applies only where the operator explicitly instructs it for the specific current message/thread.

Manual draft deletion suppression is controlled by `03D_EA_MANUAL_DRAFT_DELETION_SUPPRESSION_RULE_1111_09092026.md`. Known operator deletion remains recipient-level suppression unless a new explicit operator instruction authorizes the specifically requested draft. Thread/case scoping remains `PENDING_REVIEW`.

Calendar exclusions remain absolute for new follow-up creation: invoices, payment/billing/collection items, failed Autopay, subscription payments, customs, Tolletaten and Altinn customs notices.

Confirmed/operator-authorized meetings retain popup reminders 1 day and 2 hours before the meeting. External attendees, invitations, external meeting changes, purchases, commitments, file sharing/deletion/permission changes and Level 2B/2C actions remain outside native scheduled-task authority unless separately approved for the exact action.

## Cadence routines — reconciled 10.10.2026

The new unified Calendar & Commitments daily operating contract is defined in `07C_EA_UNIFIED_CALENDAR_DAILY_BRIEFING_20261010.md`. The native daily task was reactivated and rescheduled by current explicit operator instruction on 10.10.2026. No Google Calendar morning-priority event was created.

| Task | Current live schedule | Live state 10.10.2026 | Scope |
|---|---|---|---|
| Ea Daily Calendar Briefing (formerly Ea Morning Briefing) | Daily 07:00 Europe/Oslo / Europe/Madrid | **ENABLED** | Calendar-first agenda, 7/14/30-day commitments, Gmail/GitHub/Drive reconciliation, bounded Level 2A preparation |
| Ea Mid-Day Review | Monday–Friday 14:00 Europe/Oslo | **DISABLED** | Previous bounded review remains dormant, not changed |
| Ea Evening Close | Monday–Friday 21:00 Europe/Oslo | **DISABLED** | Previous evening review remains dormant |
| Ea Saturday Review | — | NOT ACTIVE | No separate native task; included in daily briefing |
| Ea Sunday Planning | — | NOT ACTIVE | No separate native task; included in daily briefing |

Native task ID `6a9287f458048191ad59286eba6eea2d`; mode `exact_schedule`; first new scheduled run 11.10.2026 at 07:00. Task-update acknowledgement confirms configuration only, **not successful future execution**, access to all sources or bidirectional synchronization.

**Drift disclosure:** This document previously recorded the Morning and Mid-Day routines as enabled on 29.09.2026, but live task state observed on 10.10.2026 was disabled for both. The latest operator instruction authorizes restoring a *daily* morning Calendar briefing; Mid-Day is not re-enabled. This historical state discrepancy is retained as evidence and is not silently merged.

The hourly `Ea Business Email Watch` remains enabled and unmodified. All cadence routines inherit 03D, duplicate controls, Calendar exclusions, post-write verification and Level 2A external-action boundaries. Dynamic Calendar source access must be reported as unavailable if the scheduled run cannot access connected data.

## 03:00 managed update

Status: HOLD.

A 03:00 file-aware managed update requires a managed backend if it must persist case state, process attachments/archives, synchronize Drive/GitHub governance or perform managed event ingestion. Level 2A activation does not itself authorize this nightly backend routine.

## Global approval rule

Level 2A scheduled tasks may prepare and verify drafts, private internal controls, meeting preparation, attachment validation, state reconciliation and concise internal audit metadata. They may not send/forward email, send invitations, add/change external attendees, modify external meetings, make purchases/refunds, share/delete files, change permissions, store confidential transcripts without separate authorization, promote `PENDING_REVIEW`, or accept pricing, warranty, delivery, exclusivity, liability, legal, tax, accounting or regulatory commitments.

Level 2B and Level 2C remain HOLD.

## Validation

The hourly task is enabled, hourly and synchronized to canonical `condition_watch`. The prior `exact_schedule` control-plane drift is RESOLVED as of 29.09.2026.

Open validation items:
- continue representative Gmail draft and private Calendar follow-up readback tests;
- verify 03D across hourly and cadence recovery routines;
- validate stable case identity/idempotency/freshness controls in the managed Level 2A backend;
- validate event-driven Gmail/Calendar ingestion before reducing reliance on polling;
- retain Level 2B/2C HOLD until separate promotion gates are met.
