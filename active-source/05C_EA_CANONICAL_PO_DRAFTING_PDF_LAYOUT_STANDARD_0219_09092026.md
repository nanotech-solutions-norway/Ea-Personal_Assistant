# 05C — Ea Canonical Purchase Order Drafting and PDF Layout Standard — 02:19, 09.09.2026

Status: CANONICAL / OPERATOR-INSTRUCTED  
Authority: Explicit operator instruction dated 09.09.2026  
Scope: Purchase Order drafting, fixed-layout rendering and final PDF release for Ea

## 1. Purpose and automatic trigger

Apply this standard automatically whenever the operator asks Ea to create, draft, generate, recreate, populate or finalize a Purchase Order / PO, unless the operator explicitly instructs another layout or format.

This standard controls the PO's **drafting logic, A4 visual composition, typography, branding, signature placement and final PDF release**.

The existing `05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md` remains controlling only for retrieval and preservation of the legacy functional XLTM/XLSM workbook when an editable Excel PO is explicitly requested or functionally required.

Where the old PO-specific visual rules in 05B conflict with this standard, **05C controls the final PO PDF**.

## 2. Controlling canonical references

Canonical Drive folder: `Canonical Document Templates`  
Drive folder ID: `19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`

Canonical PO fixed-layout reference:
- `EA_CANONICAL_PO_LAYOUT_REFERENCE_v2.0_09092026.pdf`
- Drive file ID: `1NliiqekZMO6Uii8vTXSs11aoFylXZ8CA`

Canonical top-right PO logo:
- `EA_CANONICAL_PO_TOP_RIGHT_LOGO_v2.0.png`
- Drive file ID: `1V4KpZwpXteMHVOAFsZh68bc6juDtfAmq`

Legacy functional editable template:
- `EA_Template_PO_v1.0.xltm`
- Drive file ID: `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM`
- Target sheet: `PO`

The canonical PDF reference governs **visual layout only**. Its vendor, quotation reference, items, prices, dates, lead time, destination and other transaction values are example/current-transaction data and must never be reused as defaults.

## 3. Source authority for PO content

Populate each PO from the current authoritative transaction source(s), using this order:

1. Current explicit operator instruction.
2. Current supplier quotation or other explicitly designated commercial source for the order.
3. Current verified supplier correspondence where it materially updates the quotation.
4. Current approved product/commercial records where the quotation is incomplete.
5. Unresolved/PENDING_REVIEW field when a required commercial value cannot be verified.

Do not infer or invent commercial values.

When multiple supplier quotations exist, select the quotation matching the exact ordered configuration. Do not combine prices, charges, lead times or terms from different quotations unless explicitly approved.

Operator overrides are transaction-specific unless explicitly promoted to a standing rule. For example, a lead time such as `1 week after payment confirmation` must not become a universal PO default unless separately approved.

## 4. Canonical A4 layout

Final PO PDF:
- Page: A4 portrait, 210 × 297 mm.
- One intended page unless the operator explicitly approves additional pages.
- Use the canonical PDF reference for exact content footprint, spacing, block widths and visual balance.
- Keep all content inside the printable page without clipping, overlap or accidental scaling.

Required section order:
1. Purchase Order title at top left.
2. Canonical PO logo at top right.
3. PO reference and PO date beneath the top-right heading area.
4. Customer (Invoice) block left.
5. Vendor block right.
6. Quote reference / PO reference / vendor email metadata.
7. Terms and conditions block.
8. Items table.
9. Total order value block aligned right.
10. Note box lower left when needed.
11. Signature block lower right.
12. Main Office footer lower left.

Do not place an additional logo in the bottom-right corner.

## 5. Typography — Libre Baskerville only

All visible PO text must use **Libre Baskerville**.

Allowed variants:
- Libre Baskerville Regular
- Libre Baskerville Bold
- Libre Baskerville Italic

Canonical size hierarchy based on the approved reference:
- Main title: 18 pt Bold.
- Section headings: 12 pt Bold.
- Standard body / table / terms text: approximately 9.96 pt.
- Compact metadata, footer and signature labels: approximately 8.04 pt.
- Preserve relative size hierarchy when layout constraints require minor adjustment.

Do not mix in DejaVu Sans, Helvetica, Arial, Times or other substitute fonts in the final PO.

## 6. Terms and conditions block

Use a two-column label/value structure.

Every terms row must retain the thin grey divider line beneath it, including the **Lead time** row.

Typical labels include:
- Quotation ref.
- Payment terms
- Currency
- Lead time
- Quote validity
- Transportation terms
- Delivery
- Packing
- Destination

Values must come from the controlling source or explicit operator instruction.

Quotation reference may use the approved blue emphasis used in the canonical reference. Currency may use Bold.

## 7. Items table

Use the canonical grey-header table with these columns:
- Description
- Unit
- Qnt.
- Price
- Sub total

Rules:
- One row per supplier/source line item.
- Preserve source item order unless explicitly instructed otherwise.
- Use canonical Ea product names in customer-facing descriptions where appropriate.
- Legacy supplier wording may be retained in parentheses where needed for traceability.
- Include the correct currency symbol in monetary fields, e.g. `¥` for Japanese yen.
- Independently validate quantity × unit price and all subtotals.
- Validate the grand total against the controlling quotation/order source.
- Packing, delivery, bank, freight or other charges must be separate line items when separately quoted.

## 8. Branding and logo

Use only the canonical PO top-right logo registered above.

Rules:
- Position in the top-right header area.
- Preserve aspect ratio.
- Do not duplicate the logo elsewhere on the page.
- Do not substitute the older outlined/legacy top-right mark when the canonical PO logo is available.
- Do not add the old bottom-right logo.
- Do not add the old PO Address/Website QR-code graphics to the final 05C PDF unless the operator explicitly requests them.

This final-PDF rule supersedes the older 05B requirement for two PO QR-code graphics.

## 9. Signature block

Use the validated Ruben A. Meyer stamp/signature asset from the canonical PO reference.

Rules:
- Lower-right signature area.
- Signature/stamp must be materially smaller than the historical oversized version.
- Target width: approximately 45 mm.
- Center the signature over the signature line.
- The handwritten signature baseline must sit directly on the grey signature line.
- Do not float the signature above the line.
- Preserve the line beneath the signature.
- Name/title/company remain centered below the line.
- Use Libre Baskerville for signature labels.

Default signature labels:
- Ruben A. Meyer
- CTO
- NanoTech Solutions Norway AS

If the sender/signatory is explicitly different, replace the labels and signing asset only when authorized.

## 10. Reference, currency and date handling

- Preserve the established PO reference-number convention.
- Do not invent a new numbering scheme.
- Display the PO reference consistently in the top-right metadata and PO reference field.
- Use the controlling quotation reference exactly.
- Currency symbol must be shown in all displayed monetary values where appropriate.
- Preserve operator-approved date style and formatting used in the canonical layout unless another format is explicitly requested.

## 11. Final-PDF generation workflow

1. Gather the exact current supplier quotation/order source and any materially relevant updated correspondence.
2. Confirm the ordered configuration, quotation reference, quantities, unit prices, charges, total, payment terms, delivery terms, destination, lead time and validity.
3. Draft the PO into the 05C canonical A4 layout.
4. Apply Libre Baskerville to all visible text.
5. Apply the canonical top-right logo only.
6. Position the validated signature/stamp directly on the signature line.
7. Validate arithmetic independently.
8. Render the PDF.
9. Re-render the PDF to an image and visually inspect the complete A4 page.
10. Release only after the validation gate passes.

If an editable Excel PO is explicitly required, use the legacy canonical XLTM/XLSM workflow under 05B for the editable workbook, but use 05C as the controlling final-PDF visual standard unless the operator explicitly requests the legacy workbook rendering.

## 12. Validation gate

Before release, confirm:

### Content
- correct vendor/customer;
- correct quotation reference;
- correct PO reference/date;
- exact item configuration;
- correct quantities/units;
- correct unit prices and charges;
- arithmetic and total match source;
- correct currency and currency symbols;
- correct payment/delivery/Incoterms/lead-time/validity/destination values;
- no stale transaction values from a prior PO.

### Visual
- A4 portrait and one intended page;
- canonical top-right logo is present;
- no duplicate/bottom-right logo;
- all text is Libre Baskerville family;
- section hierarchy matches the canonical reference;
- every Terms and conditions row has its grey divider line;
- items table geometry is intact;
- no clipping, overlap, broken glyphs or black squares;
- signature is approximately 45 mm wide and sits directly on the signature line;
- note, total and signature blocks do not overlap.

### Release status
Use:
- `PASS`
- `PASS WITH WARNINGS`
- `FAIL`

Do not claim PASS if a material source value or visual requirement could not be verified.

## 13. Precedence

For Purchase Order work:

1. Current explicit operator instruction.
2. `05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md`.
3. Current verified supplier quotation / transaction evidence for factual values.
4. `05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md` for editable workbook retrieval/functionality when applicable.
5. `05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md`.
6. `05_EA_DOCUMENTS_TEMPLATES_REGISTERS_INDEXES.md`.
7. Older supporting files and examples.

Do not silently merge contradictory sources.

## 14. Canonical status

This 05C standard is the current Ea canonical PO drafting and final-PDF layout authority from 09.09.2026 until superseded by a later explicit operator-approved canonical PO rule.
