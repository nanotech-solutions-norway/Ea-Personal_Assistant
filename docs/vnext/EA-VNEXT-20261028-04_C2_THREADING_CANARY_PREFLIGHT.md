# Ea vNext — M5 C2 Existing Draft Threading Canary: Controlled Preflight

**Work ID:** `EA-VNEXT-20261028-04`  
**Status:** `PROPOSAL_ONLY / EXACT_CASE_APPROVAL_REQUIRED`  
**Date:** 28 October 2026, Europe/Oslo  
**Scope:** Two known internal technical draft cases, no other customer cases; publicly described here using anonymized IDs `C2-A`, `C2-B`.

## Current verified technical limitations

- Existing Gmail drafts are each native unsent `DRAFT` objects in their own separate threads, **not** in the required original customer/mill source conversation.
- `update_draft` does not expose a native cross-thread reparent/rethread selector; it cannot be assumed to move an existing draft into the source thread.
- `create_draft` can use a specific reply message anchor, but new creation while the old draft exists risks violating one-draft-per-case; deleting a draft may also violate the 03D operator-deletion protocol.
- The current Gmail connector exposes no explicit `From` send-as alias setter. If the required sender cannot be proven, record `SENDER_ALIAS_UNVERIFIED` and stop rather than generate wrong-persona content.
- Original C2-A source correspondence is long and requires complete or demonstrably sufficient latest-message evidence; an earlier 60-message bounded retrieval was marked truncated against 63 total.
- C2-B has a recipient/CC mismatch and partner technical confidentiality controls. One case's recipient cannot be inferred from the other case's account.
- Existing body text may be clean (no manual signature), but clean text alone does **not** establish an acceptable draft.

## Read-only preflight and stop conditions

1. Recheck full current source conversation, including latest **SENT**, all relevant inbound, authorized Reply-To and CC, exact account and intended sender.
2. Confirm two draft IDs still exist and have not been deleted by operator, and check recipient-level 03D suppression status from positive evidence (absence alone is not evidence).
3. Verify source technical claims, application method, attachment requirements, commercial/NDA disclosure boundaries, approval prerequisites, and exact thread anchor.
4. Compare existing draft bodies and preserved attachments to current approved response content.
5. Prefer an operator-assisted manual correction rather than creating a duplicate if connector cannot rethread safely. A manual Outlook channel is **mandatory** for any Espen-authored case; do not create an Espen Gmail draft.
6. Any actual provider mutation must name exact case + account + allowed draft action + prestate + compensating plan, and must have a *separate explicit* operator grant. Do not delete, duplicate, send, invite, share or change permissions.
7. Immediately perform provider readback of exact thread, sender identity, To/CC, subject, body, no manually authored signature, attachment state and draft/unsent label. Failed or ambiguous postwrite verification => `DRAFT_QA_FAILED` and stop; no blind retry.
8. Keep original thread, legacy draft and audit evidence separately linked in private register. Never copy raw customer material into public GitHub.

## Release decision

No supported native in-place rethread action was demonstrated. **C2 writes remain HOLD** until a feasible nonduplicative repair method and separately attributed operator approval are both available. Run completion, GitHub merge, or CRM draft-QA status does not grant Gmail write authorization. External sending is never within this canary.
