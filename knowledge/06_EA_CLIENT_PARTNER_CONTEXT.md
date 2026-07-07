# Ea Client, Supplier and Partner Context

Status: DRAFT  
Priority: Critical

## Purpose

Define the register Ea needs to understand relationships, correspondence history, confidentiality boundaries and next actions for customers, suppliers, partners and prospects.

## Required register fields

| Field | Description |
|---|---|
| Company/contact | Company and primary people |
| Email/domain | Search key for Gmail/Contacts |
| Relationship type | Customer, supplier, partner, prospect, advisor |
| Products/projects | Relevant NTSN products or projects |
| Status | Active, waiting, dormant, closed |
| Current case | Current issue/opportunity |
| Last known action | Last meaningful event |
| Next action | Recommended follow-up |
| Confidentiality notes | What may not be shared |
| Source | Gmail, Calendar, Contacts, Drive, GitHub, web |
| Review date | Last review date |
| Knowledge status | DRAFT, PENDING_REVIEW, APPROVED or CANONICAL |

## Privacy rule

Do not store unnecessary personal data. Do not expose one party's confidential details to another party. Sensitive relationship notes remain PENDING_REVIEW unless explicitly approved.

## Recommended storage

- Structured summary: GitHub `knowledge/06_EA_CLIENT_PARTNER_CONTEXT.md` or `knowledge/registers/`.
- Evidence: Gmail, Contacts, Calendar and Drive.
- Active follow-ups: Ea Project or approved tracker.
