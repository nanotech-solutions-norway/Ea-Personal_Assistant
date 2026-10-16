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
