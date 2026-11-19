# 05E — NTSN Operator-Selected Commercial Template Sources — 13:30, 19.11.2026 (Europe/Madrid)

**Status:** OPERATOR-APPROVED VISUAL SOURCE SELECTION (19.11.2026); repository incorporation and production master replacement remain **PENDING_REVIEW** until branch review/merge, secure Drive file registration, and functional validation.
**Work ID:** EA-COMM-DOC-20261119-01. **Source:** direct operator statement "Approved templates attached" with eleven attached files in the current Ea - Personal Assistant conversation.
**Scope:** PO, Quote (Ruben / Espen), RFQ, Packing List (Ruben / Espen). **Invoice not included** in the approved attachments.
**Authority boundary:** operator approval of a reference design is not approval of sample transaction facts, sender identity for future documents, item descriptions, prices, tax determination, new accounting issue, runtime VBA compatibility or external dispatch.

## 1. Explicit design selection and hierarchy

Current operator-selected, uploaded PDF versions control the **visual target** within the identified document family, subject to validation and the defects noted below. Preserve their page geometry, logo, Libre Baskerville text appearance, grid structure, line weights, footer, intended signer/graphics, and each family-specific field placement. Do not paste their sample transaction values into new documents. For editable/functional Excel operation, preserve the existing registered 05B master until a verified replacement is safely registered, tested and approved. 05A preservation rules still apply. PO operator selection conflicts with older 05C and is a newer **explicit design choice** within this scope; flag the supersession for proper versioned canonical maintenance, rather than silently editing 05C.

| Family | Operator PDF visual reference | Page / structure | Workbook evidence | Adoption scope |
|---|---|---|---|---|
| PO | `PO - Template_v3.0_2024.pdf` | A4 portrait, one page; upper-right logo, left buyer/right supplier, PO/RFQ/quote refs, Delivery information, square Address/Website QR pair, item grid, Purpose of use, total, lower-right signature, Main Office footer | `PO - Template_v3.0_2024.xls` is legacy OLE Excel file; functionality not qualified | **APPROVED VISUAL** with functional master **NOT_VERIFIED** |
| Quote (Espen) | `Quote - Espen Olsen.pdf` | A4 portrait, one page, upper-right logo, Costumer/Vendor, ruled terms, grey Description/Unit/Qnt./Price/Sub total table, note, total, signature/footer; no VAT | No corresponding Espen .xlsm in this upload | **APPROVED VISUAL; EDITABLE SOURCE MISSING** |
| Quote (Ruben) | `Quote - Ruben A. Meyer.pdf` | A4 portrait, one page, same quotation family; per-source contact variant and signature graphic | `Quote - Ruben A. Meyer.xlsm` contains VBA but requires regression | **APPROVED VISUAL; FUNCTIONAL QA PENDING** |
| Packing List (Espen) | `Packing list - Espen Olsen.pdf` | A4 **landscape**, one page; shipping/delivery columns; packing and freight metadata; Ordered/Delivered/Remaining/Weight/sub total Weight; note and footer | Matching .xlsm present, contains VBA, requires regression | **APPROVED VISUAL; FUNCTIONAL QA PENDING** |
| Packing List (Ruben) | `Packing list - Ruben A. Meyer.pdf` | A4 landscape, same geometry, source contact/mark variation | Matching .xlsm present, contains VBA, requires regression | **APPROVED VISUAL; FUNCTIONAL QA PENDING** |
| RFQ | `RFQ - Template_v3.0_2024.pdf` | **NOT A VALID RFQ PDF**: rendered page is pixel-identical to uploaded PO and is titled **Purchase Order** | `RFQ - Template_v3.0_2024.xls` distinct OLE file; RFQ target-sheet extraction not validated | **PENDING_REVIEW**; use registered 05B RFQ master and established RFQ workflow until correct RFQ preview is confirmed |
| Invoice | **Not supplied** | Existing separately approved invoice family only | No revised invoice editable source supplied | **NO CHANGE**, pending operator invoice template |

## 2. Differences versus superseded or pending instructions

1. **PO:** the selected PO intentionally includes Address and Website QR codes plus Delivery information and Purpose of use. These displace the older 05C no-QR Terms and conditions standard visually. The new PO title and layout should be matched for future POs after the exact reusable editable source is verified. Do not combine both sets of regions on one page.
2. **Quotations:** preserve the source label `Costumer`, total placement, signature/footer geometry and source-specific contact variant. Do **not** reuse the exemplar's visible `Approved` status as authorization for a new transaction. The 16.11.2026 pre-discount Price / net Sub total rule still controls the formula and export; no VAT line or VAT statement.
3. **Quotation signer ambiguity:** the Ruben-named quotation shows Ruben as vendor attention/contact but the bottom signature artwork identifies Espen. Do not infer the authorized signatory from filename, contact or artwork alone. **PENDING_REVIEW_Q-SIGNER** for future signatory selection. The Espen-named reference is not permission to send via Gmail on Espen's behalf.
4. **Packing Lists:** selected A4 **landscape** overrides any generic A4-portrait defaults. Ordered, Delivered, Remaining and weights must come from verified records; sample shipping date, parcel counts, weights, freight and Incoterms do not become default facts.
5. **RFQ:** separate filename is not enough to establish a distinct visual source. The uploaded PO/RFQ PDFs have different byte hashes but produce the **same rendered pixels**, and both are titled Purchase Order. Do not label the PO design as a verified RFQ layout.
6. **Technical font evidence:** the PO PDF embeds Libre Baskerville variants and also Calibri. The operator-approved appearance, not an untested assertion that every glyph uses exclusively Libre Baskerville, is the accurate observation. Preserve visually while flagging the conflict with the 05C all-Libre rule.
7. **Product naming:** sample text is historical transaction evidence. For new documents use current approved names (e.g. Hirec-R, Hirec PFW9 water-based, Hirec PFS10 solvent-based); do not import historical product nomenclature from the sample.
8. **Invoice:** apply current approved 07.11.2026 invoice design and tax/filing workflow; no new uploaded invoice visual was reviewed.

## 3. Functional Excel inspection and STOP rules

Source workbook package read-only inspection:
- Ruben Quote .xlsm and both Packing List .xlsm contain a VBA project, 11 worksheets including `Quote`, `Packing list`, supporting lists and very-hidden `QuoteLog`; 28 formula elements in the Quote sheet and 44 in Packing list; seven visible drawing-bearing sheets.
- **Each of the three .xlsm files has cached `#VALUE!` at `Quote!AA34:AA36`.** The affected cells require cause analysis, formula recalculation, and current Excel QA. Do not claim PASS simply because the rendered PDF appears sound.
- **VBA project hashes are different** from the registered August 05B masters; byte preservation of the August VBA cannot be asserted, and run-time functionality is untested.
- Legacy `.xls` files are OLE/BIFF and do not expose an OOXML `xl/workbook.xml` package; no reliable claim was made about macros/formulas/individual-sheet rendering. Their differing file hashes do not prove RFQ/PO functional validity.
- No native Microsoft Excel macro execution took place. **No replacement XLTM / XLSM master has been promoted.** No original Drive file was overwritten.

## 4. Approval and versioned migration gate

1. Securely register the exact uploaded source PDFs and workbooks in the NTSN business **Canonical Document Templates** folder only after specific authorized upload action and provider readback. Do not place their raw values, stamps, bank data or customer details in public GitHub.
2. Distinguish **visual reference** (approved where noted), **editable functional master** (not yet qualified), **authorized signer** (separately verified), **commercial transaction** (independently approved), and **external filing/sending** (separate approval).
3. Validate the correct RFQ rendering from its source worksheet; if the RFQ file is actually PO-only, request an independent RFQ specimen.
4. Validate Workbook-level calculations, cached errors, VBA/button execution, validation lists, print areas, PDF A4 shape geometry and source-to-preview fidelity **for each variant** before replacing registered 05B masters.
5. Keep the invoice family on the existing approved standard until a new invoice source is explicitly submitted and accepted.
6. Update 05B/05C, the registered template inventory and 05D only through approved, diff-reviewed, versioned changes with readback. This file records the newer operator-selected visual preference but **is not proof that older master files were physically replaced**.

**Data handling:** public GitHub contains only source filenames/technical findings, not raw uploaded files or any customer-specific values. The original attachments remain at their controlled conversation source until separately stored. No external email, invoice issue, Drive overwrite, or accounting mutation is authorized by this approval.
