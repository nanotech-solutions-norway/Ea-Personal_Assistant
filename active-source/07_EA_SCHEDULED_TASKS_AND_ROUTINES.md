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

Native task ID `6a9287f458048191ad59286eba6eea2d`; mode `exact_schedule`; first new scheduled run 10.10.2026 at 07:00. Task-update acknowledgement confirms configuration only, **not successful future execution**, access to all sources or bidirectional synchronization.

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


## 14.11.2026 — Current live task state and sample-fulfilment handling

Live native task inspection on 14 November 2026 shows `Ea Business Email Watch` (ID `6a6336e9994c8191b25966dc451c2db0`) **DISABLED**, notwithstanding earlier historical enabled assertions in this document and 07B. The separately configured `Ea Lead Changes` (ID `6ad1dc166c888191b928bc03c96934ff`) is **ENABLED** on its existing daily schedule. Live provider state controls any claim of current execution; do not silently re-enable the hourly task. The operator-approved `03I_EA_SUPPLIER_TO_CUSTOMER_SAMPLE_FULFILMENT_20261114.md` is eligible for bounded source-reconciled internal processing only within an enabled, specifically authorized routine. No such schedule guarantees push delivery, full coverage or source readback without an observed run; no autonomous send, shipping release, public claims or Level 2B/2C activation.

## 14.11.2026 — Paused Ea Business Email Watch readiness, operator activation pending

The existing native business Email Watch (task `6a6336e9994c8191b25966dc451c2db0`) was updated **while disabled** under explicit operator instruction. Provider readback confirmed `is_enabled=false`, hourly recurrence, `condition_watch`, Europe/Oslo, and the replacement prompt containing current 07B/03F/03D/03I sample-fulfilment source gates. Operator will enable it later. Do not resume the task automatically; the enabled daily Lead Changes monitoring is a different task and must not be duplicated or rescheduled. Historical source passages claiming the hourly task is enabled are superseded by this dated live-state observation.

Current Gmail connector lacks a `from_address` setter. For each drafted business reply require native sender/From verification in addition to in-thread clean-body/DRAFT readback; no substitution or false send-ready. Supplier sample handling includes LOT, labels, exact bottle printable dimensions/sprayer specification, logistics fees, separate upstream/downstream drafts and private duplicate-safe Calendar follow-ups with **no reminders**. Unattended future runtime and notification delivery remain `NOT_VERIFIED`. No external send, dispatch, meeting invitation, CRM/Drive/GitHub autonomous write or Level 2B/C promotion follows from configuration.

### 14.11.2026 live state follow-up (19:44 Europe/Madrid)

A later independent provider peek observed the **same** Email Watch task in `is_enabled=true` state, `updated_at=2026-11-14T18:36:41.586938Z`, after the earlier in-place prompt update had been verified while paused. Ea **did not enable it** and cannot attribute the change to an actor. Hourly `condition_watch`, Europe/Oslo and the fully updated prompt remain unchanged. Do not silently disable/re-enable. Last recorded run predates this updated prompt, so unattended runtime acceptance is still PENDING. When checking current operation, retrieve live task state rather than relying on either dated status statement.
