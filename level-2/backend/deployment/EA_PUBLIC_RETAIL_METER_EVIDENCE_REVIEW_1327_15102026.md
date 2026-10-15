# EA Unified Calendar — Public retail meter evidence review — 13:27, 15.10.2026

**Classification:** Engineering process / AUTO_APPROVED. Resource or production release approval: **PENDING_REVIEW**.
**Project:** EA Personal Assistant, **not** AtlasOrbit ACSEE/Azure MCP.
**Guardrails unchanged:** West Europe; single private EA tenant; full **€20/month** including applicable taxes; **48-hour synthetic-only** proposed staging; existing immutable OIDC Reader retained; no paid cloud deployment, no real-provider OAuth, no live synchronization; Level 2B/2C HOLD.

## Why this step was necessary

The Microsoft public EUR Retail Prices API observations include *zero-valued* `Standard vCPU Active Usage` and `Standard Memory Active Usage` meters under `Azure Container Apps`, despite the documentation specifying chargeable Consumption vCPU-second and GiB-second usage and subscription-shared monthly allowances. This cannot be interpreted as a validated subscription credit, zero-priced workload, or evidence that the all-in €20 cap is satisfied.

Other notable selection hazards include:
- A **free Standard Load Balancer** meter with a distinct meter ID alongside a paid `Standard Included LB Rules and Outbound Rules` first-bundle meter.
- Azure DNS `Private Zone` **lower-priced high-volume tiers**; a single staging zone must not be priced using `tierMinimumUnits=25`.
- Standard managed egress public-IP serviceName is **`Virtual Network`**, productName `IP Addresses`; service filter `IP Addresses` alone can fail to retrieve its tariff.
- Subscription-specific discounts, taxes, billing, actual free-grant exhaustion and residual managed resources are not available from the unauthenticated public catalog.

## Implemented verification

- `pricing/reconcile_public_retail.py`: consumes the existing read-only public catalog artifact and selects exact known meter IDs, product/service identity, base tier, declared unit, preferred West Europe/Global region and effective date. Outputs a **candidate-only**, allowlisted price/evidence file; never an account quote.
- `pricing/test_reconcile_public_retail.py`: adversarial tests for mismatched SKU, meter/product/unit, negative/NaN, premium tiers, stale/tampered source header, truncated retrieval, region preference, conflicting rates, and zero-priced meter interpretation.
- `.github/workflows/ea-azure-private-topology-price.yml`: after public catalog read, runs the offline tests and reconciler; preserves both raw public evidence and the sanitized candidate reconciliation for **30 days** as a GitHub Actions artifact.

**Key classifications**:
- `PUBLIC_METER_CANDIDATE_UNVERIFIED`: matching positive public retail meter; still not account-specific billing.
- `ZERO_PUBLIC_RATE_NOT_A_VERIFIED_FREE_BENEFIT`: a genuine zero-valued public row, **not** a validated free tenant benefit.
- `MISSING_PUBLIC_METER`, `CONFLICTING_PUBLIC_METERS`, or `EVIDENCE_INCOMPLETE`: need independent investigation; do not default to zero.

All outputs carry `all_in_cost_verified=false`, `deployment_authorized=false`, and `live_sync_authorized=false`. A valid catalog match cannot clear any deployment gate.

## Specific observed public meter candidates (15 October 2026)

Source: authenticated **GitHub CI logs of an unauthenticated Microsoft retail API query**, [run 38728808039](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38728808039). The source is public catalog evidence; no Azure subscription-specific rate or metered invoice was retrieved.

| Component | Exact public meter | Observed EUR rate | Unit | Confidence / decision |
| --- | --- | ---: | --- | --- |
| ACA egress IP | `9c150bf9-2bad-430e-a53c-c213804f49ef` | 0.0044 | hour | Candidate; one egress IP modeled |
| ACA managed LB rule bundle | `27827eb0-7f60-4928-940b-f5fe15e7a4cb` | 0.022 | hour | Candidate; do not substitute Free meter |
| Standard LB processed data | `dfc7cc11-fbe2-41c8-b6fa-24a574223938` | 0.0044 | GB | Candidate; ingress and egress management operations may apply |
| ACA active vCPU | `0426badc-b719-5201-b141-b2d5c4943b7d` | **0.0** | second | **UNRESOLVED** — do not conclude CPU execution is free |
| ACA active GiB memory | `3ba64b1c-cb46-5ee0-b086-a68736392ac0` | **0.0** | GiB-second | **UNRESOLVED** — do not conclude memory execution is free |
| ACA Standard Requests | `b110d175-46b6-5bbc-adde-cf3438ed87f0` | 0.4928 | 1M requests | Candidate; subscription free-grant eligibility not verified |
| DNS private zone | `0b608a26-f611-4232-8192-ce81b6b57194` | 0.44 | retail `1` | Base tier candidate; independently confirm month/time billing |
| DNS private queries | `46cff9cb-4b15-4af0-bf41-25143827fef8` | 0.352 | 1M queries | Candidate; billing tier and quantity validation required |

**Remaining cost categories:** PostgreSQL backup excess, ACA CPU/memory rates and actual usage/free-grant offsets, managed auxiliary resources, storage/zone lifetime, Key Vault, DNS request and traffic quantities, registry, logging and retention, outbound data, support/other-cloud, billing VAT/tax treatment, contingency and billing after 48-hour teardown. No actual subscription invoice, hard spending cutoff or physical Azure test is claimed.

## Evidence-driven next gates

1. Identify the correct billable ACA **Consumption** active vCPU/GiB meters independently; do not use zero-valued `Standard` rows to clear costs. Verify rates and consumption model against Microsoft documentation and any subscription-specific rate card.
2. Verify exact private DNS zone billing period; evaluate data processing, logs, backup and registry charges conservatively, without silently using free benefits.
3. Calculate the *complete* 48h + teardown-residual **tax-inclusive** cost envelope and compare against €20/month, with evidence for every line including exclusions.
4. Obtain independent security/private-route/least-privilege and teardown review; proceed with a dedicated deployer authorization only after required gates. Never modify the existing Reader identity.
5. Record independent readback in GitHub and approved EA Drive project folder. Account-specific confidential estimates, if received, must remain private and must **not** be copied into this public repository.

**Microsoft primary sources:**
- [Azure Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing)
- [Azure Container Apps custom VNet charges](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks)
- [Azure budgets do not stop resource consumption](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices)

**Decision:** `PUBLIC_METER_RECONCILIATION_ENGINEERING_ONLY` / `CLOUD_DEPLOYMENT_HOLD` / `LIVE_PROVIDER_SYNC_HOLD`. No software release approval or financial/tax conclusion.
