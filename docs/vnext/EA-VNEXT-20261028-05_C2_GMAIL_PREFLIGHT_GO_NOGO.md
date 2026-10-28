# Ea vNext — M5 C2 Gmail Threading Canary: Independent Go/No-Go Preflight

**Work ID:** `EA-VNEXT-20261028-05`  
**Date:** 28 October 2026, Europe/Oslo  
**Status:** `C2_PREFLIGHT_READ_ONLY_COMPLETE / C2_WRITE_NO_GO / SENDER_ALIAS_UNVERIFIED`  
**Source:** Approved 03D manual draft deletion suppression, 03F draft hygiene, merged C2 threading preflight from PR #104, M5 acceptance plan, current Gmail provider readbacks.  
**Authority:** Operator said "Merged. Proceed as recommended" after PR #104, authorizing revalidation and proposal preparation only; the merged C2 plan explicitly requires **case-specific authorized draft actions and a feasible, nonduplicative method** before provider mutations. This is not a release, send, or draft deletion approval.  
**Privacy:** This PUBLIC-repo report uses anonymized case labels only. No recipient addresses, message/draft IDs, confidential correspondence, business prices, technical formulation details, partner identities or source thread URL are included.

## 1. Exact verified state, 28 October

| Check | C2-A | C2-B |
| --- | --- | --- |
| Full original Gmail source conversation | 63 of 63 messages; `truncated=false` | 10 of 10; `truncated=false` |
| Existing standalone draft thread | One message, `DRAFT`, no corresponding source conversation | One message, `DRAFT`, no corresponding source conversation |
| Original conversation contains the draft | NO | NO |
| Draft carries reply-style subject header | NO (independent subject) | NO (independent subject) |
| Draft has an Ea-authored signature | NO evidence | NO evidence |
| Draft attachment summary | Zero | Zero |
| Current Gmail draft-summary `From` | Not populated | Not populated |
| Explicit send-as alias selection in connector create/update API | UNAVAILABLE | UNAVAILABLE |
| Exact overlap between current draft primary recipient and latest original inbound's reply mailbox | **MATCH — per-message Gmail `read_email(reply_detail=true)`** | **NO MATCH — per-message Gmail `read_email(reply_detail=true)`** |
| Primary recipient overlap with historical sender/reply mailboxes | Not needed for latest authoritative Reply-To; latest match confirmed | Historical per-message Reply-To not yet exhaustively compared; latest authoritative Reply-To mismatched |
| Latest source inbound CC recipients | None | Two |
| Draft CC matches latest source CC | No CC expected on latest inbound | None of the two matched; present draft has one CC |
| Can be independently marked send-ready | NO | NO |

**Resolved C2-A mailbox observation:** A first thread-summary read returned blank `from` and no `reply_recipients`, so an attempted mailbox comparison falsely appeared to indicate a mismatch. Subsequent **single-message `read_email(reply_detail=true)`** returned the original authoritative reply mailbox and it exactly matched C2-A's draft primary recipient (one of one). This confirms the destination for a response to the latest inbound, agreeing with the earlier watch summary; it **does not** fix the detached thread, verify the sender-alias or independently approve the technical text. The initial absence-of-overlap statement is superseded, not silently treated as real mismatch.

**C2-B recipient classification:** A single-message `read_email(reply_detail=true)` of the latest inbound provided its authoritative reply mailbox, which does **not** match C2-B's primary recipient. It also returned two source CC addresses, neither of which matches the draft's single CC. `DRAFT_QA_FAILED_WRONG_RECIPIENT_UNTHREADED` remains appropriate. Do not copy a third party on technical formulation disclosures without verifying relevance and authorization.

## 2. Connector capability decision

- `update_draft` supports changing existing draft body/To/CC/subject, but exposes **no `thread_id` or `reply_message_id` parameter**. Thus there is no documented/verified in-place reparent/rethread operation.
- `create_draft` supports an actual source message ID as `reply_message_id`, but it would create a **second** draft while the old detached one exists.
- The connector schema reviewed has no explicit `From`/send-as alias selector. Account profile verifies account access, **not** arbitrary author/sender persona.
- No safe atomic `move existing draft to correct thread`/replace old draft is established. A delete-then-create pair can lose user-authored content, create a duplicate, and/or trigger the 03D manual deletion suppression. **Do not run such a sequence without a separately verified protocol and exact operator action.**
- Any customer Gmail draft or Calendar change would require independently approved case-level scope; outbound email, file sharing, meeting invitation and external commitments remain prohibited absent separate authorization.
- In particular, the Espen-author alias rule (chat-only manual Outlook) must never be defeated through an NTSN Gmail draft.

**C2 write decision:** `NO_GO`. Do not update, rethread, delete, recreate, send or relabel either existing draft based on current evidence. Their verified CRM dispositions from the preceding session remain source-supported, and should not be prematurely promoted to `READY`.

## 3. Additional draft-inventory regression observed

A previous complete business Gmail draft listing returned **four** unsent drafts; the new bounded listing returned **two** (both C2 cases), with no next page. One previous in-thread customer draft is no longer present in its source thread, and one previously observed standalone vendor draft thread could not be fetched.

**No positive evidence proves why these objects disappeared.** Do not call this a user deletion, send, connector failure or silent cleanup. Treat as `DRAFT_DISAPPEARED_CAUSE_UNVERIFIED / DO_NOT_RECREATE_AUTOMATICALLY`; inspect original thread, SENT state, account and operator suppression signal before proposing any new draft. A missing draft *alone* does not satisfy 03D's known-manual-deletion criterion.

## 4. Candidate operator-controlled resolution (NOT EXECUTED)

| Gate | Required decision/evidence | On failure |
| --- | --- | --- |
| Identity | For each named case, exact author persona and Gmail/Outlook account verified by operator | `SENDER_ALIAS_UNVERIFIED` |
| Recipients | Intended To, relevant authorized CC, Reply-To and partner confidentiality verified against latest original conversation | `RECIPIENT_AUTHORITY_PENDING_REVIEW` |
| Draft ownership and preservation | Existing two unsent draft objects still present; source/attachments/approved text verified, deletion policy checked | `DRAFT_IDEMPOTENCY_HOLD` |
| Safe user action | Authorized operator opens **original** conversation in the appropriate mail client, manually constructs a true in-thread reply draft and verifies intended recipients and sender. Existing detached drafts remain preserved until operator makes an explicit, separate decision about cleanup | No new connector-created duplicate draft |
| Post-action QA | Verify new draft `DRAFT`, source thread, From, To/CC, body, no manual signature, attachments; reconcile old draft without assuming operator deletion | `DRAFT_QA_FAILED`, no send |
| Audit and closure | Add private evidence pointer and case disposition only after successful provider readback | `PENDING_REVIEW` |

**Consent required before any canary mutation:** The operator must identify **which** case (C2-A, C2-B, or both), the intended sender identity/account, the permitted action (in-place field correction, manual in-thread creation and optional later cleanup), and whether any existing draft may be deleted. A generic continuation instruction or GitHub PR merge does not grant this.

## 5. Non-production acceptance status

| Requirement | Status |
| --- | --- |
| PR #104 merged (source gate) | VERIFIED — commit `d6af79cceba6f11167b22a76a4ba9cddc1332fb4` |
| Both original conversations read in full | PASS |
| Detached draft presence and no Ea-authored signatures | PASS |
| Exact source-thread, recipient, sender and no-duplication canary gates | FAIL/BLOCKED |
| Safe native rethread mutation available | NO |
| C2 provider mutation / sender verification / postwrite readback | NOT EXECUTED |
| Historical Calendar reminder cleanup | NOT EXECUTED — separate scope; past events |
| Existing CRM draft-QA corrections | PRESERVED |
| 100-case/14-day production acceptance | NOT MET |
| Level 2B/C, Azure managed backend and production cutover | HOLD |

**Disposition:** `M5_C2_READ_ONLY_PREFLIGHT_COMPLETE / LIVE_GMAIL_WRITE_NO_GO / MANUAL_SENDER_AND_DRAFT_SCOPE_AUTHORIZATION_REQUIRED`.

## Per-message Reply-To verification addendum (same read-only session)

**Why the correction matters:** Bulk Gmail `read_email_thread` returned original inbound message bodies but blank `from` and `reply_recipients` for all inspected inbound messages. Consequently the first source-recipient comparison lacked valid expected mailbox values; zero overlap was an artifact of absent source metadata. It could not be used to call C2-A's actual recipient wrong.

A subsequent `read_email(message_id,reply_detail=true)` on each case's latest source inbound returned authoritative `reply_recipients` and CC fields. It verified C2-A `To` as correct (1/1 match), and C2-B `To` as wrong (0/1 match) with no overlap against the two relevant CC addresses (0/1 draft CC match). The corrected table above now reflects this evidence. **No Gmail mutation** occurred, and `C2_WRITE_NO_GO` remains unchanged due to lack of in-place rethread capability, sender-alias proof, case-specific consent and approved duplicate-handling sequence.
