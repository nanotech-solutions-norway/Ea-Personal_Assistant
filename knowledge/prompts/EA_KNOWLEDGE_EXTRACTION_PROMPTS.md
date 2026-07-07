# Ea Knowledge Extraction Prompts

Status: ACTIVE_PROMPT_PACK  
Use in: Ea Project  
Level 2: HOLD

## General connector rules

Use connectors where available:

- Gmail for sent/received email patterns, pricing references, supplier/customer terms and relationship history.
- Google Drive for TDS, SDS, SOPs, reports, templates, meeting notes and generated documents.
- Google Calendar for meeting history, recurring contacts and project timelines.
- Google Contacts for contact/company mapping.
- GitHub for Ea, Atlas, SolarEX, Conta MCP and other project source files.
- Web search only for current public company/product/regulatory context where needed.

Do not store or expose passwords, API keys, bearer tokens, private headers, .env values, credentials or unnecessary private customer data.

Classify extracted knowledge as DRAFT, AUTO_APPROVED, PENDING_REVIEW, APPROVED, CANONICAL or DEPRECATED.

Pricing, warranties, delivery commitments, legal, tax, accounting, product claims, public claims, confidentiality rules and high-risk skills must be PENDING_REVIEW unless explicitly approved.

---

## PROMPT 01 — Master knowledge extraction plan

```text
Build an Ea Knowledge Extraction Plan.

Use available connectors to identify the source sets needed for:

1. Product knowledge.
2. Email language profile so Ea writes like Ruben/NTSN.
3. Writing format and signatures.
4. Document templates.
5. Company context.
6. Client, supplier and partner context.
7. Pricing and commercial terms.
8. Active projects and operations.
9. Legal and financial boundaries.
10. Knowledge update protocol.

For each category, list:

- connector/source to use;
- exact search queries to run;
- expected evidence files/emails/events;
- sensitivity classification;
- proposed output file;
- approval status required;
- risks and exclusions.

Do not extract or store secrets. Do not treat evidence as canonical until reviewed.
```

---

## PROMPT 02 — Product knowledge extraction

```text
Use Google Drive, Gmail and GitHub to extract structured NTSN product knowledge.

Search for TDS, SDS, SOPs, application notes, quotes, product reports and relevant email threads for:

- Hirec-R / Hirec100 legacy references;
- Hirec PFW9 / water-based Hirec 450 references;
- Hirec PFS10 / solvent-based Hirec 450 references;
- SolarEX Quartz SiO₂;
- SolarEX Titan TiO₂;
- SurfaceGuard-X;
- SurfaceGuard-T;
- Gentoo 4700;
- Ultra-Ever Dry;
- textile coating R&D;
- anti-stick / industrial coating candidates.

For each product, create a structured product file with:

- approved product name;
- legacy names;
- category;
- short approved description;
- main use cases;
- suitable substrates;
- unsuitable substrates;
- source-backed technical claims;
- forbidden/unverified claims;
- application method;
- coverage/consumption;
- drying/curing;
- durability/service-life/warranty wording;
- safety handling notes;
- regulatory/shipping notes;
- MOQ/sample policy;
- lead time;
- pricing references;
- source documents/emails;
- last reviewed date;
- approval status.

Use these naming rules:

- Hirec100 -> Hirec-R;
- Hirec 450 water-based -> Hirec PFW9;
- Hirec 450 solvent-based -> Hirec PFS10;
- SiO2 -> SiO₂;
- TiO2 -> TiO₂.

Mark performance claims, pricing, warranty, durability and regulatory statements as PENDING_REVIEW unless already explicitly approved.
```

---

## PROMPT 03 — Email language profile extraction

```text
Use Gmail sent mail to create an Ea Email Language Profile so Ea drafts emails in Ruben/NTSN style.

Search sent emails in these categories:

- customer replies;
- supplier requests;
- partner/distributor emails;
- follow-up emails;
- technical clarification emails;
- quote/proposal emails;
- meeting rescheduling emails;
- apology or delay emails;
- Norwegian-language emails;
- high-importance commercial emails.

Extract generalized style rules only. Do not store private customer details.

Create `knowledge/02_EA_EMAIL_LANGUAGE_PROFILE.md` with:

- default language rules;
- greeting style;
- closing style;
- tone and formality;
- sentence and paragraph style;
- how Ruben asks for help;
- how Ruben follows up;
- how Ruben discusses pricing/lead time;
- how Ruben handles technical limitations;
- supplier style;
- customer style;
- partner style;
- apology/delay style;
- Norwegian vs English differences;
- preferred phrases;
- phrases to avoid;
- signature behavior;
- examples converted into anonymized patterns;
- review status.

Classify the profile as PENDING_REVIEW until Ruben approves it.
```

---

## PROMPT 04 — Writing format and signature extraction

```text
Use Gmail sent mail, Google Drive templates, proposals, reports and prior documents to extract Ea writing format rules.

Create `knowledge/03_EA_WRITING_FORMAT_AND_SIGNATURES.md` with:

- default English signature;
- default Norwegian signature;
- short signature;
- full company signature;
- subject-line patterns;
- email paragraph format;
- quote/proposal email format;
- technical reply format;
- follow-up format;
- meeting reschedule format;
- attachment wording;
- date/time format;
- currency format;
- measurement/unit format;
- standard caveats for technical, legal, financial and commercial uncertainty.

Flag uncertain or conflicting signature/company details as PENDING_REVIEW.
```

---

## PROMPT 05 — Document template extraction

```text
Use Google Drive and GitHub to find existing NTSN templates, proposals, reports, memos, QA logs, meeting notes and contract-review documents.

Create template requirements and draft templates for:

- email replies;
- meeting memos;
- meeting minutes;
- follow-up emails;
- due diligence reports;
- legal review memos;
- contract risk tables;
- financial reviews;
- tax/VAT notes;
- product recommendation memos;
- technical customer responses;
- quotation emails;
- lead lists;
- action registers;
- session-close packs.

For each template, include:

- purpose;
- when to use;
- required inputs;
- output structure;
- approval requirements;
- confidentiality classification;
- source/evidence section;
- version/date;
- status.

Do not create final legal, tax or accounting advice templates. Mark those as business-support only.
```

---

## PROMPT 06 — Company context extraction

```text
Use Google Drive, GitHub, Gmail, current websites and approved prior documents to create Ea Company Context for NanoTech Solutions Norway AS.

Extract:

- legal company name;
- organization number;
- address;
- websites and domains;
- approved short company description;
- approved long company description;
- product portfolio overview;
- target customer groups;
- geographic focus;
- standard commercial posture;
- approved public claims;
- claims that must not be made without approval;
- standard disclaimers/caveats;
- source references;
- review date and status.

Mark public claims and marketing language as PENDING_REVIEW unless explicitly approved.
```

---

## PROMPT 07 — Client, supplier and partner context extraction

```text
Use Gmail, Google Contacts, Calendar and Drive to create an Ea Client, Supplier and Partner Context Register.

For each relevant company/contact, extract:

- company name;
- contact name and role;
- email/domain;
- relationship type: customer, supplier, partner, prospect or advisor;
- relevant product/project;
- current status;
- last known action;
- next recommended action;
- important history;
- confidentiality notes;
- source references;
- review date;
- status.

Search by domains, contacts, project names, products and recent threads.

Do not expose confidential details across unrelated parties. Mark sensitive entries PENDING_REVIEW.
```

---

## PROMPT 08 — Pricing and commercial terms extraction

```text
Use Gmail, Google Drive, quotes, supplier emails, customer proposals and project reports to build Ea Pricing and Commercial Terms.

Extract:

- product/service;
- price/reference price;
- currency;
- unit;
- MOQ;
- sample policy;
- lead time;
- Incoterms;
- payment terms;
- discount rules;
- warranty/service-life wording;
- quote validity;
- approval requirement;
- source document/email;
- review date;
- status.

Pricing, discount, warranty, delivery, exclusivity and payment terms must remain PENDING_REVIEW unless explicitly approved.

Do not make customer-facing commitments in the output. Create a review table for Ruben to approve.
```

---

## PROMPT 09 — Active projects and operations extraction

```text
Use GitHub, Google Drive, Gmail and Calendar to build Ea Projects and Operations knowledge.

Include:

- Ea Personal Assistant;
- SolarEX;
- Atlas AI;
- Conta MCP / Conta Bridge;
- Domeneshop MCP;
- PowerShell environment;
- NTSN Orchestrator Control Plane;
- active customer/product projects.

For each project, extract:

- project name;
- purpose;
- current status;
- current milestone;
- active repository/domain/folder;
- relevant contacts;
- known risks/blockers;
- latest validated decision;
- next recommended action;
- update frequency;
- source references;
- review date.

Classify uncertain or conflicting project states as PENDING_REVIEW.
```

---

## PROMPT 10 — Legal and financial boundary knowledge extraction

```text
Use Ea protocol files, prior legal-review examples, budget-review examples, invoice/quote examples and approved business rules to build Ea Legal and Financial Boundaries knowledge.

Extract:

- allowed legal business-support tasks;
- forbidden final legal conclusions;
- lawyer-review trigger list;
- allowed financial-support tasks;
- forbidden final tax/accounting conclusions;
- accountant/tax-advisor review trigger list;
- standard caveat wording;
- official-source requirements;
- risk classification table;
- examples of safe wording.

Do not create final legal, tax or accounting advice. Mark this knowledge PENDING_REVIEW until approved.
```

---

## PROMPT 11 — Knowledge update pack

```text
After extracting a knowledge category, create a Knowledge Update Pack containing:

- source summary;
- extracted knowledge;
- excluded sensitive data;
- contradictions found;
- proposed target file path;
- proposed status: DRAFT, AUTO_APPROVED, PENDING_REVIEW, APPROVED, CANONICAL or DEPRECATED;
- approval requirements;
- validation checks;
- changelog entry.

Do not update canonical knowledge until Ruben approves high-risk items.
```

---

## PROMPT 12 — Knowledge validation pass

```text
Validate the Ea knowledge layer.

Check:

- all required knowledge files exist;
- no secrets or credentials are stored;
- evidence is separated from instructions;
- pricing, legal, tax, accounting, warranty, product claims and public claims are PENDING_REVIEW unless approved;
- source references are present;
- review dates are present;
- Level 2 remains HOLD;
- Custom GPT knowledge contains only stable sanitized files;
- Project knowledge contains compact current operational files.

Create an update for `knowledge/11_EA_KNOWLEDGE_VALIDATION_REGISTER.md` and `knowledge/12_EA_KNOWLEDGE_CHANGELOG.md`.
```
