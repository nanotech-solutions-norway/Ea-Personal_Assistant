# EA Unified Calendar — Synthetic staging cost envelope — 13:27, 15.10.2026

**Classification:** PROCESS IMPLEMENTATION / AUTO_APPROVED; numerical workload scenario, tax assumption, deployment and RBAC authority: **PENDING_REVIEW**.
**Scope:** Ea-Personal_Assistant ONLY. West Europe, one private EA tenant, full €20/month cap, max 48-hour synthetic-only staging, no Azure creation, no live provider synchronization. Unrelated AtlasOrbit infrastructure is excluded.

## Completed in this branch

1. Added a **nondeployable, 48-hour bounded workload what-if specification**:
   [EA_48H_SYNTHETIC_USAGE_ENVELOPE_PROPOSED_20261015.json](./pricing/EA_48H_SYNTHETIC_USAGE_ENVELOPE_PROPOSED_20261015.json).
2. Added an offline analyzer [scenario_envelope_gate.py](./pricing/scenario_envelope_gate.py), which reads that scenario plus the existing [partial rate quote](./pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json), computes bounded units, identifies all unpriced categories, and always returns `deployment_authorized=false` and `live_sync_authorized=false`.
3. Added [adversarial unit tests](./pricing/test_scenario_envelope_gate.py) and invoked them in the protected offline CI workflow. Tests reject live sync, cloud writes, altered region, duration, scope, unapproved replica/IP/LB scale-out, unbounded or malformed measurements, nonfinite/negative values and unsupported teardown claims.

## Synthetic assumptions — not live workload evidence

| Maximum test dimension (review proposal) | Bound | Notes |
| --- | ---: | --- |
| Workload timebox | 48h | Actual teardown and lingering billable tail still unverified |
| Container Apps peak replicas | 1 | Pure-Consumption proposed |
| Per replica allocated vCPU, memory | 0.25 vCPU, 0.5 GiB | Not an observed deployed SKU |
| Per replica aggregate active running time | 7,200 seconds (2 hours) | Compute 1,800 vCPU-s; 3,600 GiB-s |
| HTTP requests, private DNS queries | 10,000 each | Demand ceiling, not incurred cost |
| LB data processed, outbound egress | 0.5 GB each | Meter quantities need confirmation |
| Log ingestion | 0.1 GB | Retention/export/billing configuration unverified |
| Key Vault operations | 1,000 | Source traffic hypothetical |
| Excess PostgreSQL backup | 0.1 GB-month | Cannot assume 0 if WAL/backups spike |
| Container registry storage | 0.2 GB-month | Registry billing model/service to be selected |
| ACA-managed static public IP, Standard LB first rule bundle | 1 each | Pricing recorded in earlier public catalog readback |

**The assumptions are PENDING_REVIEW.** No synthetic cap is proof that a deployed service can enforce that cap, and subscriptions may share Container Apps free grants. No subscription-free benefits may be presumed.

## Cost evidence and remaining risk

Previously independently recorded public EUR rates:
- PostgreSQL B1ms 48h compute €0.840 and modeled full-month 32 billed storage units €3.856 (public retail evidence [run 38714329616](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38714329616)).
- ACA-managed Standard static egress public IP 48h €0.2112 and Standard LB first rule bundle 48h €1.056 (public retail evidence [run 38725912112](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38725912112)).
- **€5.9632 is only an arithmetic partial subtotal at the recorded public rates; it is not a subscription-specific, tax-inclusive or all-in quote, and not a guaranteed lower or upper billed amount.**

Still **UNKNOWN/BLOCKING**: Container Apps vCPU-/GiB-seconds and request tariff **without assumed free grant**, managed auxiliary infrastructure charges, extra LB rule/data tariffs, private DNS queries/zone lifetime, networking and egress, ACR vs GHCR commercial charges, Key Vault usage, logs/retention, PostgreSQL backup overages, tax treatment, support/ancillary billing and charges after the 48h deadline. Azure `Budget` alerts do **not** halt spending or guarantee the cap. Exact B1ms location/allocation, dedicated least-privilege deployer, resource-group deletion rights, safe managed-RG inventory and independently verified empty-after-delete readback remain unverified.

Primary sources:
- [Azure Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing): vCPU-seconds, GiB-seconds and requests; shared subscription free grants cannot be assumed.
- [Custom virtual networks](https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks): managed public IP and load-balancer costs for VNet integration.
- [PostgreSQL backup/restore](https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore): 100% provisioned storage backup allowance and billable excess, including transaction logs.
- [Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets): alerts are not automatic spend cutoffs.

## Offline verification

```powershell
python -m unittest discover -s level-2/backend/deployment/pricing -p test_scenario_envelope_gate.py -v
python level-2/backend/deployment/pricing/scenario_envelope_gate.py level-2/backend/deployment/pricing/EA_48H_SYNTHETIC_USAGE_ENVELOPE_PROPOSED_20261015.json level-2/backend/deployment/pricing/EA_TIMEBOX_48H_QUOTE_TEMPLATE_20261015.json
```

**Expected result:** scenario `model_validation=PASS`, deployment `BLOCKED_NO_DEPLOYMENT`; original all-in quote `BLOCKED`. This is a *test of the proposed model*, not test execution evidence until a CI run completes.

## Next gated actions

1. Obtain and independently verify exact component meter units and remaining subscription-specific charges; retain an explicit unknown-cost ledger.
2. Model timebox plus managed-network/IP/LB/zone/storage retention and teardown slippage, taxes where applicable and contingency without breaching **€20/month**.
3. Validate security boundary, end-to-end synthetic worker / PostgreSQL operational fit and backup/restore/teardown in a non-production design review; do not create the infrastructure.
4. Operator/independent review of numeric workload bounds, cost and security decisions. Only after all evidence passes consider a **separate deployer** with narrowly scoped permissions. Immutable preflight Reader remains Reader; Level 2B/2C and real Calendar sync stay HOLD.

**Security statement:** This branch contains no Azure credentials, tenant IDs, customer data, calendar events, emails or deployment configuration. No cloud write or GitHub automation uses privileged Azure identity.
