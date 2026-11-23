# Ea P1 — Shared Workstream Contracts (synthetic-only)

**Status:** IMPLEMENTED_IN_REPO / PENDING_REVIEW / NOT_DEPLOYED / NOT_CANONICAL  
**Owner:** Ea Personal Assistant — NanoTech Solutions Norway AS  
**Scope:** Shared case identity, event idempotency, source/attachment review, internal-only planning, field ownership and synthetic regression tests.  

This package implements the **P1 contract and testing groundwork**, not a production mail-processing agent or a managed backend. It never calls Gmail, Drive, Calendar, GitHub, CRM or accounting systems. It never sends, drafts, files, edits, deletes, or approves external objects. No change to existing Level 2A permissions, Level 2B/2C holds, 07B active email task, Lead Changes or Order Book Sync.

## Files

- `contracts.json` — proposed field/data ownership and two versioned commercial workstream contracts.
- `engine.py` — standard-library-only pure functions to perform exact case correlation, source version conflict checks, attachment comparison, quotation reference/arithmetic checks, deterministic internal plan and projection preflight.
- `tests/test_engine.py` — synthetic, nonconfidential regression fixtures.
- `.github/workflows/ea-p1-workstream-contract-tests.yml` — pull-request CI; standard library, no credentials required.
- `docs/workstreams/EA_P1_WORKSTREAM_CONTRACT_IMPLEMENTATION_20261119.md` — full implementation design and promotion gates.

## Source precedence

1. Current explicit operator instruction and applicable legal/provider rights.
2. Owning-project latest verified APPROVED/CANONICAL Ea rules: 03A/B/C/D/F, 05A/B/C/D, approved quotation workflow, 03I, 07B and Level 2 restrictions.
3. Verified current Gmail/CRM/Order Book/Drive/Calendar source state as evidence.
4. Historical correspondence as context, not override.

Reference architecture: [private ai-memory-ops PR #169](https://github.com/nanotech-solutions-norway/ai-memory-ops/pull/169) merged 19 November 2026. Its proposal designation is not promoted by the merge. Never interpret this README, green tests, or GitHub merge as permission to deploy or send.

## Two bounded contracts

`EA.COM.INQUIRY_TO_REPLY.v0.1`: case match → full current thread and historical SENT → product/authority fit → single correct-channel unsent draft → actual attachment and draft readback → authorized CRM projection → operator decision before external communication.

`EA.COM.RFQ_TO_QUOTE_DRAFT.v0.1`: reuse case → exact customer RFQ, legal roles, product/quantity → commercial source/price check → canonical quotation/05D reference, PDF and independent arithmetic QA → matching email draft and PDF attachment → verified CRM/Order Book source event projections → explicit content and commercial approval before any issue/send.

An internal plan marked `INTERNAL_PLAN_READY` is **not** a completed provider draft/quotation. `PREPARE_*` action names describe nonexecuting intentions. A real `DRAFT_VERIFIED` or `QUOTE_AND_DRAFT_VERIFIED` state requires independent provider readback outside this package and authorized connector writes.

## Case and source safety

Exact immutable source identifiers only (account+thread, message, CRM lead/opportunity, Order Book case, form response, quotation or PO reference). Similar names, subjects, domains or product descriptions never merge cases. Cross-key conflict, missing source, unapproved technical file, inconsistent references, stale attachment, unsupported price and wrong writer all block.

No automatic source-claim promotion. Revisions are not approved merely because newer. SiO₂/TiO₂ and product formulation boundaries remain distinct. Known manually deleted Gmail drafts are recipient-suppressed under 03D; Espen Olsen remains Outlook chat-only under 03F; no Ea-authored Gmail signatures and no upstream manufacturer disclosure in customer-facing drafts.

## Deterministic dispatch ownership — proposed, not installed

- Email Watch: classify communication and own single Gmail draft state under current 07B/03F.
- Lead Changes: own CRM relationship/lead/opportunity writeback under current approved CRM scope.
- Order Book Sync: own Order_Book and Document_Index/Production_Tracker/Shipment_Legs under current approved scope.
- Calendar: only genuine private no-reminder internal follow-ups and confirmed meeting controls.
- Accounting: exclusively controls invoices/posting/payments; CRM/Order Book link verified status only.

Do not add a fourth concurrent writer before case queue/field ownership and connector idempotency are approved, installed and validated.

## Run tests (local or CI)

```sh
python -m unittest discover -s workstreams/p1/tests -p 'test_*.py' -v
```

These tests prove only the behavior of synthetic pure functions and JSON contract shape. They cannot prove mailbox state, attachment bytes, registered external permissions, durable storage, scheduling reliability, production readiness, legal/regulatory clearance, or integration deployment.

## Next gated stage

P2 requires an explicit scoped decision on crosswalk/owner mapping, a measured read-only test cohort, action-level write permissions, evidence freshness and approval handling for Gmail attachment-bearing drafts. Any live Level 2A pilot requires before/after provider readback, one canonical redacted work-ID ledger and regression test acceptance. Level 2B/C external execution remains HOLD.
