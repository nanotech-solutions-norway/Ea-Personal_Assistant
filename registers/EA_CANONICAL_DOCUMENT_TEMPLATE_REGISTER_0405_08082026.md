# Ea Canonical Document Template Register — 23:52, 08.08.2026

Status: APPROVED / CANONICAL — MARKUP-CORRECTED  
Drive folder: `Canonical Document Templates` (`19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`)

| Document | Canonical file | Source workbook / sheet | Drive template ID | PDF preview ID | Template SHA-256 | PDF SHA-256 | Validation |
|---|---|---|---|---|---|---|---|
| Quote | `EA_Template_Quote_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Quote` | `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv` | `1zeaE_REXzfI6L0qJBt4hDsytWtjUzAwu` | `b3d208012bae0c58c8c154384d805ebf0b33d048c2a7e655ce4c06c948384281` | `ebce820ec294dd2dc13e87c35df467e8412fd2e88838ff4757e944ae8706008b` | PASS WITH RUNTIME WARNING |
| Packing List | `EA_Template_Packing_List_v1.0.xltm` | `Quote (Espen Olsen) - v5.38.xlsm` / `Packing list` | `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO` | `18vsnWSB48nQtrb_H6I1jNnfQ9hSZJIEd` | `95359e3de2ce6a1f0db159e2249351c30ddf2676800de31192152c7d0db3139e` | `ed341d2ae2438b30fb21deb3b1449b10b7c5441b9e613e11962dffd8ea2182a8` | PASS WITH RUNTIME WARNING |
| RFQ | `EA_Template_RFQ_v1.0.xltm` | `RFQ - v3.1.xlsm` / `RFQ` | `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO` | `1htXMem90Xj_zf0hCk74gjNtxR3CsuGRY` | `4e7a47a7e41616c38fb692fbbb72907cb9944c0998acaffdf1ceb30e972510f5` | `db20352284a90b6331dc96aa8f4619dc63b2f208733be17711c7997d5c3b1e27` | PASS WITH RUNTIME WARNING |
| PO | `EA_Template_PO_v1.0.xltm` | `RFQ - v3.1.xlsm` / `PO` | `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM` | `1a7H57WZ7gOgoDYOHOduJ68FU1Hh7qTVZ` | `8c8fd03231fc5cb6817f77eecd699d9a9ca3a14ccfeb4013dbe42ae2a1f6cf11` | `59ff24b076757b510d2ce6557969d388d233d7f862ebde7024801192d5c0857b` | PASS WITH RUNTIME WARNING |

## Current canonical layout controls

- Left and right print margins are 8.4 mm, a 5% increase from the prior 8.0 mm setting.
- Top and bottom workbook print margins remain 8.0 mm.
- Each target sheet is fitted to one intended page.
- Red-marked alignment/spacing/line-break defects from the operator review dated 08.08.2026 are corrected.
- Purple-marked visible dropdown indicators/data validations are removed from the target-sheet locations identified by the operator.
- The static `%` character on the Quote discount row is removed.
- Quote vendor phone/email/web fields are aligned and kept on one line within the printable width.
- Packing List `Contact:` alignment is corrected.
- RFQ purchase email is kept on one line.
- PO customer address block, PO-reference alignment, attention line and email wrapping are corrected.
- Circular stamp/signature graphics preserve 1:1 geometry.
- PO contains two square QR-code graphics: `Address` and `Website`, restored/recreated using the original `RFQ - v3.1.xlsm` PO design as the reference.
- One-page PDF previews were regenerated and visually validated against the operator's marked PDFs.

## Workbook preservation controls

- Templates remain macro-enabled Excel templates (`.xltm`).
- Original VBA project binaries remain preserved byte-for-byte.
- Supporting hidden/very-hidden sheets remain available as workbook dependencies.
- Formulas and cross-sheet relationships remain intact where applicable.
- No visible `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?` or `#N/A` errors were detected in final target-sheet scans.

## VBA preservation hashes

- Quote/Packing VBA SHA-256: `e795c8b9b38ce385264e3f63686a59fb0276b2a1b451d7eaa7463981ff788834`.
- RFQ/PO VBA SHA-256: `0559726a7b6be079e6bd93bb8d9765c487e5382a9134556e49588a529b6467c6`.

## Runtime warning

Microsoft Excel/VBA runtime execution was not available during the markup correction. Package integrity, target-sheet rendering, formula-error scanning, marked-layout correction, QR/stamp geometry and VBA-binary preservation passed. Macro/button execution should still be acceptance-tested in Microsoft Excel when those controls are relied upon.
