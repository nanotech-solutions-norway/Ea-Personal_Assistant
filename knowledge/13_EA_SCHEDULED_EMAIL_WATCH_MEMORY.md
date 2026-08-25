# Ea Scheduled Email Watch Memory

**Status:** APPROVED / CANONICAL  
**Updated:** 18:10, 25.08.2026 Europe/Oslo  
**Scope:** Hourly Gmail business-email review plus authorized private Gmail/Calendar write-back

## Current operating memory

- Run one bounded monitoring/execution cycle per scheduled execution. Level 2 remains HOLD.
- Current native task: `Ea Email Draft & Follow-up Watch`, hourly `condition_watch`, enabled.
- For every actionable business thread, classify whether reply, follow-up, both, waiting, scheduled, closed or excluded.
- If NTSN owes a reply, the cycle must end with one current in-thread Gmail draft unless a concrete tool/permission/safety failure prevents it. Reconcile/update existing drafts before creating another. Never send.
- If a genuine business follow-up is required, the cycle must end with one duplicate-safe private solo Calendar follow-up unless excluded. Private internal follow-up execution is specifically operator-authorized by the current runtime; this does not authorize external calendar effects.
- Gmail is the default draft channel. Inster, Grupo Oesía and Tecnobit remain chat-only unless Gmail drafting is explicitly requested for the specific message.
- Review the complete relevant thread, including sent mail, drafts and supported attachments, and cross-check related Gmail plus Calendar/Drive/GitHub only when materially relevant.
- Deduplicate notifications separately from execution. A previously reported case may still require draft/calendar write-back.
- Never create new calendar entries for invoices, payment/billing/collection notices, failed Autopay, subscription-payment items, customs, Tolletaten or Altinn customs matters.
- Confirmed meetings preserve popup reminders 1 day and 2 hours before the meeting.
- Product/technical/commercial claims require authoritative current evidence; unsupported claims remain PENDING_REVIEW.
- Verify exact attachment version, filename, reference, recipient and substantive scope. Do not state that a file is attached unless the completed draft confirms it.
- NTT-AT already has the NTSN address; do not repeat it unless explicitly requested.
- In Norwegian drafts, use `coating` rather than `belegg` for a coating product/system.
- Never send, forward, invite, purchase, commit, share, delete evidence, modify Drive/GitHub governance from the scheduled cycle, or claim Level 2 capabilities.
- If required Gmail/Calendar execution fails, notify the operator with the exact failed thread/action and error reason.

## Current controlling source

`active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`

## Validation state

`ACTIVE_VALIDATION` as of 25.08.2026. Core scheduled execution is enabled and working. One intermittent Gmail draft payload failure remains PENDING_REVIEW; see `validation/Ea_Scheduled_Function_Audit_1810_25082026.md`.
