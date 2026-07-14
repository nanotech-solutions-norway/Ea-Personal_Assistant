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

## Relationship-chain requirement

NanoTech Solutions Norway often acts as a distributor, licensee, product-transfer party or intermediary. A customer email may depend on separate upstream correspondence with the manufacturer, developer, supplier, agent or forwarder.

For product-related email work, the context register and source review must map the full chain:

**manufacturer/developer/supplier → agent/forwarder where applicable → NanoTech Solutions Norway → customer/client/end user**

The related upstream and downstream correspondence must be searched, read and validated before technical or commercial email drafting. Manufacturer-controlled claims must be checked against the latest reliable manufacturer/developer evidence. Customer requirements and test feedback must be checked against the relevant downstream thread. Contradictions remain PENDING_REVIEW until resolved.

## Operator-confirmed relationship-routing examples — 14.07.2026

| Product chain | Upstream party | Intermediate party | NanoTech Solutions Norway role | Downstream examples | Validation note |
|---|---|---|---|---|---|
| Hirec | NTT Advanced Technology Corporation (NTT-AT): developer, manufacturer and supplier | None normally identified | European distributor and product-transfer party | Minze, Inster and other customers/end users | Exact current territory, exclusivity and commercial authority must be checked against the latest agreement and correspondence before external commitments. |
| Gentoo and Ultra-Ever Dry | UltraTech International: manufacturer, developer and supplier | Lars Birkedal and GB Service: forwarders/agents in the supply chain | Norwegian licensee | RealProgress, Eximod and other customers/end users | Validate product, pricing, stock, freight and territory through the responsible upstream party before replying downstream. |

These rows are approved as relationship-routing instructions for evidence retrieval and email cross-checking. They are not blanket approval for customer-facing technical claims, pricing, availability, warranties, delivery commitments, exclusivity or legal conclusions.

## Privacy rule

Do not store unnecessary personal data. Do not expose one party's confidential details to another party. Sensitive relationship notes remain PENDING_REVIEW unless explicitly approved.

## Recommended storage

- Structured summary: GitHub `knowledge/06_EA_CLIENT_PARTNER_CONTEXT.md` or `knowledge/registers/`.
- Evidence: Gmail, Contacts, Calendar and Drive.
- Active follow-ups: Ea Project or approved tracker.
