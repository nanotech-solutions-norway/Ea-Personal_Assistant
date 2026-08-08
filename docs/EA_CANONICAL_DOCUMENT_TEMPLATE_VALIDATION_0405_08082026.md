# Ea Canonical Document Template Validation — 23:52, 08.08.2026

Status: PASS WITH FUNCTIONAL EXECUTION WARNING

## Scope

Re-validation of the four canonical macro-enabled Excel templates after implementation of the operator's marked-PDF corrections:

- Quote → `EA_Template_Quote_v1.0.xltm`
- Packing List → `EA_Template_Packing_List_v1.0.xltm`
- RFQ → `EA_Template_RFQ_v1.0.xltm`
- PO → `EA_Template_PO_v1.0.xltm`

The review basis included the four operator-marked PDF previews plus the original source workbooks `Quote (Espen Olsen) - v5.38.xlsm` and `RFQ - v3.1.xlsm`.

## Validation results

| Template | Package integrity | Formula scan | VBA preservation | Markup corrections | Shape/QR geometry | PDF preview | Result |
|---|---|---|---|---|---|---|---|
| Quote | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — circular stamp/signature geometry preserved | PASS — 1 page | PASS WITH WARNING |
| Packing List | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — circular stamp preserved | PASS — 1 page | PASS WITH WARNING |
| RFQ | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — circular stamp/signature geometry preserved | PASS — 1 page | PASS WITH WARNING |
| PO | PASS | PASS — 0 visible formula errors | PASS — byte-for-byte | PASS | PASS — circular stamps; Address + Website QR codes square | PASS — 1 page | PASS WITH WARNING |

## Operator-markup corrections verified

### Global
- Left and right workbook print margins increased by 5% from 8.0 mm to 8.4 mm.
- Top and bottom workbook print margins retained at 8.0 mm.
- Target documents remain one-page outputs.
- Red-marked text alignment, excess spacing and unwanted line breaks were corrected.
- Purple-marked visible dropdown indicators/data validations were removed from the marked target-sheet fields.
- Blue-marked shape geometry remains corrected.

### Quote
- Customer/currency/transport/carrier/application/item dropdown indicators removed from the marked target-sheet locations.
- Static `%` character removed from the Discount row.
- Vendor contact labels and phone/email/web values aligned and prevented from wrapping/clipping.
- Final PDF is one page with 8.4 mm left/right margins.

### Packing List
- `Contact:` label alignment corrected.
- Circular stamp retains 1:1 aspect ratio.
- Final PDF is one page with 8.4 mm left/right margins.

### RFQ
- Transport/carrier and item-row dropdown indicators removed from marked target-sheet locations.
- Purchase email kept on one line.
- Final PDF is one page with 8.4 mm left/right margins.

### PO
- Customer address block no longer contains the marked unwanted blank line.
- `PO ref.` alignment corrected to match adjacent reference labels.
- `Att.: Ruben A. Meyer` restored as one aligned line.
- Email kept on one line.
- Item dropdown indicators removed.
- The left `Address` graphic is now a square QR code, matching the original PO workbook's intended QR-code treatment.
- The right `Website` graphic remains a square QR code.
- Both QR surfaces/canvases are square in the final package and final preview.
- Final PDF is one page with 8.4 mm left/right margins.

## Structural checks

- Macro-enabled template content type remains present.
- Only the intended operator-facing target sheet is visible in each canonical template.
- Supporting workbook sheets remain available as hidden/very-hidden dependencies.
- Formula/cross-sheet relationships remain intact where applicable.
- No visible `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?` or `#N/A` errors were detected in final target-sheet scans.
- ZIP/package integrity checks returned no corrupt entries.
- All four regenerated PDF previews contain one intended target document page.

## VBA preservation

- Quote/Packing VBA SHA-256: `e795c8b9b38ce385264e3f63686a59fb0276b2a1b451d7eaa7463981ff788834`.
- RFQ/PO VBA SHA-256: `0559726a7b6be079e6bd93bb8d9765c487e5382a9134556e49588a529b6467c6`.

The corrected templates preserve the prior canonical VBA project binaries byte-for-byte.

## Functional execution warning

Microsoft Excel/VBA runtime execution was not available in the correction environment. Buttons, macro entry points and VBA runtime behavior were therefore not executed end-to-end in Microsoft Excel. Production acceptance should retain an Excel runtime test when those controls are relied upon.

## Final result

PASS WITH WARNINGS — marked layout corrections, side-margin increase, dropdown/% removal, QR/stamp geometry, rendering, package integrity, formula scanning and VBA preservation passed; Microsoft Excel macro execution remains the outstanding runtime acceptance test.
