# EA Unified Calendar — Azure compute tariff evidence — 14:27, 15.10.2026

**Classification:** `AUTO_APPROVED` engineering evidence / `PENDING_REVIEW` private subscription tariff and deployment cost.
**Scope:** Ea-Personal_Assistant only; independent of AtlasOrbit Azure MCP/ACSEE. Region **West Europe**, max **€20/month all-in**, single private EA tenant and **48-hour synthetic-only** contemplated staging.
**Cloud authorization:** `NO_DEPLOYMENT`. Paid resource provisioning and all live Calendar/Gmail/Drive sync continue **HOLD**; preflight OIDC Reader stays Reader.

## Verified incremental progress

- Operator-reported merger of [PR #72](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/72) independently confirmed on GitHub (merge `3ad1206ed87e8d19522fdfca50a5ec757d245cfe`).
- Broader, unauthenticated price discovery is implemented by [`aca_compute_catalog_probe.py`](./pricing/aca_compute_catalog_probe.py), retaining all matched West Europe active compute public retail rows and avoiding cherry-picked positive/zero records, with no Azure subscription credential or resource access.
- Eight additional negative tests in [`test_aca_compute_catalog_probe.py`](./pricing/test_aca_compute_catalog_probe.py) passed in protected [pricing CI run #38734763203](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38734763203).
- The complete live public-catalog query through that run reported `ACA_CPU_POSITIVE_CANDIDATES=0`, `ACA_CPU_ZERO_CANDIDATES=1`, `ACA_MEMORY_POSITIVE_CANDIDATES=0`, `ACA_MEMORY_ZERO_CANDIDATES=1`. This is a successful **catalogue discovery** but **not** successful identification of an authorized billable compute rate.

## Exact public evidence — live 15.10.2026

| Candidate | Public meter ID | Retail response | Region / type | Interpretation |
|---|---|---|---|---|
| `Standard vCPU Active Usage`, `1 Second` | `0426badc-b719-5201-b141-b2d5c4943b7d` | `EUR 0.0` | West Europe / `Consumption` | **Rate unresolved; not accepted as a zero-cost subscription guarantee** |
| `Standard Memory Active Usage`, `1 GiB Second` | `3ba64b1c-cb46-5ee0-b086-a68736392ac0` | `EUR 0.0` | West Europe / `Consumption` | **Rate unresolved; not accepted as a zero-cost subscription guarantee** |

Both rows share `skuName=Standard`, `skuId=DZH318Z0B0NC/0001`, `isPrimaryMeterRegion=true` and `tierMinimumUnits=0`. No positive-cost alternative matching the active compute filters was observed within the returned public `Azure Container Apps` West Europe rows. **We have not proven** whether the zero-valued records are promotional, metering peculiarities or actual applicable prices. Do not re-label zero as billable or free based only on public pricing.

Microsoft [Container Apps billing documentation](https://learn.microsoft.com/en-us/azure/container-apps/billing) describes resource consumption billed by active vCPU-seconds and GiB-seconds plus external requests, with free grants **shared per subscription per month** (first 180,000 vCPU-seconds, 360,000 GiB-seconds and 2,000,000 requests). Availability/remaining balance of those grants on the operator's subscription has **not** been independently verified, and the model must assume none. Additional VNet managed public IP/LB charges are distinct.

## Remaining blockers

1. **ACA active vCPU/GiB unit tariff:** obtain independent subscription-applicable estimate through Azure pricing calculator / negotiated rate sheet / provider billing view that identifies exact SKU, region, price, billing periods and free allowance treatment; retain only sanitized status and evidence reference in public GitHub.
2. Complete all other categories in [48-hour quote template](./pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json), including private DNS month vs time prorating, ACA request billing, registry, Key Vault, backup excess, logs, data, VAT/tax as applicable, contingency, and post-teardown residuals.
3. **No spend ceiling proof:** Azure Cost Management budget notifications are informational thresholds, not a hard payment cap. Require operational bounded spend and verified teardown plan with independent empty-resource inventory readback; `48h` runtime end is not proof all charges cease.
4. **No release:** project must receive separate independent security/cost/least-privilege reviews before a new deployer identity or billable resources; existing Reader may not be elevated. Level 2B/2C and live sync continue HOLD.

## Decision

`PUBLIC_ACA_ACTIVE_METER_NO_POSITIVE_TARIFF_FOUND`; `ACCOUNT_SPECIFIC_BILLING_UNKNOWN`; `ALL_IN_20EUR_QUOTE_BLOCKED`; `TEARDOWN_COST_UNKNOWN`; `PROVIDER_SYNC_DISABLED`; `DEPLOYMENT_AUTHORIZED=false`.

**Default safe path:** continue in existing disposable PostgreSQL GitHub Actions CI (synthetic-only, no paid Azure subscription resources) while account-specific pricing evidence is missing. The code change and 30-day public-catalog artifacts do not change any production rights.

**Evidence:** [PR #73](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/73), [CI run #38734763203](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38734763203), [Microsoft Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing), [Microsoft Retail Prices API contract](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices).
