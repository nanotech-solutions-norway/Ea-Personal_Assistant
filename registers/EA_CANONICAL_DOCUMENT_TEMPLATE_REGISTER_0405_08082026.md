# Ea Canonical Document Template Register — 11:53, 08.08.2026

Status: APPROVED / CANONICAL — LAYOUT-CORRECTED  
Drive folder: `Canonical Document Templates` (`19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`)

| Document | Canonical file | Source workbook / sheet | Drive template ID | PDF preview ID | Template SHA-256 | PDF SHA-256 | Validation |
|---|---|---|---|---|---|---|---|
| Quote | `EA_Template_Quote_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Quote` | `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv` | `1zeaE_REXzfI6L0qJBt4hDsytWtjUzAwu` | `193c96574e7dd3ea00d408bcb1e58afb7ae4677bd1ce93b9cff310d5d27e3d0b` | `1ca532780d15ae54ebdfe0405ddc5183ed426d6996996be015649bc933f4ab81` | PASS WITH RUNTIME WARNING |
| Packing List | `EA_Template_Packing_List_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Packing list` | `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO` | `18vsnWSB48nQtrb_H6I1jNnfQ9hSZJIEd` | `efdad6142ec99430788282d6b48103d66e984b21795d551ebdc9a4b84f35e4d5` | `0f4ec234967020a8745d4dd1c4d01cb95172841250b51a87cef7b76f1262deb1` | PASS WITH RUNTIME WARNING |
| RFQ | `EA_Template_RFQ_v1.0.xltm` | `RFQ - v3.1.xlsm` / `RFQ` | `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO` | `1htXMem90Xj_zf0hCk74gjNtxR3CsuGRY` | `16f4941a33bdc814d05c751e344966227fd375ac9d48fe819dc91863eb4982c4` | `c219bec8af5826b8711a6c0f833f83e3911f635208cb89c901e1acac0de24e56` | PASS WITH RUNTIME WARNING |
| PO | `EA_Template_PO_v1.0.xltm` | `RFQ - v3.1.xlsm` / `PO` | `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM` | `1a7H57WZ7gOgoDYOHOduJ68FU1Hh7qTVZ` | `ebe276a262d9f8966fa3af7f85c15dfd8c595b24a4aa1fabb52ad05104e61f17` | `5a6d7e8ced145a4bb911568bda7965386620840815165482370066ac377405f4` | PASS WITH RUNTIME WARNING |

## Construction and layout notes

- Templates are macro-enabled Excel templates (`.xltm`).
- Original VBA project binaries remain preserved byte-for-byte.
- Non-target sheets remain hidden/very-hidden dependencies rather than being removed.
- Populated transaction-specific values are cleared from reusable fields.
- Repeating line-item calculations remain generalized into reusable formulas where applicable.
- Target-sheet formulas suppress unintended zero placeholders where upstream fields are blank.
- Left, right, top and bottom page margins are standardized to approximately 8 mm.
- Print ranges are horizontally centered and fitted to one intended page.
- Content widths were adjusted to use the printable page area more evenly while preserving the existing design language.
- Long email/web fields use non-wrapping shrink-to-fit formatting where required.
- Stamp graphics preserve 1:1 geometry when intrinsically circular/square.
- PO QR surfaces are square and the QR image canvas is square to avoid geometric distortion.
- Packing List subtotal-weight heading was widened/merged to prevent clipping.
- PO attention/contact and Address/Website label wrapping defects were corrected.
- One-page PDF previews were regenerated from the corrected canonical layouts and visually validated.

## VBA preservation hashes

- Quote/Packing source VBA SHA-256: `e795c8b9b38ce385264e3f63686a59fb0276b2a1b451d7eaa7463981ff788834`.
- RFQ/PO source VBA SHA-256: `0559726a7b6be079e6bd93bb8d9765c487e5382a9134556e49588a529b6467c6`.

## Runtime warning

Microsoft Excel/VBA runtime execution was not available during layout correction. Package integrity, target-sheet rendering, formula-error scan, one-page PDF rendering, geometry checks and VBA-binary preservation passed. Macro/button execution should still be acceptance-tested in Microsoft Excel when those controls are relied upon.
