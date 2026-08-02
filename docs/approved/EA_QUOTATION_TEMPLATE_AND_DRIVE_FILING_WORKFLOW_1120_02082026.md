# Ea Quotation and Invoice Drive Filing Workflow — 11:53, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Quotations / Invoices / Google Drive

## Approved quotation design

Use the approved 2026 NanoTech Solutions Norway AS one-page A4 quotation design for future quotation drafts. Preserve the source logo/header, Customer and Vendor columns, Libre Baskerville typography and source font sizes, ruled terms section, grey items table, total block, note box, stamp/signature block and Main Office footer.

Use the current quotation workbook and 2025–2026 quotation PDFs as the controlling layout evidence. Do not reconstruct quotations as plain-text documents and do not merge the separate legacy 2023 blue-header quotation design unless explicitly instructed.

## Approval boundary

A quotation or invoice remains a draft until the operator explicitly approves its commercial content. Approval of layout/design alone does not approve recipient data, prices, quantities, commercial terms or external issue.

## Quotation Drive filing after approval

Quotation root:

`https://drive.google.com/drive/folders/1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`

After explicit operator approval of a quotation:

1. Search the quotation root for the recipient company folder.
2. Save the approved quotation PDF in the existing company folder.
3. If no company folder exists, create one under the quotation root using the confirmed company name and existing sibling-folder naming style.
4. Upload the PDF using the approved quotation reference and filename.
5. Verify the upload through Drive readback.

Do not create a company folder merely because a quotation draft exists.

## Quotation post-approval modifications

If the operator requests quotation modifications after approval:

1. Apply the requested changes.
2. Preserve the quotation reference and filename unless instructed otherwise.
3. Overwrite the existing quotation PDF in the corresponding quotation company folder.
4. Preserve the Drive file ID when technically possible through in-place byte replacement.
5. Do not create duplicate, `_v2`, `REVISED` or date-suffixed copies by default.
6. Verify the replacement through Drive readback.
7. Treat the latest operator-approved replacement as active.

Create a separate revision only when the operator explicitly requests a new reference or retained revision history.

## Invoice creation gate

Create the corresponding invoice only after quotation approval and operator confirmation, using the latest approved quotation as the commercial source unless explicitly changed.

## Invoice Drive filing after approval

Invoice root:

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

After explicit operator approval of an invoice draft:

1. Search the invoice root for the recipient company folder.
2. Save a PDF copy of the approved invoice in the existing company folder.
3. If no company folder exists, create one under the invoice root using the confirmed company name and the existing sibling-folder naming style.
4. Use the approved invoice filename and number, normally `Invoice[Number].pdf`.
5. Verify the saved PDF and parent folder through Drive readback.

Do not file an unapproved invoice draft in the invoice root and do not create a customer folder there merely because an invoice draft exists.

## Confidentiality

Public GitHub records must exclude customer addresses, personal email addresses and confidential correspondence. Approved commercial PDFs belong in the access-controlled Google Drive customer folders.
