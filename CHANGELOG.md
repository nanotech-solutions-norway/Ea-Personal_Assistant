# Changelog

## 2026-08-08

- Added canonical default static rules for Ea document/template work involving DOCX, PDF and XLSX/XLSM.
- Added template reverse-engineering rules for populated source files, including fixed/variable/conditional field classification.
- Added source-authority, no-invention, conversion/recreation, formula/macro preservation and validation requirements.
- Added document-format defaults for DOTX/DOTM, DOCX, XLTX/XLTM, XLSX/XLSM and PDF.
- Created canonical macro-enabled Excel templates for Quote, Packing List, RFQ and PO from the operator-supplied workbooks.
- Added `05B_EA_CANONICAL_XLTM_TEMPLATE_USAGE_RULE_0405_08082026.md` so matching operator requests automatically use the registered canonical template unless explicitly overridden.
- Added the canonical document-template register, operator decision and validation record with Drive IDs and integrity hashes.
- Added one-page PDF previews for all four canonical templates and stored the masters/previews in the Ea `Canonical Document Templates` Drive folder.
- Verified formula-error scans, target-sheet visibility and byte-for-byte VBA project preservation; Microsoft Excel runtime macro execution remains an acceptance-test warning.
- Updated the Ea master index and optimized source manifest so the new rules and canonical template mapping are automatically discovered and applied.
- Preserved precedence of explicit operator instructions and document-specific approved/canonical workflows such as quotation and invoice controls.

## 2026-08-05

- Added the canonical hourly Ea Business Email Watch Schedule prompt.
- Added invoice, payment and customs calendar exclusions.
- Added the current Microsoft Teams draft-invite override.
- Added scheduled-email-watch memory and source-reconciliation log.
- Updated the scheduled-routine source, master index, source manifest and knowledge index.
- Preserved Level 2 HOLD and external-action approval boundaries.
