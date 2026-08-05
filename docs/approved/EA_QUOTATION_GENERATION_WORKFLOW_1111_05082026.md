# Ea Quotation Generation Workflow — 11:11, 05.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Quotations / Google Drive / Gmail  
**Scope:** QUOTATIONS ONLY

## 1. Mandatory separation from invoices

Quotation generation and invoice generation are separate workflows.

When drafting or correcting a quotation:

- use only the quotation workbook, quotation PDFs and quotation records;
- use only the `Quote` sheet from the current quotation workbook;
- do not use invoice templates, invoice workbooks, invoice numbering, invoice status fields, due-date blocks, invoice VAT layouts or invoice filing rules;
- do not convert a quotation task into an invoice task;
- do not create, update or attach an invoice unless the operator separately instructs and approves the invoice action;
- ignore non-quotation sheets such as packing-list, product-maintenance, customer-import and other administrative sheets except when they are required to populate the quotation workbook itself.

## 2. Controlling source hierarchy

Use the following sources in order:

1. Current explicit operator instruction.
2. This canonical quotation-generation workflow.
3. The current `Quote - v5.31.xlsm` quotation workbook and its `Quote` sheet.
4. Recent `RAW - [quotation reference].xlsx` quotation workbooks.
5. Recent approved quotation PDFs, prioritizing files created or modified within the previous three months.
6. Older quotation files only as supporting evidence when recent sources are insufficient.

Do not reconstruct a quotation from a generic document, invoice template, email body or plain-text table when the quotation workbook or recent quotation PDF is available. Prefer editing a copy of one of the operator-designated guideline quotations or the current quotation workbook so that the original layout remains intact.

## 3. Primary quotation guidelines and recent evidence

The operator-designated primary visual guidelines are:

- `Quotation - ITYCS-20260729-01` — Hirec PFS10 quotation
- `Quotation - ITYCS-20260701-01` — Hirec PFW9 quotation

Use these two quotations as the first visual comparison for every new or corrected quotation. Preserve their page geometry, section order, label spelling, line positions, grey item header, note box, signature/stamp area and footer. The source labels `Costumer`, `Qnt.` and `Sub total` are template labels and must remain unchanged unless the operator explicitly approves a template revision.

Additional quotation evidence within the three-month review window includes:

- `MH-20260728-03` — 28.07.2026
- `ES-20260608-01` — 08.06.2026
- `MH-20260522-01` — 22.05.2026

The associated recent RAW quotation workbooks confirm that the controlling output is the `Quote` sheet. These sources are quotation evidence only and must not be treated as invoice templates.

## 4. Mandatory quotation layout

Preserve the approved 2026 NanoTech Solutions Norway AS quotation design:

- one-page A4 portrait format when content reasonably fits;
- Libre Baskerville typography and source font hierarchy;
- `Quote` heading at the upper left;
- quotation date at the upper right;
- NanoTech Solutions Norway AS logo in the upper-right header area;
- customer and vendor columns beneath the header;
- ruled `Terms and conditions` section;
- grey item-table header with the columns `Description`, `Unit`, `Qnt.`, `Price` and `Sub total`;
- ruled item rows;
- `Total order value` block at the lower right;
- bordered note box at the lower left;
- source stamp/signature block at the lower right;
- `Main Office` footer at the lower left;
- original margins, spacing, line weights, table geometry and section positions;
- the exact source labels and capitalization, including `Quote`, `Costumer`, `Vendor`, `Terms and conditions`, `Items`, `Qnt.`, `Sub total`, `Total order value`, `Note:` and `Main Office`.

Do not substitute:

- a plain-text or word-processing quotation layout;
- a generic corporate quotation layout;
- a large `QUOTATION` banner layout;
- an invoice-style summary table;
- the separate legacy 2023 blue-header quotation design unless explicitly instructed.

## 5. Variable fields permitted for editing

Change only the fields required for the specific quotation:

- quotation date;
- customer company, contact and delivery/billing address;
- verified EORI or tax identifiers, otherwise leave the field blank;
- vendor contact when required;
- quotation reference;
- payment terms;
- currency;
- discount;
- lead time;
- quote-approval status;
- transportation terms;
- carrier;
- application method;
- quotation validity;
- item descriptions;
- units;
- quantities;
- unit prices;
- subtotals;
- total order value;
- quotation-specific notes;
- signature block only when the selected approved template or operator instruction requires a different authorized signatory.

Do not add unverified commercial, tax, customs, dangerous-goods, warranty, delivery or product-performance commitments.

## 6. Draft and approval status

- Commercial content remains `PENDING_REVIEW` until explicitly approved by the operator.
- Record status in the existing `Quote approval` row.
- Do not redesign the header to add a new status banner.
- Layout approval does not approve prices, quantities, terms, recipient data or external issue.
- Do not send or externally share the quotation without explicit approval.

## 7. Naming and reference control

- Customer-facing PDF filename: exact quotation reference only, for example `ST-20260731-01.pdf`.
- Editable quotation source base name: exact quotation reference only.
- Gmail attachment and Drive quotation filename must match the exact quotation reference.
- Do not add `Quotation -`, customer names, `FINAL`, `APPROVED`, `REVISED`, `_v2` or other suffixes.
- A new commercial issue receives the next sequential reference.
- A non-commercial correction may overwrite the same quotation only when the operator treats it as the same quotation.

## 8. Item and total controls

Before export:

1. Confirm each line description, unit and quantity.
2. Confirm unit price and subtotal independently.
3. Confirm discount treatment.
4. Recalculate the total order value.
5. Confirm currency formatting and decimal separators.
6. Confirm that transport, handling and product lines are not duplicated.
7. Confirm that quotation values were not imported from an invoice.

## 9. Note-box controls

Keep notes concise enough to remain inside the source note box. Use only quotation-relevant conditions, such as:

- special sample or MOQ handling;
- appearance after application;
- carrier or dangerous-goods dependency;
- excluded destination charges;
- other operator-approved quotation conditions.

Do not place invoice payment instructions, invoice due dates, bank-remittance blocks or invoice legal wording in the quotation note box.

## 10. Border and geometry preservation

When changing any value:

- preserve every original grey horizontal rule;
- restore the complete rule if an edit covers or removes any part of it;
- preserve the note-box border, item-table rules and total-block rules;
- do not leave white gaps beneath replaced values;
- do not change page margins or move source graphics unless explicitly instructed.

## 11. Validation gate

Before reporting a quotation as complete:

- compare it visually against both operator-designated guideline quotations when available, and at minimum against one recent quotation PDF from the previous three months;
- validate the controlling source is a quotation source and not an invoice source;
- render the PDF and inspect it at high zoom;
- confirm one-page A4 output when expected;
- confirm no clipped text, overlaps, missing glyphs or substituted fonts;
- confirm the logo, customer/vendor columns, terms table, item table, total block, note box, signature and footer are present;
- confirm all modified ruled rows have continuous borders;
- confirm reference, date, recipient, terms, line values and total;
- confirm filename and Drive parent by readback;
- confirm no invoice was created, modified or attached as part of the quotation task.

## 12. Drive and Gmail boundaries

- Draft quotation files may remain in the quotation working area until approved.
- Create or use the customer quotation folder only according to the approved quotation filing workflow.
- Do not file quotation drafts in the invoice archive.
- Do not attach invoice files to quotation emails.
- Do not send the quotation email without explicit operator approval.

## 13. Confidentiality

Public GitHub instructions and learning records must not contain customer addresses, personal email addresses, confidential correspondence or private commercial attachments. Customer-specific quotation files belong in controlled Google Drive storage.
