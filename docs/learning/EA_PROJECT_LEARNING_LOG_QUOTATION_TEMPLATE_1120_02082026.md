# Ea Project Learning Log — Quotation Template and Generation Separation — updated 11:11, 05.08.2026

**Status:** APPROVED / CANONICAL  
**Category:** Correction / Decision / Workflow / Validation  
**Subsystem:** Documents / Quotations / Google Drive

## Issue observed

A quotation was reconstructed as a new generic document instead of following the established 2026 quotation family. The resulting output used a large `QUOTATION` banner, a different logo position, different typography, different table structure, a generic commercial-terms layout and invoice-like summary conventions.

## Source review

Recent Google Drive quotations within the three-month review window were compared:

- `ITYCS-20260729-01`
- `MH-20260728-03`
- `ITYCS-20260701-01`
- `ES-20260608-01`
- `MH-20260522-01`

Associated recent RAW quotation workbooks and `Quote - v5.31.xlsm` confirmed that the controlling source is the quotation workbook's `Quote` sheet.

## Root cause

The quotation was generated from parsed commercial content and generic document-generation logic rather than the actual quotation workbook/PDF geometry. Quotation generation controls were also stored alongside invoice workflow language, which increased the risk of importing invoice conventions into quotations.

## Corrective decision

1. Quotation generation is now governed by the quotation-only canonical file `EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md`.
2. Quotation and invoice generation must remain separate.
3. Use only the quotation workbook, the `Quote` sheet and recent quotation PDFs for quotation generation.
4. Preserve the approved one-page A4 layout, Libre Baskerville typography, logo/header, customer/vendor columns, ruled terms section, grey item table, total block, note box, stamp/signature block and Main Office footer.
5. Do not reconstruct quotations as plain-text documents or generic commercial documents.
6. Do not use invoice numbering, invoice due-date blocks, invoice VAT layouts, invoice status banners or invoice filing rules in quotations.

## Corrected quotation action

Quotation `CS-20260803-01` was rebuilt against the recent 2026 quotation family while preserving the same quotation reference and commercial line values. The correction uses the approved quotation geometry and remains `Pending internal approval` in the `Quote approval` row.

## Validation controls

- Compare every new quotation against a quotation PDF from the previous three months.
- Confirm the source artifact is a quotation source, not an invoice source.
- Render and inspect the PDF at high zoom.
- Check continuous ruled-cell borders after every edit.
- Check logo, typography, section positions, line values, total and filename.
- Confirm that no invoice was generated, modified or attached during the quotation task.

## Confidentiality check

This log contains workflow rules and quotation references only. It excludes customer addresses, personal email addresses and confidential correspondence.
