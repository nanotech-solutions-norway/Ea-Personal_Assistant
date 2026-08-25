# 07 — Ea Scheduled Tasks and Routines

Status: ACTIVE / LEVEL_1_CUSTOMIZED  
Authority: Active-source framework with approved operator overrides  
Level: Level 1 active, Level 2 automation on HOLD

## Purpose

Define Ea's native scheduled routines and separate them from Level 2 managed automation.

## Native scheduled tasks

Scheduled tasks perform one bounded cycle per run. They must not be described as continuous monitoring, universal recording, automatic project-file awareness, autonomous file/governance write-back, attachment archiving or another Level 2 backend capability.

## Active hourly email task

**Task title:** `Ea Email Draft & Follow-up Watch`  
**Timing mode:** `condition_watch`  
**Schedule:** hourly  
**State:** enabled and under production validation as of 25.08.2026.

Current controlling runtime source:

`07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`

Historical predecessor prompts remain supporting evidence only and must not override the current operator-approved runtime.

The hourly task may search/read connected sources, create or update private Gmail drafts, and create or update duplicate-safe private internal calendar follow-ups exactly as authorized by the current runtime. For actionable threads, required private draft/follow-up write-back must not be suppressed merely because the case was previously reported. Notification deduplication and execution deduplication are separate controls.

Calendar exclusions remain absolute for new follow-up creation: invoices, payment/billing/collection items, failed Autopay, subscription payments, customs, Tolletaten and Altinn customs notices. Historical legacy entries may remain as evidence unless separately cleaned up.

Confirmed meetings retain popup reminders 1 day and 2 hours before the meeting. External attendees, invitations, external meeting changes, purchases, commitments, Drive/GitHub governance writes and Level 2 claims remain outside the scheduled task's authority.

## Other recommended routines

| Task | Schedule | Purpose |
|---|---|---|
| Ea Morning Briefing | Monday–Friday 07:00 Europe/Oslo | Calendar, urgent emails, preparation needs and approvals |
| Ea Mid-Day Review | Monday–Friday 14:00 Europe/Oslo | Changed meetings, unanswered emails and follow-up gaps |
| Ea Evening Close | Monday–Friday 21:00 Europe/Oslo | Tomorrow preparation, pending approvals and session-close items |
| Ea Saturday Review | Saturday 10:00 Europe/Oslo | Weekly administration and open-loop review |
| Ea Sunday Planning | Sunday 18:00 or 21:00 Europe/Oslo | Monday and weekly planning |

These additional routines are recommendations unless separately enabled as native tasks.

## 03:00 nightly update

Status: HOLD for Level 2.

A 03:00 file-aware update requires managed automation if it must access files, update registers, write back to Drive/GitHub, process attachments, extract archives or validate by readback. Native tasks must not claim these capabilities.

## Global approval rule

Scheduled tasks may prepare drafts, recommendations and expressly approved private internal controls. They may not send emails; send or externally notify meeting invitations; add external attendees; modify files, permissions, memory or governance records; place orders or issue purchase orders; accept pricing, warranty, delivery, exclusivity, liability, legal, tax, accounting or regulatory commitments; share data; store confidential transcripts; or promote rules without approval.

## Validation

The current hourly task was audited on 25.08.2026. See `validation/Ea_Scheduled_Function_Audit_1810_25082026.md`. Phase 09 remains `ACTIVE_VALIDATION` while the intermittent Gmail draft payload failure is investigated.
