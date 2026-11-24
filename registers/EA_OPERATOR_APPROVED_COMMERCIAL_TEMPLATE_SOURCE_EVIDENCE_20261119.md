# NTSN Commercial Template Source Approval — Evidence Register — 13:31, 19.11.2026 (Europe/Madrid)

**Work ID:** EA-COMM-DOC-20261119-01. **Authority:** operator's direct 19.11.2026 approval of eleven chat attachments, within PO/Quote/RFQ/Packing List only. **Status:** SOURCE-IDENTITY VERIFIED (attached byte hashes); PDF visual inspection VERIFIED; functional workbook acceptance and permanent Drive registration **NOT_VERIFIED**. This is a proposed repository record in draft PR #158 until reviewed and merged.

## Attachment checksums — exact bytes, read-only

| Source type | Exact attached file | SHA-256 | Outcome |
|---|---|---|---|
| PO PDF | `PO - Template_v3.0_2024.pdf` | `b0e58c01e8a5edffd4733dc623ca18699343e6461f8ebab0609907f0ebad7b2f` | Approved visual, A4 portrait |
| PO legacy Excel | `PO - Template_v3.0_2024.xls` | `a83d5103bc89641781a54dd289386f7bcbd1252a43814731df60569ff3c92c36` | Source provided; functional acceptance pending |
| RFQ PDF | `RFQ - Template_v3.0_2024.pdf` | `7c673de7f1f9e178c42f7f7d48a9a264d3626cac684a905220d20d9fb9ef7d60` | **BLOCKED**: pixel-identical to PO preview |
| RFQ legacy Excel | `RFQ - Template_v3.0_2024.xls` | `98667f3f875a7c606b5fdfcf40c1411cfd380e2a9dfa9920c761d3c35e6f987c` | Source provided; functional acceptance pending |
| RFQ corrected PDF — **follow-up** | `RFQ - Template_v3.0_2024(1).pdf` | `7e1255d6db41fced9fca0aa6b3cba6f4ede2c94faba4516dd50dd55f2550e8b6` | **VERIFIED corrected RFQ visual**: distinct from PO, true RFQ heading, A4 portrait; populated examples not defaults |
| RFQ corrected legacy Excel — **follow-up** | `RFQ - Template_v3.0_2024(1).xls` | `024c7baaf7cd9273e1ca8701ac0eb61eb328df973760cc8492504b0540b3aef1` | BIFF structure and cached formula states inspected; **changed VBA streams** require security/Excel runtime review |
| Quote Espen PDF | `Quote - Espen Olsen.pdf` | `49e43e20f218d43dac747b987031e701be1d9ef3335760f54ca0bc2073b6065c` | Approved visual, A4 portrait |
| Quote Ruben PDF | `Quote - Ruben A. Meyer.pdf` | `69bee7b5db3460945317bf58abc60933554c81071d17e8795605bc748ccc3e62` | Approved visual; signer ambiguity |
| Quote Ruben editable | `Quote - Ruben A. Meyer.xlsm` | `ab4d9f5d9df1e68eeeedeac6fe1d1c22ddddbc01aebd02c30ea6e9da85b92d48` | VBA present; cached Excel errors and runtime QA outstanding |
| Packing Espen PDF | `Packing list - Espen Olsen.pdf` | `e7db88fe036edb90d83f721ab3ce7adf271fffde327dc2895584573cd1e45e0b` | Approved visual, A4 **landscape** |
| Packing Espen editable | `Packing list - Espen Olsen.xlsm` | `78eb0e8edbc56b3bd3f66bcc6504b7cf365b8d6ec6d31dd72d28ec0dfcb8eec1` | VBA present; cached Excel errors and runtime QA outstanding |
| Packing Ruben PDF | `Packing list - Ruben A. Meyer.pdf` | `f8049696f2b790ca9f7f5c3513352bc6f9e4620af25986c61bf74b8994a4bd60` | Approved visual, A4 landscape |
| Packing Ruben editable | `Packing list - Ruben A. Meyer.xlsm` | `210d7da70247ab2130f02305a7bd06557f87461cc4ebff1dfeb4ff979bdb213e` | VBA present; cached Excel errors and runtime QA outstanding |

**Initial upload: 11 distinct attachments** (6 PDF / 5 spreadsheets). **Follow-up correction: 2 additional RFQ attachments** (1 PDF / 1 XLS), superseding only the defective original RFQ candidate. **Not included:** invoice PDF or operational invoice template; Quote Espen .xlsm. Earlier review-only DOCX proposals are not these approved source masters.

## Technical acceptance / differences

| Gate | Observation | Classification |
|---|---|---|
| PDF page size | PO, RFQ and Quote are A4 portrait; both Packing Lists are A4 landscape | VERIFIED |
| RFQ initial preview identity | Original RFQ/PO PDFs have different file hashes but identical rendered pixel samples at 1.5× and both display Purchase Order | **HISTORICAL FAIL — superseded by corrected `(1)` RFQ PDF** |
| RFQ corrected PDF | Replacement is independently rendered and displays Request for Quote (RFQ), with distinct RFQ reference, terms and item grid | **VISUAL VERIFIED, operator acceptance of revised file not separately verbalized** |
| RFQ corrected OLE/BIFF8 structure | Five worksheets (RFQ/PO visible; Packing List/Products/Freight Forwarder hidden), 103 formula records, zero cached formula-error results; dedicated Workbook stream 697,395 B | **STATIC STRUCTURE VERIFIED**, not Excel runtime |
| RFQ VBA parity with original RFQ XLS | New file has modified Module1–4, ThisWorkbook, PROJECT and VBA/dir streams and workbook content | **MACRO DIFFERENCE / SECURITY & RUNTIME TEST REQUIRED** |
| Excel .xlsm package structure | 11 worksheets; VBA projects and source drawings present in all 3 uploaded .xlsm files | VERIFIED STRUCTURE ONLY |
| Cached formula outputs | All 3 .xlsm sources: `Quote!AA34:AA36` are cached `#VALUE!` cells | **FAIL/INVESTIGATE** |
| Macro / button run | No Microsoft Excel runtime test performed | NOT_VERIFIED |
| August canonical VBA-byte parity | Uploaded files have different VBA SHA-256 from registered August 05B masters | NOT_PRESERVED; pending code / security review |
| Normalized quote/pack data | Source PDFs have genuine transaction-specific values; never use as reusable defaults | RULE ENFORCED |
| Ruben-named quotation | Bottom signatory appears inconsistent with the vendor attention variant | PENDING_REVIEW_Q-SIGNER |
| Invoice design update | No new invoice source | NOT_SUPPLIED |
| Persistent Drive source ID and parent | These were attached to conversation; none of the 11 was separately filed in Drive by this pass | NOT_VERIFIED |

## Prior registered authority and acceptance gates

05B registered XLTM IDs remain: Quote `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv`; Packing List `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO`; RFQ `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO`; PO `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM`. The PO September 05C PDF continues to exist at `1NliiqekZMO6Uii8vTXSs11aoFylXZ8CA`; newer approved PO PDF is a *new visual selection*, not a verified replacement of that Drive item.

**Open actions:** (1) RFQ PDF visual correction **verified**; qualify the new RFQ source's changed VBA and exact Excel-to-PDF fidelity; (2) evaluate quotation/packing worksheet error cells; (3) validate new VBA/macros in real Excel, with security review; (4) clarify quote signer selection; (5) obtain Espen quote editable file and approved invoice source if desired; (6) source/Drive persistence with explicit authorization; (7) versioned 05B/05C/register update and readback before retired-master substitution.

Never add raw customer values, bank information or PDF samples to the public repository.

## 19.11.2026 follow-up revision readback

Comparison baseline: incorrect initial RFQ PDF pixel SHA-256 at 1.5× `1a2728c1db9e35a3d3316c38c87f00b3de5e3a90e0b331acee9ad36a919bb484`; corrected RFQ PDF pixel SHA-256 `6947d680e3d178b77f124ff9f4e06134e71f31000655685861273502eb16217d`. Corrected PDF page geometry approximately 210.02 × 297.01 mm. New source's raw document and VBA must remain in controlled storage; public register contains only SHA-256 and sanitized structural metadata. **No Excel macros were executed; no Drive master replaced.**
