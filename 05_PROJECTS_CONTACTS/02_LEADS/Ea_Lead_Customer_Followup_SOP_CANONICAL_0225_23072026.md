# Ea Lead and Customer Follow-up SOP — 02:25, 23.07.2026

**Status:** CANONICAL  
**Scope:** Ea Level 1 — Gmail, Google Calendar, Google Drive and GitHub assisted workflow  
**Level 2:** HOLD

## 1. Purpose

Ensure that every active lead, customer, supplier and partner relationship has a documented status, a clear next action and an appropriately timed private follow-up reminder. The procedure prevents missed commitments, duplicate follow-ups, premature commercial commitments and loss of project context.

## 2. Mandatory trigger

Apply this SOP whenever any of the following occurs:

- A new business inquiry or referral is received.
- A quotation, proposal, technical package, sample, test plan or requested information is sent.
- A meeting, technical call, sample shipment, pilot, trial or customer test takes place.
- NTSN is waiting for customer, supplier, manufacturer or internal input.
- A material deadline, decision, payment, delivery or production dependency is identified.
- An active relationship has had no substantive contact within its appropriate follow-up interval.

## 3. Source review

Before setting or updating a follow-up:

1. Read the complete relevant Gmail thread, including attachments and the latest sent and received messages.
2. Search related Gmail threads by company, contact, domain, project, product and legacy product terms.
3. Check relevant Google Drive, GitHub and Project sources when the case depends on technical, commercial, contractual, regulatory or historical context.
4. Check Google Calendar for meetings, deadlines and existing follow-up reminders.
5. Separate:
   - confirmed facts;
   - reasonable inference;
   - unknown or missing information;
   - confidential information and disclosure boundaries.
6. Do not silently merge contradictory sources. Prefer the latest approved/canonical source and classify unresolved conflicts as `PENDING_REVIEW`.

## 4. Case classification

Every case must have one current status:

| Status | Definition |
|---|---|
| `ACTION_REQUIRED_NTSN` | NTSN owes a response, document, decision, quote, sample, technical conclusion or other action. |
| `WAITING_EXTERNAL` | Waiting for a customer, supplier, manufacturer, partner or third party. |
| `WAITING_INTERNAL` | Waiting for an internal NTSN decision, review, production step or approval. |
| `SCHEDULED` | A meeting, test, shipment, production step or agreed decision date is scheduled. |
| `DORMANT` | No active next step after appropriate attempts; retain for controlled re-engagement. |
| `CLOSED_WON` | Commercial or project objective completed successfully. |
| `CLOSED_LOST` | Opportunity ended or was declined. |
| `CLOSED_NO_ACTION` | Inquiry is invalid, irrelevant, duplicate or requires no further action. |

## 5. Follow-up timing rules

Use the case facts and stated deadlines first. Where no explicit deadline exists, use these defaults:

| Situation | Default follow-up |
|---|---|
| Urgent customer deadline, production block or payment decision | Same business day or next business day |
| Quote, proposal or requested technical package sent | 2–3 business days |
| Waiting for a customer or supplier response | 5 business days |
| Meeting, sample delivery, test, trial or pilot completed | 2 business days |
| Contact is on leave or gave a future review period | First suitable business day after return or stated period |
| Dormant but strategically relevant lead | 14–30 days |
| Agreed long-term milestone | 3–5 business days before the milestone |

Do not use generic high-frequency reminders when the correspondence supports a later date.

## 6. Calendar reminder standard

Before creating a reminder, search the calendar for the company, contact, project and product to prevent duplicates.

Create or update one internal reminder per actionable follow-up:

- **Title:** `Follow up — [Company/contact] / [case]`
- **Duration:** 15 minutes unless more preparation is required
- **Attendees:** none
- **Visibility:** private
- **Transparency:** transparent
- **Google Meet:** disabled
- **Reminder:** popup 30 minutes before
- **Timezone:** Europe/Oslo

The description must contain:

1. **Case summary** — one or two sentences.
2. **Latest confirmed status** — what was last sent, received, agreed or completed.
3. **Required action** — the exact next step at reminder time.
4. **Dependency/risk** — approval, confidentiality, technical, commercial or source limitation.
5. **Source note** — Gmail thread/date and any relevant Drive/GitHub source.

A reminder is an internal control point. It must not invite external attendees or create an external commitment.

## 7. Follow-up register fields

Maintain a current register containing at minimum:

| Field | Requirement |
|---|---|
| Company/contact | Canonical company and contact identity |
| Case/project | Short operational description |
| Product/application | Canonical product terminology where relevant |
| Last substantive contact | Date and direction |
| Current status | One status from Section 4 |
| Confirmed facts | Source-supported only |
| Missing information | Required before the next decision |
| Next action | Specific and owner-assigned |
| Due date | Calendar-aligned date and time |
| Dependency/risk | Approval, confidentiality, source or technical boundary |
| Source/thread | Gmail/Drive/GitHub reference |
| Reminder state | Created, existing, rescheduled, completed or cancelled |
| Closure status | Open, dormant or closed classification |

## 8. Execution at reminder time

1. Re-read the latest thread before drafting or acting.
2. Check whether the required response or decision arrived after the reminder was created.
3. If resolved, record the outcome and close or reschedule the reminder.
4. If still open, prepare the appropriate draft, question list, technical review or decision request.
5. Update the register and create the next reminder only when a genuine next action remains.
6. Avoid repeated generic messages. Each follow-up must reference the actual outstanding item and provide a useful path forward.

## 9. Approval and confidentiality controls

Explicit approval is required before:

- sending an email;
- sending or changing an external calendar invitation;
- forwarding emails or attachments;
- sharing or changing permissions for files;
- making pricing, delivery, warranty, exclusivity, liability, regulatory, legal or other commercial commitments;
- disclosing one party’s confidential information to another party.

Use customer and supplier information only for the relevant relationship. Never expose credentials, secrets, bank/accounting data or unrelated confidential customer material.

## 10. Product and source controls

Use canonical terminology, including SiO₂/TiO₂, Hirec-R, Hirec-RAS, Hirec PFW9, Hirec PFS10, BioSativa, VitaCoat, HydroCrete, NanoFloor, SurfaceGuard-X, SurfaceGuard-T, SolarEX Quartz SiO₂ and SolarEX Titan TiO₂.

Retrieve the exact current source before customer-facing performance, application, durability, warranty, safety, regulatory, logistics, ROI, pricing or commercial statements. Keep unresolved claims or source conflicts under `PENDING_REVIEW`.

## 11. Level 2 boundary

This is a Level 1 connector-assisted workflow. It does not establish autonomous mailbox monitoring, automatic file-aware background execution, automatic sending, external invitation creation, or unattended write-back. Level 2 managed backend automation remains HOLD.

## 12. Quality gate

A case is compliant only when:

- the latest thread and relevant context were reviewed;
- facts, inference and unknowns are separated;
- the case has one current status;
- a specific next action and due date exist, or the case is formally dormant/closed;
- duplicate reminders were avoided;
- the reminder contains a useful case summary and risk boundary;
- no external action or commitment occurred without explicit approval.
