# Ea P2 — Controlled Integration Read-Only Pilot — 12:54, 19.11.2026

**Classification:** VERIFIED_BOUNDED_SOURCE_RECONCILIATION / PENDING_REVIEW_CORRECTION / NO_LIVE_WRITES
**Owner:** Ea Personal Assistant, NanoTech Solutions Norway AS
**Work ID:** EA-WORKSTREAM-P2-20261119-01
**Runtime:** NOT_DEPLOYED / NO_NEW_AUTOMATION / NO_EXTERNAL_EXECUTION.

## 1. Mandate

Continue P1 (merged Ea PR #161, SHA 48bad5617a4999bbf7816d064a6ef532fe3ff53b) with a bounded read-only business-source pilot. Compare two representative case types against native Gmail, NTSN CRM Master Register and Commercial Order Book, plus Drive source authority; add a pure reconciliation function and synthetic regression tests. Do not mutate a live business record.

## 2. Actual bounded source reads

- GitHub Ea P1 main contracts/engine, 07B/03F/master-index governing rules; private ai-memory-ops Drive index and audit rules.
- Native NTSN CRM Master Register: spreadsheet metadata before exact Leads, Opportunities, Activities, Follow_Ups and Draft_Attachment_Gate read-only ranges.
- Native NTSN Commercial Order Book: metadata before Order_Book, Document_Index and Event_Log read-only ranges.
- Authorized Gmail: business mailbox SENT source and separate personal business-form intake for pilot A; a complete 25-message customer thread and a separate three-message supplier thread for pilot B. The current business draft listing and latest SENT attachment metadata were read independently.
- Google Drive AI-Memory-Vault and NTSN Drive business index read-only. Index is partial, non-live and does not establish document content or approval.

**Coverage:** Two selected cases and their relevant source paths only, not an exhaustive historical CRM/email backfill. Original sender identity, customer details, prices, message bodies and attachments are deliberately excluded from this public design report. A source timestamp must be timezone-aware for automated freshness comparison.

## 3. Pilot A — technical inquiry, customer reply already sent

**Verified:** A website-form business inquiry arrived in a separately authorized mailbox, followed by a NTSN business Gmail SENT technical-qualification response. Current Order Book Event_Log and Order_Book correctly indicate WAITING_EXTERNAL. The corresponding CRM Lead and Activity still call for an UNSENT reply and NTSN action. The Order Book contains a source-message pointer to the same original form, but lacks a typed CRM lead/opportunity link. An older unsent draft remains indexed as historical documentation.

**Read-only corrective findings:**
- CRM_DRAFT_STATE_STALE / CRM_ACTION_OWNER_STALE: re-evaluate current next actor from verified original Gmail SENT; do not generate a second customer draft.
- MISSING_TYPED_CASE_CROSSWALK: reconcile native CRM/Order IDs via exact source keys, not company spelling or product similarity.
- DOCUMENT_DRAFT_SUPERSEDED_REVIEW: preserve historical draft metadata but distinguish it from current SENT response; do not delete source history.
- TECHNICAL_SUITABILITY_UNVERIFIED: no anti-icing product suitability, flight safety or purchase recommendation without the qualified technical source.

No customer email, sample/quote, or Calendar follow-up was created by the pilot.

## 4. Pilot B — revised quotation after prior customer decline

**Verified:** A full customer thread records a prior quotation, an explicit decline of that earlier offer, and a later separately scoped quotation sent by NTSN with one PDF attachment. Gmail metadata confirms the attachment name/size, not its entire PDF content. CRM Opportunity/Follow_Up still describe an older unsent-draft stage. Order Book retains an older issued quote reference and an older Document_Index entry; the latest SENT quote version is absent from the bounded Document_Index scan. A supplier thread separately presents unresolved composition and SDS evidence conflict. The newest quote's product/unit scope differs from the earlier bulk inquiry and must be preserved as a distinct commercial revision.

**Read-only corrective findings:**
- CRM_SOURCE_POINTER_STALE / CRM_ACTION_OWNER_STALE: the older unsent description is superseded by actual SENT; verify no newer inbound before choosing next action.
- LATEST_QUOTE_NOT_DOCUMENT_INDEXED: propose an additional immutable Document_Index entry after exact file/reference verification. Do not overwrite the previous issued quote or assume the new offer is accepted.
- PRESERVE_OLDER_QUOTE_VERSION: the earlier customer decline and distinct later offer remain separate commercial events.
- QUOTE_ATTACHMENT_METADATA_ONLY: actual PDF contents, printed reference, amount, product quantity, document hash and released document classification are not independently verified in this P2 stage.
- QUOTATION_SCOPE_AND_PRODUCT_REVIEW: changing unit/volume and formulation/SDS source evidence must be reviewed by qualified commercial/technical owners before another commitment.

No quote, Gmail draft or supplier message was generated by this pilot.

## 5. P2 implemented components

- `workstreams/p2/read_only.py`: dataclasses for normalized provider metadata; typed finding codes; timezone-aware SENT/INBOUND comparison; CRM/Order case-link guard; old-versus-new immutable quote pointer test; attachment metadata limitation; bounded coverage; empty business writes/external actions.
- `workstreams/p2/tests/test_read_only.py`: 20 synthetic/nonconfidential tests for both scenarios, exact case ambiguity, source timestamps and labels, quote versions, no duplicate outputs, incomplete evidence, and mandatory read-only operation.
- `.github/workflows/ea-p2-readonly-reconciliation-tests.yml`: compile, P1 and P2 regression suite, and import-time disallowing of supported network/database/provider I/O modules.
- `workstreams/p2/README.md`: activation and safety boundaries.

The P2 code does not fetch any live provider record by itself; only authorized bounded provider reads made by Ea during this review supplied the findings. CI success cannot prove a deployed backend or complete all-case coverage.

## 6. Non-deployed integration design and ownership

- Existing Email Watch owns email classification and current in-thread draft state under 07B/03F/03D.
- Existing Lead Changes owns source-qualified CRM relationship/Lead/Opportunity/Activity updates under its current approved scope.
- Existing Order Book Sync owns bounded commercial state and Document_Index/prod/shipment updates under its current approved scope.
- Gmail remains authority for SENT/DRAFT and attachments, native Google Drive file versions for document storage, Google Calendar for booked events, and qualified accounting provider for invoices/payments.
- No extra writer, live shared queue or background orchestrator installed. All Level 2B/C activation remains HOLD.

Before any future internal corrected row: re-read latest Gmail thread and SENT, exact native row ID and source revision; verify field-owner authority, current approved template/source, stable idempotency, one owning work-ID write-ahead ledger, exact allowed cells, and independent after-write provider readback. The P2 recommendation itself is not authorization for those writes.

## 7. Remaining P2→P3 gates

1. Approve typed case ID crosswalk between the pilot CRM Lead and Order Book case without over-merging other account cases.
2. Independently verify the most recent quotation PDF bytes/printed ref/quantity and exact commercial source claims before documenting as QA-complete.
3. Decide who owns correction of stale CRM next-action and Event/Document Index pointers; preserve immutable history and current live scheduled task ownership.
4. Resolve separate Customer Register/CRM Accounts and Shipment Register/Order Book Shipment_Legs field ownership.
5. Verify current Gmail connector support for replacing attachments in existing drafts; never assert that draft attachment exists absent saved-state provider evidence.
6. Establish a durable per-case coverage window/checkpoint and readback so a bounded scheduled run cannot claim complete enterprise reconciliation.
7. Use exact /Button select per-work-ID options and optional notes for future remediation; notes are not authorization to send.
8. No external sending, supplier PO release, approved quote issue, legal/regulatory product claims, financial posting or permissions changes without the appropriate separate approval.

## 8. Traceability

- Source: `Ea-Personal_Assistant/active-source/12_EA_MASTER_INDEX.md`@d3cd16d2a3e12326ece2f776ea5cfa123db736e9; 07B@85691ccfe575ec1c4231bad8f5c5b023fffaa721; 03F@c40ad6581b1ffb8c25861eb36fc8d7160b0d0725; `ai-memory-ops` event protocol@0171fa4518ddfffef4c05254893da2bfe04ee9ac.
- P1 merged PR #161 and private architecture PR #169.
- NTSN Drive index README@fb2d2be6c6cdf9aa970949aa42d2931860f2d690 and CSV@6a178e6005079c105005c7d04056c8d89d6995be. Live CRM/Order metadata and bounded row and source-message reads performed on 19.11.2026.
- Private redacted work-ID ledger: `nanotech-solutions-norway/ai-memory-ops/sessions/2026-11-19_EA-WORKSTREAM-P2-20261119-01.md`.

This review does **not** constitute a complete all-project workstream inventory, live integration deployment, audited quotation issue, product regulatory approval or full historical source backfill.
