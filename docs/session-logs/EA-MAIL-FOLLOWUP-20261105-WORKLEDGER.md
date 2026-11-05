# Ea business email and follow-up reconciliation — 05.11.2026

**Work ID:** `EA-MAIL-FOLLOWUP-20261105-01`  
**Scope:** Single owner-authorized, unsent draft and private follow-up reconciliation; two existing business Gmail drafts, two newly required reply candidates, three Calendar events and the private CRM ledger.  
**Status:** `PROPOSED_LEDGER / OPERATIONAL_PARTIAL_SUCCESS / GMAIL_WRITE_FAILED / NO_SEND`  
**Authority:** Explicit user instruction of 05.11.2026; approved Ea 07B revision `63c4aa2e46727ddcb13b8deada8a9eb2a13c0661`, 03D revision `06b89e44e0abcd38c6fedd181f4a7ec36f9de9db`; `ai-memory-ops/protocols/operational_event_logging_rollback_CURRENT.md` revision `0171fa4518ddfffef4c05254893da2bfe04ee9ac`.  
**Boundary:** No provider secrets, private names, raw mail content, addresses, customer contracts or quotations stored here. This feature-branch ledger is **not approved/canonical** until reviewed. No deployment, independent task automation, external sending or authority change.

## Preconditions and controls
- Business Gmail original threads and outbound reply history re-reviewed; current Gmail drafts read in provider.
- Prior explicit manual-draft deletion suppressions remain effective; no suppressed drafts created.
- Two existing current unsent in-thread drafts verified and deliberately left unchanged; no repeat outreach on waiting-external cases.
- Two fresh reply candidates classified as required by latest source state. Draft creation was attempted once per case with original inbound message anchor, without sending.
- Private follow-up Calendar entries limited to existing authenticated primary calendar, solo/no reminders; new event is transparent/private with no meeting link.
- CRM target spreadsheet and exact tab/cell preimages read. No external pricing, invoice, dispatch or shipping assertions committed.
- Write-ahead durable ledger was **not verified before the initial provider attempts**; these entries are a post-action redacted reconstruction, not fabricated preflight proof.

## Append-only event record (all events 05.11.2026, Europe/Oslo)
| Event ID | Phase | Scope / provider | Before -> after | Independent evidence / result | Open action |
|---|---|---|---|---|---|
| E001 | READBACK | Gmail inventory | Two active unsent drafts -> same two verified drafts | Business Gmail thread-and-message readback PASS | Do not duplicate or send |
| E002 | FAILED | Gmail create_draft, case C-A | No thread draft -> provider UNKNOWN creation failure | Subsequent `in:drafts` inventory still lacked new case draft; no send | Operator copy-ready response or connector repair; sender alias remains UI-unverified |
| E003 | FAILED | Gmail create_draft, case C-B | No thread draft -> provider UNKNOWN creation failure | Subsequent independent draft inventory still lacked new case draft; no send | Confirm supplier fulfilment facts; operator copy-ready response or connector repair |
| E004 | VERIFIED | Calendar existing internal C-A | Obsolete October instructions -> updated to current factual dependency and draft failure | Provider readback: same event ID/time, zero attendees and reminders | Invoice mailbox and order acceptance remain unverified |
| E005 | VERIFIED | Calendar existing waiting-external C-C | Older technical follow-up -> latest supplier-customer waiting state and no-repeat rule | Provider readback: same event ID/time, zero attendees/reminders | Await external substrate/OEM data |
| E006 | VERIFIED | Calendar new internal C-B | No matching case event -> one new private transparent solo 15-minute review on 05.11 at 11:15 Europe/Oslo | Readback: title, status detail, no attendee, no reminder, private and transparent; event ID `bfukp6v3oqplht0vdrnlcvfvfo` | Verify dispatch/tracking before any customer ETA |
| E007 | VERIFIED | Private CRM `Follow_Ups` + `Draft_Attachment_Gate` | Outdated source and draft state -> current waiting/verified/failed classifications and one new factual-blocker case | Google Sheets batchUpdate 23 requests accepted; independent cell readback of new row, waiting-external status and failed drafting PASS | Other cases remain within existing follow-up review; CRM is private authority only |
| E008 | PENDING_REVIEW | Repository governance evidence | No current-workstream ledger -> redacted feature-branch ledger proposal | Branch-scoped creation/readback required, no main mutation | Review before promotion; optional derived Drive mirror only after approved session summary |

## Open actions
1. **Technical fact gate:** Independently confirm actual supplier fulfilment, carrier tracking and delivery for case C-B before final customer ETA. Do not state shipment from historical commitments alone.
2. **Billing gate:** Confirm the malformed customer invoice mailbox for case C-A. Do not generate an invoice from an inferred email address.
3. **Gmail connector:** Diagnose recurring provider `UNKNOWN: GmailConnectorError: Failed to create draft`; use original thread and exact reply anchor, re-read provider state before any later bounded retry. Do not create unthreaded fallback or recreate suppressed drafts.
4. **Waiting cases:** Preserve existing unsent drafts; no further follow-up for case C-C while awaiting external evidence.
5. **Governance/logging:** Branch proposal and independent readback are not proof of live canonical logging; Drive mirror remains `MIRROR_PENDING` until created and read back. Persistent event capture before initial side effects was unavailable.

**Rollback reference:** Non-recurring Calendar event and two description updates are individually reconcilable by provider IDs; no rollback requested or claimed. CRM edits are versioned by the provider; targeted restoration would require a fresh original-preimage and separate current approval. Gmail attempts produced no observed active drafts.  
**Security:** No customer data or mail body uploaded; only abstract operational outcomes and opaque internal event ID appear here.

## Operator-requested Gmail retry — 05.11.2026

| Event ID | Phase | Scope / provider | Before -> after | Independent evidence / result | Open action |
|---|---|---|---|---|---|
| E009 | READBACK | Business Gmail, C-A/C-B draft preflight | Both case drafts absent; two unrelated approved drafts remain | Current `in:drafts` inventory PASS; original in-thread messages re-read, no material case change | One bounded retry per failed case authorized by operator |
| E010 | FAILED | Gmail create_draft retry, C-A | Intended in-thread draft -> provider `UNKNOWN: GmailConnectorError: Failed to create draft` | Fresh `in:drafts` read after failure confirms no case draft; existing drafts preserved | `WRITE_FAILED`; do not create unthreaded fallback |
| E011 | FAILED | Gmail create_draft retry, C-B | Intended in-thread draft -> provider `UNKNOWN: GmailConnectorError: Failed to create draft` | Fresh `in:drafts` read after failure confirms no case draft; existing drafts preserved | `WRITE_FAILED`; supplier shipment evidence still required |
| E012 | VERIFIED | GitHub feature-branch ledger | Existing redacted workstream ledger -> appended retry and provider readback events | Readback required after branch-only write; main and draft PR #121 remain review-scoped | Diagnose Gmail draft-create connector; no send |

**Retry disposition:** Gmail read/search works, but native `create_draft` remains blocked with an opaque provider error for both intended threads; two case drafts still absent. No messages sent. Draft PR #121 remains unmerged and is not approved/canonical.
