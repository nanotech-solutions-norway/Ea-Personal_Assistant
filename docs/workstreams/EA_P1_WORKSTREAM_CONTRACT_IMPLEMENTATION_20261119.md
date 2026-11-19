# Ea Workstream P1 — Shared Contracts & Synthetic Validation — 19.11.2026

**Classification:** PENDING_REVIEW / IMPLEMENTED_IN_REPO / NOT_CANONICAL / NOT_DEPLOYED  
**Owner:** Ea Personal Assistant / NTSN  
**Work ID:** EA-WORKSTREAM-P1-20261119-01  
**Input:** Private ai-memory-ops [PR #169](https://github.com/nanotech-solutions-norway/ai-memory-ops/pull/169) and its merged workstream mapping.  
**Non-effects:** No business account emails or drafts, live registers, Drive files, Calendar, runtime task configurations, accounting, supplier orders, shipments or access permissions were modified by this P1 implementation.

## 1. P1 scope and result

Create a reusable and testable **contract** for how source changes become one case, one workstream instance, one internal artifact plan and one next decision. The package consists of `workstreams/p1/engine.py`, `contracts.json`, unit tests, and a PR-triggered synthetic check. No provider adapter is attached and no managed queue or persistent database is created.

This is narrower than P2. It gives the existing enabled Ea routines a shared vocabulary without changing their schedule or launching new workers. Source-of-truth ownership and full crosswalk migration are **proposals requiring review**, not silent changes to CRM, Order Book or Calendar.

## 2. Exact identity, no false consolidation

Link an existing case by exact approved source keys: case ID, CRM Lead ID, CRM Opportunity ID, Order Book Case ID, mailbox-qualified Gmail thread ID, form response ID, reference-numbered quote/customer PO or shipment ID. Preserve buyer vs payer vs reseller vs brand owner vs manufacturer vs technical user vs consignee roles.

An exact match returns the existing case ID. No match returns NEW_CANDIDATE_REVIEW, not authorization to create. If separate records match conflicting identifiers, the result is AMBIGUOUS_CASE or CONFLICTING_CASE_IDENTIFIERS, with no mutation. Company-name similarity, message-subject similarity and common product use are NEVER sufficient to merge records. Multiple product opportunities for the same account remain separate.

Stable event key: SHA-256 digest over mailbox ID, source message ID, event type and existing case ID. The identifier is for deduplication within the approved destination; it does not replace the underlying Gmail message ID. Existing business event logs and redacted operational ledgers remain distinct artifacts.

## 3. Field ownership crosswalk — current proposed disposition

| Domain | Proposed authority | Projection/outbound boundary |
| --- | --- | --- |
| Leads, Accounts/Contacts, Opportunities, Activities | CRM Master Register, exact native tab/record ID | Existing Ea Lead Changes scope, no unapproved bulk edits |
| Business drafts and sent evidence | Gmail mailbox + thread + message/draft ID | 07B/03F; 03D suppression; no send |
| Customer master details | Ea Customer Register (provisional for its own customer-specific fields) | Conflict/duplicate handling with CRM Accounts is PENDING_REVIEW |
| Orders, production, logistics | Commercial Order Book Order_Book, Production_Tracker, Shipment_Legs | Existing Order Book Sync's approved field list only |
| Document references and case linkage | Commercial Order Book Document_Index; real source file in Google Drive | No asserted attachment without provider readback |
| Separate Shipment Register | Existing Shipments tab | **Ownership ambiguity:** designate primary vs projection before dual writes |
| Follow-up actions and actual events | CRM Follow_Ups / Google Calendar events | Calendar is authority for booked time; internal follow-ups no reminders |
| Product source truth | Latest scope-specific approved original Drive documents and product governance | Historical/GitHub metadata are not new approvals; qualified review still required |
| Quotes and documents | Current 05B/05C/05D, approved quote workflow, Google Drive company folder | Reference/version immutable, independent render/field QA, operator before issue |
| Invoices/payment | Approved external accounting source | R4 human-only; no autonomous posting or payment; no invoice/payment/calendar follow-up |

Actual header names were refreshed read-only on 19.11.2026 from the native CRM/Order Book and Shipment Register; the JSON contract references existing tabs and identifiers. No field ownership is promoted to APPROVED by this file.

## 4. Shared reusable modules

- **Case correlation:** exact stable source identity; anonymous candidate or ambiguous match is review-only.
- **Evidence manifest/source gate:** exact formulation, application, jurisdiction, revision, approval and recipient fitness; a newer unapproved source cannot override approved truth.
- **Correspondence context:** require full relevant current Gmail thread, SENT precedent and valid sender/reply anchor before draft.
- **Document/reference QA:** PDF basename, printed quote reference and email reference must agree per current 05D; price and arithmetic are separately gated.
- **Attachment QA:** selected file IDs, names, versions, fingerprints, actual observed draft attachments and recipient suitability must match.
- **Operator gate:** /Button select VERIFY/PREPARE/HOLD with independent optional operator input; text does not grant approval. External SEND/ISSUE/PO dispatch remain separate.
- **Projection preflight:** correct system field owner, verified source/before-target read, idempotency and prewrite operational logging before any proposed internal write.

These are pure deterministic test functions and non-executing plans. They do not perform actual Gmail draft composition or document rendering.

## 5. End-to-end stage test A: inbound lead → draft

**Synthetic trigger:** NEW_LEAD (a valid mailbox-qualified thread with a source message ID).

1. Match or review existing case; do not duplicate Lead or Account.
2. Check current email + SENT history, operator draft suppression, sender/alias and correct reply anchor.
3. Select exact approved product/version and safe attachments; unresolved technical/safety claims block.
4. Produce an internal plan to prepare exactly one in-thread **unsent** Gmail draft.
5. Require independent Gmail readback of To/CC/thread/body, zero added signature and actual attachments; only then CRM activity projection in approved scope.
6. Case can remain AWAITING_OPERATOR_APPROVAL after DRAFT_VERIFIED. No external send action is created by the plan.

**P1 synthetic acceptance:** valid evidence yields INTERNAL_PLAN_READY with only PREPARE_IN_THREAD_UNSENT_DRAFT, VERIFY_GMAIL_DRAFT, PROPOSE_CRM_ACTIVITY_PROJECTION; wrong alias, stale thread, missing approval, 03D recipient suppression and sender-specific Outlook case block appropriately.

## 6. End-to-end stage test B: RFQ → quote + draft

**Synthetic trigger:** RFQ_RECEIVED, linked to same case identity when exact identifiers agree.

1. Reuse case context, verify exact variant, requested unit/quantity and legal buyer.
2. Reconcile source price, logistics, tax and currency; do not equate historical quote with current customer commercial authorization.
3. Prepare quote via controlling canonical template and 05D reference-only filename.
4. Validate independent item and total arithmetic, PDF A4 layout and email-reference equality.
5. Prepare one unsent in-thread email; verify the **actual** attachment list and reference.
6. Propose restricted CRM/Order Book projections only if ownership and readback gates pass.
7. Keep customer quote issue/send status awaiting explicit operator review and sender approval.

**P1 synthetic acceptance:** valid evidence yields INTERNAL_PLAN_READY and the internal quote/document/draft plan. Missing current price, arithmetic error, reference mismatch, unverified PDF or attached file produce BLOCKED_INTERNAL_PREPARATION.

## 7. Regression and approval gates

Tests cover exact/ambiguous case matching, company/domain not used as identity, conflicting strong keys, no duplicate new-case creation, reproducible event idempotency, scoped product approval, conflicting approved versions, recipient-specific attachment permission, stale versions, reference mismatch, Decimal arithmetic, lead and RFQ progression, supplier-price gaps, 03D suppression, Espen chat-only, sender alias/thread-anchor/staleness, existing attachment-bearing draft, unknown triggers, disallowed external actions, optional work-ID notes and source/owner/readback/ledger gates.

**Production promotion requirements:** (a) operator-approved field ownership and crosswalk, (b) scoped connector adapters with read-only P2 dry-run evidence, (c) current API capability review for existing Gmail drafts with attachments, (d) exact source/price/document QA including rendered PDF, (e) independent before/after provider readback, (f) full observed queue coverage and error recovery, (g) security/permission gate. Level 2B/C remain HOLD regardless of test success or merged PR.

## 8. Risk and open review decisions

1. Choose cross-workstream case-correlation authority (existing CRM IDs or new private transactional case state); do not auto-allocate universal IDs.
2. Resolve overlapping Customer Register/CRM Accounts and separate Shipment Register/Order Book Shipment_Legs field ownership.
3. Approve exact eligible CRM/Order Book write fields and who may update existing event logs under concurrent runs.
4. Confirm Gmail attachment-bearing draft replacement strategy; connector capabilities and provider saved-body evidence must be validated, not assumed.
5. Choose P2 synthetic/read-only pilot case coverage, after owner accepts the P1 contract; no real customer changes for design testing.
6. Confirm source-manifest conflict resolution for overlapping approved versioned TDS/SDS/price documents.
7. Establish operator approval receipt and expiry semantics if a future Level 2B program is separately promoted; current Level 2A stays internal.

## 9. Traceability

- Source owner: `active-source/12_EA_MASTER_INDEX.md` and the 07B, 03C, 03D, 03F, 05D, approved quote and Level 2 rules.
- Baseline: private `ai-memory-ops` PR #169 and merged 19.11.2026 architecture report.
- Synthetic package: `workstreams/p1/contracts.json`, `engine.py`, `tests/test_engine.py`.
- Automated quality: `.github/workflows/ea-p1-workstream-contract-tests.yml`.
- Redacted owning workstream audit: private `ai-memory-ops/sessions/2026-11-19_EA-WORKSTREAM-P1-20261119-01.md` (one ledger, no shadow ledger).
