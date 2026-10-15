# EA Unified Calendar — 48-hour private staging teardown and billing-tail review
**Date:** 15 October 2026 (Europe/Madrid)  
**Status:** `STATIC_DESIGN_VALIDATION_ONLY / ALL_IN_QUOTE_INCOMPLETE / NO_DEPLOYMENT`  
**Governance:** code/test/process changes AUTO_APPROVED; numerical usage and rate assumptions, cloud deployment, new identity/RBAC, real provider sync and all-in VAT cost sign-off PENDING_REVIEW.

## Verified context
- [PR #74](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/74) merged into EA `main`, adding a local-only billing profile CSV candidate validator. It does not retrieve private billing rates automatically or authorize resources.
- Target is the **EA Personal Assistant project alone**. Private **synthetic-only** West Europe tenant, proposed maximum 48 hours and **€20 total monthly bill including applicable taxes and residual charges**, with no deployment yet.
- The existing quoted €5.9632 arithmetic sum is a **PUBLIC RETAIL PARTIAL** for 48h PostgreSQL B1ms compute, full-month PostgreSQL 32-unit storage, ACA-managed public IP and LB base rule bundle. It neither establishes account-specific rates nor a guaranteed lower/upper bill.

## New static teardown-evidence inventory
[Proposed JSON obligations](./pricing/EA_48H_TEARDOWN_OBLIGATIONS_PROPOSED_20261015.json) and [offline gate](./pricing/teardown_liability_gate.py) define **15 separately traceable resource/charge classes**, including:

1. EA staging resource group and the **managed ACA infrastructure resource group** (possible default `ME_` for workload profile, not the unrelated `MC_` consumption-only profile).
2. ACA environment, its managed Standard public outbound IP, Standard load balancer and network data processing.
3. PostgreSQL Flexible Server and persisted backup/storage billing, independent of a compute stop.
4. Private DNS zone and VNet link, VNet/delegated subnets and all connected dependencies.
5. Registry/image artifacts, Key Vault/secrets, log storage/retention and other service billing tails.

Every proposed item is `NOT_OBSERVED`, its deletion readback `NOT_PERFORMED`, and tail billing `UNVERIFIED`. The machine-readable document **cannot** be changed into actual evidence by inventing Azure resource IDs, deletion results, financial amounts or a `DELETE_SUCCESS` state. Tests reject fabricated claims, unexpected cloud controls, missing items, extra resources, wrong region, live sync and elevated spend assumptions. The tool never authenticates, provisions, alters RBAC or issues an Azure deletion.

**Important correction for managed resources:** Microsoft says an app environment with custom VNet creates a platform-managed infrastructure RG, usually `ME_` for workload profile; do **not** manually modify that managed RG. When a *legitimately authorized* deletion of its owning ACA environment is completed, an independent post-deletion GET/inventory check must verify the managed dependencies actually disappeared. Do not delete broad `ME_*` or `MC_*` matches; they could belong to other services. A resource group deletion request may be asynchronous, locked or fail on dependencies; mere receipt of HTTP 202 is not evidence of complete deletion. References: [ACA custom VNet/managed costs](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks), [Azure RM resource-group deletion and post-delete GET](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group), [ACA VNet tutorial cleanup](https://learn.microsoft.com/en-us/azure/container-apps/vnet-custom).

## Public priced subset sensitivity — hypothetical tail after 48h

The only known recorded public billing subset is modeled as €3.856 full-month PG storage + **€0.0439 hourly** across PG B1ms compute, ACA static public IP and Standard LB initial rule bundle. An extension in billable resource lifetime gives:

| Hypothetical extra billable resource lifetime | Subset illustration, EUR | Is it total invoice/upper bound? |
|---:|---:|---|
| 0 hours | 5.9632 | **NO** |
| 6 hours | 6.2266 | **NO** |
| 24 hours | 7.0168 | **NO** |
| 48 hours | 8.0704 | **NO** |

These are hypothetical *delayed removal of the three selected hourly meters* scenarios, not verified actual lifetimes or proof those three components survive equally. In particular, the remaining true cost **cannot** be inferred by subtracting this subset from €20, because ACA compute/memory/request rates, managed extra resources, data traffic, DNS, backup excess, registry, logging, tax and deleted-but-billable storage are **unknown**. The same budget does not guarantee an automatic spend shutdown: [Microsoft Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).

## Required independent teardown acceptance (not performed)
- **Before creation:** identify a dedicated EA subscription/resource group with protected lifecycle tags, exact owning relationship to managed ACA RG, a least-privilege deployer **separate** from immutable Reader, and a clear account-level €20 budget feasibility assessment. No cloud writes until all gate approvals recorded.
- **During timebox:** enforce schedule/synthetic-only, disabled customer/provider OAuth and no unsanctioned extra resource SKU; independently monitor resource additions, actual billed usage and projected residual charges. Budget alerts are not an enforced cap.
- **Termination:** only a separately authorized operator/infrastructure process may invoke deletion, with explicit resource group IDs and ownership review; avoid wildcard deletes, managed group tampering and unrelated subscription/resource-group actions.
- **Independent readback:** verify **actual** ARM absence of explicitly enumerated primary and managed resources, VNet/subnet/DNS link, public IP/LB and retained storage/backups, registry, secrets and logs. Record any surviving dependencies, lock errors, deletion 202 pending states and expected data-retention billing.
- **Billing reconciliation:** recheck subscription cost detail **after enough billing ingestion time**; confirm account-specific tax-inclusive charge and absence/presence of tail charges. An ARM inventory devoid of resources alone is insufficient to claim zero future billing.

## Engineering result

The code may report `model_validation=PASS` for the **honestly incomplete design** and simulate delay sensitivity, while every positive authorization output remains `false`. It deliberately retains `quote_gate=BLOCKED`, `all_in_cost_upper_bound_verified=false`, `zero_post_teardown_liability_verified=false`, `independent_arm_resource_deletion_verified=false`.

Next gate: merge CI-passing engineering changes; independently establish account billing contract/rates and remaining free allowance; price every cost component plus VAT, teardown delay and contingency; review real private architecture and deletion authority. If an all-in bound <= €20 **cannot be proved**, do not provision Azure, and continue GitHub Actions disposable PostgreSQL tests instead.

**No customer data, Azure subscription identifiers, secrets, personal schedules, or private rate sheets are in this public document or the associated test fixtures.**
