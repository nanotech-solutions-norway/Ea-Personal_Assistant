# EA Unified Calendar — Independent all-in meter coverage review
**Date:** 15 October 2026, Europe/Madrid  
**Project:** `nanotech-solutions-norway/Ea-Personal_Assistant` only  
**State:** `NONDEPLOYABLE_EVIDENCE_INVENTORY` — `€20_ALL_IN_COST_NOT_ESTABLISHED`

## Context: confirmed prior merge
- [PR #76](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/76) is confirmed **MERGED**, merge commit `4bfbcec0f893170fabb59149659809476fb80445` at 13:08:30 UTC on 15 October 2026.
- The 48-hour West Europe, single private synthetic EA environment is **proposed, not deployed**.
- The previously validated €5.9632 is the *sum of just four public retail billed lines*, not a floor, cap, quote, subscription tariff or guaranteed invoice.
- Existing [`timeboxed_cost_gate.py`](./pricing/timeboxed_cost_gate.py) can prove only *internal arithmetic and a 20-parent-category table*; a human or test fixture can fill missing parents with invented `"priced":0` and a syntactically valid `https://` link and get a `QUOTE_WITHIN_CAP_PENDING_INDEPENDENT_GATES` result. That preliminary status is **not evidence of a true charge**. It never grants `deployment_authorized`. The new finer-grained audit records and tests this distinction explicitly without breaking legacy synthetic price-gate tests.

## 37 independent charge dimensions / 20 parent categories
[Machine-readable, entirely public and non-account-specific evidence matrix](./pricing/EA_ALL_IN_BILLABLE_METER_MATRIX_PROPOSED_20261015.json) and [offline coverage tool](./pricing/all_in_meter_coverage.py) split every required parent into its separately priced/justified subordinate billed components. Inventory spans:
- PostgreSQL server compute, storage, backup-excess and retention/post-deletion storage.
- Container Apps vCPU-seconds, GiB-seconds, requests and idle billing; any environment management charges.
- ACA **managed public outbound IP hourly charge AND lingering charge**, **Standard LB base rules AND billable data processing / extra rules AND lingering charge**, other managed resource group items.
- Optional private endpoint, NAT gateway, Private Link and VNet meters, with *proposed exclusion not yet verified* — not silently assumed free.
- DNS zone billing period **and query traffic**, registry storage/tier, Key Vault transaction/tier, monitoring ingestion/retention/other service meters, egress and transfer.
- Other ancillary and late post-delete billing, VAT/other taxes, contingency.

### Current published candidate distribution
| Evidence state | Meter count | Meaning |
|---|---:|---|
| `PUBLIC_RETAIL_PARTIAL_UNVERIFIED` | **4** | Prior public Azure rate candidates for PostgreSQL compute and full-month storage, ACA-managed IP and Standard LB first-rule bundle; source-bound to old CI. Not a private agreement rate. |
| `PROPOSED_EXCLUSION_NOT_ACCEPTED` | **4** | Provisional architecture scope for pure Consumption environment management, standalone ACA endpoint, standalone NAT and standalone Private Link; not independently confirmed. |
| `UNKNOWN` | **29** | No subscription-specific, all-in applicable rate, verified nonapplicability or tax/retention bound. |
| **Total dimensions** | **37** | No dimensions independently approved as account-priced or zero cost. |

**Specific original quote omissions:** A parent `container_apps_managed_load_balancer` marked `priced` includes a rate only for the base rule-hours, **not** data processed, additional rules, or teardown tail. `container_apps_managed_public_ip` omits extra resource lifetime. PostgreSQL storage's initial full-month pricing cannot certify no further retained storage billing or backup excess. The audit surfaces these mismatches as `parent_marked_priced_but_child_meters_unverified`.

## Independent assurance requirements
The matrix is a static **inventory of unknowns**; it must **not** be promoted to a cloud clearance workflow by adding `PRIVATE_ACCOUNT_VERIFIED` or `INDEPENDENTLY_APPROVED` strings in GitHub. Unit tests reject unsupported verified states, missing charge dimensions, zero-substitution of the four historical partial amounts, wrong evidence links, spurious charge exclusions, unexpected approval fields, 48h expansion, real provider sync and cloud writes. It deliberately cannot output any positive spending or live-sync authorization.

### What is actually required to close this gate
1. **Privately identify the EA subscription's real Azure billing agreement** (Microsoft Customer Agreement, EA, CSP/partner, trial etc.). Do not guess MCA based on a price sheet or public docs.
2. Use the appropriate agreement's billing-admin console/authorized private export. For MCA only, the merged [offline local billing-profile candidate parser](./pricing/private_billing_evidence.py) helps audit CPU/Memory candidate consistency. It does **not** authenticate the agreement or reveal the private prices in public CI.
3. Separately verify the applicable subscribed rates and free-grant balance for **every billable meter**, including **ACA active CPU/GiB** rows that public Retail Prices API returned as `0`; zero returned by public REST catalogue is not proof of zero account charge.
4. Use a local confidential model to quantify bounded active usage + **a conservative post-teardown liability interval**, billing period/minimums, backup retention, ancillary managed RG resources, VAT (if applicable), taxes and contingency. Do not equate only the proposed 48h execution with full lifetime of all charge-bearing resources.
5. Independently review scope, least-privilege deployment identity, termination ownership, resource readback, alert limitations and actual **tax-inclusive ≤€20** feasibility. A budget notification is **not a spending kill switch**.
6. If account data/contract evidence cannot be obtained or upper bound is uncertain, **remain on no-charge synthetic GitHub CI** and do not create Azure billable resources.

## No-change protected boundaries
Current preflight GitHub OIDC **Reader stays Reader**. No new `Contributor` grants, IAM changes, credential acquisition, API calls to private subscription billing, Azure resource create/delete, customer data, live Gmail/Calendar/Drive/Bring sync, public webhook or Level 2B/2C promotion.

**Assessment:** Static model coverage PASS ≠ independently priced completion. The correct decision remains `NO_DEPLOYMENT`. Existing independent security and teardown reviews are still required even after subscription-specific financial evidence arrives.

References: [Azure Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing), [Azure Container Apps VNet managed infrastructure](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks), [Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets), [retail price API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices).
