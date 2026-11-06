# Proposed Ea quotation-generation addendum — 13:09, 06.11.2026
**Status:** PENDING_REVIEW / NOT CANONICAL  
**Work ID:** EA-QUOTE-PLAYBOOK-20261106  
**Applies to:** Ea quotation workflow, not invoices or packing lists  
**Authority:** Current operator-initiated learning proposal, subordinate until separately approved to current canonical quotation generation, filing and discount playbooks

## Purpose
Prevent the failure modes identified in a recent three-quotation pilot: clipping after spreadsheet export, an absent light-grey divider between the first and second items, header logo too distant from the header rule, transient preview links, source/PDF drift, and confusion between customer-facing fields and internal approval controls.

## Compatibility (do not overwrite existing approved rules)
1. Continue using the verified approved `Quote` worksheet from `Quote - v5.31.xlsm`, recent RAW quotation sources, and the operator-designated 2026 guideline PDFs.
2. Generate from the validated spreadsheet source first, not a generic PDF/Docs/Canva mock-up. An overlay repair is an exceptional scoped correction, not the standard authoring process.
3. Preserve the exact original labels `Quote`, `Costumer`, `Vendor`, `Terms and conditions`, `Items`, `Description`, `Unit`, `Qnt.`, `Price`, `Sub total`, `Total order value`, `Note:` and `Main Office`.
4. Before editing a source template, duplicate it into a controlled working copy. Avoid changes to unrelated tabs, master formulas, print area, image anchors or hidden pricing data.
5. Recheck *rendered PDF*, not just the source workbook, at 150–200 dpi and high zoom. Visual QA is a release gate, not optional.

## Table rule and logo regression controls
- The item header must remain grey, with all five approved columns.
- Every line item is separated by the complete matching horizontal grey rule. In particular, verify the divider **between item 1 (product) and item 2 (freight)**: no skipped, shortened, interrupted, overwritten or white-covered segment.
- Validate divider stroke tone, thickness, left/right endpoints and row geometry by comparison with adjacent row rules.
- For the header logo, place the **visible lower edge** about **10 CSS px (~7.5 PDF pt at 96 dpi)** above the header rule, retaining existing right alignment and scale. This specific clearance is an operator-directed pilot calibration; first reconcile with any later approved source template before generalization.
- The rule/date must remain where the template places them. Do not move other elements to mask bad logo placement.
- Verify no text/graphic collisions or off-page export, especially Notes, Main Office footer and signature.
- Render actual PDF(s) anew after each source change and compare side-by-side with the approved primary references.

## Commercial calculation gates
- Preserve canonical product naming (including `SolarEX Quartz SiO₂`, `SolarEX Titan TiO₂`) and distinguish product formulations.
- A physical quantity allowance (e.g. 15% extra product) is **not** a discount nor a 15% price increase.
- Confirm the current, dated, product-specific, customer-applicable list/offer price; an old pilot discount must not automatically become the base list price.
- Discount belongs in the existing Terms `Discount` row and applies only to the operator-approved items. Do not discount freight, DG, packaging or handling without explicit approval.
- Freight and handling are independent line items when explicitly required; never invent a carrier quote, parcel count, fuel surcharge, DG acceptance or customs/tax obligation.
- A case-specific handling amount or lead time is **not automatically a universal default**.
- When an FCA Incoterm 2020 quotation also lists freight, flag the delivery/risk/cost allocation for commercial/logistics review before external issue.
- Owner SPV, plant ownership and VAT references belong in the **Note box**, not in extra product rows, when the operator directs that structure.

## Approval split
- `Quote approval` is a **customer-visible value field** within the quotation, editable according to explicit current instruction (e.g. `Upon payment confirmation`).
- `PENDING_REVIEW` is the **internal** gate for actual commercial approval, pricing/claims verification, external issue, filing and sending. A positive-sounding customer-visible field does not bypass it.
- Never send, externally share or make a legal/commercial commitment without appropriate explicit approval.
- Any quotation visual approval does not approve its commercial values.

## Output and filing
- Customer quote reference-only basename for source/PDF; no `FINAL`, `_v2`, recipient, date suffix or `Quotation -` additions.
- Drafts stay private; **after** commercial approval file in the verified recipient-company subfolder beneath the canonical quotation root; do not file drafts there simply to have a place.
- After authorized in-place correction, confirm the same file ID only when explicitly intended and verify parent, contents and size by Drive readback.
- For private transfer packs and internal reports, descriptive package names are allowed; do not confuse them with customer quotation filenames.
- Public GitHub contains only process rules, synthetic examples and redacted ledgers. Never store real customer, partner, pricing, shipping, private signatures or confidential PDF examples in the public repo.

## QA matrix
| Acceptance test | Required evidence |
|---|---|
| A4 portrait, one page | PDF page geometry (595.3 × 841.9 pt), rendered page |
| Fonts | Libre Baskerville (unless explicitly approved variation) |
| Logo clearance | Visible lower edge around 10 px above header line, matched to approved source |
| First product→freight divider | Full-width visible grey line at expected template row boundary |
| All further row rules | Continuous, comparable stroke |
| All terms | Correct text fields and no clipping |
| Product amounts | Independent price×quantity Decimal check |
| Freight and handling | Once each, provisional where applicable |
| Note | All relevant wording visible inside box; owner SPV/VAT if required |
| Signature and footer | Present, authorized, not clipped or duplicated |
| Approval | Internal PENDING_REVIEW maintained until sign-off |
| Storage | Exact filename and Drive parent/permissions verified after write |

## Transfer/replication
The private transfer pack is a reference implementation and recovery dossier. It includes the approved source workbook, the latest locally verified quotation PDFs, synthetic examples, source-data schema, Python arithmetic/QA tools and manual Excel export instructions. It does **not** distribute proprietary fonts or imply a new system has deployment authority.

## Pending review items
1. Operator review to promote this addendum or merge the bounded amendment into the approved quotation workflow.
2. Verify all transport tariff quotations and carrier restrictions at actual issue.
3. Confirm whether a current workbook beyond `Quote - v5.31.xlsm` has been formally adopted.
4. Confirm signature asset/reuse authorization for each new external quotation.
5. Maintain one redacted work-ID ledger with write/readback and failure evidence.
