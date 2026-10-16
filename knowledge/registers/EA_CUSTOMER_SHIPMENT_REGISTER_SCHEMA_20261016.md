# Ea Customer and Shipment Registers — Operating Schema

Status: DRAFT / PENDING_REVIEW | 16 October 2026
Classification: PUBLIC SCHEMA ONLY. NO CUSTOMER, FINANCIAL OR TRACKING DATA.

## Canonical source policy
- The restricted Google Sheets CRM Master is the account, contact, opportunity and follow-up source. Do not duplicate legal entities or silently merge subsidiaries.
- Restricted operational customer/shipment rows belong in access-controlled Google Sheets, not this PUBLIC repository.
- Only schema, validation policies, non-sensitive aggregate metrics, and code may be committed to GitHub.
- Customer IDs and shipment IDs must be stable and cross-referenced; legacy/source naming may be retained in evidence but customer-facing product fields must use Ea canonical product names.
- Customer vs supplier vs intermediary are distinct roles. One shipment may contain multiple legs, consignees, and documentation states.
- Proposed quotation, invoiced sample, booked label, shipped carrier event, customer receipt, customs clearance, and end-recipient acceptance are distinct statuses.
- Each material row requires source references, confidence, last verified date, owner, confidentiality classification, exception and review status.
- Source conflicts are PENDING_REVIEW, not automatically resolved.
- No unattended polling, autonomous booking, external sending, customs/legal conclusions, or sensitive GitHub writeback is authorized.

## Customer fields
Customer ID; organization; entity role; relationship state; contact; canonical product/application; owner; last evidence; next action; due date; entity hierarchy; CRM lead ID; source evidence; confidence; review state.

## Shipment fields
Shipment ID; customer ID; ordering and receiving entity; PO; canonical goods; quantity and unit; shipper; carrier; tracking source; dispatch date; receipt date; state; documents/customs; exception/action; evidence; verification.

## Acceptance checklist
1. Unique identities and foreign-key integrity.
2. Distinguish confirmed customer accounts from unqualified leads and suppliers.
3. Distinguish quotations and purchase orders from shipments.
4. Verify customer-confirmed receipt separately from carrier event.
5. Check whether personal mailbox messages are relevant business correspondence without forwarding or storing unrelated personal material.
6. No bank, accounting, pricing, customer-contact, shipment-tracking or confidential attachments in public GitHub.
7. Private register existence and readback verified.
8. End-to-end four-year backfill and cross-source deduplication NOT YET CERTIFIED.

## Account normalization update (16 October 2026)
- Use one legal-entity record per invoicing party, receiving company and any corporate parent, even where a relationship is within one group.
- Group affiliation is recorded as a relationship; not consent to reassign invoice entity, bank details, shipment consignee or commercial obligation.
- For overlaps, preserve verified dated operational evidence, exact known legal identifiers and existing CRM linkage. No source CSV line dates means no automatic latest-by-date resolution.
- Source-only customer candidates remain distinct from confirmed accounts until a legal-identity key is matched; do not invent merges or invoice-recipient authority.
- Redaction boundary remains mandatory for public GitHub; all commercial rows live in restricted Google Drive.
