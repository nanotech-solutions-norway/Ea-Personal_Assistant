# Ea Product Register — Source Import Governance

Status: DRAFT / PENDING_REVIEW | 16 October 2026
Classification: PUBLIC METADATA AND SCHEMA ONLY — NO PRIVATE CUSTOMER, CONTACT, FINANCIAL, PRICING, OR SHIPMENT ROWS.

## Import and reconciliation
- Source: operator-provided product accounting/billing CSV, preserved verbatim in restricted Google Sheets.
- Preserve source product number, original text, VAT fields, historical sales counts, and revenue as source evidence only.
- Price fields in a historical billing CSV are not approved current selling prices, price commitments, cost bases, tax advice, or public price lists.
- Do not infer currency, stock on hand, delivery performance, warranty, available quantities, or current fiscal settings from the CSV.
- Use a stable internal product-record ID distinct from SKU; missing and duplicate SKUs are possible.
- Reconcile product variants with Ea Product Knowledge Master and the approved Product Truth archive before canonicalizing any technical attributes.
- Canonical product naming for customer-facing drafts: Hirec-R, Hirec-RAS, Hirec PFW9, Hirec PFS10, BioSativa, VitaCoat, HydroCrete, NanoFloor, SurfaceGuard-X, SurfaceGuard-T, SolarEX Quartz SiO₂, SolarEX Titan TiO₂.
- Audit unresolved duplicates, service rows, shipping charges, inactive items, unit mismatches and legacy supplier SKU aliases. Flag PENDING_REVIEW, not automatic merge.
- Link operational Customer Register entries to independently validated legal entities in the existing CRM Master; source billing records do not establish unique account identity.

## Release gate
1. Verify source row count and headers against the CSV; document original import date separately from the source export as-of date.
2. Audit exact duplicates and repeated SKU values; require distinct SKU-to-item mapping before joining invoices.
3. Preserve all source prices as confidential historical evidence; no public GitHub row data.
4. Verify the customer CSV import and original live Customer Register remain available and distinct; flag collision candidates.
5. Product approval, regulatory claims, transport classifications, pricing, and commercial terms remain separate review gates.
6. No automatic background integration or write-back while Ea Level 2 is HOLD.

## Operator-directed 16 October 2026 reconciliation
- Both imported CSV datasets remain immutable evidence; internal register rows can have normalized/linked identities without destroying original accounting rows.
- Source customer duplicate candidates resolve by independently verified legal identity and dated correspondence. A corporate group, an operational consignee and a purchasing subsidiary are different possible roles; maintain distinct entity IDs and a parent-group relationship.
- Source CSV records do not carry per-row modification timestamps. NEVER call their source order a verified last-update date. A source-order preference is explicitly provisional, and cannot be represented as dated precedence.
- All source product rows are retained; stable internal row IDs and unique EA SKU identifiers are assigned. An empty source SKU receives a new unique EA SKU; duplicate numbers that represent materially different products are split, not falsely merged. Preserve original source SKU unchanged.
- A dated, vendor-issued multi-currency price list may verify currency and correct a product-code crosswalk. Crosswalk corrections require item name, package and quoted unit/price consistency. Never use a source price row or a customer-specific discount as a general price by inference.
- Imported product amounts are the DEFAULT internal price amounts, while original VAT, unit sales counts, revenues and historical price fields stay intact. Currency remains explicitly unverified unless dated product-specific evidence confirms it.
- Dated 2026 list prices, historical 2025 price tiers, individually issued quotations, supplier bulk estimates, transport fees and project-specific discounts must reside in distinct auditable evidence records, with product identity, pack, currency, effective date and precedence controls.
- Only a verified comparable, operator-approved general list price supersedes a baseline price. A later quote to one customer does not update a global price. Manufacturer and service availability remain independently verified release gates.
- Sensitive operational data and numeric product prices stay in restricted Sheets, not this repository.
- CSV account overlap and SKU identity normalization are complete for the supplied source files; enterprise-wide historical coverage, product availability and commercial current-price validation are not certified by this step.
