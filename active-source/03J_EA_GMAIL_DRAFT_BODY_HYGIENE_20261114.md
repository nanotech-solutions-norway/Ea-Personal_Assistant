# EA Gmail Draft Hygiene — 16:33, 14.11.2026 (Europe/Madrid)

Status: USER_INSTRUCTED; proposed source-control adoption via PR pending checks.
Authority: Direct operator instruction of 14.11.2026; scope is EA/NTSN draft composition only.

## Rules
- Draft body must contain ONLY newly written reply text. Do not manually paste quoted historical conversation, email reply chains, previous sender headers, old signatures or disclaimers into the new draft body. Keep reply linkage through Gmail thread metadata.
- Never manually append a signature or sign-off block (including 'Kind regards', name, position, company or contact details). Gmail's configured signature is handled by the Gmail client and must not be duplicated in the draft text.
- Preserve actual substantive new reply text, recipients, CC, subject and thread ID; never remove customer history from the underlying Gmail thread.
- Before updating, check existing draft and attachments. If an attachment-bearing draft cannot be edited safely, leave it intact and report the limitation. Never recreate and lose attachments.
- After each edit, verify Gmail DRAFT (not SENT), correct recipients and thread, and absence of quoted history and manual signature. Do not send messages without separate authorization.
- This rule does not override contact exclusions, suppression flags, privacy rules, external-commitment gates or EA Level 2 HOLD.

## Initial evidence — 14.11.2026
- NTSN business Gmail: 13 current drafts inspected; 11 edited to remove manual signature and/or copied history; one Nils Arne Ro draft already compliant and unchanged.
- The remaining Realtest/SJ draft contains an attachment; Gmail connector disallows in-place edits of attachment-bearing drafts, so it was left unchanged.
- All 12 editable drafts read back as DRAFT, not SENT, with no manually appended signature or quoted history.

## Review
- Operator instruction is approved for practical draft generation immediately; GitHub PR merge is governed by repository checks and branch protections.
