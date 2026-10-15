# EA Azure — 16 unresolved 48-hour cost categories: evidenced rates and proposed exclusions

Date: 2026-10-15
Status: PUBLIC_RETAIL_CANDIDATES_ONLY / SUBSCRIPTION_ALL_IN_QUOTE_BLOCKED / NO_DEPLOYMENT

## Strict scope

- Project: Ea-Personal_Assistant only, one private, synthetic-only tenant; West Europe; maximum 48h; Azure charge ceiling EUR20 inclusive of tax where applicable.
- Intended topology: PostgreSQL B1ms with 32 provisioned storage units and VNet injection; Container Apps workload-profiles v2 default pure Consumption with internal ingress, one managed static public egress IP and a Standard LB; one VNet, private DNS, Entra and dedicated Key Vault; no live Bring/Gmail/Calendar data.
- Existing four independently checked EUR catalog line items: PostgreSQL B1ms EUR0.840 for 48h, storage EUR3.856 for one conservative model month, managed static IPv4 EUR0.2112 and Standard LB first rule bundle EUR1.056 for 48h. **Known partial sum EUR5.9632**. See GitHub retail runs 38714329616 and 38725912112.
- Existing 20-category quote template still contains 16 unverified entries. THIS FILE IS A REVIEW PROPOSAL and does NOT change any state from unverified to priced/excluded in the authoritative machine quote. The default safety flags, Reader OIDC identity and production sync hold remain unchanged.

## 16 remaining quote categories

The EUR prices below are explicitly candidate retail rates from the successful GitHub Azure Retail Prices API output, unless designated documentation or assumptions. Quote completion requires matching actual SKU/tier, billable units, retention, contract/tax treatment and independently reviewed exclusion rationales.

| Code | Category | Rate or proposed 48-hour treatment | Provisional modeled EUR | Approval state |
|---|---|---|---:|---|
| 01 | postgres_backup | Flexible Server Backup Storage LRS EUR0.0906/GB-month for **excess** over included backup (up to 100% of provisioned storage). Max hypothetical excess 0.1GB-month. | 0.00906 | Unverified quantity; baseline may be included but never assume it |
| 02 | container_apps_usage | Proposed cap 1,800 vCPU-seconds, 3,600 GiB-seconds, 10,000 requests; requests rate EUR0.4928 per 1 million yields EUR0.004928. Paid vCPU/GiB metering cannot be inferred from 0-rated rows/free grant in observed catalog; determine chargeable per-unit rates or prove remaining shared subscription grants. | 0.004928 **PLUS UNKNOWN compute** | HOLD |
| 03 | container_apps_environment_fee | EUR0.1258/hour *if* paid feature is enabled (EUR6.0384 / 48h). Proposed no Dedicated profile, planned maintenance, or environment private endpoint. | 0 if formally EXCLUDED | Conditional exclusion; verify exact SKU/rules |
| 04 | container_apps_managed_auxiliary_resources | Additional Standard LB traffic: observed EUR0.0044/GB × proposed 0.5GB = EUR0.0022; extra LB rules, other managed infrastructure and traffic still require readback. Existing base managed IP/LB prices MUST NOT be double counted. | 0.0022 **PLUS UNKNOWN auxiliaries** | HOLD |
| 05 | container_apps_private_endpoint | Optional environment Private Endpoint rate EUR0.1258/hour (EUR6.0384/48h) if configured. Current internal VNet environment does not enable this feature. | 0 if formally EXCLUDED | Conditional exclusion |
| 06 | vnet_subnets | VNet/subnet allocation proposed in same VNet. No inter-VNet peering or cross-region VNet transfer. Peering, Private Link, LB, IP, egress and DNS belong to their own components. | 0 for basic allocation | Conditional exclusion of base VNet meter, prove no peering/NVA |
| 07 | private_dns | One private Azure DNS zone EUR0.44 per first-zone/month (full-month provision; actual billing prorated daily), and 10,000 queries × EUR0.352/million = EUR0.00352. | 0.44352 | Public catalog rate matched; account/tier and actual zone count need verification |
| 08 | nat_or_egress_gateway | No NAT Gateway in topology. ACA managed egress public IP already counted, Azure bandwidth egress separately priced. | 0 if formally EXCLUDED | Conditional exclusion with enforced no-NAT topology |
| 09 | private_link | Optional Azure Private Endpoint base EUR0.0088/hour (EUR0.4224/48h) **plus charged transfer** if used. Postgres uses private VNet injection, not Private Link. Key Vault network path must be independently proven using an allowable restricted service endpoint or budget changed for Private Link. | 0 **only if no Private Link** | Security-dependent HOLD |
| 10 | container_registry | If using dedicated ACR Basic: observed EUR0.1466/day × 2 full days = EUR0.2932. Verify included storage versus extras and app image transfer. Public GHCR might avoid Azure ACR but has separate provider/security/provenance review; do not assume private GHCR zero-cost. | 0.2932 | Candidate ACR amount; private billing confirmation required |
| 11 | key_vault | Standard vault secret operations observed EUR0.0264/10,000; cap 1,000 => EUR0.00264. No HSM/premium keys. Verify network path and vault/secret cleanup. | 0.00264 | Candidate rate, networking unresolved |
| 12 | logs_monitoring | Example 0.1 GB Analytics Logs ingestion at paid West Europe EUR2.6311/GB = EUR0.26311, plus conservative 0.1GB-month retention at EUR0.1144/GB-month = EUR0.01144. Also check alerts, retention, query/egress paid features. | 0.27455 | Partial; actual workspace/meter tier unknown |
| 13 | data_egress | Model 0.5GB outbound × conservative first-tier Microsoft Global Network candidate EUR0.0766/GB = EUR0.0383; first 100GB/month free may apply but deliberately not counted. Confirm exact region routing/tier and potential billing beyond quota. | 0.0383 | Candidate nonfree tier; account discounts/free tier not counted |
| 14 | other_cloud | Do not use third-party hosted provider services/extra paid runner/network/image egress. Exclude only after verified service inventory and GitHub billing review. | 0 if formally EXCLUDED | HOLD pending inventory; GHCR/CI charge possible |
| 15 | taxes | Tax jurisdiction and invoice-reverse-charge status of the actual Azure business subscription UNKNOWN. An **illustrative** 21% VAT sensitivity is not an assertion of applicable tax; do not record 0 or 21% until verified. | UNKNOWN | HARD HOLD |
| 16 | contingency | Recommend an operator-selected 20–25% modeled reserve, plus explicit teardown-tail hour assumptions and service minimum charges. This is a risk provision, not a published Azure retail charge. | 25% of confirmed subtotal as sensitivity only | HARD HOLD |

## Provisional arithmetic (NOT a quote)

Previously verified four-line retail subtotal: **EUR5.9632**.

Additional *conditional* modeled amounts, assuming all optional features truly excluded:
- Backup overage: 0.00906
- ACA HTTP requests only: 0.004928 (CPU/memory still unknown)
- Managed LB 0.5GB processing: 0.0022 (other auxiliaries still unknown)
- One private zone + 10,000 DNS queries: 0.44352
- ACR Basic 2 days: 0.2932
- Key Vault 1,000 ops: 0.00264
- 0.1GB paid logging + modeled retention: 0.27455
- 0.5GB paid-band egress: 0.0383

Arithmetic-only total of known/candidate rows = **EUR7.031598**. This is neither the provider's all-in invoice nor a complete upper bound. Excludes: paid ACA CPU and memory, extra managed resources, real Key Vault networking path, optional premium endpoint, actual tax, residual cleanup, billing surprises and possibly CI/provider charges.

Example sensitivity **only** if all missing items were later independently proven zero: EUR7.031598 * 1.25 contingency * 1.21 illustrative VAT = **EUR10.635292**. This example must NOT be used for deployment authorization or evidence of tax treatment.

## Exclusion checklist and independent verification requirements

Conditional exclusions can be accepted only when the deployed topology and billing evidence explicitly prove they are **not provisioned**:
- No Dedicated Container Apps profile, no managed environment Private Endpoint and no planned maintenance that triggers the environment management rate.
- No NAT Gateway, Azure Firewall, DNS Resolver, peering, separate Private Link endpoint or cross-region network. An internal VNet design does **not** negate the mandatory managed public IP and Standard LB.
- If Key Vault firewall requires a private endpoint and secure VNet service endpoint cannot be proven from the actual Container Apps subnet, **do not exclude Private Link**; re-price and review the design instead.
- No external registry or runner billing beyond an already confirmed allowance; do not use unknown as zero.
- Included PostgreSQL backup is conditional on **Backup Storage Used** remaining <= provisioned 32GiB; 7-day retention and low synthetic workload alone do not prove this.
- Paid ACA active vCPU/GiB rate and existing shared subscription free allowance require exact pricing/benefit evidence; observed zero-rate catalog rows are not sufficient to conclude an incremental deployment is free.
- DNS zone month, DNS queries, actual total LB data processing including platform management traffic, outbound routing, ACR storage, Key Vault operation count and retention/log ingestion need account-specific or conservative independent bounds.
- Apply verified actual invoicing/tax treatment and a separate budgeted teardown-delay reserve. Post-delete independent ARM inventory and actual cost reconciliations remain mandatory.

## Recommendation and gates

1. Use this as an engineering **proposal only**, retaining the original machine-readable 20-category quote template as BLOCKED. No fake verified prices/exclusions.
2. Run a scoped read-only quote from actual EA subscription billing/retail and Container Apps SKU for each unresolved charge. Obtain the account VAT/tax information privately, outside this public GitHub repo.
3. Verify managed Key Vault network access without introducing an unpriced private endpoint. Review immutable resource inventory and cleanup authority for ACA managed infrastructure groups.
4. Request a dated, itemized all-in quote including <=EUR20 worst-case 48h resource plus cleanup tail, independently approved security/financial gate, **then** consider creating a separate deployer identity. Keep the existing GitHub OIDC Reader unchanged.
5. Do not provision Azure resources, expand cloud RBAC, enable Bring runtime access, transfer real shipment data or turn on autonomous synchronization while the quote is BLOCKED.

## Source evidence

- [GitHub EUR retail rates: PostgreSQL and ACA](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38714329616)
- [GitHub EUR retail rates: network, DNS, Key Vault, logs, registry and bandwidth](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38722335284)
- [GitHub EUR retail rates: managed Standard IP/LB and DNS](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38725912112)
- [Microsoft: ACA VNet managed resources, public IP and LB](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks)
- [Microsoft: Container Apps consumption billing and shared grants](https://learn.microsoft.com/en-us/azure/container-apps/billing)
- [Microsoft: PostgreSQL included backup storage and excess charges](https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore)
- [Microsoft: Private DNS zones and query charges](https://azure.microsoft.com/en-us/pricing/details/dns/)
- [Microsoft: Key Vault VNet service endpoints and firewall](https://learn.microsoft.com/en-us/azure/key-vault/general/overview-vnet-service-endpoints)
- [GitHub: Packages billing for public versus private container images](https://docs.github.com/en/billing/concepts/product-billing/github-packages)
- [Microsoft: budgets alert but do not halt resources](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)

**Release result: INCOMPLETE_ALL_IN_QUOTE / AZURE_DEPLOYMENT_HOLD / PRODUCTION_SYNC_DISABLED.**
