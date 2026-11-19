# 05D — NTSN Unified PO, Quotation, RFQ, Packing List and Invoice Playbook — 13:32, 19.11.2026 (Europe/Madrid)

**Status:** CONSOLIDATED CANDIDATE / PENDING_REVIEW FOR CANONICAL PROMOTION.
**Authority sought:** operator's explicit 19.11.2026 consolidation instruction, subject to prior APPROVED/CANONICAL scope rules and source verification.
**Scope:** NanoTech Solutions Norway AS (NTSN) commercial document drafting, source population, design fidelity, output, validation, Gmail attachment and approved Drive filing. **No automatic sending, invoice posting or commercial release.**
**Work ID:** EA-COMM-DOC-20261119-01.
**Implementation principle:** ONE governance entry point, **FIVE distinct document families**, each with its own controlled layout and functional master. A PO, quotation and invoice must be consistent *within its own document class*, not visually identical to each other.

## 1. Invocation, authority and source selection

On every request for **PO/Purchase Order**, **Quote/Quotation** or **Invoice/Faktura**, invoke this playbook without needing a reminder. Determine document type before selecting the master, and stop if the action would cross from one type into another without a separate instruction.

Precedence:
1. Current explicit operator instruction, including an explicitly selected alternative reference for that transaction.
2. The applicable APPROVED/CANONICAL document-specific rules and latest scoped amendments (listed below). **Until this playbook is separately approved, those source rules remain controlling.**
3. Exact registered canonical template/master, visual reference and company-approved logo/signature.
4. 05A document recreation/conversion/static rules; 05B Excel master functions where applicable; general Ea source/approval/confidentiality controls.
5. Latest verified commercial transaction evidence (quote/order/PO/RFQ), relevant entire Gmail conversation including SENT responses and attachments, approved product/price/customer registers and current records.
6. Older chats, examples and files as historical evidence only.

Preserve exact source values and signatures; do not silently import transaction data from examples. For material conflicts use latest verified approved scope authority; otherwise **PENDING_REVIEW** with source, date and revision. A newer filename alone does not establish a new master. The Google Drive business location index is navigational only: verify current Drive file identity/metadata/parent/content before reliance. Do not mix NTSN with a different legal invoice identity.

## 2. Shared invariants — apply to all three types

**Template lock.** Begin from the current designated master or approved reference; use a controlled working copy. Do not improvise a fresh generic PDF, PowerPoint, Canva, HTML or Word layout when a canonical master exists. Preserve page footprint, margins, line rules, section order, table columns, borders, padding, row heights, line breaks, headers/footers, logo anchor, hyperlinks, typography, ink colors, note box, signature position and pagination. Changes to static design require a separately reviewed master revision, not ad hoc edits per transaction.

**Source/value lock.** Only transaction-specific fields may change: document number/date, legal parties and contacts, PO/quote/order references, verified addresses, delivery/incoterms/lead times, product identity and variant, unit/net quantity, unit of measure, unit price, approved discounts/charges, tax where relevant, currency, authorized signatory and verified terms. Confirm all current details from the actual source; unresolved values remain visibly unresolved internally and prevent release. Never substitute zero/N/A/TBD as if confirmed. No example's invoice number, bank details, sender, destination or supplier quote may become a default.

**Brand lock.** Use the correct NTSN logo from the governing template and preserve its size, ratio and position; do not reconstruct a near match or introduce a second logo. Use the appropriate exact authorized combined stamp/signature asset once, aligned on its signature line; never counterfeit, crop, combine or duplicate marks. Ruben A. Meyer / CTO and Espen Olsen / Account Manager are selectable *only when current transaction authority and validated asset permit*. Signature labels alone do not prove signing authority. Never store signature assets in public GitHub.

**Type lock.** Match the font family, permitted regular/bold/italic variants, point sizes, line spacing, link color/underlining, numeric formats and spelling of the selected canonical template. **Libre Baskerville** is mandatory for 05C PO and the approved quotation family; invoice text follows its own verified approved invoice reference (do not silently substitute the PO/quote font if the approved invoice differs). For a selected template, do not mix font families or create one-off smaller/bolder fields.

**Content lock.** Use SiO₂/TiO₂ and the approved product names (Hirec-R, Hirec-RAS, Hirec PFW9 water-based, Hirec PFS10 solvent-based, VitaCoat, SurfaceGuard-X/T, SolarEX Quartz SiO₂, SolarEX Titan TiO₂) according to the actual product boundary. Legacy aliases may be used for source retrieval or when needed for supplier order-line traceability; **never expose manufacturer/original brand to end customers** unless operator explicitly authorizes that disclosure. Supplier-directed POs may retain the supplier's exact ordering name/SKU when operationally necessary; do not rewrite it into an ambiguous product.

**Commercial lock.** Independently reconcile line amount, discounts, freight/packing/handling once each, rounding, decimal precision, currency, subtotal, tax (invoice only) and total. Use precise decimal arithmetic rather than visible spreadsheet rounded text alone. Do not convert physical product allowance into discount, freight into product cost, or an indicative quote into an accepted order. Pricing, warranty, MOQ, logistics, customs, environmental/efficacy claims and Incoterms commitments require source verification and proper approval.

**PDF lock.** Render the *actual output PDF*, not a screenshot of an editor, at 150–200 dpi or higher and inspect the full page and relevant details. Validate embedded/available fonts, page count and A4 portrait geometry (595.276 × 841.890 pt), exact logo visibility, single correct signature, grey rules/dividers, notes, links, metadata, table rows, glyphs and no clipping/overlap. If PDF disagrees with source, repair source, re-export and compare again. Return `PASS`, `PASS WITH WARNINGS` or `FAIL`; any material missing field/visual issue means not complete.

## 3. Purchase Order — locked PO standard

**Primary governing rule:** `active-source/05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md` (APPROVED/CANONICAL, 09.09.2026). **Canonical fixed-layout visual reference**: `EA_CANONICAL_PO_LAYOUT_REFERENCE_v2.0_09092026.pdf`, Drive ID `1NliiqekZMO6Uii8vTXSs11aoFylXZ8CA`. **Header logo**: `EA_CANONICAL_PO_TOP_RIGHT_LOGO_v2.0.png`, Drive ID `1V4KpZwpXteMHVOAFsZh68bc6juDtfAmq`. **Functional editable** master (only when Excel PO is required): `EA_Template_PO_v1.0.xltm`, sheet `PO`, Drive ID `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM`; retain hidden RFQ dependencies, formulas, validation, controls and VBA.

**Final default**: one intended A4 portrait page; `Purchase Order` upper left, **one** canonical logo upper right; PO ref/date beneath header; Customer (Invoice) and Vendor blocks; quote/PO/vendor metadata; two-column `Terms and conditions` with a thin grey divider **under every row including Lead time**; grey-header `Items` (`Description | Unit | Qnt. | Price | Sub total`); right-aligned `Total order value`; lower-left `Note` box as applicable; lower-right authorized signature aligned **directly on signature line**; `Main Office` footer lower left. No extra lower-right logo. 05C's default final PDF does **not** include Address/Website QR codes; 05B does include them in the legacy Excel template.

**Typography**: Libre Baskerville Regular/Bold/Italic only, 18 pt bold title, 12 pt bold section headings, approximately 9.96 pt body and 8.04 pt compact metadata/signature/footer; preserve actual reference geometry. Authorized Ruben A. Meyer combined mark approximately 45 mm wide, handwritten baseline touching the grey signature line.

**Transaction source**: exact latest supplier quote for the ordered configuration, subsequent confirmed supplier correspondence and explicit operator overrides. Include separately quoted packing/delivery/handling lines and correct symbols (e.g. JPY ¥). PO ref must use established sequence and be consistent throughout. Show draft/proposed status if supplier quotation/prices/acceptance remain unconfirmed. **Do not infer** PO issue or supplier acceptance from a PDF or Gmail draft.

**19.11.2026 exception evidence**: a newer one-page approved-for-specific-draft supplier PO visual example (Gmail attachment with a delivery-information section, two QR graphics and `Purpose of use` box) is **not** evidence that 05C's default final-PDF rule has been globally superseded. The alternative is `PENDING_REVIEW_PO_LAYOUT` until explicitly designated as the permanent master. This unresolved conflict must be exposed whenever an operator requests this newer design as the universal default.

## 4. Quotation — locked quotation standard

**Primary governing source**: `docs/approved/EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md`, including operator-approved 07.11.2026 visual adoption and **16.11.2026 mandatory fidelity/arithmetic gate**, plus `docs/approved/EA_QUOTATION_DISCOUNT_APPLICATION_RULE_2154_19082026.md` and `docs/approved/EA_QUOTATION_TEMPLATE_AND_DRIVE_FILING_WORKFLOW_1120_02082026.md`. **Registered editable master**: `EA_Template_Quote_v1.0.xltm`, sheet `Quote`, Drive ID `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv`, with preview ID `1zeaE_REXzfI6L0qJBt4hDsytWtjUzAwu`. The register identifies its provenance as `Quote (Espen Olsen) - v5.38.xlsm`; older workflow also names `Quote - v5.31.xlsm` and 2026 ITYCS guideline PDFs. **These differing provenance/version references do not authorize switching to an unvalidated v6.x workbook**. Preserve full workbook dependencies and use only the Quote sheet for the final PDF.

**Layout**: A4 portrait, one page when possible; `Quote` upper left; date and small NTSN logo upper right; exact side-by-side `Costumer` and `Vendor` blocks (retain the approved spelling `Costumer`); ruled `Terms and conditions`; grey-header `Items` table (`Description | Unit | Qnt. | Price | Sub total`); intact grey dividers between **every item row**, especially product→freight; lower-right `Total order value`, bordered lower-left `Note:`, approved lower-right combined signer/stamp, lower-left `Main Office`. No large `QUOTATION` banner or invoice summary. Preserve Libre Baskerville, source link blue/underline, original margins and logo line clearance from the selected approved reference. **Note text flush left**, uniform font and line spacing, fully inside border. No internal SKU in item description unless requested.

**Discount precedence**: the **latest 16.11.2026 scoped display amendment** requires `Price` to show the **pre-discount unit price**, `Sub total` to show quantity × that price minus approved discount, and total to sum net lines; the `Discount` field displays the actual approved percentage exactly once, in regular weight with one % sign. The older 19.08.2026 discount workflow instructs a reduced displayed unit price in some scenarios: **do not silently combine these conflicting presentations**. Apply the latest specific 16.11.2026 quote display rule for current examples; record `PENDING_REVIEW_DISCOUNT_SCHEMA` when the functional workbook formula or a deal's approved commercial terms cannot reproduce this representation. Product-only discounts exclude freight/handling/DG unless specifically approved. Do not create a negative discount item. Round each displayed amount consistently with the selected currency; verify the line and net total mathematically. Distinguish cumulative display discount from mathematically effective discount.

**Quote-only tax treatment**: **no VAT/tax line, statement or VAT-excluded note** in quotations. `Quote approval` is an existing **document field** and is not the same as internal commercial approval. Keep internal `PENDING_REVIEW` until release authorization. Transport/carrier, FCA cost allocation, supply conditions, discounts and note text remain transaction-specific. When expressly instructed, preserve exact statement such as `Transport costs are excluded.`; never make it a permanent term across other quotes.

**Export and reference**: edit/validate XLSM or approved spreadsheet first, export only `Quote`, never directly patch PDF as the routine authoring method; preserve macro/formula/styles and print area. Filename stem **exact quotation reference only** (e.g. `REF-YYYYMMDD-01.pdf`); no `Quotation -`, customer name, FINAL, _v2, REVISED. Any approved in-place correction keeps existing reference/Drive file ID; a new commercial issue gets the next sequential reference.

## 5. Invoice — locked invoice standard

**Primary governing sources**: `docs/approved/EA_INVOICE_APPROVAL_AND_DRIVE_FILING_WORKFLOW_1153_02082026.md` with **07.11.2026 visual/VAT amendment**; NTSN Drive `NTSN Invoice Generation Operating Standard — 14:10, 28.07.2026` (document ID `1ZSNKXzmoZSWlSi0b3GjC22WYhhbUPkV8-kBdL6jtn5Q`). **NTSN-only** reference family `Invoice15xxx.pdf` / `Faktura15xxx.pdf`, including `Invoice15159_Minze_Health_v4.pdf` as transaction-specific visual evidence (Drive ID `12JSa4t8fDlYhhUh4f2jCw3w-tiDgsNFU`). **Never** adopt Onyx Scandinavia invoice identity, layout, seller or payment details.

**Layout**: one-page A4 portrait where feasible; NTSN wordmark/logo at **upper left**, issuer and invoice metadata upper right, recipient and relevant quote/PO reference block left; compact invoice/delivery/due-date metadata; full-width line-items `DESCRIPTION | PRICE | QTY. | DISCOUNT | VAT | AMOUNT`; separated VAT rate/base/amount and Net amount/Total due; payment-information block in the approved lower-page location; statutory/legal footer and page number. Credit notes use matching family but correct credit-note wording and signed amount; do not call a credit a quote or vice versa. Preserve the exact typography and margins of the selected current NTSN invoice sample, not those of the PO or quote.

**Accounting facts**: Invoice number comes **only** from the current accounting register/system or an explicit authorized operator assignment; do not derive the next number by incrementing a historical PDF. Verify invoice language (English/Norwegian), customer legal entity, verified billing/delivery/contact, current prices/discounts, source order/quote, invoice and due dates, currency, Incoterms, exchange rate/VAT basis where required and **approved current NTSN payment details from a controlled source**. Never expose live payment details in GitHub. New invoices remain draft until explicitly approved. No Conta/ledger posting by document generation.

**VAT**: invoices only. Domestic Norway normally 25% **when current product/transaction tax treatment confirms standard rate**; other treatment must be evidence-based. For foreign recipients, **0% only after confirming foreign status and transaction-specific legal/export treatment**, not merely a foreign address, currency or language. Show base, VAT rate and VAT amount consistently, including NOK basis only if supported by approved accounting convention/source. Uncertain classification -> `PENDING_REVIEW_TAX` + qualified accounting review, no issue.

**Filename**: accounting-controlled `Invoice[Number].pdf` or `Faktura[Number].pdf` exactly; no customer, date, FINAL, _v2 or REVISED suffix. Keep original source separate; do not overwrite issued invoices, create an arbitrary number or imply a posted invoice.

## 6. Drive working areas, filing and Gmail

**Canonical template directory:** `Canonical Document Templates` Drive ID `19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`. **Commercial root:** `Quote & Invoice` Drive ID `1hkq3P-zfEutnwev9cduc1SQGshil3iN8`; subfolders: `PO` ID `1ozfYyGfU8vTbtojv9NBoXVK3cqCTR9RT`, `Quote` ID `1imwSEdP7k4GoWmv9aUf_FvwTtueBF-YR`, `Invoice` ID `17UTt1HjdaThZeu844NcKsNq4ygOhC8gX`, `00_Pending_Review_Quotation_Drafts` ID `1YX9JAJIg3gqVoeh3yXRO89rz3vbsdtnb`, and `Instructions & Validation` ID `10hAW4_V20Hv4eNWJzdEgw1x4rrXeApOP`. All IDs must be revalidated live before write.

Draft quotes stay in the controlled pending working folder, **not** customer-approved archives. After explicit commercial approval, locate the customer's existing child folder under the correct Quote/Invoice root; only create a missing company folder after authorized filing and verified identity. Preserve the exact canonical filename. PO supplier order archive uses the PO route only after appropriate PO filing/issuance authority; never file a supplier PO as a quotation or invoice.

Before creating/update of a Gmail draft, inspect **complete relevant thread, SENT replies, earlier drafts, attachments and authoritative recipients/CC/alias**. Preserve threading and the existing in-thread draft where appropriate; honor suppression of known operator-deleted drafts, unless a new explicit instruction authorizes that specific draft. Document and attachment must be verified as matching **exact filename**; PDF file existence is not proof of attachment. Do not claim a file is attached until provider readback confirms. Do not hand-add Gmail signature. **No send/forward without explicit authorization.**

For file update, verify account, Drive ID, folder parent, revision and access; make bounded write once, then reread file contents, filename, size and parent. In-place replacement only when expressly allowed; no blind overwrites, extra archives, root uploads, sharing or permissions changes.

## 7. End-to-end generation state machine

1. **DISCOVER** — classify document type and authority; resolve exact latest approved rule/template, source revision, user instruction, transaction and storage.
2. **EXTRACT** — read full relevant correspondence including SENT and attachments, current product/price/tax/company records, exact source quote/order and any case-specific corrections.
3. **PREPARE** — choose and clone fixed template in controlled workspace, lock immutable static design, mark every transaction variable and unresolved value; record source revision/approved signatory.
4. **POPULATE** — modify only variable fields, preserve workbook formula/VBA/validation, use correct company identity/approved language/product names.
5. **CALCULATE** — independent decimal ledger for each item, discounts, freight, handling, VAT where applicable and total; verify currency/rounding/formula outputs.
6. **RENDER** — export from validated source to requested editable and A4 PDF; confirm exact layout against **that document class's canonical** visual reference.
7. **VALIDATE** — complete content + visual + commercial + source authority + attachment/folder checks and classify PASS/PASS WITH WARNINGS/FAIL. Correct and re-render any failed output.
8. **APPROVE** — source/design approval is independent of commercial-content approval, signature authorization, external issue and accounting posting. Keep drafts unsent/unissued until authorized.
9. **FILE / DRAFT MAIL** — after approval only, verified Drive recipient folder/reference, archive readback and Gmail draft attachment identity; never infer sending.
10. **LOG / CLOSE** — one redacted per-workstream append-only event ledger with precondition, source SHA/revision, actor/tool, exact effect, idempotency, after-state readback, error and open actions; mirror only a sanitized approved pointer to AI-Memory-Vault.

## 8. QA acceptance matrix (per generated document)

| Gate | PO | Quote | Invoice |
|---|---|---|---|
| Master identity and selected source revision verified | 05C PDF/05B Excel | XLTM Quote sheet + reference PDF | NTSN-only invoice family |
| A4 portrait, intended page count, no clipping | Required | Required | Required |
| Exact logo visible in correct header position, no duplicate | Top right | Top right | Upper left |
| Source font family/size, spacing and link treatment preserved | Libre Baskerville | Libre Baskerville | Own invoice reference |
| Header/body/terms/rows/totals/note/footer geometry | 05C | Quote reference | Invoice reference |
| Correct signature asset/line placement | 05C authorized | Authorized source only | If reference calls for one |
| Item identities, quantities, pre/post discount, currency and totals independently checked | Required | 16Nov display, source-approved discount | Required with VAT |
| VAT presentation | Only if explicitly sourced for PO; no inference | **Never** | **Only invoice**, confirmed treatment |
| Appropriate approval/issue status | Draft if unresolved | PENDING_REVIEW until approved | Draft until approved / accounting gate |
| Exact reference-only filename and correct Drive destination | Established PO scheme | Quote ref only | Invoice/Faktura number only |
| Gmail attachment confirmation / no unapproved send | Required if mailing | Required if mailing | Required if mailing |
| Provider readback / audit work-ID | Required for writes | Required for writes | Required for writes |

A checklist tick or a successful connector response without rendered visual comparison is **NOT_VERIFIED**, not PASS. Do not publish/issue a FAIL. `PASS WITH WARNINGS` is not a commercial release authorization.

## 9. Sources of truth and change-control register

- [05A static rules](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/active-source/05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md) — generic template and preservation contract.
- [05B registered functional XLTM use](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/active-source/05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md) — all four workbook template families, including legacy PO Excel QR layout.
- [05C current PO PDF standard](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/active-source/05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md).
- [Canonical template register](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/registers/EA_CANONICAL_DOCUMENT_TEMPLATE_REGISTER_0405_08082026.md) and [PO register](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/registers/EA_CANONICAL_PO_DRAFTING_STANDARD_REGISTER_0219_09092026.md).
- [Quotation generation and 16Nov amendment](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/docs/approved/EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md), [discount rule](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/docs/approved/EA_QUOTATION_DISCOUNT_APPLICATION_RULE_2154_19082026.md), [filing](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/docs/approved/EA_QUOTATION_TEMPLATE_AND_DRIVE_FILING_WORKFLOW_1120_02082026.md).
- [Invoice approval and November amendment](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/blob/main/docs/approved/EA_INVOICE_APPROVAL_AND_DRIVE_FILING_WORKFLOW_1153_02082026.md); private Drive NTSN Invoice Generation Operating Standard, revised 07.11.2026.
- 06.11.2026 `EA_QUOTATION_PLAYBOOK_ADDENDUM_20261106_PENDING_REVIEW.md` and transfer report: evidence-only proposals; do not silently promote the specific 10px logo clearance or other pilot calibration as global authority.
- 11–19.11.2026 Gmail and ChatGPT PO/quote corrections: evidence of local use/defects, not a standing layout promotion without confirmation; no customer terms/prices imported into this public playbook.

## 10. Open conflicts / PENDING_REVIEW (not silently promoted)

| ID | Evidence tension | Governing treatment now | Required resolution |
|---|---|---|---|
| P-01 PO QR/delivery/purpose layout | 05C default excludes QR and uses Terms; the operator directly approved the new QR/Delivery/Purpose PO PDF as visual template on 19Nov | **19Nov operator-selected PO visual governs the new review layout**; August/September Excel/PDF master revision and migration still pending | Register approved PDF in controlled Drive, qualify editable source, version/merge successor to 05C |
| Q-01 Pre-discount vs net unit price | 19Aug discount rule sometimes changes displayed Price; latest 16Nov approved quote rule shows pre-discount Price with net Sub total | Apply **16Nov display rule**; validate each workbook formula | Confirm reusable discount formula/schema matches selected master |
| Q-02 Workbook lineage | 05B XLTM traced to v5.38; older quote workflow names v5.31; unverified later v6.x may exist | Registered XLTM + approved example control; do not auto-switch to v6.x | Verify latest official master and regression test Excel macro/function |
| Q-03 Pilot layout calibration | 06Nov 10px logo clearance addendum is explicitly pending | Follow exact selected approved source, no blind 10px constant | Owner promotion only after visual comparison |
| I-01 Invoice master/editable file | Approved invoice family and sample exist; no current signed-off master DOCX/XLSM identified in this pass | Use NTSN 07Nov invoice reference layout and controlled PDF/DOCX draft | Register an exact immutable invoice master revision and visual QA |
| R-01 Individual documents/signers | New PO/quote examples contain multiple signer choices and variable legal/header addresses | Per-template authorized controlled mark + current company identity, verified for each transaction | Validate signer and company legal/footer fields before release |
| F-01 RFQ revised visual source | Original RFQ PDF mistakenly showed PO, but follow-up `(1)` PDF correctly shows **Request for Quote (RFQ)** with distinct layout and metadata | **RFQ corrected visual VERIFIED**; 05B functional XLTM remains operational until the new workbook passes security and Excel validation | Validate changed VBA streams, Excel formulas, PDF export, Drive source ID before functional replacement |
| F-02 Workbook cached errors/VBA drift | Uploaded three .xlsm contain cached Quote!AA34:AA36 #VALUE! and changed VBA hashes | Approved visual only; **functional master promotion BLOCKED** | Excel runtime formula/VBA regression, secure master replacement |
| Q-04 Selected contact and signer variants | Ruben quote PDF vendor attention differs from bottom signature identity; Espen editable XLSM not uploaded | Preserve variants as visual evidence, do not infer authorized signing identity | Verify signed artwork ownership and source per variant |
| P-02 Packing List orientation | Two newly selected operator references are A4 landscape, not generic portrait | Apply **A4 landscape** to both packing-list variants | Register both PDF variants and validate corresponding workbook exports |

**Until these items are resolved, this playbook is an integrated implementation candidate only; it must not be described as superseding the approved 05A/05B/05C or quote/invoice authorities.** When approved, promote it through an operator-verified decision, update the master index and register, validate one synthetic PO, quote (including discounted quote) and invoice (domestic and export), and record GitHub/Drive readback. No customer document issue or external posting is authorized by playbook approval alone.


## 11. 19.11.2026 operator approval — PO, Quote, RFQ, Packing List source reconciliation

**Approval event:** operator explicitly states "Approved templates attached"; see **[05E operator-selected visual sources](./05E_NTSN_OPERATOR_APPROVED_TEMPLATE_SOURCE_SELECTION_20261119.md)** and **[source evidence register](../registers/EA_OPERATOR_APPROVED_COMMERCIAL_TEMPLATE_SOURCE_EVIDENCE_20261119.md)**. The uploaded samples control only their verified visual family and not any embedded customer/transaction values.

- **PO:** use the approved **QR / Delivery information / Purpose of use** A4 portrait reference as the visual target. This directly selects the alternative that P-01 previously lacked. Do not mix with the 05C Terms-grid/no-QR layout; maintain 05C as historical authority until version-controlled successor is reviewed and the new source is registered in Drive. Loaded .xls functional parity is NOT_VERIFIED.
- **Quote:** use the two approved A4-portrait contact variants (Ruben / Espen), preserving `Costumer`, ruled Terms, item table, lower-left note, signature line, and current discount-display instructions. A previous sample's `Approved` cell does not approve subsequent transactions. The Ruben contact sample contains an Espen bottom signatory; **signer mismatch pending review**. Espen .xlsm missing; Ruben source .xlsm has cached formula errors and a different VBA hash from 05B.
- **RFQ:** the first PDF incorrectly showed a PO. The operator's follow-up `RFQ - Template_v3.0_2024(1).pdf` provides a **visually verified RFQ A4 layout** with Request for Quote heading and RFQ-specific terms. Source OLE workbook has visible RFQ/PO sheets, no cached BIFF formula errors, **but changed VBA modules/project streams** versus prior `.xls`. Use the corrected PDF as candidate visual reference; keep registered 05B production XLTM until Excel runtime, macro security, export fidelity and Drive source registration pass.
- **Packing List:** apply two approved sender/contact variants in **A4 landscape**, with shipper/consignee columns; item columns Ordered, Delivered, Remaining, Weight (KG), sub total Weight (KG); dated/parcel/freight/reference metadata and note. Weight and shipping facts must be independently sourced. Both editable .xlsm variants require Excel runtime tests; do not flatten or transplant their VBA blindly.
- **Invoice:** no invoice reference in this batch. The 07.11.2026 approved NTSN invoice workflow is unchanged. A separately approved invoice master and VAT calculation test remain outstanding.
- **General:** original source PDFs/workbooks remain private conversation attachments. No Drive source IDs for the 11 new files have been verified; publishing source hashes/QA metadata in GitHub is not a substitute for controlled archival. No commercial issue, invoice posting, external email, VBA master overwrite or automatic template promotion.

**Technical STOP gate:** In all three uploaded .xlsm files the Quote sheet has cached `#VALUE!` values at `AA34:AA36`. VBA packages are present but differ from the old registered template and have not been run in Excel. Correct/qualify those errors, compare macros with approved baseline and render each target sheet before substituting the files as production masters.

## 12. 13:38, 19.11.2026 — Corrected RFQ attachment reconciliation

The replacement PDF **corrects the earlier source defect**: one A4 portrait page explicitly headed `Request for Quote (RFQ)`, with request date, PO/RFQ references, supplier fields, Terms and conditions, item/total table, Note, signature and footer. The source is transaction-populated and must be converted to variable fields when templating. Read-only OLE/BIFF inspection of matching `.xls` confirms RFQ and PO visible tabs, five total worksheets, 103 formula records, and **zero cached formula-error records**. Several VBA source streams and the Workbook stream differ from the previous upload, so do **not** assume macro code parity or functional safety. No macro execution, registered XLTM update, provider Drive replacement, commercial release or canonical promotion has been performed. The source evidence register and 05E carry the exact hashes and remaining gates.
