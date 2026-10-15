# EA Azure — West Europe networking EUR pricing, quota and future identity gate

**Date:** 15 October 2026  
**Status:** `PUBLIC_PRICE_CATALOG_RESEARCH / PRIVATE_QUOTA_READ_PENDING / DEPLOYER_UNCONFIGURED / NO_DEPLOYMENT`

## Verified context
- [EUR retail base rate run](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38714329616) and [48h cost gate](./EA_AZURE_48H_SYNTHETIC_STAGING_PLAN_20261015.md) confirm PostgreSQL B1ms compute 48h €0.840 and a conservative month of 32 storage units €3.856; this **€4.696 subtotal excludes network, Container Apps, backups, logs and taxes**.
- [Azure Reader identity probe](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38717508118) established non-free billing type, but free-account PostgreSQL allowance **INCONCLUSIVE**; assume no discount.
- Microsoft documents Container Apps Consumption subscription-shared grants but extra own-VNet charges can apply: https://learn.microsoft.com/en-us/azure/container-apps/billing
- VNet-integrated **workload profiles** Container Apps environment supports minimum `/27` subnet, unlike older Consumption-only environments requiring `/23`: https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks
- PostgreSQL Flexible Server quota API: https://learn.microsoft.com/en-us/rest/api/postgresql/quota-usages/list?view=rest-postgresql-2025-08-01

## Implemented read-only public Azure price discovery
`.github/workflows/ea-azure-network-quota-readonly.yml` runs `pricing/azure_network_retail_probe.py` using Microsoft's public [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices). Searches network/support **retail meter candidates** for Virtual Network, Azure DNS, Private Link, NAT Gateway, Bandwidth, Container Apps, Container Registry, Key Vault, Log Analytics and PostgreSQL. Outputs a public-only, 30-day artifact with meter IDs/prices, not secrets.

**Interpretation:** A catalog search returning zero rows for a name is an unknown price, **not free service**. Meters can be globally billed under unexpected `serviceName` or associated with conditional options. Before advancing the €20 quote gate, select only precise features of an independently reviewed network topology, identify their specific billing meters, check price units, and explicitly exclude others with proof.

## Implemented protected read-only quota discovery
Once this PR has merged, manually dispatch:
```powershell
gh workflow run ea-azure-network-quota-readonly.yml --repo nanotech-solutions-norway/Ea-Personal_Assistant --ref main
```

The quota job reuses exactly the **existing immutable GitHub OIDC `ea-staging-preflight` Reader** identity. It asserts the target tenant/subscription, executes this supported **GET only**:
```text
https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.DBforPostgreSQL/locations/westeurope/resourceType/flexibleServers/usages?api-version=2025-08-01
```
The sanitized result reports only whether `standardBSFamily` and overall `cores` show positive, zero or unknown quota headroom. It never emits subscription or customer IDs or raw quota records.

**Important:** Even positive quota does not prove a specific `Standard_B1ms` physical capacity/zone at deployment time. A 403, unsupported API, absent record or malformed result reports **UNKNOWN** and blocks eligibility; do not expand Reader to Contributor for diagnostics.

## Suggested cost-optimized private layout (design only)

- PostgreSQL Flexible Server with **private VNet injection**, delegated subnet, dedicated private DNS (no public DB IP).
- Separate Container Apps Consumption **workload-profiles VNet** integration subnet, isolated from delegated PostgreSQL subnet; choose an internal environment/ingress for synthetic testing only.
- Proposed addressing must be checked against the real Azure subnet delegation, min `/27` workload-profile requirement, DNS records, routing, traffic controls and resource provider behavior. No inbound public webhooks or tenant data.
- **Avoid enabling Container Apps Environment Private Endpoint unless the threat model actually requires it.** VNet integration for outbound connectivity is not the same as a private endpoint on the environment; the latter was observed at retail €0.1258/hour and would add €6.038 for 48 hours *if enabled*. No claim that internal VNet topology itself costs zero.
- Avoid unnecessary always-on NAT gateway and dedicated image registry; **do not** replace them with unverified free external-hosting assumptions. Direct authenticated GHCR image pulls and supply-chain evidence must be validated if chosen.
- Use application-managed identity and Key Vault access without expanding Reader; no customer secret activation. Run DB integration from a trusted in-network execution environment because ordinary public GitHub-hosted runners cannot access private VNet endpoints by default.
- All paid resources must be in a **dedicated, expiry-tagged, synthetic-only EA RG**, eventually demolished after a precisely approved 48h window, with independent ARM inventory proof and cost reconciliation.

### Required price gate, not yet satisfied

Use the strict [17-category quote validator](./pricing/timeboxed_cost_gate.py) and [incomplete template](./pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json). It **must continue to return BLOCKED** until each priced or explicitly excluded service is verified (including taxes if applicable), accurate recurring/residual costs and full usage units, no unsupported free credits, and review of SKU quota, topology and actual-account billing. Azure budgets warn only and cannot guarantee a spending cap.

## Future separate deployer identity — instructions only, NOT created

Do **not** reuse `ea-github-oidc-preflight` or alter its **Reader** permission. Only **after cost, quota and reviewed topology gates pass**:

1. Authorized Entra administrator creates **separate** app registration `ea-github-oidc-deployer` with one immutable GitHub environment federated credential:
   - Issuer `https://token.actions.githubusercontent.com`
   - Environment `ea-staging-deploy`
   - Subject `repo:nanotech-solutions-norway@215678827/Ea-Personal_Assistant@1289533798:environment:ea-staging-deploy`
   - Audience `api://AzureADTokenExchange`.
2. GitHub maintainer creates separate **protected** environment `ea-staging-deploy` (main-only, required review where plan supports it). Add only the new **deployer** client ID as an environment variable, together with the verified tenant/subscription IDs; no secrets are necessary for workload federation.
3. Azure administrator independently creates/approves the *dedicated EA resource group* only **after** the full bill is accepted. Then grants the new deployer **Contributor restricted to this EA RG**, not the entire subscription. Resource provisioning may need further custom least-privilege permissions; a separate administrator, not the deployer, handles role assignments, policy exceptions and tenant scope.
4. Before any actual deployment, audit scope/effective permissions, restrict allowed resource kinds and names, test an exact-group fail-closed dry run and deletion operator fallback. Do not grant Owner, User Access Administrator, subscription-wide Contributor or secrets access to the preflight identity.
5. Never enable the deployer environment, create its resource group, configure live provider OAuth or perform resource creation based solely on this document.

## Required follow-up
1. Run public retail price CI and examine candidate meters; resolve true feature-specific prices and uncertainties.
2. Manually dispatch the protected Reader quota GET after merge; evaluate categorized quota and independent ARM capacity.
3. Build a fully evidenced **EUR20 all-in** estimate for a 48h test with **no free credits counted**.
4. Only then discuss the separate deployer identity, specific resource approvals, teardown rehearsal and possible synthetic test launch. Existing production/live scopes remain **HOLD**.

No paid resources, account changes or external data synchronization are performed in this PR.

## Actual Microsoft public retail meter evidence — 15 Oct 2026

[Public EUR network/catalog run 38722335284](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38722335284) **PASS** on the proposed PR; 30-day public artifact contains all matching meter IDs and prices. This is **not** a subscription bill or a priced approved topology. Price units and tier applicability still require human mapping.

| Potential feature/meter | Public retail EUR unit rate | Illustration for 48h, only if enabled | Important caveat |
| --- | ---: | ---: | --- |
| PostgreSQL B1ms compute | €0.0175/hour | €0.840 | plus storage, backup etc. [earlier verified] |
| PostgreSQL assumed full-month 32 storage units | €0.1205/billed GB-month | €3.856 | conservative full-month assumption [earlier verified] |
| Virtual Network Private Link — **Standard Private Endpoint** | €0.0088/hour | €0.4224 | optional endpoint; data processed is additional |
| NAT Gateway — **Standard Gateway** | €0.0396/hour | €1.9008 | exclude only when secure topology proves not required; data processing is additional |
| Azure Container Apps — **Environment Management Hour** | €0.1258/hour | €6.0384 | verify plan/environment billing applicability; distinct from app consumption |
| Azure Container Apps — **Environment Private Endpoint** | €0.1258/hour | €6.0384 | only for this endpoint feature; do not automatically assume required |
| Azure DNS — **Private Zone** | €0.44 for unit `1` (also lower volume-tier row €0.088) | **No 48h estimate** | meter unit lacks explicit month; tier and billing basis must be corroborated before quote |
| Azure Container Registry — Basic Registry Unit | €0.1466/day | €0.2932 for 2 full days | only if ACR actually used; image data and external transfers can add costs |
| Log Analytics — Analytics Logs Data Ingestion | €2.6311/billed GB (a zero-rated tier row also exists) | depends on actual billable ingestion | do not assume `0` without account allowance proof |
| Key Vault Standard — Operations | €0.0264 per 10,000 ops | depends on operations | actual transaction mix and retention still unknown |

Potential conditional total **without DNS, app consumption, network data, backup, log usage or tax** if PostgreSQL base + both Container Apps environment meters + NAT + standard Private Link endpoint + two days of ACR Basic are all active: `€4.696 + €6.0384 + €6.0384 + €1.9008 + €0.4224 + €0.2932 = €19.3888`. This is **only arithmetic of selected conditional meters** and **not** evidence that they can or should be deployed together, nor a feasible complete €20 bill. Even small additional charges could exceed the ceiling.

**Pricing source:** [Microsoft Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices). Retail EUR values are reference rates, not an account-specific contracted quote. Missing/unmatched serviceName (for example `Azure Private Link` returned zero, whereas a Private Link endpoint meter appeared under `Virtual Network`) means catalog search mismatch, **not free**.

The new `pricing/azure_quota_readonly.py` has passed PR offline unit tests. It is deliberately **not executed during PR CI**; the subscription-specific GET requires manual dispatch from `main` after merge. Thus actual PostgreSQL B-series quota/placement remain **NOT VERIFIED**.
