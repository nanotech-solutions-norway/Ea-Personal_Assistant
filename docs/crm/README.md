# CRM Operating System

**Implementation timestamp:** 15:34, 24.07.2026  
**Status:** CONTROLLED WORKING BASELINE  
**Scope:** Business leads, customer follow-up, accounts, contacts, opportunities, activities, meetings, commercial handoff, privacy, audit and connector-assisted operation.

## Purpose

This package defines the version-controlled governance and schema layer for the NanoTech Solutions Norway AS CRM workspace. Google Drive and Google Sheets are the operational working environment; Gmail, Google Calendar and accounting systems remain evidence/authority sources for their respective domains.

GitHub stores sanitized governance, schemas, enums, mappings, decisions and validation evidence. It must not store live customer records, confidential attachments, credentials, bank data or official accounting records.

## Operating principles

- One Account per legal/business organization.
- One Contact per identifiable business-contact relationship.
- One Opportunity per distinct commercial or strategic pursuit.
- One current case status and one specific next action for every active case.
- Every material record has an owner and source reference.
- Activities and audit events are append-only evidence.
- External messages, invitations, file sharing and commercial commitments require explicit approval.
- Accounting remains authoritative for invoices, credit notes, VAT, payments and ledger state.
- Conflicting or unsupported information is `PENDING_REVIEW` and is never silently merged.

## Core files

- `CRM_MASTER_INSTRUCTIONS.md` — source authority, approval boundaries and quality gates.
- `CRM_BLUEPRINT.md` — relational objects, identifiers, lifecycle and ownership.
- `CRM_PLAYBOOK.md` — lead intake, qualification, conversion and follow-up procedures.
- `DRIVE_FILE_INDEX.md` — operational Drive folder and artifact index.
- `../../schemas/crm/crm-schema.json` — machine-readable entity schema.
- `../../config/crm/statuses.yaml` — controlled status/stage enumerations.
- `../decisions/ADR-CRM-001-source-authority-and-approval-boundary.md` — design decision.
- `../pending-review/CRM-PENDING-REVIEW.md` — unresolved implementation and policy items.

## Product terminology

Use `Hirec-R` for Hirec100 variants, `Hirec PFW9` for water-based Hirec 450 variants and `Hirec PFS10` for solvent-based Hirec 450 variants. Always write `SiO₂/TiO₂`.

## Automation boundary

Level 1 connector-assisted review, drafting and controlled internal write-back is supported. Level 2 unattended sending, external invitation creation and financial posting remain **HOLD** until separately approved and validated.
