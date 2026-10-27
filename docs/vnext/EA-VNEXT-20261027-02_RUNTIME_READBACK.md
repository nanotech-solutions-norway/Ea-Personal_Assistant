# Ea vNext — Live Email Watch Classification Repair: Verified Readback

**Date:** 27.10.2026, after 17:59 Europe/Oslo  
**Work ID:** `EA-VNEXT-20261027-02`  
**Status:** `LIVE_NATIVE_TASK_PROMPT_REPAIRED / CONFIGURATION_VERIFIED / RUNTIME_OUTCOME_PENDING`  
**Authority:** operator directed post-merge continuation of the approved narrowly scoped repair. The underlying reminder-free policy was approved on 20 October in 03A and is **not changed**.

## Exact mutation envelope

- Target: existing `Ea Business Email Watch` native hourly task only.
- Input: full before-prompt was read from provider. The single specific line `D. Inspect event.reminders overrides ...` existed once.
- Changed **only** paragraph D. The new paragraph requires internal follow-ups/tasks with `use_default=false` and empty overrides to be classified `FOLLOWUP_REMINDERS_OFF_BY_POLICY`, with popup/email reminder settings unchanged.
- It separately identifies `FOLLOWUP_REMINDER_POLICY_MISMATCH`, preserves confirmed-meeting alerts, says Calendar events do not trigger drafts, and disallows unverified notification-delivery claims.
- All other prompt characters were preserved by exact string replacement.
- Provider update returned success with expected complete prompt.
- A separate `Automations.peek` read confirmed **exact full prompt equality** and equality for task ID, title, enabled=true, schedule and timing_mode=`condition_watch` with hourly recurrence.
- Original prompt length 9,601 characters; corrected prompt length 10,038. Before and after are held only in verified native task state, **not** copied into public GitHub because of potentially sensitive contextual provider links.

## Observed outcome vs acceptance

| Check | Evidence classification |
| --- | --- |
| 03A/03B canonical no-reminder rule remains unchanged | VERIFIED |
| Existing native task updated, exact-prompt provider readback | VERIFIED |
| Task enabled, hourly condition_watch, same identity/title/schedule | VERIFIED |
| No Calendar event or external attendee/meeting write | VERIFIED — not attempted |
| No Gmail draft creation or send during this repair | VERIFIED — not attempted |
| Independent case-state improvement on next scheduled hourly run | PENDING FUTURE OBSERVATION |
| Actual ChatGPT notification delivery | UNVERIFIED |
| Sender alias selection through current Gmail draft connector | UNSUPPORTED BY EXPOSED INPUT SCHEMA |
| Level 2A accepted sustained case window | NOT TESTED |
| Azure deployed backend or Level 2B/C | HOLD |

## Next verification

At the next naturally scheduled Email Watch execution, independently inspect the latest run result to confirm correct reminder classification, fair backlog coverage, verified drafts or exact blocked dispositions and no autonomous customer sends. Do not claim that a successful prompt readback guarantees the future run uses every instruction correctly.

This file is a *documentation/verification record*, not a source of new permissions or a changed commercial/regulatory/personal-data rule.
