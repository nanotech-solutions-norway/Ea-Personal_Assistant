# ADR-CRM-001 — Source Authority and Approval Boundary

**Timestamp:** 15:34, 24.07.2026  
**Status:** PROPOSED / PENDING_REVIEW  
**Decision owner:** User approval required

## Context

CRM work combines user instructions, approved Ea operating rules, Gmail/Calendar evidence, Drive/GitHub documents, working Sheets and accounting records. Silent conflict resolution or uncontrolled external actions would create commercial, confidentiality and audit risk.

## Decision

1. Apply source authority in this order: current explicit instruction; latest approved/canonical rule; approved CRM register; verified system/source evidence; labelled inference; unknown/conflict as `PENDING_REVIEW`.
2. Do not silently merge contradictory sources.
3. Every active record requires status, owner, next action, due date and source reference.
4. External emails, forwarding, invitations, sharing changes and commercial/legal commitments require explicit approval.
5. Internal drafts, internal private reminders and controlled internal records may be prepared without creating external commitments.
6. Accounting remains authoritative for invoices, credit notes, VAT, payments and ledger status. CRM contains only handoff and reconciliation fields.
7. GitHub stores sanitized governance/schema material only; operational customer records remain in controlled Drive/CRM systems.

## Alternatives considered

- Treat the latest edited file as automatically authoritative: rejected because edit time does not prove approval.
- Allow connector automation to act on inferred intent: rejected because it can create external or commercial commitments.
- Store all evidence directly in CRM/GitHub: rejected because it duplicates sensitive material and weakens access control.

## Consequences

- More records may remain `PENDING_REVIEW`, but conflicts are visible.
- Automation must support idempotency, source links, approvals, audit and rollback.
- A working CRM status does not replace source-system truth.
- Formal promotion to `APPROVED` or `CANONICAL` requires explicit decision.
