# Ea Canonical Template Markup Correction — 23:52, 08.08.2026

Status: APPROVED / CANONICAL IMPLEMENTATION LOG  
Project: Ea Personal Assistant

## Operator instruction

Review the four marked canonical PDF previews and update the corresponding Quote, Packing List, RFQ and PO Excel templates.

Markup legend supplied by the operator:
- Red: align text and/or remove excess spacing or unwanted line breaks.
- Purple: remove dropdown indicator/triangle or `%` character.
- Blue: adjust shape geometry; previously corrected geometry must remain correct.
- Additional PO instruction: the `Address` graphic to the left of the Website QR code must also be a QR code, using the original XLSM PO sheet as the reference.
- Increase both left and right margins by 5%.

## Implementation

### Global
- Left/right print margins changed from 8.0 mm to 8.4 mm.
- Top/bottom print margins retained at 8.0 mm.
- One-page print fitting retained.
- Marked target-sheet dropdown validations/indicators removed.
- Existing corrected circular/square geometry retained.

### Quote
- Removed marked dropdowns.
- Removed static `%` from Discount.
- Corrected vendor contact alignment and single-line phone/email/web presentation.

### Packing List
- Corrected `Contact:` alignment.
- Retained circular stamp geometry.

### RFQ
- Removed marked dropdowns.
- Corrected purchase-email single-line layout.

### PO
- Removed marked item dropdowns.
- Corrected customer-address spacing, PO-ref alignment, attention line and email wrapping.
- Replaced/recreated the left `Address` graphic as a square QR code.
- Retained/recreated the right `Website` QR code as a square QR code.
- QR treatment was checked against the original `RFQ - v3.1.xlsm` PO sheet.

## Canonical Drive updates

The existing canonical Drive files were replaced in place, preserving file IDs:

- Quote XLTM: `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv`
- Packing List XLTM: `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO`
- RFQ XLTM: `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO`
- PO XLTM: `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM`
- Quote preview PDF: `1zeaE_REXzfI6L0qJBt4hDsytWtjUzAwu`
- Packing List preview PDF: `18vsnWSB48nQtrb_H6I1jNnfQ9hSZJIEd`
- RFQ preview PDF: `1htXMem90Xj_zf0hCk74gjNtxR3CsuGRY`
- PO preview PDF: `1a7H57WZ7gOgoDYOHOduJ68FU1Hh7qTVZ`

## Final hashes

### XLTM
- Quote: `b3d208012bae0c58c8c154384d805ebf0b33d048c2a7e655ce4c06c948384281`
- Packing List: `95359e3de2ce6a1f0db159e2249351c30ddf2676800de31192152c7d0db3139e`
- RFQ: `4e7a47a7e41616c38fb692fbbb72907cb9944c0998acaffdf1ceb30e972510f5`
- PO: `8c8fd03231fc5cb6817f77eecd699d9a9ca3a14ccfeb4013dbe42ae2a1f6cf11`

### PDF
- Quote: `ebce820ec294dd2dc13e87c35df467e8412fd2e88838ff4757e944ae8706008b`
- Packing List: `ed341d2ae2438b30fb21deb3b1449b10b7c5441b9e613e11962dffd8ea2182a8`
- RFQ: `db20352284a90b6331dc96aa8f4619dc63b2f208733be17711c7997d5c3b1e27`
- PO: `59ff24b076757b510d2ce6557969d388d233d7f862ebde7024801192d5c0857b`

## Validation

- Package integrity: PASS
- Target-sheet formula error scans: PASS — 0 visible errors
- VBA project preservation: PASS — byte-for-byte
- Marked PDF correction coverage: PASS
- Left/right 8.4 mm margins: PASS
- Dropdown indicator removal: PASS
- Quote `%` removal: PASS
- PO Address + Website square QR pair: PASS
- Final PDF visual review: PASS
- Microsoft Excel macro/button runtime execution: NOT TESTED

## Result

PASS WITH RUNTIME WARNING.
