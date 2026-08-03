# CRM Pending Review Register

**Timestamp:** 15:34, 24.07.2026  
**Status:** ACTIVE REGISTER

| ID | Item | Why review is required | Recommended decision |
|---|---|---|---|
| CRM-PR-001 | Promote working governance set to CANONICAL | New operating policy requires explicit approval | Review Docs and ADR; approve, revise or reject |
| CRM-PR-002 | Formal privacy notice and exact retention periods | Jurisdiction-specific legal review is required | Approve a separate privacy/retention policy before publishing the form |
| CRM-PR-003 | Create and publish native Google Form | Current connector cannot create Google Forms directly | Build from the approved Form_Schema and complete test checklist |
| CRM-PR-004 | Role and access matrix | Named users/roles and folder permissions were not supplied | Define owner, editor, viewer and accounting/technical restrictions |
| CRM-PR-005 | Level 2 automation | Unattended sending, invitations and financial posting remain HOLD | Approve only after security, idempotency, audit, rollback and legal validation |
| CRM-PR-006 | Accounting connector/write scope | Official posting method and write authorization are not approved | Keep CRM handoff/readback only; accounting remains authoritative |
| CRM-PR-007 | Legacy `CRM/Data/Temp` content | Existing content was preserved and not classified | Inventory separately; migrate/archive only after evidence review |
| CRM-PR-008 | Production data migration | No source data set or approved mapping was provided | Use migration workbook, sample import, duplicate checks and reconciliation |
| CRM-PR-009 | Public-form controlled upload route | Confidential file handling requires access and retention design | Use post-validation secure request until approved |
| CRM-PR-010 | Dashboard thresholds and forecast policy | Business-specific targets were not supplied | Approve targets after baseline data exists |

## Rule

Do not mark an item resolved without a dated decision, owner, evidence/reference and implementation/validation result.
