# NTSN Azure account pricing — common source-of-truth policy
**Applies:** current and future Azure-dependent NTSN projects. **Registered:** 2026-10-16.
**Maturity:** COMPLETE_SOURCE_ARCHIVE / NO_AUTOMATIC_BILLING_REFRESH_YET / NO_DEPLOYMENT_AUTHORIZATION.

## Canonical private data
Google Drive contains an owner-only folder called **NTSN Azure Billing & Pricing — Restricted** (discover by title through the connected authorized Drive account). It contains the COMPLETE October 2026 Azure billing-profile price sheet (20 checksum-verifiable binary parts reconstructing the original ZIP of 20 CSV files, 3,045,302 meter rows), the private subscription-plan grid and detailed usage export, a private subscription registry, 5,537-row regional price lookup cache, integrity manifest, restore script and private financial review.

**Do not commit** the ZIP/parts, negotiated `UnitPrice`, account/billing/tenant/subscription identifiers, invoices, confidential exports or derived confidential price tables to ANY GitHub repository (public or private), CI logs, workflow artifacts or broadly shared Google documents. Do not copy this source to each repo: reference the restricted vault from each project after authenticating. Archive is available to connected users with authorized Drive access only; plain GitHub readers and GitHub Actions have no implicit access.

## How agents and projects use this baseline
1. Query the authorized private Drive catalog **before asking the operator to re-upload an existing price sheet**. Prefer the small region cache for known October rates; use the full original archive for missing meters.
2. Independently establish the target *project -> Azure subscription -> billing profile -> contractual offer/agreement* binding. October subscription-plan export currently includes two active and one deleted entry; do not assign them to projects by similar names.
3. Match meter ID, service/SKU, region, tier, term, billing and price currencies, effective start/end dates; account price sheet is a historical snapshot **only valid for 2026-10-01 to 2026-10-31**. Account currency may be NOK although unit prices are USD.
4. For later months fetch an authenticated newer billing-profile sheet via **separately approved read-only billing-scoped identity**, with agreement-specific REST API. Until configured, warn `AUTOMATED_REFRESH_NOT_CONFIGURED`. Public Azure Retail Prices API is a fallback for estimates, never a contracted account rate.
5. Independently calculate all-in project costs across subscriptions, free-grant sharing, chargeable resources, storage/backup, network, logging, taxes, invoice FX, delayed teardown and contingency. Azure budget alerts are not spending kill switches.
6. Every project retains its own budget, independent review, operator decision, security/identity and teardown gates. **Current baseline is not proof of free Azure credits or permission to provision/delete infrastructure, modify RBAC, issue OAuth grants or sync live user data**.
7. Any future Azure-dependent repo should adopt this file at project onboarding. **Automatic inheritance across future GitHub repositories is a separate integration**; a checked-in document alone cannot enforce it.

## Confidential source lifecycle
Archive source: October 2026 private account export, 20 ZIP CSV members / 3,045,302 rate rows. Whole-file SHA-256 is stored in the restricted Drive archive manifest and must be verified before use. Derived October private cache covers 5,537 rows for selected regional services and is **not** the entire sheet. Keep historical versions immutable; refresh monthly or after material changes. Require independently verifiable role-scoped authorization for programmatic private billing API access. No passwords, personal Azure sessions, wildcard Contributor or resource access may be introduced for billing retrieval.

## Approval & verification checklist
- [ ] The *requested* month's private account price sheet is present and integrity-checked, or estimate-only mode is explicit.
- [ ] The specific project/subscription/billing profile and contract offer are verified.
- [ ] All relevant meters, term/tier, taxes, invoice FX and residual charges are costed or justified.
- [ ] A read-only authenticated billing ingestion and secret management design has independent security approval before automation.
- [ ] A separate budget owner/reviewer approved the actual project's ceiling, teardown and cloud authorities.
- [ ] Project docs or governance workflows require this policy during Azure onboarding; do not claim organization-wide automatic enforcement before tested.

Reference: [Microsoft Cost Management price sheet API, billing profile](https://learn.microsoft.com/en-us/rest/api/cost-management/price-sheet/download-by-billing-profile?view=rest-cost-management-2025-03-01) for MCA/MPA; enterprise agreement uses the distinct [billing account price sheet API](https://learn.microsoft.com/en-us/rest/api/cost-management/price-sheet/download-by-billing-account?view=rest-cost-management-2025-03-01).

## Repository adoption — Ea-Personal_Assistant
EA project-specific exception: existing 37-meter October 2026 financial coverage, synthetic-only 48-hour scenario and hard decision ceiling of EUR20/month including tax and teardown remain governed by Issue #84. The uploaded sheet improves source evidence but does NOT authorize cloud deployment or change Reader RBAC, Level 2B/2C or real Calendar sync.

**Cross-project canonical reference:** https://github.com/nanotech-solutions-norway/ntsn-mcp-integrations/blob/main/governance/AZURE_PRICING_SOURCE_OF_TRUTH.md (requires GitHub access).
