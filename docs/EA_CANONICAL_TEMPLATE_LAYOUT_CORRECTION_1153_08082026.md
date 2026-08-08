# Ea Canonical Template Layout Correction — 11:53, 08.08.2026

Status: APPROVED / IMPLEMENTED  
Scope: Quote, Packing List, RFQ and PO canonical Excel templates and PDF previews.

## Operator instruction

Review the source XLSM workbooks and generated PDF files and correct alignment, line breaks, margins and shape geometry. Circular stamps must render round; QR codes must render square. Left/right margins should be reduced to approximately the same visual distance as top/bottom margins.

## Findings and corrections

- Previous PDF previews underused horizontal A4 space and produced disproportionately large side margins.
- Quote email/web text approached or clipped the right print boundary.
- Packing List subtotal-weight heading was clipped.
- RFQ purchase email wrapped at the final character.
- PO contact/email/label text had incorrect line breaks and a duplicated attention-string artifact.
- Several stamp/signature images were anchored with distorted aspect ratios.
- PO QR display geometry was not guaranteed square.

Implemented corrections:
- standardized A4 print margins to approximately 8 mm on all sides;
- widened printable content proportionally and centered it;
- corrected single-line contact fields using shrink-to-fit where necessary;
- corrected Packing List subtotal heading span;
- corrected PO attention/contact structure and Address/Website label geometry;
- restored intrinsic stamp/signature aspect ratios;
- enforced square PO QR geometry/canvas;
- regenerated and visually validated all four one-page PDF previews;
- replaced canonical Drive template and PDF bytes in place, preserving existing Drive IDs;
- retained VBA projects byte-for-byte.

## Validation

Result: PASS WITH RUNTIME WARNING.

Outstanding acceptance item: Microsoft Excel VBA/button runtime execution was not available and should be tested when macro controls are relied upon.
