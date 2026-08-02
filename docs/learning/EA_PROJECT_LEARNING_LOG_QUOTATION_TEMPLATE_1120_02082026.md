# Ea Project Learning Log — Quotation Template and Filing — 11:20, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Category:** Correction / Decision / Workflow / Validation  
**Subsystem:** Documents / Files / Google Drive

## Issue observed

Initial quotation outputs did not reproduce the established quotation template. Their structure, font family, font sizes, spacing, tables, graphics, signature block and footer differed materially from the source quotation family.

## Root cause

The output was reconstructed as a new document from parsed content instead of using the actual current quotation workbook/PDF geometry as the controlling visual template.

## Corrective rule

Use the approved 2026 quotation design and current quotation workbook/source PDFs as the controlling template. Preserve the original page structure and change only variable commercial fields.

## Approved design controls

- One-page A4 portrait layout.
- Libre Baskerville source typography.
- Logo/header, Customer and Vendor columns, terms table, grey item table, total block, note box, signature/stamp and footer retained.
- Do not substitute a plain-text layout.
- Do not mix in the separate legacy 2023 blue-header design unless explicitly instructed.

## Filing decision

After explicit operator approval of quotation content, save the PDF in the recipient company folder under the quotation root in Google Drive. Create the company folder only when it does not already exist.

## Post-approval modification decision

If the operator requests modifications after approval, overwrite the existing quotation PDF in the corresponding company folder. Preserve the filename, quotation reference and Drive file ID when possible. Create a separate revision only when explicitly requested.

## Approval boundary

The operator approved the quotation layout/design and future workflow. Current quotation content is not deemed approved unless separately confirmed.

## Evidence

- Current 2025–2026 quotation PDFs.
- `Quote - v5.31.xlsm`.
- Operator confirmation that the corrected layout and design are good.
- Operator instructions on approved-PDF filing and post-approval overwriting.

## Confidentiality check

This log contains workflow rules only. It excludes customer addresses, personal email addresses and confidential correspondence.

## Future application

Apply this workflow to all future NanoTech Solutions Norway AS quotation drafting, approval, Drive filing, modification and invoice-generation tasks.
