# Ea Decision — Canonical Purchase Order Drafting Standard — 02:19, 09.09.2026

Status: APPROVED / CANONICAL  
Decision authority: Explicit operator instruction  
Effective: 09.09.2026

## Decision

The operator approved the final Purchase Order drafting setup developed and validated during the NTT-AT Hirec-R PO workflow as Ea's canonical PO drafting and final-PDF standard.

Canonical implementation:
- Active-source rule: `05C_EA_CANONICAL_PO_DRAFTING_PDF_LAYOUT_STANDARD_0219_09092026.md`
- Drive rule ID: `1L_MZD3Y-JnyI6nTHKV7E6eJAUsmtY8wp`
- Canonical PDF visual reference: `EA_CANONICAL_PO_LAYOUT_REFERENCE_v2.0_09092026.pdf`
- PDF Drive ID: `1NliiqekZMO6Uii8vTXSs11aoFylXZ8CA`
- Canonical top-right logo: `EA_CANONICAL_PO_TOP_RIGHT_LOGO_v2.0.png`
- Logo Drive ID: `1V4KpZwpXteMHVOAFsZh68bc6juDtfAmq`
- Canonical folder: `Canonical Document Templates` (`19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`)

## Scope of supersession

For PO work, 05C supersedes prior PO-specific **visual/layout/PDF** controls in `05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md` where they conflict.

05B remains applicable to:
- retrieval of `EA_Template_PO_v1.0.xltm`;
- preservation of workbook logic, formulas, supporting sheets and VBA;
- creation of an editable Excel PO when explicitly requested or functionally required.

05C controls:
- PO drafting;
- final A4 layout;
- Libre Baskerville typography;
- top-right branding;
- signature size and placement;
- terms-row divider lines;
- final PDF QA and release.

The older requirement for two Address/Website QR graphics does not apply to the 05C final PDF unless explicitly requested.

## Non-transferable transaction facts

The canonical visual reference contains transaction-specific NTT-AT/Inster data. Those values are not defaults. Each new PO must be populated from the current controlling supplier quotation/order evidence and current explicit operator instructions.

## Validation requirement

Before release of any PO under 05C, Ea must validate:
- source values and arithmetic;
- correct currency symbol;
- A4 one-page output;
- Libre Baskerville-only visible text;
- correct top-right logo and no duplicate bottom-right logo;
- grey divider under every Terms and conditions row;
- signature directly on the signature line;
- no clipping, overlap or stale prior-transaction content.

Decision state: APPROVED / CANONICAL.
