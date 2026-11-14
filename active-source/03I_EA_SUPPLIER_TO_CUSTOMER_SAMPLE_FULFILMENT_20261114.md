# 03I — Ea Supplier-to-Customer Sample Fulfilment Workflow — 14:15, 14.11.2026

**Status:** OPERATOR-APPROVED / CANONICAL for Level 1 and controlled INTERNAL Level 2A workflows.  
**Authority:** Explicit operator instruction 14 November 2026.  
**Scope:** Supplier/manufacturer → intermediary/brand owner → NTSN → customer, including sample bottles, dropship consignments, PDF labels, cost estimates, production/LOT information and downstream customer correspondence.  
**Not authorized:** autonomous external send, forwarding of third-party documents, dispatch/release of goods, commercial guarantees, regulatory/label approval, Level 2B/C activation, new unattended mail-routing or resumption of disabled tasks.

## Case trigger and preflight
When a business customer requests product samples, quotes, labels or delivery, or a supplier replies with fulfilment information:
1. Retrieve latest current APPROVED/CANONICAL Ea, project and product rules. Apply 03C historical sent-context, 03D recipient-level deleted-draft suppression, 03F clean one-draft/no-signature handling, 03A/03B private calendar conventions, and 07B idempotency and readback.
2. Read the FULL current and relevant upstream/downstream Gmail threads, SENT replies, existing DRAFTs and relevant attachments; search other accessible accounts only when warranted and authorized. Confirm which entity is manufacturer, formulator, brand owner, intermediary, reseller, payer, consignee or customer; do not silently combine roles.
3. Resolve the latest verified customer shipping/contact address and requested product, formulation, sample size, quantity and delivery timing from original evidence. If a quote, PO, supplier order or customer request disagrees, separate allocations and classify PENDING_REVIEW; never silently shift extra stock into a customer consignment.
4. Check status and exact product variants of sample requests (for example hard surface versus textile) separately. Add optional additional samples only if the recipient actually requested or accepted them; ask supplier for availability and sample size, not an unapproved order.
5. Resolve any commercial release, payment, export, dangerous-goods, SDS, REACH/CLP/BPR or labeling dependencies via the proper qualified approval process. Invoices, invoice due dates, payments and customs remain OUT of Calendar follow-up scope.

## Supplier-side correspondence and evidence
6. Reconcile the existing manufacturer thread and draft. Create exactly ONE clean in-thread supplier reply where genuinely replying; otherwise use a new descriptive subject for a distinct order or shipping quotation. Preserve verified business sender identity, intended To/CC and native reply threading where relevant. Never write Gmail signature, quoted email history or legal disclaimers into outgoing body. Do not send.
7. Request written confirmation of:
   - the exact shipment allocation, quantity, bottle size, pack count and any separate products or samples;
   - destination and freight estimate, proposed transport mode and delivery lead time;
   - availability/ready date, estimated dispatch date and delivery estimate, distinguishing assumptions from commitments;
   - freight, packing, handling, customs-document, surcharges, transport restrictions and any other applicable charges, with currency and whether taxes are included;
   - current product-specific LOT/batch number(s), or when assigned, for each variant; where needed, manufacturing/expiry or best-before information must be obtained from the correct responsible party;
   - the approved PDF label artwork, print format/quantity and packing-list needs, which NTSN will supply when final and appropriate.
8. Explicitly state "quotation/planning only; do not dispatch until shipping instructions and compliant labels are confirmed" where dispatch is not already authorized. Do not state that PDFs are attached unless the exact versions are attached and verified. Do not infer regulatory label compliance merely because artwork exists.
9. If third-party manufacturer correspondence indicates a different batch quantity than the customer request, ask which units belong to which shipment; do not incorporate an unrelated allocation into the customer freight estimate.

## Incoming supplier response → downstream draft
10. On a VERIFIED new supplier response, read entire supplier thread and relevant downstream correspondence again. Update per-case status from WAITING_SUPPLIER to supplier-confirmed facts, PARTIAL_REPLY/QUESTIONS_OPEN or READY_FOR_OPERATOR_REVIEW. Check quoted freight and fees, LOT/product mapping, label readiness, dispatch condition and any changed allocation.
11. Draft the appropriate short customer-side reply in the customer's established language and tone, with confirmed logistics only. Clearly label estimates and outstanding dependencies; do not disclose upstream confidential prices, third-party agreements, or unrelated correspondence. If manufacturer still owes details, prepare an in-thread supplier follow-up instead. Never auto-send any draft.
12. Preserve the supplier and customer as separate Gmail threads; do not forward privileged correspondence to bridge them. Reconcile exactly one draft per actionable thread; use readback to verify To, CC, subject, body, DRAFT label, attachments, no signature, no copied quotation and stable draft ID.
13. Reconcile the existing case with the CRM/follow-up register and the private calendar; one active 15-minute solo transparent private Calendar follow-up per genuine next action, standard urgency colors, Europe/Oslo, no attendees, no conference, no reminders. Exclude invoice/payment/billing/Altinn/customs follow-ups and never recreate removed calendar routines.
14. Record one minimized workstream ID with append-only actions, source revisions, provider IDs, idempotency key, before/after, verified result, blockers and open actions. Store private customer/order particulars only in approved restricted systems. Only a redacted generic rule may be published publicly. Approved derived Drive session pointers reference the single canonical GitHub ledger, not a duplicate ledger.

## Automatic processing / execution boundary
- Apply this lifecycle opportunistically within currently ENABLED and approved Ea business lead/email-monitoring tasks. The presence of this file DOES NOT enable or resume a disabled native automation, activate a background backend, provide Gmail push/webhook coverage or guarantee continuous monitoring.
- A scheduled task may read, classify, reconcile, prepare or update an authorized unsent draft and an internal private follow-up within granted scopes. Keep source freshness, recipient-level 03D suppression, existing drafts, verified send-as identity, per-case idempotency, and failure isolation. If tools/permissions are unavailable, record NOT_VERIFIED or WRITE_FAILED and notify operator once on material state change.
- No external send/forward, customer-facing legal/regulatory/commercial commitment, supplier production release, shipping instruction, file share or autonomous Level 2B/C transition follows from a schedule or from operator approval of this internal protocol.

## Acceptance and regression checks
1. Reconstruct the full multi-party chain from original correspondence; verify address and conditional sample type, detect any quantity/allocation disagreement.
2. Draft identity and body pass 03D/03F; Gmail saved draft remains DRAFT and is not duplicate or SENT.
3. Manufacturer LOT, transport/handling costs, delivery ETA, labels and shipment release are marked as CONFIRMED only after source evidence; missing details stay open.
4. Calendar reuses an existing case where appropriate and has correct 15-minute time, color, private/transparent, no reminders/attendees/Meet; exclude payment/customs matters.
5. A new supplier reply triggers a source-reconciled downstream in-thread DRAFT only, not an external SEND.
6. Scheduled task active/paused state and each provider readback are verified independently; no claims of always-on automation without a successful observed run.
7. Public source contains no personal/customer payload or sensitive commercial/financial data; restricted workstream ledger and approved Drive pointer use redacted provenance.
