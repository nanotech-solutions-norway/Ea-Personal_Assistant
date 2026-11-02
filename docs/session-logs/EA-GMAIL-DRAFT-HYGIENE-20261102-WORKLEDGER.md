# Ea Gmail 03F — scoped draft-hygiene verification (02.11.2026)
Status: ACTIVE / PREPARED / redacted operational log
Work ID: EA-GMAIL-DRAFT-HYGIENE-20261102
Authority: current explicit operator instruction 02.11.2026; approved/canonical 03F (GitHub blob 6f79063583d4bc8f217fd529456123b9464680c8) and 03D; 07B hourly watch. Do not silently change these authorities.
Scope: ONE existing unsent, in-thread customer Gmail draft shown in user screenshot. Retain its draft/thread identity, existing To/CC/subject and original messages. Replace ONLY newly composed draft body to remove prior quote chain, meeting details, historical signatures and hand-added sender signature. Preserve user-authored current reply meaning; no send.
Source: screenshot supplied by operator, current Gmail thread readback, current Gmail draft list, 03F canonical Drive/GitHub; current hourly task peek. No source email body, private email addresses, meeting links, attachment, or credentials stored.
Target: Gmail DRAFT (provider draft identifier held only in runtime); task EA Business Email Watch inspected read-only.
Actor/tools: operator authorizes; Ea via Gmail.update_draft/read_email_thread and GitHub feature-branch tooling.
Preconditions: correct active draft exists with DRAFT label in existing thread; prior copied correspondence is present; no attachment; sender-alias selector not exposed in connector; no sent action authorized.
Expected after: same draft ID + same thread + intended recipients/subject + DRAFT + no quoted earlier emails + no reconstructed signature. Gmail UI signature presence cannot be proven by connector. If update fails, do not blindly recreate or send; classify DRAFT_QA_FAILED and preserve existing draft.
Idempotency: work ID EA-GMAIL-DRAFT-HYGIENE-20261102; single in-place edit; no automatic retry after ambiguous write.
Rollback/recovery: re-read current provider draft and reconcile before any restoration; never assume old body restorable or messages reversible. GitHub feature proposal can be closed without merge.
Project authority: protected main unchanged; this ledger is a feature-branch proposal until reviewed and merged.
## Append-only events
| Event | Phase | Actor/tool | Target | Before | After | Evidence/readback | Open action |
|---|---|---|---|---|---|---|---|
| E001 | PREPARED | Operator / Ea | Scoped existing Gmail draft | Draft in original thread contains quoted chain and signature text | No edit attempted | Gmail thread/draft preflight; 03F rule confirmed | Perform one in-place body clean and independent readback |
| E002 | PREPARED | GitHub / Ea | Governance work log | No dedicated work-ID ledger for this occurrence | Proposal initialized on nonprotected feature branch | Branch creation confirmed; file write/readback pending | Verify logging persistence |
