# CRM Blueprint

**Timestamp:** 15:34, 24.07.2026  
**Status:** CONTROLLED DESIGN BASELINE

## Object model

- **Account:** legal/business organization; parent for Contacts, Leads, Opportunities, Activities, Follow-ups, Meetings and Commercial records.
- **Contact:** identifiable business contact belonging to an Account.
- **Lead:** unconverted inquiry/prospect; may convert to/link Account, Contact and Opportunity.
- **Opportunity:** distinct commercial/strategic pursuit with stage, case status, value, probability, owner, action, risk and source.
- **Activity:** append-only evidence of substantive email, call, meeting, document, sample, test, review or decision.
- **Follow-up:** one internal control point for a genuine next action.
- **Meeting:** preparation, decisions, actions and source references; Calendar remains scheduling authority.
- **Commercial:** quote, order, accounting-handoff and delivery references; source documents/accounting remain authoritative.
- **Audit event:** append-only material change, approval, import, correction or automation evidence.

## Identifier standards

- `LEAD-YYYYMMDD-NNNN`
- `ACC-NNNNN`
- `CON-NNNNN`
- `OPP-YYYY-NNNN`
- `ACT-YYYYMMDD-NNNN`
- `FUP-YYYYMMDD-NNNN`
- `MTG-YYYYMMDD-NNNN`
- `CH-YYYYMMDD-NNNN`
- `AUD-YYYYMMDD-NNNN`

Identifiers are immutable and never reused.

## Lifecycle

New inquiry → validation/duplicate check → qualification → Account/Contact linking → Opportunity or nurture → activity/follow-up → quote/order/accounting handoff → delivery/payment follow-up → closed/dormant outcome.

## Qualification

100-point model:

- strategic/product fit 30;
- need/problem clarity 20;
- authority/access 15;
- timing 15;
- commercial potential 10;
- engagement/evidence 10.

Routing: 75–100 Priority A; 55–74 Priority B; 35–54 controlled nurture; below 35 disqualify/minimize. Safety, confidentiality, compliance or source conflict overrides scoring and becomes `PENDING_REVIEW`.

## Opportunity stages

`DISCOVERY`, `TECHNICAL_REVIEW`, `QUALIFIED`, `SAMPLE_OR_TEST`, `PROPOSAL`, `NEGOTIATION`, `PROCUREMENT`, `ORDERED`, `DELIVERY`, `CLOSED_WON`, `CLOSED_LOST`.

Stage expresses progress; case status expresses the current blocker/owner of the next action.

## System boundaries

Gmail = communication evidence. Calendar = scheduling/reminder source. Drive = controlled documents. Sheets = working registers. GitHub = schemas/governance/change history. Accounting = official financial records.
