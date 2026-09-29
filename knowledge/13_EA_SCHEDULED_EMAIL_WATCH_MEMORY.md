# Ea Scheduled Email Watch Memory

**Status:** APPROVED / CANONICAL  
**Updated:** 22:54, 29.09.2026 Europe/Oslo  
**Scope:** Hourly Gmail business-email review plus Level 2A controlled internal Gmail/Calendar write-back

## Current operating memory

- Run one bounded monitoring/execution cycle per scheduled execution.
- Level 2A controlled internal autonomy is ACTIVE. Level 2B and Level 2C remain HOLD.
- Current native task: `Ea Business Email Watch`, hourly `condition_watch`, enabled.
- For every actionable business thread, classify whether reply, follow-up, both, waiting, scheduled, closed or excluded.
- If NTSN owes a reply, the cycle must end with exactly one current in-thread Gmail draft unless 03D suppression or a concrete tool/permission/safety failure prevents it. Reconcile/update existing drafts before creating another. Never send.
- If a genuine business follow-up is required, the cycle must end with one duplicate-safe private solo Calendar follow-up unless excluded. This does not authorize external Calendar effects.
- Gmail is the default draft channel for all business contacts unless the operator explicitly instructs chat-only/no-Gmail for the specific current message/thread.
- Review the complete relevant thread, including sent mail, drafts and supported attachments, and cross-check related Gmail plus Calendar/Drive/GitHub when materially relevant.
- Deduplicate notifications separately from execution. A previously reported case may still require draft/calendar write-back.
- Never create new calendar entries for invoices, payment/billing/collection notices, failed Autopay, subscription-payment items, customs, Tolletaten or Altinn customs matters.
- Confirmed/operator-authorized meetings preserve popup reminders 1 day and 2 hours before the meeting.
- Product/technical/commercial claims require authoritative current evidence; unsupported claims remain `PENDING_REVIEW`.
- Verify exact attachment identity/version/filename/recipient/substantive fit. Do not state that a file is attached unless the verified draft confirms it.
- NTT-AT already has the NTSN address; do not repeat it unless explicitly requested.
- In Norwegian drafts, use `coating` rather than `belegg` for a coating product/system.
- Apply 03D known-manual-deletion suppression. Current approved scope remains recipient-level; thread/case scoping is `PENDING_REVIEW`.
- Use stable thread/draft identity, pre-write freshness checks, idempotent semantics, typed failure handling and post-write readback where supported.
- Never send/forward email, invite external attendees, make purchases/refunds, share/delete files, change permissions, promote governance or `PENDING_REVIEW`, or make approval-controlled commitments from Level 2A.

## Current controlling source

`active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`

## Validation state

`LEVEL_2A_ACTIVE / EXTENDED_VALIDATION` as of 29.09.2026. The hourly task is enabled and reconciled to canonical `condition_watch`; the prior timing-mode drift is resolved. Continue validation of exactly-one-draft behavior, duplicate-safe follow-ups, 03D suppression, failure isolation, readback verification and managed persistent case/audit state.
