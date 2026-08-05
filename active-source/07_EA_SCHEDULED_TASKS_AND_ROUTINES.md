# 07 — Ea Scheduled Tasks and Routines

Status: ACTIVE / LEVEL_1_CUSTOMIZED  
Authority: Active-source framework with approved operator overrides  
Level: Level 1 active, Level 2 automation on HOLD

## Purpose

Define Ea's native scheduled routines and separate them from Level 2 managed automation.

## Native scheduled tasks

Scheduled tasks perform one bounded cycle per run. They must not be described as continuous monitoring, universal recording, automatic project-file awareness, autonomous write-back, attachment archiving or another Level 2 backend capability.

## Recommended routines

| Task | Schedule | Purpose |
|---|---|---|
| Ea Business Email Watch | Hourly | New or materially updated business email, overdue correspondence, draft replies, private relationship follow-ups and meeting controls |
| Ea Morning Briefing | Monday–Friday 07:00 Europe/Oslo | Calendar, urgent emails, preparation needs and approvals |
| Ea Mid-Day Review | Monday–Friday 14:00 Europe/Oslo | Changed meetings, unanswered emails and follow-up gaps |
| Ea Evening Close | Monday–Friday 21:00 Europe/Oslo | Tomorrow preparation, pending approvals and session-close items |
| Ea Saturday Review | Saturday 10:00 Europe/Oslo | Weekly administration and open-loop review |
| Ea Sunday Planning | Sunday 18:00 or 21:00 Europe/Oslo | Monday and weekly planning |

## Ea Business Email Watch

**Task title:** `Ea Business Email Watch`  
**Timing mode:** `condition_watch`

```ical
BEGIN:VEVENT
RRULE:FREQ=HOURLY
END:VEVENT
```

Use the complete prompt in:

`07A_EA_GMAIL_BUSINESS_EMAIL_WATCH_PROMPT_2351_05082026.md`

Apply the following controlling overrides before older workflow notes:

- `03A_EA_EMAIL_DRAFT_CHANNEL_OVERRIDE_1744_05082026.md`
- `03B_EA_CALENDAR_EXCLUSIONS_AND_DRAFT_MEETING_OVERRIDE_2351_05082026.md`

The hourly task may search and read connected sources, create or update private Gmail drafts, and create or update duplicate-safe private internal calendar controls exactly as authorized by the prompt. It may not send email, send invitations, notify external attendees, make purchases or commitments, modify Drive/GitHub governance files, or claim Level 2 execution.

## Morning briefing prompt

Prepare my Ea morning briefing. Review today's calendar, urgent emails, meeting preparation needs, missing documents, overdue follow-ups, pending approvals and recommended actions. Do not send, book, cancel, share or change anything without approval.

## Mid-day review prompt

Prepare my Ea mid-day review. Check meeting changes, unanswered emails, follow-up gaps, open approvals and preparation gaps for remaining meetings. Draft recommendations only. Do not execute external actions without approval.

## Evening close prompt

Prepare my Ea evening close. Summarize tomorrow's meetings, missing documents, pending approvals, overdue follow-ups, unresolved issues and suggested session-close updates. Classify proposed learning updates as AUTO_APPROVED or PENDING_REVIEW.

## Saturday review prompt

Prepare a weekly administration and open-loop review. Identify unresolved emails, pending tasks, lead-list updates, project follow-ups, missing files and next-week preparation items.

## Sunday planning prompt

Prepare Monday and weekly planning. Review upcoming meetings, deadlines, follow-ups, pending approvals and documents required for the week.

## 03:00 nightly update

Status: HOLD for Level 2.

A 03:00 file-aware update requires managed automation if it must access files, update registers, write back to Drive/GitHub, process attachments, extract archives or validate by readback. Native tasks must not claim these capabilities.

## Global approval rule

Scheduled tasks may prepare drafts, recommendations and expressly approved private internal controls. They may not:

- send emails;
- send or externally notify meeting invitations;
- add external attendees;
- modify files, permissions, memory or governance records;
- place orders or issue purchase orders;
- accept pricing, warranty, delivery, exclusivity, liability, legal, tax, accounting or regulatory commitments;
- share data;
- store confidential transcripts;
- promote rules without approval.

## Validation

Before enabling or materially changing a routine:

- confirm the account task limit;
- run a manual test;
- verify full-thread reading and duplicate detection;
- verify notification suppression for unchanged cases;
- verify no calendar entries are created for invoices, payment reminders, customs, Tolletaten or Altinn customs matters;
- verify the correct attachment version is used when a draft includes a file;
- verify the Inster/Grupo Oesía/Tecnobit channel exception;
- verify the NTT-AT address rule and Norwegian `coating` terminology rule;
- verify draft meeting invitations use the current Teams handling rule;
- verify no external action occurs;
- record the result in the validation tracker.
