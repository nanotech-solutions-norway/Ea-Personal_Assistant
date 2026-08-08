# Ea Decision — Canonical Quote/Packing List/RFQ/PO Templates — 04:05, 08.08.2026

Status: APPROVED / CANONICAL  
Decision authority: Explicit operator instruction

## Decision

The newly created macro-enabled Excel templates are the default Ea masters for the following operator requests:

- Quote / quotation → `EA_Template_Quote_v1.0.xltm`.
- Packing list → `EA_Template_Packing_List_v1.0.xltm`.
- RFQ / Request for Quote → `EA_Template_RFQ_v1.0.xltm`.
- PO / Purchase Order → `EA_Template_PO_v1.0.xltm`.

Ea must automatically use the matching template when the operator requests the corresponding document, unless the operator explicitly specifies another template, layout or source authority.

## Canonical implementation

- Usage rule: `active-source/05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md`.
- Template register: `registers/EA_CANONICAL_DOCUMENT_TEMPLATE_REGISTER_0405_08082026.md`.
- Drive folder ID: `19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`.

## Authority order

1. Current explicit operator instruction.
2. Current document-specific APPROVED/CANONICAL workflow or explicitly designated alternative template.
3. 05B canonical template rule and registered master.
4. 05A general document/template static rules.
5. General Ea framework and verified evidence.

## Classification

CANONICAL because the operator explicitly instructed Ea to create, upload and automatically use these templates for future matching prompts.
