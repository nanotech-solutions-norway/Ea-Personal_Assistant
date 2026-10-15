# EA Azure 48h — private topology and complete managed infrastructure cost review

**As of:** 15 October 2026  
**State:** `DESIGN_REVIEW_COMPLETE_FOR_STATIC_CONFIGURATION / PRICE_METERS_PENDING / NO_RESOURCES`  
**Decision:** `NO_DEPLOYMENT`. Operator ceiling €20 including applicable taxes, for one private **synthetic-only** EA tenant.

## 1. Reference architecture — no Azure deployment manifest

Canonical machine-readable proposed private VNet specification: [EA_48H_PRIVATE_TOPOLOGY_PROPOSED_20261015.json](./pricing/EA_48H_PRIVATE_TOPOLOGY_PROPOSED_20261015.json). Static security checks: [validate_private_topology.py](./pricing/validate_private_topology.py); adverse/negative tests: [test_validate_private_topology.py](./pricing/test_validate_private_topology.py).

- **Azure VNet:** proposed `10.88.0.0/24` (illustrative; must check for overlaps with real subscription networking). Both app and DB in the *same VNet, separate subnet delegations*.
- **Private PostgreSQL Flexible Server:** `10.88.0.0/28` delegated **exclusively** to `Microsoft.DBforPostgreSQL/flexibleServers`; `Standard_B1ms` only a candidate, 7-day locally redundant backup, no HA, no public database endpoint and no bypass firewall rule. VNet-injected servers require Private DNS; propose `ea-staging.postgres.database.azure.com` linked to this VNet.
- **Container Apps environment:** workload profiles (v2) with the default **Consumption** profile only, custom VNet `10.88.0.64/27` (delegated to `Microsoft.App/environments`), internal ingress and synthetic jobs only; no planned maintenance, Dedicated profile or Container Apps environment private endpoint unless separately reviewed.
- **Application execution:** minReplicas=0 where feasible, no external Gmail/Calendar/Drive/Bring/GitHub OAuth, no public webhooks. Synthetic migrations and probes must run from an approved **in-VNet** execution path; a standard GitHub-hosted runner cannot directly connect to private PostgreSQL.
- **DNS/routing:** use Azure Private DNS with VNet link. No separate Azure DNS Private Resolver or NAT Gateway assumed. Actual platform-managed egress routing must be tested before pricing complete.
- **Identity:** current `ea-staging-preflight` immutable OIDC principal stays **Reader**, no Contributor/Owner or resource write rights. Separate deployer identity remains **uncreated** until complete cost/teardown approvals.
- **Teardown:** dedicated prospective `rg-ea-stg-westeurope`; inventory managed Container Apps infrastructure RG (default `ME_`), managed load balancer, static egress IP, private DNS links, retained logs, backups and orphaned managed resources. `az postgres flexible-server stop` is **not** a teardown. Independent ARM readback and cost reconciliation required; never blindly delete unrelated managed RGs. No deletion workflow or Azure role is created now.

Microsoft references:
- [PostgreSQL private VNet injection, /28 minimum, private DNS and delegated subnet](https://learn.microsoft.com/en-us/azure/postgresql/network/concepts-networking-private)
- [Container Apps workload v2 VNet subnet /27 and network restrictions](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks)
- [Container Apps billing: the Consumption profile vs dedicated management and private endpoint costs](https://learn.microsoft.com/en-us/azure/container-apps/billing)
- [PostgreSQL backup: 7-day default and included backups up to provisioned storage](https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore)

## 2. Required cost correction: **platform-managed IP and LB are billable**

Microsoft's [Container Apps custom virtual networks documentation](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks) states **additional bills for one Standard static public egress IP and a Standard load balancer** for a workload-profile environment integrated with a customer VNet, *including internal environments*. The infrastructure may appear in a separate managed infrastructure resource group. In other words, **no public app ingress does not mean no public egress IP resource charge.**

**Cost-gate correction:** the existing [17-category €20 quote gate](./pricing/timeboxed_cost_gate.py) previously missed these required costs. It now explicitly demands three additional categories:
- `container_apps_managed_public_ip`
- `container_apps_managed_load_balancer`
- `container_apps_managed_auxiliary_resources`

Each category must have a dated evidence reference and explicit EUR pricing or independently justified exclusion. The [quote template](./pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json) remains intentionally **BLOCKED** until all mandatory costs are accounted for. The template is not a deployment manifest.

[Public EUR retail probe](./pricing/azure_foundation_meter_probe.py) retrieves catalog candidates for `IP Addresses`, `Load Balancer`, `Virtual Network`, `Azure Container Apps` and `Azure DNS` without credentials. Results are 30-day **public** GitHub CI artifacts. Tiered price rows with the same meter ID and different values must be matched against exact `skuName`, `tierMinimumUnits`, region and usage; selecting arbitrary lowest tier price is forbidden.

## 3. Economic scenario (illustrative, not quote)

The only previous directly price-verified base case remains the conservative 48-hour PostgreSQL B1ms compute **€0.840** plus 32 storage units charged for one modeled month **€3.856** = **€4.696**.

**Do not add unnecessary premium features:** for pure Consumption without dedicated workload profile, private endpoint or planned maintenance, Microsoft documents that **Dedicated-plan management fees are not charged**. The catalog's €0.1258/hour `Environment Management Hour` cannot automatically be treated as mandatory for this proposed pure-Consumption environment. The `Environment Private Endpoint` meter also does **not** apply when the environment endpoint is not enabled. This is a conditional design exclusion, **not an all-in cost approval**. Need confirm exact Azure environment implementation/tariff before reliance.

**Backup:** PostgreSQL includes storage for backups up to **100% of provisioned server storage**. For a small synthetic DB with 7-day retention and no geo redundancy, paid excess backup **may** be zero; this is a *usage assumption*, not independently observed actual backup volume. Heavy WAL or other backup usage may exceed the allowance; cost gate needs an explicit bound.

**Still need an independently priced, current 48-hour BOM including:** PostgreSQL compute/storage/excess backup, Container Apps actual vCPU/memory/requests (do not automatically assume unused subscription-shared free grants), managed **public static egress IP**, managed **Standard load balancer** (rule-hours and data processed), Private DNS zone and queries, all network egress/traffic, container image registry/pull/egress, Key Vault, logs, taxes and contingent billing past teardown. Premium endpoint/NAT/DNS resolver must be separately excluded or explicitly priced with evidence; no shadow charges treated as zero.

### Why the deployment is still held

1. The exact IP/LB retail meters and feature-specific quantities must be read, not guessed; managed groups and teardown costs need a validated inventory.
2. Current West Europe PostgreSQL **Burstable and core quota headroom** was verified positive via [manual run 38723036350](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38723036350), but **B1ms real-time zone capacity is not reserved**.
3. Free-account benefit verification is **inconclusive**; assume no PostgreSQL free credit.
4. Even if arithmetic appears ≤€20, the gate verifies only completeness/consistency, not real Azure account prices, future billing, ability to delete in time or deployment authorization. Independent cost, security and least-privilege signoffs remain required.

## 4. Next gated engineering tasks

1. Capture actual *mandatory* managed Public IP / Standard Load Balancer EUR retail meter candidates and applicable hourly/processed-data units, using the new read-only CI run; produce a dated line-item estimate.
2. Reconcile Private DNS billing units and service-specific backup/storage/ACA consumption assumptions, including a **net and VAT-inclusive** ceiling test when VAT applies.
3. Recalculate design option **pure Consumption + VNet-injected PostgreSQL** against €20; select/reject premium options explicitly. Define test traffic limits and cost contingency; use conservative billed 48h+ teardown delay.
4. Perform independent threat-model and route/DNS/private ingress review, inventory management resource groups and required delete permission; conduct a **non-deploying** teardown checklist validation.
5. Only if a complete independently audited quote ≤€20 and deployment safety proof exist: define a **separate** `ea-staging-deploy` identity with resource-group-scoped RBAC for reviewed exact resources. Keep existing Reader untouched. No Azure resources created in this engineering batch.

**Project flags:** `paid_resource_creation_enabled=false`, `live_provider_sync_enabled=false`, `level_2b_enabled=false`, `level_2c_enabled=false`. No cloud write/role assignment/e-mail action is authorized by this document.
