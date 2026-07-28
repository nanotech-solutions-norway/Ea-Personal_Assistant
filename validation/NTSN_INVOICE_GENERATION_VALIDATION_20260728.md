# NTSN Invoice Generation Validation — 28.07.2026

**Status:** VALIDATED FOR LEVEL 1 CONTROLLED DRAFTING  
**Classification:** AUTO_APPROVED operating validation  
**External issuance/posting:** NOT AUTHORIZED BY THIS RECORD

## Validation basis

The approved NTSN invoice workflow was validated against historical outgoing invoices issued by NanoTech Solutions Norway AS and named `Invoice15xxx` / `Faktura15xxx`.

Onyx Scandinavia invoices were excluded from the NTSN reference set.

A controlled Drive-only source-reference register was created for validated NTSN examples by language, currency, VAT pattern and layout relevance. Customer-specific invoice content remains outside GitHub.

No customer names, invoice PDFs, bank details, identifiable prices or accounting exports are included in this public validation record.

## Validated decisions

- NTSN-only historical reference set.
- Separate NTSN and Onyx invoice template families.
- English filename pattern: `Invoice15xxx`.
- Norwegian filename pattern: `Faktura15xxx`.
- Official invoice number source required.
- One-page A4 baseline.
- Logo upper left without overlap.
- Customer block left; seller/invoice metadata right.
- Full-width aligned item table.
- Aligned VAT, total and payment-information sections.
- Rendered PDF is the authoritative visual output.
- Official sending, issuing, posting and booking remain approval-controlled.

## Test record

| Test | Result |
|---|---|
| NTSN issuer/reference boundary | PASS |
| Onyx exclusion | PASS |
| Drive source-reference register | PASS |
| Filename/language convention | PASS |
| Invoice-number source control | PASS |
| Logo clearance | PASS |
| Header-block alignment | PASS |
| Item-column alignment | PASS |
| VAT/total presentation | PASS |
| Payment-information placement | PASS |
| One-page printable output | PASS |
| PDF visual inspection gate | PASS |
| Approval boundary | PASS |
| GitHub confidentiality boundary | PASS |

## Required future checks

Every future invoice draft must independently revalidate:

- source quote/order/PO;
- invoice number;
- dates and due date;
- customer legal information;
- currency and calculations;
- VAT treatment;
- payment information;
- page geometry and logo clearance;
- filename/language;
- approval state.

## Limitations

This validation does not provide legal, tax, accounting, customs or regulatory approval. Unclear or conflicting treatment must be classified `PENDING_REVIEW` and escalated to qualified review.

Domestic 25% MVA accounting evidence was identified, but the corresponding invoice PDF was not located in the reviewed Drive results. That reference remains secondary and `PENDING_REVIEW` for visual-template use.

Level 2 accounting write-back remains HOLD.
