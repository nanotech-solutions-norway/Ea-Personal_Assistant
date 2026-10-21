# Ea Calendar Entry Defaults — 08:40, 31.07.2026

**Status:** CANONICAL / AUTO_APPROVED / USER_INSTRUCTED  
**Authority:** Latest explicit user instruction  
**Effective:** 31.07.2026  
**Scope:** Google Calendar tasks, follow-ups, meetings and appointments  
**Level:** Ea Level 1  
**Level 2:** HOLD

## 1. Supersession rule

This file supersedes conflicting calendar-entry instructions in:

- `active-source/03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md`;
- `05_PROJECTS_CONTACTS/02_LEADS/Ea_Lead_Customer_Followup_SOP_CANONICAL_0225_23072026.md`;
- older follow-up-register implementation notes requiring popup reminders or the title format `Follow up — [Company/contact] / [case]`.

Where no conflict exists, the older files remain applicable.

## 2. Follow-up entry defaults

Use the title format:

`[Company/contact] - [urgency] - Follow-up`

Use lowercase urgency labels:

- `low`;
- `medium`;
- `high`;
- `critical`.

Apply Google Calendar event colors as follows:

| Urgency | Calendar color | Event color ID |
|---|---|---:|
| Low | Banana | 5 |
| Medium | Pumpkin | 6 |
| High | Flamingo | 4 |
| Critical | Tomato | 11 |

Follow-up entries must be:

- private;
- transparent;
- internal;
- without external attendees;
- without Google Meet;
- without popup or email reminders.

Existing follow-up reminders must be removed when the entry is reviewed or reconciled.

Keep a concise operational description containing:

1. case summary;
2. latest confirmed status;
3. exact required action;
4. dependency or risk;
5. source reference.

Search for duplicates before creating a new follow-up entry. Maintain one active follow-up per genuine next action.

## 3. Meetings and appointments

- Keep reminders for meetings and appointments unless the user explicitly instructs otherwise.
- When Microsoft Teams is used, do not write `Microsoft Teams` in the location field.
- Use the calendar videoconference or conference field for Microsoft Teams when the connected tool supports it.
- If the connected tool cannot create a Microsoft Teams conference, preserve an existing Teams link or conference detail and do not substitute Google Meet without explicit instruction.
- Preserve attendee, meeting-link, location, agenda and reminder details unless the user specifically asks for changes.

## 4. Removed routine

Do not create or restore the recurring calendar entry:

`Daily task review — morning priorities`

The existing series was removed from Google Calendar on 31.07.2026.

## 5. Application scope

Apply these defaults to:

- existing relevant follow-up entries when reviewed;
- all future follow-up entries;
- future meeting and appointment creation or modification;
- CRM and scheduled-task workflows that prepare calendar actions.

External invitations, attendee changes, cancellations and other externally effective calendar actions continue to require explicit approval.

## 6. Validation record — 08:40, 31.07.2026

- Primary Google Calendar reviewed for future follow-up entries through 31.07.2027.
- Twelve future follow-up entries were identified.
- Seven legacy-format follow-up entries were normalized to the current title, color and no-reminder standard.
- Five entries were already compliant and were left unchanged.
- The obsolete recurring morning-priority series was removed.
- No upcoming primary-calendar entry containing `Microsoft Teams` or `Teams` was found in the reviewed period.
- Meeting and appointment reminders were not removed.
- No external invitation was sent and no attendee list was changed.

## 7. Operator clarification — 20.10.2026 (merged 21.10.2026)

- Follow-up and internal task/action entries must not trigger **any** event reminders, whether popup or email: set `reminders.useDefault=false` and `reminders.overrides=[]` on the relevant privately owned Google Calendar event. Do not change unrelated meeting or appointment reminders.
- Meetings/appointments retain their existing reminders (normally one day and two hours before confirmed business meetings where configured). Do not convert tasks into meeting events to obtain reminders.
- Existing and newly created follow-ups/tasks are to be checked for legacy notification overrides and corrected when within operator-approved scope; read back each changed event. No invitations, attendees, titles, times or conference details are to be changed by a reminders-only reconciliation.
- Google Calendar's native `Daily agenda → Email` is a per-calendar/account setting in the Calendar web interface; event-level tools do not activate or verify it. A separate custom daily email to `nanotech.solutions.norway@gmail.com` requires independently authorized execution; a one-off email request is not a recurring send authorization.
- **Merge-verified:** This clarification was incorporated in `main` through PR #93 on 21.10.2026 (merge commit `2545c1a2e1880d6e4764af98098dd4192457d5b4`). The earlier 03A/03B/07B no-reminder rules remain effective and are consistent with this clarification. This line records provenance only; it does not authorize recurring external emails or assert activation of Google Calendar's native Daily agenda email setting.
