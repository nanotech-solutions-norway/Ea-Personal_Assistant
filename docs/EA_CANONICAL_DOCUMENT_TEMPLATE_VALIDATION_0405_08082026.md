# Ea Canonical Document Template Validation — 11:53, 08.08.2026

Status: PASS WITH FUNCTIONAL EXECUTION WARNING

## Scope

Re-validation of the four canonical macro-enabled Excel templates after operator-requested layout correction against both the source XLSM workbooks and the generated PDF previews:

- Quote → `EA_Template_Quote_v1.0.xltm`
- Packing List → `EA_Template_Packing_List_v1.0.xltm`
- RFQ → `EA_Template_RFQ_v1.0.xltm`
- PO → `EA_Template_PO_v1.0.xltm`

## Validation results

| Template | Package integrity | Formula scan | VBA preservation | Layout/alignment | Shape geometry | PDF preview | Result |
|---|---|---|---|---|---|---|---|
| Quote | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — stamp/signature aspect preserved | PASS — 1 page | PASS WITH WARNING |
| Packing List | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — stamp round | PASS — 1 page | PASS WITH WARNING |
| RFQ | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — stamp/signature aspect preserved | PASS — 1 page | PASS WITH WARNING |
| PO | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — stamps round; QR square | PASS — 1 page | PASS WITH WARNING |

## Corrected layout controls

- Left/right/top/bottom page margins standardized to approximately 8 mm.
- Horizontal centering enabled for the target print regions.
- Printable-width utilization increased so side margins visually match the top/bottom spacing.
- Quote phone/email/web fields corrected to remain on a single line without right-edge clipping.
- Packing List `sub total Weight (KG)` heading corrected to a clean merged heading without clipping.
- RFQ purchase email corrected to remain on a single line.
- PO `Att.: Ruben A. Meyer` structure corrected; email and Address/Website labels no longer break incorrectly.
- Stamp/signature graphics were resized using their intrinsic aspect ratios rather than distorted anchor rectangles.
- PO QR image surface/canvas corrected to square geometry.

## PDF margin verification

- Quote: left/right 8.00 mm; top/bottom approximately 8.08 mm.
- Packing List: left/right approximately 8.10 mm; top/bottom 8.00 mm.
- RFQ: left/right 8.00 mm; top/bottom approximately 8.10 mm.
- PO: left/right 8.00 mm; top/bottom approximately 8.06 mm.

The sub-0.1 mm differences are caused by proportional A4 page fitting and are visually negligible.

## Structural checks

- Macro-enabled template content type remains present.
- Only the intended operator-facing target sheet is visible in each canonical template.
- Supporting workbook sheets remain available as hidden/very-hidden dependencies.
- Original workbook formulas, validations and cross-sheet relationships remain intact where applicable.
- No visible `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?` or `#N/A` errors were detected in target-sheet scans.
- All four regenerated PDF previews contain one intended target document page.
- ZIP/package integrity tests returned no corrupt entries.

## VBA preservation

- Quote/Packing VBA SHA-256: `e795c8b9b38ce385264e3f63686a59fb0276b2a1b451d7eaa7463981ff788834`.
- RFQ/PO VBA SHA-256: `0559726a7b6be079e6bd93bb8d9765c487e5382a9134556e49588a529b6467c6`.

The corrected templates preserve the prior canonical VBA project binaries byte-for-byte.

## Functional execution warning

Microsoft Excel/VBA runtime execution was not available in the correction environment. Buttons, macro entry points and VBA runtime behavior were therefore not executed end-to-end in Microsoft Excel. Production acceptance should retain an Excel runtime test when those controls are relied upon.

## Final result

PASS WITH WARNINGS — layout, rendering, package integrity, formula scanning, geometry and VBA preservation passed; Microsoft Excel macro execution remains the outstanding runtime acceptance test.
