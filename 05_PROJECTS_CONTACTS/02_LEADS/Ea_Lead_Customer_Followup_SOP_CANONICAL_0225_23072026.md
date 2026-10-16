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

## 13. Pre-draft correspondence and attachment verification (operator directive 16.10.2026)

For every business lead, customer or supplier reply and follow-up:

1. Retrieve the latest complete relevant Gmail thread, related side threads, recipient and CC routing, prior sent proposals, current payment/shipment state, and any existing drafts before drafting. Respect intentionally deleted drafts as a suppression signal unless the operator explicitly requests a fresh draft.
2. Check Google Calendar, the current CRM lead register, approved Ea product-truth sources, Google Drive and GitHub case evidence.
3. Decide if a customer-facing email is warranted. When the recipient was just answered, a meeting is already scheduled, or the case was expressly paused, prepare only an internal task/preparation record instead of unnecessary repeat contact.
4. Identify the appropriate recipient-specific attachments: approved quotations, invoices, price tables, agreements, TDS/SDS, application instructions or technical packages. Fetch and verify the exact existing file, newest authoritative version, product formulation, recipient, date, currency, supersession, validity, disclosure rights and technical/commercial approval before attaching. Prefer existing valid evidence over inventing or regenerating documents.
5. Do **not** attach supplier wholesale price lists, unrelated customer records, proprietary third-party material, expired draft quotations, unapproved technical claims or unreconciled invoices as current customer offers. Missing or conflicting material becomes a PENDING_REVIEW approval/verification action; create non-binding internal quote/invoice/technical-preparation instructions where appropriate.
6. Use the existing email thread and correct owner/sender where technically possible. Inster/Oesía/Tecnobit communications must be authored by Espen Olsen; if his mailbox is unavailable, prepare an internal handoff instead of an external draft under the wrong sender. Never send a message without approval.
7. After drafting, record recipient, thread, Gmail draft URL, intended/attached/missing documents, lead status, owner, due date and source in the lead register, and create or update one deduplicated, private, no-attendee Calendar follow-up with no Meet link and no external notifications.
8. Verify each draft's recipient, CC, subject, wording, actual attachment presence, evidence boundaries and next action before marking ready. If a customer-facing quotation, invoice, regulatory claim or document requires qualified review, retain PENDING_REVIEW until separately approved.

Level 2 automatic mailbox write-back and autonomous sending remain HOLD.

## 14. Sample-request intake, dispatch planning and carrier-cost estimate (operator directive 16.10.2026)

For **every new or outstanding sample request** identified in business/personal email, CRM or meeting follow-up, create and maintain a structured **sample-request list** as an internal linked record before claiming shipment readiness. Reconcile existing entries and past dispatches to avoid duplicate requests. Record one request header and one line per requested product/variant/packaging; do not silently conflate samples with confirmed paid orders.

Mandatory request-header fields:

| Field | Requirement |
|---|---|
| Sample request ID / lead / project | Stable identity linked to the CRM lead, opportunity and source email/thread |
| Request date | Exact original date of request, with timezone if relevant; distinguish original request from later amendments |
| Recipient | Verified addressee/contact and legal company, distinct from any invoicing/procurement entity where applicable |
| Delivery address | Full ship-to name/company, street, suite, postal code, city, region and country; phone/email when carrier requires them; protect private address data from public repositories |
| Dispatch origin and intended ship date | Verified ship-from location and proposed dispatch date; distinguish requested versus approved/confirmed date |
| Status and owner | REQUESTED, MISSING_DETAILS, PENDING_TECHNICAL_APPROVAL, RATE_PENDING, PENDING_COMMERCIAL_APPROVAL, READY_FOR_APPROVAL, APPROVED_FOR_DISPATCH, SHIPPED, DELIVERED or CLOSED; owner and next action |

Mandatory item-level fields: canonical **sample product name and exact variant/SKU**, requested **amount and unit (mL, L, g or kg)**, number of bottles/cans/packs, volume/weight **per unit and aggregate total**, whether amount is requested/proposed/confirmed, sample purpose, and applicable product suitability, SDS/CLP/DG and disclosure review. Never infer sample quantity, formulation or packaging when unverified; mark MISSING_DETAILS and ask the requester/owner.

Mandatory transportation estimate procedure:

1. Check accessible, actually operational **Bring and/or FedEx** rate-quote services, choosing only a carrier that supports the ship-from/ship-to route, parcel and commodity. Prefer a defensible service comparison (standard vs express when supported). FedEx or Bring MCP repository existence does **not** prove a functioning live rate connection.
2. Collect validated origin and destination postcodes/countries, contact delivery requirements, shipment date, dimensions, **gross packed weight**, parcel count, declared shipment value and shipment restrictions (including solvent, flammable/air-transport/DG conditions), export/customs requirements when relevant. Product volume is not parcel gross weight. Ask for missing values; do not fabricate them.
3. Record **estimated transport cost per carrier/service** with numerical amount, currency, rate source (live carrier quote/reference or clearly labeled nonbinding historical/manual estimate), quote retrieval date/time, validity, transit estimate when carrier provides it, and whether fuel surcharge, handling, VAT, duties, clearance or insurance are included/excluded/unknown.
4. If carrier API, account or live rates are inaccessible, record `RATE_PENDING_CARRIER_ACCESS` and exact missing inputs instead of inventing a freight price; a historical manual benchmark may be recorded distinctly but never represented as a live Bring/FedEx quotation.
5. Display a concise internal sample-request table for the operator showing **sample(s), quantity and total volume, recipient, full private shipping address in authorized context, original request date, and estimated Bring/FedEx shipping cost/status**, with links to the originating correspondence and rate evidence. Protect the private address in public GitHub documents, shared files or cross-customer outputs.
6. Before packing, dispatch, invoice, freight agreement or customer confirmation, obtain applicable operator approval and any required technical, commercial and qualified transport/DG/export review. No booking, waybill generation, rate acceptance, shipping purchase or commercial promise is authorized merely by this checklist.

Update the CRM's existing sample/shipment/follow-up tracking **only in an explicitly authorized interactive write workflow**; scheduled Ea Business Email Watch runs prepare the table, pending-data requests and PROPOSED changes without autonomous Google Drive, GitHub, carrier or accounting writeback. Deduplicate items and update status from actual evidence when available.

**Sample intake quality gate:** each requested sample has an identified quantity or MISSING_DETAILS, the true original request date, verified recipient and address or a clear missing-data marker, and a sourced price quote or RATE_PENDING_CARRIER_ACCESS. No invented recipient details, shipping amount or shipment completion.
