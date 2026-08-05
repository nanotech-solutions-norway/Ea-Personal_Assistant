# Ea Calendar Exclusions and Draft Meeting Override — 23:51, 05.08.2026

**Status:** APPROVED / CANONICAL / OPERATOR-INSTRUCTED  
**Authority:** Latest explicit operator instruction  
**Effective:** 05.08.2026 at 23:51 Europe/Oslo  
**Scope:** Scheduled Gmail review, CRM follow-ups, calendar controls and draft meeting invitations  
**Level:** Ea Level 1  
**Level 2:** HOLD

## 1. Supersession

This file supplements and, where stated, supersedes conflicting calendar instructions in:

- `active-source/03_EA_EMAIL_CALENDAR_MEETING_WORKFLOWS.md`;
- `active-source/03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md`;
- older CRM and follow-up implementation notes.

A current explicit operator instruction remains higher authority.

## 2. Follow-up calendar standard

For genuine lead, customer, supplier or partner follow-ups, maintain one duplicate-safe private solo event per next action.

- Title: `[Company/contact] - [urgency] - Follow-up`
- Urgency: `low`, `medium`, `high`, `critical`
- Low: Banana, event color ID 5
- Medium: Pumpkin, event color ID 6
- High: Flamingo, event color ID 4
- Critical: Tomato, event color ID 11
- Default duration: 15 minutes
- Timezone: Europe/Oslo
- Visibility: private
- Availability: transparent
- Attendees: none
- Reminders: none
- Google Meet: none

The description must contain the case summary, latest confirmed status, exact required action, material dependency or risk, and source reference.

Do not create or restore `Daily task review — morning priorities`.

## 3. Calendar exclusions

Never create, include, or maintain a calendar event or reminder for:

- invoices;
- invoice due dates;
- payment reminders;
- billing notices;
- collection notices;
- failed Autopay notices;
- subscription-payment items;
- customs matters;
- customs declarations;
- Tolletaten notices;
- Altinn customs notices.

These items may still be reported when they create a genuine deadline, service interruption, collection exposure, legal risk, or other material attention need. The report must state that no calendar event was created because the item is excluded from Ea calendar workflows.

If a prohibited invoice, payment, customs or Altinn calendar entry is discovered during reconciliation, flag it for removal or correction. Do not silently recreate it.

## 4. Confirmed meetings

When correspondence clearly confirms an exact date, time and timezone:

1. Search Google Calendar for duplicates.
2. If no matching event exists, create a private event with no attendees.
3. Preserve the confirmed title, date, time, timezone, meeting link, location, agenda and source-thread context.
4. Do not add Google Meet.
5. Preserve meeting and appointment reminders unless the operator explicitly instructs otherwise.

## 5. Proposed meetings and draft invitations

When a meeting is proposed but an outbound invitation still requires review:

1. Create or update a private tentative event titled `[DRAFT INVITE] <meeting title>`.
2. Add no attendees.
3. Set location to `Microsoft Teams`.
4. Include proposed attendees, date, time, timezone, agenda, source-thread reference and Microsoft Teams details in the description.
5. Include a valid Teams URL when present in the correspondence.
6. Otherwise write `Microsoft Teams link required before sending.`
7. Do not add Google Meet.
8. Never send an invitation or notify external attendees.

For draft invitation events, the instruction to set location to `Microsoft Teams` supersedes the older rule in `03A_EA_CALENDAR_ENTRY_DEFAULTS_0840_31072026.md` that left the location field blank.

## 6. Notification control

Notify Ruben only when an email genuinely needs attention, a material deadline or risk exists, an overdue commitment requires action, or a draft meeting invitation was created or materially updated.

Do not repeatedly notify an unchanged case. A new notification requires a new message, a material factual change, a newly reached or escalated deadline, a changed risk, a required operator decision, or a materially changed calendar action.

Do not notify merely because a Gmail draft was created or a routine private follow-up was normalized.

## 7. Approval boundary

This file authorizes only the private internal calendar actions expressly described above when the operator runs or schedules the approved Gmail-review workflow. It does not authorize sending invitations, notifying attendees, accepting or declining meetings, creating Google Meet links, or making external commitments.
