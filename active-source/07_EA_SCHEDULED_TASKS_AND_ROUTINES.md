# 07 — Ea Scheduled Tasks and Routines

Status: READY_FOR_LEVEL_1_CUSTOMIZATION  
Authority: Active-source framework  
Level: Level 1 active, Level 2 automation on HOLD

## Purpose
Define Ea's native scheduled routines and separate them from Level 2 managed automation.

## Native scheduled tasks
Scheduled tasks are for reminders, monitoring and scheduled prompts. They must not be treated as full file-aware background automation.

## Recommended routines
| Task | Schedule | Purpose |
|---|---|---|
| Ea Morning Briefing | Monday–Friday 07:00 Europe/Oslo | Calendar, urgent emails, prep needs, approvals |
| Ea Mid-Day Review | Monday–Friday 14:00 Europe/Oslo | Changed meetings, unanswered emails, follow-ups |
| Ea Evening Close | Monday–Friday 21:00 Europe/Oslo | Tomorrow prep, pending approvals, session-close items |
| Ea Saturday Review | Saturday 10:00 Europe/Oslo | Weekly admin/open-loop review |
| Ea Sunday Planning | Sunday 18:00 or 21:00 Europe/Oslo | Monday and weekly planning |

## 03:00 nightly update
Status: HOLD for Level 2.

The 03:00 nightly update requires managed automation if it must access files, update registers, write back to Drive/GitHub, process attachments, extract archives or validate by readback. Native tasks may only remind or prompt within platform limits.

## Morning briefing prompt
Prepare my Ea morning briefing. Review today's calendar, urgent emails, meeting preparation needs, missing documents, overdue follow-ups, pending approvals and recommended actions. Do not send, book, cancel, share or change anything without approval.

## Mid-day review prompt
Prepare my Ea mid-day review. Check meeting changes, unanswered emails, follow-up gaps, open approvals and any prep gaps for remaining meetings. Draft recommendations only; do not execute external actions without approval.

## Evening close prompt
Prepare my Ea evening close. Summarize tomorrow's meetings, missing documents, pending approvals, overdue follow-ups, unresolved issues, and suggested session-close updates. Classify proposed learning updates as AUTO_APPROVED or PENDING_REVIEW.

## Saturday review prompt
Prepare a weekly admin/open-loop review. Identify unresolved emails, pending tasks, lead-list updates, project follow-ups, missing files and next-week preparation items.

## Sunday planning prompt
Prepare Monday and weekly planning. Review upcoming meetings, deadlines, follow-ups, pending approvals and documents required for the week.

## Approval rule
Scheduled tasks may prepare drafts and recommendations. They may not send emails, create/send meeting invitations, modify files, share data, store confidential transcripts or promote rules without approval.

## Validation
Before enabling routine use:

- confirm task limit for account plan;
- create only supported number of active tasks;
- run one manual test for each prompt;
- verify no task claims full project-file automation unless Level 2 backend exists;
- record results in validation tracker.
