# Ea Quotation Pricing, Margin, Carrier and Fulfilment Disclosure Rule — 12.11.2026

**Status:** MERGED / OPERATOR-INSTRUCTED SCOPED RULE. PR #134 merged to `main` on 12.11.2026 at 13:09:11 UTC; verified main blob `74b18c97a45bde8caad6c79ac573d1c08e3b9dc2`. Adopted for quotation-process routing only; not a blanket approval of prices, products, discounts, logistics or external issue.
**Authority:** Explicit operator instruction dated 12.11.2026.
**Scope:** NanoTech Solutions Norway AS quotation generation only. This supplements, and does not replace, the approved quotation, discounted-product, product-knowledge, confidentiality and Drive-filing controls.

## 1. Quote source priority
1. Resolve the latest buyer email and original thread, current product identity and variant, quantity, units, package and intended application.
2. Search the restricted authoritative Ea product-price register for an **exact** active, approved customer price (variant, size, tier, currency, effective date). A dated historic rate is reference evidence, not automatically a current list override.
3. If a price is absent or not appropriate to the requested tier, search approved supplier correspondence and original cost records, preserving intermediary/direct-channel distinction and validity.
4. Record missing prices or relevant dated source evidence in the restricted product register's **Historical Quote Evidence** or scoped pending-review area, with source date, reference, unit, currency, pack/tier and status. Do **not** silently overwrite a general price, invent a manufacturer cost, reuse an unrelated customer-specific price or promote provisional evidence.
5. Do not assume product identity, availability, concentrate/RTU interchangeability or functional equivalence from names alone.

## 2. Comparable historical gross-margin method
When the operator asks to repeat the margin from a comparable prior sale, reconcile the historical customer-facing **net unit selling price** against the verified supplier channel's net unit cost for the same product, variant, pack/unit and relevant date. Convert to the same currency with a stated reference FX rate and date. Exclude VAT, freight, handling, unusual discounts and other non-product lines unless explicitly included in the approved margin basis.

- Historic gross margin: `m = (net_selling_price - converted_supplier_unit_cost) / net_selling_price`.
- Proposed new net unit selling price for comparable confirmed supplier unit cost `c`: `p = c / (1 - m)`.
- Never substitute a markup percentage (`(p-c)/c`) for gross margin (`(p-c)/p`).
- Preserve exact calculation internally; round customer unit prices first and recalculate displayed subtotals from rounded unit prices.
- Do **not** apply a supplier-derived margin on top of an existing approved customer list price. Never extrapolate margin from unrelated products or from unverified channel rights. Flag material differences as `PENDING_REVIEW_COMMERCIAL`.

## 3. Units, technical scope and risk
A kg request must not be treated as L without a verified product density at the relevant temperature and concentration. For an explicitly illustrative budget scenario, state the assumed density and keep all calculated prices and totals visibly **non-binding**. Separate concentrate from ready-to-use alternatives. Obtain formulation, application method, SDS transport classification, packaging and regulatory/technical compatibility checks before a final commercial issue.

## 4. Carrier quotation and DHL online check
For shipments arranged via DHL, retrieve current DHL online quote/official tariff data using the **actual internal** fulfilment origin and destination, shipment gross/volumetric weights, piece/pallet dimensions, packaging, DG classifications/UN details, service and shipment date.
- Prefer a live carrier quote with validity, inclusion/exclusion breakdown and account rate when available.
- Published service guides and tariff tables are **reference-only**; explicitly flag all unverified actual weight, fuel/seasonal surcharges, DG, customs, taxes, handling and booking acceptance. Do not present a calculated base tariff as a live, accepted freight price.
- Do not use a normal parcel service merely to bypass DG restrictions. Request qualified DG/transport review when applicable.

## 5. Customer-facing source disclosure
For operator-directed drop shipments, omit the subcontracted origin company's **name and street address** from the **customer-facing quotation** unless the operator directs otherwise or disclosure is legally required. Preserve the seller's verified identity. Use only verified, accurate carriage terms. **Never** falsify, omit or alter legally required consignor, origin, exporter or carrier information in transport, customs, commercial invoice or regulatory documents; those disclosure requirements prevail.

## 6. Approved quotation and Gmail gates
Use the current approved quotation workbook/source and Quote worksheet first where available; preserve one-page A4 source layout, fields, notes, total arithmetic, signature authorization and approved naming. Render and visually inspect the customer PDF. Keep supplier costs, comparable customer source sales, margin calculations and partner identities in private internal evidence, never in a public repository or customer quote.

Update the existing Gmail draft in place when possible, preserving thread and recipient. A quotation with unverified supplier/product/transport terms must remain `PENDING_REVIEW` and may not be sent, shared or filed as an approved quotation without explicit owner approval. Public GitHub holds only the redacted process rule and source pointers; the private price register holds numeric source evidence.

## 7. Audit and conflict handling
Use the existing per-workstream operational ledger with redacted event IDs and verified readback. If a higher-level approved workflow or product source conflicts with a case, stop the affected claim and place the precise disagreement in scoped `PENDING_REVIEW`; do not merge contradictory rules silently. This rule does not approve future offers at any fixed margin.
