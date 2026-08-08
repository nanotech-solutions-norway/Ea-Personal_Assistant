# Ea Canonical Document Template Register — 04:05, 08.08.2026

Status: APPROVED / CANONICAL  
Drive folder: `Canonical Document Templates` (`19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`)

| Document | Canonical file | Source workbook / sheet | Drive template ID | PDF preview ID | Template SHA-256 | Validation |
|---|---|---|---|---|---|---|
| Quote | `EA_Template_Quote_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Quote` | `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv` | `1zeaE_REXzfI6L0qJBt4hDsytWtjUzAwu` | `b2c3d56227f59b196b1e0719c9c5d7bfd31f40e36cce2a61ad6b3bd8006b4325` | PASS WITH WARNINGS |
| Packing List | `EA_Template_Packing_List_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Packing list` | `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO` | `18vsnWSB48nQtrb_H6I1jNnfQ9hSZJIEd` | `5d66a9d526ee7e5e236c41ac21d883113a31de153526eb79af04735caf6c7161` | PASS WITH WARNINGS |
| RFQ | `EA_Template_RFQ_v1.0.xltm` | `RFQ - v3.1.xlsm` / `RFQ` | `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO` | `1htXMem90Xj_zf0hCk74gjNtxR3CsuGRY` | `c461b812bc7f9a360ed81f3036751f1a3e907311346c4738810611882673ba1f` | PASS WITH WARNINGS |
| PO | `EA_Template_PO_v1.0.xltm` | `RFQ - v3.1.xlsm` / `PO` | `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM` | `1a7H57WZ7gOgoDYOHOduJ68FU1Hh7qTVZ` | `9b670cb3f67e8b32e12cfc6ea8bd1bf83aee6c62ccea96b33b16b7b0435be5fd` | PASS WITH WARNINGS |

## Construction notes

- Templates are macro-enabled Excel templates (`.xltm`).
- Original VBA project binaries were preserved byte-for-byte from their source workbooks.
- Non-target sheets were retained as hidden/very-hidden dependencies rather than removed.
- Populated transaction-specific values were cleared from reusable fields.
- Repeating line-item calculations were generalized into formulas where the populated source contained hard-coded row results.
- Target-sheet formulas were adjusted to suppress zero placeholders when upstream fields are blank.
- One-page PDF previews were generated from the target template ranges and validated visually.

## VBA preservation hashes

- Quote-source VBA SHA-256: `e795c8b9b38ce385264e3f63686a59fb0276b2a1b451d7eaa7463981ff788834`.
- RFQ-source VBA SHA-256: `0559726a7b6be079e6bd93bb8d9765c487e5382a9134556e49588a529b6467c6`.

## Validation warning

Microsoft Excel/VBA runtime execution was not available during template creation. Package integrity, target-sheet layout, formula-error scan, one-page preview generation and VBA-binary preservation passed. Macro/button execution must be acceptance-tested in Microsoft Excel before production release if those controls are relied upon.
