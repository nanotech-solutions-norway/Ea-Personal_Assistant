# Ea Decision — Document/Template Static Rules — 03:49, 08.08.2026

Status: APPROVED / CANONICAL  
Decision authority: Explicit operator instruction  
Project: Ea Personal Assistant

## Decision

The operator instructed that the document/template instructions established in the current session are to become default static Ea rules whenever the operator requests template creation, document drafting, document conversion, document recreation, information extraction and recreation/drafting, or template population involving DOCX, PDF, XLSX/XLSM or derived template formats.

## Canonical implementation

The full rule set is stored in:

`active-source/05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md`

It is indexed in:
- `active-source/12_EA_MASTER_INDEX.md`
- `active-source/ea_optimized_source_manifest.json`

## Precedence

1. Current explicit operator instruction.
2. Current document-specific APPROVED/CANONICAL workflow or designated template.
3. 05A document/template static rules.
4. General Ea document/template framework.
5. Verified source evidence.
6. Older supporting material.

Approved quotation, invoice and other document-specific workflows override the general 05A rules where they conflict.

## Core defaults approved

- DOCX/DOTX/DOTM for Word-based editable/master workflows as appropriate.
- XLSX/XLSM/XLTX/XLTM for spreadsheet/master workflows as appropriate, preserving VBA where applicable.
- PDF as final fixed-layout output and visual validation surface where appropriate.
- Populated sources must be decomposed into fixed, variable and conditional content before template creation.
- Templates control structure; supporting sources control factual data unless explicitly designated otherwise.
- No silent invention or substitution of commercially, legally, financially or technically significant data.
- Formulas, macros, named ranges, validation, controls, page setup, print settings and layout must be preserved when applicable.
- Generated/recreated outputs require explicit validation and PASS / PASS WITH WARNINGS / FAIL status.

## Classification

CANONICAL because the operator explicitly instructed these rules to be used as defaults for future Ea operation.
