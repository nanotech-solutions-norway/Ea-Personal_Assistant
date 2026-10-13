# EA private staging — deployment preparation (13 October 2026)

**Status (updated 13 Oct 2026):** `OPERATOR_DEPLOYMENT_GRANTED / CLOUD_ACCESS_AND_COST_READBACK_PENDING / NOT_DEPLOYED`
**Project:** Ea-Personal_Assistant, Level 2A only.
**Canonical operator decision:** [EA_STAGING_DECISION_WE_EUR20_20261013.json](./EA_STAGING_DECISION_WE_EUR20_20261013.json)
**Persistent staging report:** https://docs.google.com/document/d/1NBy2gBhM9trFufu47QQGoD6ekax8xSNK687hXoyILlM/edit

## 1. Operator-selected constraints (binding for planning)

| Dimension | Current decision | Interpretation |
| --- | --- | --- |
| Cloud | Microsoft Azure | No cloud deployment authority is implied |
| Subscription | UNKNOWN / NOT PROVIDED | HARD BLOCK for resource management |
| Azure location | West Europe, API code `westeurope` | Requested; confirm SKU/quota availability on selected subscription |
| Resource group | NEW dedicated EA resource group | Suggested name `rg-ea-stg-westeurope` (not created) |
| Monthly budget | **EUR 20** | Hard **operator approval ceiling**, not automatically enforced by Azure |
| Tenant scope | ONE private EA tenant | Never implicitly share AtlasOrbit, ACSEE, customer, business or family workloads |
| Data | SYNTHETIC ONLY until separately authorized | No Gmail/Calendar/Drive customer data ingestion yet |
| Autonomy | Level 2A only | Level 2B/2C HOLD; no external email sending or calendar writes |

No cost-incurring infrastructure, OAuth grant or external-provider integration is authorized by this design decision.

## 2. Feasibility and the EUR 20 gate

**Do not assume the proposed always-on topology fits EUR 20/month.**
Azure Container Apps **Consumption** offers subscription-shared monthly usage grants, but use of private endpoints, customer-owned networks, logs and supporting services can incur charges. Managed PostgreSQL Flexible Server separately charges for compute and storage; its minimum provisioned disk allocation is 32 GiB. Database storage remains a consideration even if its compute is stopped. Do not count unused-free-grant availability without examining the chosen subscription.

Official references:
- Azure Container Apps pricing: https://azure.microsoft.com/en-us/pricing/details/container-apps/
- Container Apps billing, including network extras: https://learn.microsoft.com/en-us/azure/container-apps/billing
- Azure Database for PostgreSQL Flexible Server pricing: https://azure.microsoft.com/en-us/pricing/details/postgresql/flexible-server/
- PostgreSQL storage minimum: https://learn.microsoft.com/en-us/azure/postgresql/scale/how-to-scale-storage-size
- Azure Pricing Calculator: https://azure.microsoft.com/pricing/calculator/
- Budget alerts do not automatically stop costs: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets

**Required subscription-specific all-in pre-approval quote:**
- West Europe PostgreSQL Burstable eligible compute SKU, the **32-GiB minimum** storage, backup retention/storage, optional redundancy and IOPS.
- Azure Container Apps Consumption app sizing, minimum replicas (prefer 0 for synthetic testing), logs, container registry, Container Apps environment and monitoring.
- Private DB connectivity: VNet/subnets, private DNS, network egress, NAT and/or private endpoint where needed. Never omit network components from the quote or assume they are free.
- Key Vault request/storage charges, diagnostic logs, data transfer, snapshots, forecast variability and taxes where applicable.
- Any Google Cloud/GitHub App hosting/event costs attributable to EA, if outside this Azure cost target, separately identify and obtain budget authorization. Do not silently exclude cross-cloud recurring costs from an asserted whole-project EUR 20 envelope.
- Confirm chosen subscription's remaining Container Apps free tier; shared grants may already be consumed by other apps.
- Obtain total **EUR/month** at the actual subscription rates. Block deployment if a reliable all-in estimate is missing or exceeds EUR 20. A theoretical lowest-cost compute SKU is NOT an accepted quote.

**Recommended decision if over ceiling:** Stay on ephemeral synthetic GitHub Actions PostgreSQL integration CI plus local development; do not provision always-on PostgreSQL. Provide the operator alternatives requiring an explicit budget or architecture decision. No paid workaround is presumed approved.

**Budget enforcement reality:** Configure resource-group monthly budget notifications, forecast alerts and daily cost review *after authorization*. Azure budgets **warn**, they do not stop billing. A genuine automated stop must be specifically designed and tested; pausing a managed database does not necessarily eliminate storage/backup charges and can be automatically reversed by the service.

## 3. Safe, ordered operator/deployer workflow

### Gate A — Cloud authorization, zero resources created
1. Operator chooses a dedicated Azure subscription and provides only its **subscription name or ID**. Never request passwords or refresh tokens.
2. Authorized administrator verifies tenant ownership and account permissions via `az login`, then read-only `az account list --output table`; confirm subscription belongs to the intended EA owner.
3. Confirm `westeurope` is available for the specific Container Apps plan and PostgreSQL SKU, quota and resource providers. Azure IAM/RBAC must be least privilege.
4. Obtain a priced **all-inclusive** West Europe quote, including database, storage, networking and security; record assumptions and expiry. Reject >EUR 20/month.
5. Obtain a separate, explicit operator approval *for the precise priced staging deployment* and its time horizon. This planning approval is not that approval.

### Gate B — Resource architecture (do not run yet)
1. Create `rg-ea-stg-westeurope` only with specific permission and set non-sensitive `project=ea`, `environment=staging`, `tenant=single-private`, `owner-approved=true` tags.
2. Create the resource-group monthly Azure Cost Management budget (EUR 20) with early actual + forecast alerts. Explicitly note that alerts alone cannot guarantee a hard maximum.
3. Configure separate private networking and private PostgreSQL Flexible Server. For synthetic testing select the cheapest appropriate supported SKU, **only after** pricing and security review. Do not provision public DB ingress or broad IP allowlists.
4. Apply SQL migrations `001` through `005` in order, use a restricted non-owner/no-BYPASSRLS runtime account, and verify 005 RLS policies plus legacy-table access controls. **A single intended tenant is not proof that the legacy tables are safely restricted.**
5. Establish Key Vault and restricted managed identities for service, migration and independent readback. Restrict database credentials to the service; isolate tenant identity in the authenticated workload boundary.
6. Build and deploy a staging-only HTTPS Container Apps receiver (Consumption, min replicas 0 when compatible with ingress delivery) and route verified provider notifications to durable event persistence. `/healthz == 200` does not imply readiness; require `/readyz == 200` with real private DB and delivery auth.
7. Define backup, retention, private logs, redaction, kill switch, least-privilege alerts and teardown procedures. Test all with synthetic records.

### Gate C — Provider credentials (separately authorized)
1. Create separately consented Google Workspace read-only backend OAuth grants and Google Cloud Pub/Sub; do not copy credentials from ChatGPT connectors. Initial Calendar full/incremental worker receives an authenticated scoped `events.list` transport.
2. Register Gmail `users.watch` and Calendar watch only after the staging runtime is healthy; use signed/OIDC validation, authorized account/collection mapping and renewal checks.
3. Register Drive change-token listeners with folder/permission re-read and safe tombstone handling.
4. Install a GitHub App with repo allowlist, least-privilege permissions, signed delivery checking, replay protection and independent provider-state re-read.
5. Persist minimal normalized references only; no bulk sensitive contents in the public repo or public logs.

### Gate D — Acceptance evidence (before any real customer data)
- Confirm real database restricted-role and tenant RLS tests, including legacy records.
- Confirm initial complete provider baseline, bounded pagination, incremental cursor updates and independent post-commit AND external-provider readback.
- Test Google Calendar HTTP 410, Gmail history expiration/404, Drive expired change tokens, wrong/withdrawn OAuth, wrong repo/install, duplicate webhook deliveries, partial-pages and process-restart recovery.
- Validate 03B financial/customs exclusions, 03D deleted-draft suppression and 03F draft hygiene.
- Verify no external emails, event invitations or business commitments; confirm Level 2B/2C remain HOLD.
- Confirm measured Azure charges remain within the approved cap, and report actual/forecast spend. Obtain explicit operator authorization for live-provider use and separate production cutover.

## 4. What can proceed right now

**Allowed, zero Azure spend:** engineering code review, synthetic provider fixtures, GitHub CI, portable database integration tests using the disposable GitHub PostgreSQL service, security threat review, documentation and pricing research.

**BLOCKED pending A:** Azure resource group, Container Apps, managed PostgreSQL, Key Vault, paid logging/network, backend OAuth grants, Google watches, GitHub App installations and any real data movement.

The offline `validation/staging_decision_gate.py` script validates the **design record** and always reports `deployment_authorized=false`. It is not a substitute for Azure RBAC or operator approval and contains no deployment operations.

## 5. Next missing input and deliverables

**Only missing essential operator input for next validation:** the Azure subscription name or ID (the exact target subscription must be confirmed to compute accurate quote and availability). A resource-group **name** is proposed, not a created resource.

After that input, the next allowed task is **read-only subscription/sku/pricing verification**. Provide an all-in quote, implementation alternatives for EUR 20, and an explicit approval packet. Do not create resources, provide or receive secrets through chat, authorize provider OAuth or activate live synchronization as a side effect of reading subscription metadata.

Source authority: `active-source/` canonical EA rules, `runtime/DEPLOYMENT_RUNBOOK.md`, and the latest merged engineering checkpoint. This plan does not amend EA task schedules or autonomy levels.

## 6. Operator approval update — 13.10.2026 (supersedes earlier "subscription missing" statements)

The operator provided the target Azure subscription UUID privately, attested the EUR 20/month budget is validated and expressly granted the **separate staging deployment authorization**. GitHub PR #54 has now merged. The subscription UUID must not be written into this public repository. Store it in `ea-staging-preflight` environment variable `AZURE_SUBSCRIPTION_ID` instead.

Approval is scoped to a single private synthetic-only EA tenant, West Europe and EUR 20/month maximum. Azure service principal OIDC federation, actual Azure RBAC/ownership, subscription-specific all-in quote and SKU/quotas are **not yet independently verified**. This does not override the prior no-live-sync rule. The next step is an operator-protected **manual read-only preflight**, not immediate paid provisioning.

See [EA Azure preflight handoff](./EA_AZURE_PREFLIGHT_OPERATOR_HANDOFF_20261013.md) and [manual GitHub Actions OIDC check](../../../.github/workflows/ea-azure-staging-readonly-preflight.yml). The original section 5 "subscription missing" applies only before this dated update.
