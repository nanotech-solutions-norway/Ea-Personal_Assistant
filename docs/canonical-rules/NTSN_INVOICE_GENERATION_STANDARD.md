# NTSN Invoice Generation Standard

**Status:** USER_APPROVED / ACTIVE OPERATING STANDARD  
**Classification:** AUTO_APPROVED operating logic  
**Approved:** 28.07.2026  
**Scope:** NanoTech Solutions Norway AS outgoing invoice drafting  
**Level 2 accounting write-back:** HOLD

## Purpose

Define the approved source, layout, calculation, VAT, validation, storage and approval controls for invoice drafts prepared for NanoTech Solutions Norway AS.

This file contains sanitized operating logic only. It must not contain customer names, invoice PDFs, identifiable prices, bank details, accounting exports, credentials or confidential attachments.

## Reference-source boundary

1. Use only invoices issued by NanoTech Solutions Norway AS as visual and structural references.
2. Use `Invoice15xxx` files for English invoice references.
3. Use `Faktura15xxx` files for Norwegian invoice references.
4. Exclude Onyx Scandinavia invoices from the NTSN reference set.
5. Retrieve official invoice numbers from the accounting/invoice register or explicit user instruction. Do not infer them from draft filenames.

## Source-authority order

1. Current explicit user instruction.
2. Approved quote, order, PO, delivery instruction or commercial source.
3. Official accounting/invoice register.
4. Latest comparable NTSN invoice.
5. Sent Gmail invoice attachment.
6. Historical drafts and chat outputs as supporting evidence only.

Conflicting dates, prices, currencies, VAT treatment, addresses, payment terms or references must be marked `PENDING_REVIEW`.

## Layout standard

- One-page A4 unless invoice-line volume requires a longer document.
- Logo upper left and scaled proportionally.
- No logo overlap with customer, seller, metadata or line-item text.
- Customer block left.
- Seller and invoice metadata block right.
- Invoice title aligned with the right-hand metadata block.
- Full-width item table.
- Vertically aligned description, price, quantity, discount, VAT and amount columns.
- VAT summary and total due aligned with the item table.
- Payment information positioned in the lower page area.
- Footer and page numbering kept inside the printable area.

The rendered PDF is the authoritative visual output. DOCX is an editable working copy and must be re-rendered before approval.

## Content controls

Confirm and include where applicable:

- customer legal identity and billing address;
- organization/VAT/EORI reference;
- customer and internal references;
- delivery and invoice dates;
- due date;
- invoice number;
- currency;
- quote/PO/order reference;
- payment terms;
- carrier and Incoterms®;
- product/service description;
- quantity and unit;
- unit price and discount;
- VAT rate and basis;
- line amounts, net amount, VAT and total due;
- approved NTSN payment information.

Use canonical product terminology, including SiO₂/TiO₂, Hirec-R, Hirec PFW9 and Hirec PFS10.

## Calculation controls

- Use only approved price and discount sources.
- Recalculate every line, subtotal, VAT amount and total.
- Use consistent language/currency number formatting.
- Record quote-to-invoice mismatches as `PENDING_REVIEW`.
- Include NOK VAT basis on foreign-currency invoices only when supported by the applicable NTSN convention or accounting requirement.

## VAT and export controls

- Domestic Norwegian invoices show only the confirmed applicable MVA rate.
- Cross-border VAT treatment must be source-supported.
- Do not assume export 0% solely from customer location.
- Unclear VAT, tax, customs or accounting treatment requires qualified review.

## Payment-information control

Use the latest approved NanoTech Solutions Norway AS invoice or official accounting source. Never copy payment information from an Onyx Scandinavia invoice.

## Visual QA gate

Before delivery of an invoice draft:

1. Render the PDF.
2. Compare against at least one recent comparable NTSN invoice.
3. Verify logo clearance.
4. Verify customer/seller block alignment.
5. Verify invoice metadata alignment.
6. Verify item-column alignment.
7. Recalculate totals.
8. Verify VAT presentation.
9. Verify invoice date, due date and number.
10. Verify payment information.
11. Verify page count and printable-area fit.
12. Remove draft watermarks and unintended placeholders.
13. Verify filename/language convention.

## Approval boundary

Allowed at Level 1:

- search and compare invoice evidence;
- extract approved specifications;
- calculate totals;
- prepare PDF/DOCX drafts;
- record validation and source references.

Explicit approval and approved capability are required before:

- sending or sharing an invoice;
- issuing, posting or booking an invoice;
- changing official invoice numbers;
- creating VAT, payment or ledger entries;
- moving customer invoices outside controlled storage.

## Storage boundary

- Customer-specific invoice evidence stays in controlled Drive/accounting storage.
- GitHub stores only sanitized operating logic and validation criteria.
- Historical evidence must not be silently overwritten or deleted.
