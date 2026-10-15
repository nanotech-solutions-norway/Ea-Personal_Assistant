# EA Azure — 48-hour synthetic staging plan and fail-closed EUR 20 gate

**Prepared:** 15 October 2026  
**Status:** `DESIGN_ONLY / 48H_COST_PARTIAL / RESOURCE_CREATION_DISABLED / REAL_SYNC_OFF`  
**Actual Azure resource creation:** NONE. Existing GitHub OIDC preflight remains **Reader**, not deployer.

## 1. Evidence and bounded economic baseline

Prior verified [live Microsoft West Europe EUR retail meters](./EA_AZURE_RETAIL_COST_ESTIMATE_20261015.md) show:
- PostgreSQL Flexible Server B1ms: **EUR 0.0175/hour**; 48h = **EUR 0.840**.
- PostgreSQL storage: **EUR 0.1205 per billed GB-month**; conservative 32 billed units retained for **one full month** = **EUR 3.856**. This may overstate storage cost for deletion within 48h, but does not hide remaining charges.
- **48h DB-only conservative subtotal EUR 4.696; budget residual EUR 15.304.** This is not the full staging cost.
- 24h DB-only illustration EUR 0.420 + EUR 3.856 = **EUR 4.276**.
- If Container Apps **environment private endpoint** is actually enabled, its public meter EUR 0.1258/hour gives **EUR 6.0384 per 48h**, independently of database base cost; additional Private Link/environment management fees may apply. Do not assume this feature is required by all VNet-integrated Container Apps setups.
- Azure free-account discounts = **ZERO assumed**: account-specific eligibility remained **INCONCLUSIVE** in [billing run 38717508118](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38717508118). BillingProperty reported nonfree billing type, BillingBenefits read failed. Conditional free offers do not establish current account entitlement.
- All totals must include tax if applicable to the EUR20 ceiling. Neither subscription-specific discounts nor complete private network/Container Apps meter costs have been verified.

### Alternatives considered

| Mode | Purpose | Pros | Constraints and decision |
| --- | --- | --- | --- |
| **CI-only** | PostgreSQL 16 ephemeral GitHub Actions and fixture tests | Existing, no additional Azure infrastructure | **CURRENTLY APPROVED SAFE PATH**. GitHub Actions billing separate. |
| **48h private Azure integration test** | Validate actual Azure networking, container identity, private Postgres and RLS against synthetic data | Concrete pre-production evidence | **PRICE/QUOTA/RBAC HOLD.** Current known DB lower-bound €4.696, not a complete quote. |
| **Always-on managed Azure staging** | Persistent environment | Highest availability | **NOT FEASIBLE ON VERIFIED COST EVIDENCE** under original €20 specification. |
| **Publicly reachable database to avoid private network cost** | Potential lower network cost | Superficially cheaper | **REJECTED:** violates private DB scope, expands data exposure, cannot be silently approved. |

## 2. Network and runtime design — proposed, NOT deployed

1. New dedicated EA **resource group** `rg-ea-stg-westeurope`, West Europe, unique synthetic-only tags `project=ea`, `environment=staging`, and `expires_at` for inventory/teardown. Do not share project infrastructure or identity with AtlasOrbit/ACSEE.
2. **PostgreSQL Flexible Server B1ms**, single zone/no HA, minimum suitable provisioned disk (32 GiB baseline), private-access **VNet injection** into an appropriately delegated database subnet. In this mode the database has **no public endpoint**. Enable TLS and strong runtime login; migrations run under a distinct role. PostgreSQL allows choosing public access or VNet injection at creation; changing between them is not generally supported. See https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-networking.
3. **Azure Container Apps Consumption (workload profiles v2)** with compatible customer-managed VNet integration; app subnet distinct from PostgreSQL delegated subnet; correct private DNS resolution and outbound routes. Workload Profiles v2 consumption is recommended by Microsoft. See https://learn.microsoft.com/en-us/azure/container-apps/structure . Do **not** enable a managed environment private endpoint automatically: decide using documented threat model, ingress requirement and verified price. For synthetic tests prefer internal ingress, no external watches/webhooks, and **no public database access**. An external GitHub-hosted runner cannot directly reach internal-only endpoints without an explicitly engineered authenticated access path. Run synthetic HTTP/DB tests from inside the trusted network or an appropriate isolated job instead.
4. Restrict server network policies; no 0.0.0.0/0 firewall exemptions, broad public IP allowlists or shared production subnets. Avoid always-on NAT gateway, dedicated workloads and other fixed-fee features unless their necessity and monthly charge are explicitly justified. Treat use of an Azure VNet, DNS, private endpoint and egress as **separate pricing questions**, not automatically free.
5. Prefer no permanent dedicated image registry unless needed and priced. An external registry (for example GHCR) is only a design candidate subject to authenticated pull, image supply-chain, bandwidth, privacy and provider billing review. Never count an external registry as zero-cost merely because the Azure Retail Prices API omits it.
6. Key Vault secrets, restricted user-assigned managed identity, database nonowner/no-BYPASSRLS runtime role; SQL migrations **001–006** should be reviewed (migration 006 adds Bring authorization registry). No real Bring/Gmail/Calendar/Drive/GitHub backend credentials in this synthetic deployment; no provider watches, email sends or calendar writes.
7. Minimal private monitoring and documented budget notifications. Azure budgets **notify only** and do not stop consumption: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets .

**Blocking security checks before any deployment**: full topology and DNS design review; SKU quota/capacity; authoritative itemized all-in cost; separate scoped deployer OIDC identity; protected environment with independent review; restricted PostgreSQL role and legacy RLS test plan; teardown design with privilege/readback proof.

## 3. Price evidence enforcement (implemented, cloud-write-free)

- Script: `pricing/timeboxed_cost_gate.py`; template: `pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json`.
- Template currently includes only the **two verified retail PostgreSQL lower-bound meters**, totaling EUR 4.696. All remaining mandatory pricing components are `unverified`.
- Every cost category is mandatory, including **excluded** optional features. Exclusion needs a reason, source URL and recent date; unknown costs must remain null and block the total.
- At most 48h, EUR20 cap, West Europe, **synthetic-only**, free credits off. Missing network, Container Apps usage, logging, backup, registry, taxes or egress price blocks the quote. Old/malformed pricing evidence is rejected.
- Even if every component is accounted for within EUR20, the calculator **never** authorizes Azure deployment. Actual subscription costs, topology, quota, Entra RBAC, security sign-off, operator-approved period and teardown acceptance remain **independent gates**.
- Unit and negative tests in `pricing/test_timeboxed_cost_gate.py`; automatically run on PRs and `main` using **GitHub Actions only**, no Azure login, no service principal, no ARM create/delete.

### Pricing categories (all must be verified or explicitly excluded)

PostgreSQL compute; provisioned storage; backup; Container Apps Consumption; environment management fee if applicable; environment private endpoint if applicable; VNet/subnets; private DNS; NAT or egress gateway; Private Link; image registry; Key Vault; logs/monitoring; data egress; other cloud costs; taxes; contingency.

The template's `evidence_date` and `source` fields provide a human-review trail. The offline calculator **does not fetch or authenticate evidence URLs**: it detects missing/stale documents and does not certify that a supplied quote is truthful. Independent human or a trusted reviewer must validate the evidence before deployment.

## 4. T=0 to T=48h synthetic deployment protocol — FUTURE ONLY

| Phase | Required operation and proof | Current state |
| --- | --- | --- |
| T–24h approval | Check actual benefit/account billing and full monthly cost, SKU/quotas, scope and new read/write deployer principal; pin immutable code and DB image; confirm wipe path; preauthorize **exact** group/TTL | HOLD |
| T–1h dry run | Exercise deletion/permission/readback against dummy scope or in a purely offline harness, review rollback and emergency owner escalation | HOLD |
| T0 create | Only on exact approved protected deployment workflow, deploy private network, Key Vault, minimum managed DB and app from reviewed manifest; stamp immutable deployment and expiry tags | HOLD |
| T+1h to T+40h test | Synthetic-only migrations 001–006, RLS and restricted role, transactional data readback, duplicate/replay rejection, auth, `/readyz`, logging redaction; no external integrations | HOLD |
| T+40h checkpoint | Prove entire resource inventory, spend and forecast, any residual subscriptions; optional manual early deletion | HOLD |
| T+44h shutdown alert | Separate alert and independent observer/operator notification if not deleted (alert not guaranteed nor hard stop) | HOLD |
| **T+48h full delete** | Scope-limited destroy **ENTIRE** EA ephemeral group only. Deleting the server merely by `az postgres flexible-server stop` is insufficient: server compute restarts after 7 days and storage/backup can continue billing. Keep shared/unrelated resources untouched. | HOLD |
| Post-teardown | **Independent** Azure ARM inventory empty, billing accumulation/reconciliation, verify no remaining DNS, diagnostic or network objects; capture redacted evidence and finalize cost report | HOLD |

**No deletion automation should be deployed without first demonstrating correct resource-group matching, approvals, dry-run safety, idempotency and a fallback for GitHub Actions schedule delays/failures.** Cost alerts and GitHub schedule are not hard EUR20 spend limits. A last-resort Azure administrator must be identified before any creation.

## 5. Next execution order / responsibility

1. **Now:** keep the existing synthetic PostgreSQL CI running, build and validate this offline gate, then merge via protected branch CI.
2. **Read-only evidence:** establish whether the exact EA subscription retains free B1ms/32 GB benefits using **Azure Portal's Free services for 12 months** view; the Reader GitHub billing API was inconclusive and must not receive Contributor role.
3. **Price and architecture evidence:** collect account-specific private network, PostgreSQL capacity and Container Apps (including potential management fee), registry, logs and VAT; update every quote component to either `priced` or `excluded` with a dated source. If fully priced cost exceeds €20, **HOLD**.
4. **If and only if** a complete, independently verified cost <= EUR20 exists, seek specific timeboxed scope and teardown acceptance; set up a **separate** least-privilege deployment OIDC identity; create a reviewed synthetic-only infrastructure PR (not a direct main write); full security/independent review; later authorize an isolated actual deployment.
5. No real customer data, connector reuse, OAuth activation, external emails or calendar writes, and no EA Level 2B/2C promotion in any of these phases.

**Present state:** `NO_CLOUD_DEPLOYMENT / NO_LIVE_SYNC / FULL_COST_UNVERIFIED / PRIVILEGE_NOT_GRANTED`.
