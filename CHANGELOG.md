# Changelog

## 2026-09-30

- Added Level 2A fail-closed Gmail/Calendar event-receiver runtime scaffold, durable ingestion-event migration, container entry point, and runtime regression tests.
- Webhook endpoints remain unavailable until deployment preflight passes and a durable EventStore is attached; test-only memory storage is not production-authorized.
- Validated connected NTSN Gmail, Google Calendar and Drive Level 2A read surfaces without exercising external writes.
- Added managed-runtime deployment runbook and placeholder-only staging environment contract.
- Added fail-closed runtime preflight for missing infrastructure and unsafe Level 2A external-action flags.
- Added live connector validation evidence and preflight regression tests.
- Classified Gmail users.watch, Calendar watch-channel creation, Pub/Sub, managed PostgreSQL, webhook hosting and managed identity as infrastructure-pending rather than connector failures.

- Implemented the first Ea Level 2 managed-backend foundation under `level-2/backend/` without activating Level 2B.
- Added PostgreSQL-compatible case/action/approval/audit/watch/cursor schema.
- Added deterministic Level 2A/2B policy matrix and fail-closed evaluator.
- Added stable idempotency/action-revision/payload hashing primitives.
- Added source→sink controls for untrusted external content.
- Added Gmail watch/history and Calendar watch/sync-token ingestion contracts.
- Added Level 2A vs Level 2B least-privilege identity design and MCP 2026-07-28 gateway requirements.
- Added Level 2B.1 exact-approval Gmail send staging design; Level 2B remains HOLD.
- Added backend unit CI and staging/integration validation matrix.
- Managed database, webhook/Pub/Sub runtime, separate identities and integration tests remain NOT_DEPLOYED.

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
