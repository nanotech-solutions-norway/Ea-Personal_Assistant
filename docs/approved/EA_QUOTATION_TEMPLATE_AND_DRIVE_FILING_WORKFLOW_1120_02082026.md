# Ea Quotation and Invoice Drive Filing Workflow — updated 11:11, 05.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Drive filing / Gmail attachment control

## Workflow separation

This file governs approval boundaries, naming and filing. It does not combine quotation generation with invoice generation.

- Quotation generation is controlled by `EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md`.
- Invoice generation is a separate workflow and must not use quotation templates, quotation references or quotation layout rules.
- A quotation task must not automatically create or modify an invoice.

## Approval boundary

A quotation or invoice remains a draft until the operator explicitly approves its commercial content. Approval of layout/design alone does not approve recipient data, prices, quantities, commercial terms or external issue.

## Canonical quotation naming

- The quotation filename must be the exact quotation reference and nothing else.
- Example: `ST-20260731-01.pdf`.
- Do not add `Quotation -`, customer names, `FINAL`, `APPROVED`, `REVISED`, `_v2`, dates outside the reference or descriptive text.
- The editable quotation source must use the same reference-only base name.
- Gmail quotation attachments and Google Drive quotation files must use the same exact filename.
- A new commercial issue receives the next sequential quotation reference.
- A non-commercial correction may overwrite the same file only when the operator explicitly treats it as the same quotation.

## Canonical invoice naming

- Invoice naming and numbering remain accounting-controlled and separate from quotation references.
- The invoice filename must match the approved invoice reference and established language convention, normally `Invoice[Number].pdf` or `Faktura[Number].pdf`.
- Do not use quotation references as invoice numbers.
- Do not create an invoice merely because a quotation exists.

## Quotation Drive filing after approval

Quotation root:

`https://drive.google.com/drive/folders/1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`

After explicit operator approval of a quotation:

1. Search the quotation root for the recipient company folder.
2. Save the approved quotation PDF in the existing company folder.
3. If no company folder exists, create one under the quotation root using the confirmed company name and sibling-folder naming style.
4. Save the PDF using only the exact quotation reference.
5. Verify filename, file ID, size and parent folder through Drive readback.

Do not create a company folder merely because a quotation draft exists.

## Quotation post-approval modifications

- If the operator requests a correction that remains the same quotation, overwrite the existing file in place and preserve its Drive file ID.
- If a commercially updated quotation is newly issued, allocate the next sequential quotation reference and save it separately.
- Do not use `_v2`, `REVISED`, `FINAL` or date suffixes.
- Confirm whether the change is an in-place correction or a newly issued quotation when the operator instruction does not resolve that distinction.

## Quotation border validation

For every quotation correction involving ruled cells:

1. Preserve the complete grey rule at the source-template coordinate.
2. Restore any rule segment covered by the edit.
3. Check every modified row for white gaps.
4. Validate at high zoom and in a PDF-reader-style render.

## Invoice Drive filing after approval

Invoice root:

`https://drive.google.com/drive/folders/17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`

After explicit operator approval of an invoice:

1. Search the invoice root for the recipient company folder.
2. Save the approved invoice PDF in the existing company folder.
3. If no company folder exists, create one under the invoice root using the confirmed company name and sibling-folder naming style.
4. Use only the approved invoice filename and accounting-controlled invoice reference.
5. Verify filename, file ID, size and parent folder through Drive readback.

Do not file a quotation in the invoice root or an invoice in the quotation root.

## Gmail attachment control

- Quotation emails may contain the approved quotation and operator-approved supporting files only.
- Invoice emails may contain the approved invoice and operator-approved supporting files only.
- Do not bundle a quotation and invoice merely because they concern the same customer.
- Verify every attachment filename by Gmail readback.
- Do not send without explicit operator instruction.

## Confidentiality

Public GitHub records must exclude customer addresses, personal email addresses and confidential correspondence. Customer-specific quotation and invoice files belong in controlled Google Drive folders.
