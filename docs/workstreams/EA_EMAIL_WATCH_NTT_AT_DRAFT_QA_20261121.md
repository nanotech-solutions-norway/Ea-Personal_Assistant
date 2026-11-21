# Ea Email Watch — NTT-AT single-draft repair evidence (21.11.2026)

**Status:** VERIFIED INTERACTIVE PROVIDER DRAFT; CODE-ONLY CHANGE UNDER PR; NOT DEPLOYED; NOT A GENERAL ALIAS EXCEPTION.
**Authority:** Operator explicitly authorized one specific exception to the exact sender-alias preflight for one NTT-AT Gmail reply. Approved 07B/03D/03F/03I remain unchanged, Level 2A INTERNAL UNSENT only, Level 2B/C HOLD.
**Work-ID:** EA-EMAIL-WATCH-ALIAS-QA-20261121-01; private canonical audit ledger in ai-memory-ops.
**Sources:** Gmail original inbound message 1a1f825d4a61747d (20.11.2026 08:45:44 UTC); same-thread draft-ID r8995593395544749774; verified current draft message-ID 1a2001d840e33524 (21.11.2026 21:57:44 UTC). The latter ID superseded the first temporary draft payload on in-place update.

## Before, repair and readback

1. Live NTSN draft inventory showed NO existing NTT-AT draft in the current original thread. Separate historic Gmail records mentioning older NTT-AT drafts were stale and not proof of current presence.
2. Gmail create_draft uses original inbound `reply_message_id`; connector does not expose a `from_address` selector. Operator's **one-time case-specific exception** permitted a single unsent create attempt for this thread only. This is not reusable, cannot be inferred from other aliases and cannot be promoted to unattended execution.
3. Initial draft create returned draft-ID r8995593395544749774 and original thread-ID 1a1f825d4a61747d, but Gmail appended a quoted original thread. Initial QA failed.
4. update_draft replaced the body on EXACTLY THE SAME draft-ID, without a new draft. Current message-ID became 1a2001d840e33524; prior message-ID is stale and must never be used for final QA.
5. Independent `read_email(current_message_id)` + `list_drafts` confirmed From `r.meyer@nanotech-solutions.com`, exact original thread, intended original reply recipient and two CC recipients, matching subject, exact response-only clean body without quoted history, zero Ea-authored signature, DRAFT label, no attachments and no duplicate drafts.
6. No send, Calendar event, invite or external change occurred. The meeting is only proposed in an **unsent** draft. Calendar search for NTT events 20–30 Nov returned none; no meeting was assumed or created.

## Implementation / acceptance split

- Existing fail-closed `preflight_disposition` alias gate remains in force for all unattended/new cases. No general auto-draft permission, guessed alias selection or message send.
- `one_time_draft_gate` is a synthetic internal helper to model a specifically identified and explicitly operator-authorized exception: exact case, account, original inbound message-ID and expected sender, no suppression/Espen conflict and a complete preflight. Returns `ONE_TIME_DRAFT_WRITE_ALLOWED_QA_REQUIRED`, **not** `DRAFT_VERIFIED`. No persistent approval record or provider write exists in this helper.
- `same_draft_cleanup_status` demands identical stable draft-ID/thread-ID, complete current-message readback and byte-exact clean body. A mismatched/stale/quoted draft fails. Existing `draft_readback` verifies DRAFT, current message-ID, From/To/CC, subject, body, attachments and no duplicate.
- Regression tests extend the synthetic test suite from 19 to 23 cases. This proves only code-branch behavior, not unattended runtime acceptance.
- The Gmail provider is the authority for the already saved case-specific post-write sender identity. An observed valid From for this one draft **does not prove** current connector supports selectable From or authorize a future unsupported new-draft attempt.
- GitHub main implementation requires approved PR/check/readback; Drive mirrors must be derived summary/pointers, never a competing audit ledger. Native hourly automation, CRM and Calendar are unchanged.

**Open gates:** autonomous sender selection/case preflight, provider first-action proof on actual scheduled runs, and full end-to-end unattended runtime acceptance remain NOT_VERIFIED. User notification delivery NOT_VERIFIED. 03D recipient suppression and 03F signature/no-quote rules stay binding.
