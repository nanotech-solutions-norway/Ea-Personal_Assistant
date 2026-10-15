# EA Azure staging — verified West Europe SKU results and EUR 20 deployment gate

**Date:** 15 October 2026  
**Status:** `OIDC_PASS / PROVIDER_REGISTRATION_PASS / PG_SKU_METADATA_PASS / COST_QUOTE_PENDING / QUOTA_PENDING / NOT_DEPLOYED`  
**Scope:** Single private synthetic-only EA Level 2A; `westeurope`; new EA-only resource group `rg-ea-stg-westeurope`; operator-approved maximum EUR 20/month.

## 1. Independent test evidence

| Evidence | Result |
| --- | --- |
| [Manual read-only West Europe SKU workflow](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38657630948) | **PASS**, attempt 1 |
| Protected GitHub environment / immutable OIDC login | **PASS** |
| Approved subscription and tenant state | **PASS** |
| `Microsoft.App`, `Microsoft.DBforPostgreSQL`, `Microsoft.KeyVault`, `Microsoft.Network` | **Registered** |
| `az postgres flexible-server list-skus --location westeurope` | **Returned nonempty SKU metadata** |
| SKU compute quota, current zone capacity or availability of a specific deployment | **NOT YET VERIFIED** |
| Actual retail/account-specific compute or storage prices | **NOT YET VERIFIED** |
| All-in recurring architecture quote <= EUR 20/month | **NOT YET VERIFIED** |
| Resource creation | **NONE** |

The read-only GitHub run returned these **potential PostgreSQL Flexible Server Burstable SKU identifiers**, sorted by family name:
`Standard_B1ms`, `Standard_B2s`, `Standard_B2ms`, `Standard_B4ms`, `Standard_B8ms`, `Standard_B12ms`, `Standard_B16ms`, `Standard_B20ms`.

These are **region metadata candidates, not reserved capacity or a verified price quotation**. The presence of B1ms does not demonstrate EUR 20 cost feasibility.

## 2. Price quotation worksheet — fill with *evidence*, never guesses

An acceptable quote must state **billing currency, source timestamp, subscription, SKU/meter ID, usage units, included/free grant, and price**.

| Meter / service | Required input | Evidence/status |
| --- | --- | --- |
| PostgreSQL Flexible Server compute | Choose e.g. B1ms only if fit for integration test; EUR/vCore-hour or node-hour, intended monthly running hours | **PENDING** |
| PostgreSQL provisioned disk | Minimum supported disk allocation (existing baseline assumes >=32 GiB); EUR/GiB-month; any paid IOPS | **PENDING** |
| Backup / PITR | Retention, redundancy, excess backups beyond included storage | **PENDING** |
| Container Apps Consumption | vCPU/GiB allocated seconds, HTTP requests, minReplicas 0 if appropriate; subscription-wide remaining free grants | **PENDING** |
| Private network | VNet, DNS, any dedicated environment private endpoints, routing, NAT / outbound network, data transfers | **PENDING** |
| Secrets / identities | Key Vault operations and diagnostics; managed identity/role cost implications | **PENDING** |
| Logs / registry | ACR (if used), Azure Monitor / Log Analytics retention/ingestion and alerts | **PENDING** |
| Outbound traffic / additional services | Egress and attributable cross-cloud costs | **PENDING** |
| Taxes / quote buffer | Applicable taxes and variability reserve; write final upper-bound EUR/month | **PENDING** |

**Reject deployment** unless the sum of supported items with actual assumed usage is **<= EUR 20/month**, the source quote is current, and any lower introductory price or external promotion has been explicitly disclosed. Azure budget alerts are *not* a hard spending cutoff.

Use [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) or [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) for reproducible retail-meter evidence. Retail public prices **do not necessarily match** a specific customer's contract, discount or taxation. Obtain the actual subscription-specific quote or contract adjustments through an authorized Azure billing owner. Record it privately in Google Drive, not as customer/account details in this public GitHub repository.

### Scenario comparisons — zero unsupported price claims

- **A / CI-only:** Existing ephemeral GitHub Actions PostgreSQL 16 integration suite and synthetic fixture runs; no persistent Azure PostgreSQL. This is the safe default if a complete cost quote is absent or exceeds EUR 20; GitHub Actions billing constraints are separate.
- **B / On-demand private staging:** Managed PostgreSQL + restricted runtime provisioned for a short **specified test duration**, with start/stop/teardown and storage/backup costs included. Do **not** assume stopping PostgreSQL eliminates storage charges or guarantees it stays stopped indefinitely.
- **C / Always-on managed staging:** Continuous managed PostgreSQL, private networking, Container Apps, Key Vault and monitoring. **Not approved until the actual full 730-hour plus support-service quote fits €20/month.** If infeasible, an architecture or budget exception requires separate operator decision.

## 3. Deployment authorization is present but does not clear unverified gates

The operator supplied the EA subscription ID, stated the EUR 20 budget was validated and granted separate **synthetic staging deployment authorization**. Read-only Azure OIDC authentication and all providers are now confirmed. This is **not** actual deployer role authorization and is **not** a documented itemized current quote. Do not rewrite cloud evidence/status to `DEPLOYMENT_AUTHORIZED` or enable `paid_resource_creation_enabled` from this log.

The existing OIDC preflight identity is **Reader**; keep it unchanged. A future deployer must use a separate protected environment and scope-restricted identity with explicit least-privileged Azure roles. No live Gmail/Calendar/Drive/GitHub provider credentials or synchronization are authorized by this staging approval. EA Level 2B/2C remain HOLD.

## 4. Evidence required before a paid deployment workflow

1. Capture a dated, itemized, actual-subscription West Europe monthly quote with plausible compute-hours and a clear EUR 20 comparison.
2. Read actual PostgreSQL SKU quota/capacity eligibility, including supported deployment zone, private networking, and service availability. The SKU list alone does not prove these.
3. Review the database schema `001`–`005`, legacy-table isolation, a nonowner/no-BYPASSRLS database identity, migration readback and synthetic-only controls.
4. Verify prospective **separate deployment identity** and its restricted RBAC at the proposed EA resource-group scope (least privilege). Do not expand Reader.
5. Define alerting, manual/automated teardown, back-ups, service disabling, and resource cleanup; document maximum test hours and residual charges.
6. Only if all gates pass, stage a reviewed deployment workflow for **synthetic testing only**; then independently verify security, post-commit readback and costs before any real provider data scope is considered.

### Verified links

- [SKU test — PASS](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38657630948)
- [Provider registration / OIDC test — PASS](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38655941349)
- [Approved project baseline](./EA_STAGING_DECISION_WE_EUR20_20261013.json)
- [Prior full deployment design](./EA_STAGING_PREDEPLOY_PLAN_20261013.md)
