# Ea Quotation and Invoice Drive Filing Workflow — 12:35, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Quotations / Invoices / Gmail / Google Drive

## Approved quotation design

Use the approved 2026 NanoTech Solutions Norway AS one-page A4 quotation design for future quotation drafts. Preserve the source logo/header, Customer and Vendor columns, Libre Baskerville typography and source font sizes, ruled terms section, grey items table, total block, note box, stamp/signature block and Main Office footer.

Use the current quotation workbook and 2025–2026 quotation PDFs as the controlling layout evidence. Do not reconstruct quotations as plain-text documents and do not merge the separate legacy 2023 blue-header quotation design unless explicitly instructed.

## Approval boundary

A quotation or invoice remains a draft until the operator explicitly approves its commercial content. Approval of layout/design alone does not approve recipient data, prices, quantities, commercial terms or external issue.

## Canonical document naming

### Quotations

- The quotation filename must be the exact quotation reference and nothing else.
- Example: `ST-20260731-01.pdf`.
- Do not add `Quotation -`, customer names, `FINAL`, `APPROVED`, `REVISED`, `_v2`, dates outside the reference, or other descriptive text.
- The editable source file must use the same reference-only base name, for example `ST-20260731-01`.
- Gmail quotation attachments and Google Drive quotation files must use the same exact filename.
- If a new or updated quotation is issued for the same customer in the same reference period, allocate the next sequential quotation reference, for example `ST-20260731-02`, then `ST-20260731-03`.
- Do not reuse an earlier commercial quotation reference for a newly issued quotation.
- A non-commercial layout or technical correction may overwrite the same file only when the operator explicitly treats it as the same quotation rather than a newly issued quotation.

### Invoices

- The invoice filename must match the approved invoice reference and established NanoTech Solutions Norway AS naming convention, normally `Invoice[Number].pdf` for English invoices or `Faktura[Number].pdf` for Norwegian invoices.
- Examples: `Invoice15160.pdf` and `Faktura15160.pdf`.
- Do not add customer names, dates, `FINAL`, `APPROVED`, revision labels or other descriptive text.
- Gmail invoice attachments and all Google Drive invoice copies must use the same exact filename.
- A replacement that legally or commercially requires a new invoice must receive the next valid invoice number through the accounting-controlled numbering sequence; do not invent a revision suffix.

## Quotation Drive filing after approval

Quotation root:

`https://drive.google.com/drive/folders/1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`

After explicit operator approval of a quotation:

1. Search the quotation root for the recipient company folder.
2. Save the approved quotation PDF in the existing company folder.
3. If no company folder exists, create one under the quotation root using the confirmed company name and existing sibling-folder naming style.
4. Save the PDF using only the exact quotation reference as the filename.
5. Verify the filename, file ID, size and parent folder through Drive readback.

Do not create a company folder merely because a quotation draft exists.

## Quotation post-approval modifications

- If the operator requests a correction that remains the same quotation, overwrite the existing file in place and preserve its Drive file ID.
- If an updated quotation is newly issued, allocate the next sequential quotation reference for that customer/reference period and save it as a separate file.
- Do not use ad hoc suffixes such as `_v2`, `REVISED`, `FINAL` or date additions.
- Confirm whether the change is an in-place correction or a newly issued quotation when that distinction is not clear from the operator instruction.

## Quotation cell-border preservation and validation

When replacing or redacting a value inside the ruled Terms and conditions section:

1. Preserve the original grey horizontal cell rule at its exact source-template coordinate.
2. If a redaction removes any part of the rule, redraw the complete affected rule segment after inserting the replacement text.
3. Do not leave an unintended white gap beneath a modified value.
4. Validate the result at high zoom and in a mobile/PDF-reader-style render.
5. Check every modified row, not only the text, before filing or attaching the PDF.

## Invoice creation gate

Create the corresponding invoice only after quotation approval and operator confirmation, using the latest approved quotation as the commercial source unless explicitly changed.

## Invoice Drive filing after approval

Invoice root:

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

After explicit operator approval of an invoice draft:

1. Search the invoice root for the recipient company folder.
2. Save a PDF copy of the approved invoice in the existing company folder.
3. If no company folder exists, create one under the invoice root using the confirmed company name and existing sibling-folder naming style.
4. Save the invoice using only its approved invoice reference and established language prefix, normally `Invoice[Number].pdf` or `Faktura[Number].pdf`.
5. Verify the filename, file ID, size and parent folder through Drive readback.

Do not file an unapproved invoice draft in the invoice root and do not create a customer folder there merely because an invoice draft exists.

## Gmail draft attachment control

- Before recreating a draft with corrected attachments, discard the superseded Gmail draft when explicitly instructed by the operator.
- Attach the quotation using the exact reference-only filename.
- Attach the invoice using the exact approved invoice filename.
- Read back the draft and verify both attachment filenames before reporting completion.
- Do not send without explicit operator instruction.

## Confidentiality

Public GitHub records must exclude customer addresses, personal email addresses and confidential correspondence. Approved commercial PDFs belong in the access-controlled Google Drive customer folders.
