# Ea Project Learning Log - Quotation Cell-Border Correction - 12:23, 02.08.2026

**Status:** APPROVED / CANONICAL  
**Category:** Correction / Validation / Workflow  
**Subsystem:** Documents / Quotations / PDF generation

## Issue observed

After replacing values in the ruled Terms and conditions section, the white redaction area removed part of the grey lower cell rule beneath the replacement text. The defect was visible in a mobile PDF reader at high zoom.

## Root cause

The replacement workflow restored only selected line segments after redaction. This left an unintended gap beneath the adjusted values.

## Corrective rule

For every modified ruled-table value, restore the complete affected grey horizontal rule at the original template coordinate after inserting replacement text. Validate at high zoom and in a mobile/PDF-reader-style render before Drive overwrite.

## Action taken

- Rebuilt quotation DP-20260731-01 with continuous grey lower borders beneath Discount: 100% and Quote approval: Confirmed.
- Rebuilt quotation ST-20260731-01 with a continuous grey lower border beneath Quote approval: Confirmed.
- Preserved quotation references, filenames, Drive file IDs, products, quantities, prices and totals.
- Overwrote the existing approved PDFs in their company folders and verified the resulting file metadata.

## Future application

Apply this validation to every post-approval quotation modification involving text in ruled cells.

## Confidentiality check

No customer addresses, personal email addresses or confidential correspondence are stored in this learning record.
