# 07 — Ea Scheduled Tasks and Routines

Status: ACTIVE / LEVEL_1_CUSTOMIZED  
Authority: Active-source framework with approved operator overrides  
Level: Level 1 active, Level 2 automation on HOLD

## Purpose

Define Ea's native scheduled routines and separate them from Level 2 managed automation.

## Native scheduled tasks

Scheduled tasks perform one bounded cycle per run. They must not be described as continuous monitoring, universal recording, automatic project-file awareness, autonomous file/governance write-back, attachment archiving or another Level 2 backend capability.

## Active hourly email task

**Task title:** `Ea Business Email Watch`  
**Timing mode:** `condition_watch`  
**Schedule:** hourly  
**State:** ENABLED; corrected and re-enabled 29.08.2026.

Current controlling runtime source:

`07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`

Historical predecessor prompts remain supporting evidence only and must not override the current operator-approved runtime.

The hourly task may search/read connected sources, create or update private Gmail drafts, and create or update duplicate-safe private internal calendar follow-ups exactly as authorized by the current runtime. For actionable threads, required private draft/follow-up write-back must not be suppressed merely because the case was previously reported. Notification deduplication and execution deduplication are separate controls.

Gmail is the default drafting channel for all business contacts. The former standing chat-only exception for Inster, Grupo Oesía and Tecnobit is superseded as of 29.08.2026. Chat-only/no-Gmail handling now applies only where the operator explicitly instructs it for the specific current message/thread.

Calendar exclusions remain absolute for new follow-up creation: invoices, payment/billing/collection items, failed Autopay, subscription payments, customs, Tolletaten and Altinn customs notices. Historical legacy entries may remain as evidence unless separately cleaned up.

Confirmed meetings retain popup reminders 1 day and 2 hours before the meeting. External attendees, invitations, external meeting changes, purchases, commitments, Drive/GitHub governance writes and Level 2 claims remain outside the scheduled task's authority unless separately approved for the exact action.

## Level 1 cadence routines

| Task | Schedule | State as of 29.08.2026 | Purpose |
|---|---|---|---|
| Ea Morning Briefing | Monday–Friday 07:00 Europe/Oslo | ENABLED | Calendar, urgent emails, preparation needs and approvals |
| Ea Mid-Day Review | Monday–Friday 14:00 Europe/Oslo | ENABLED | Changed meetings, unanswered emails and follow-up gaps |
| Ea Evening Close | Monday–Friday 21:00 Europe/Oslo | ENABLED | Tomorrow preparation, pending approvals and session-close items |
| Ea Saturday Review | Saturday 10:00 Europe/Oslo | PENDING_CAPACITY | Weekly administration and open-loop review |
| Ea Sunday Planning | Sunday 18:00 or 21:00 Europe/Oslo | PENDING_OPERATOR_TIME_AND_CAPACITY | Monday and weekly planning |

The native automation account currently permits five active tasks. Activation of the Saturday routine was blocked by the active-task limit on 29.08.2026. Do not claim Saturday or Sunday as active until creation succeeds. Sunday also requires the operator to select 18:00 or 21:00.

## 03:00 nightly update

Status: HOLD for Level 2.

A 03:00 file-aware update requires managed automation if it must access files, update registers, write back to Drive/GitHub, process attachments, extract archives or validate by readback. Native tasks must not claim these capabilities.

## Global approval rule

Scheduled tasks may prepare drafts, recommendations and expressly approved private internal controls. They may not send emails; send or externally notify meeting invitations; add external attendees; modify files, permissions, memory or governance records; place orders or issue purchase orders; accept pricing, warranty, delivery, exclusivity, liability, legal, tax, accounting or regulatory commitments; share data; store confidential transcripts; or promote rules without approval.

## Validation

The hourly task was re-audited operationally on 29.08.2026 after it was found disabled. It is now enabled in `condition_watch` mode with hourly recurrence. The current runtime preserves Level 1 boundaries, calendar exclusions, duplicate controls, source-authority checks, attachment validation and post-write verification.

Open validation items:

- confirm successful post-change Gmail draft and private follow-up executions across representative threads;
- confirm the superseded Inster/Grupo Oesía/Tecnobit chat-only rule no longer suppresses Gmail drafting;
- resolve active-task capacity before enabling Saturday/Sunday cadence;
- select Sunday planning time: 18:00 or 21:00 Europe/Oslo;
- keep Level 2 HOLD.
