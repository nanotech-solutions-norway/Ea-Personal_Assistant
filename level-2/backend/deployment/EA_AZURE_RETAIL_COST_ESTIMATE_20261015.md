# EA Azure staging — West Europe EUR retail cost calculation (15 October 2026)

**Verdict: the original 24×7, private, managed staging architecture is not established as feasible under EUR 20/month. Do not deploy it.**  
**Scope:** one synthetic-only EA tenant, `westeurope`, intended `rg-ea-stg-westeurope`. No paid resource provisioning, Google backend OAuth, real source synchronization or Level 2B/2C authorization.

## 1. Evidence and calculation method

Azure's live public [Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) was queried on **15 Oct 2026** for `westeurope`, `currencyCode=EUR`, `priceType=Consumption`.

- Successful GitHub evidence (public rates only): [EA EUR retail meter workflow run 38714329616](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38714329616).
- Reproducible standard-library probe: [pricing/azure_retail_meter_probe.py](./pricing/azure_retail_meter_probe.py).
- Run requires **no** Azure account access, subscription secrets or resource write access.
- One model month = **730 hours** = **30.4167 days**. **32 billed GB-month units** assumed for the minimum provisioned 32-GiB PostgreSQL allocation; note the retail meter labels its unit `1 GB/Month`, so actual storage billing conversion and final invoice require confirmation.
- EUR values are Microsoft's illustrative retail prices, **not customer-specific subscription billing**; no Azure discounts, introductory offers, VAT or variable exchange adjustments assumed.

### Directly observed meter rates

| Service and meter (exact retail name) | EUR retail rate | Quantity | Model subtotal |
| --- | ---: | ---: | ---: |
| PostgreSQL Flexible Server Burstable BS Series Compute — `B1MS` | EUR 0.0175/hour | 730 hours | **EUR 12.775** |
| PostgreSQL Flex Server Storage — `Storage Data Stored` | EUR 0.1205/GB-month | 32 billed units | **EUR 3.856** |
| **PostgreSQL minimum recurring subtotal** | | | **EUR 16.631** |
| Container Registry — Basic Registry Unit | EUR 0.1466/day | 730/24 days | EUR 4.459 |
| Log Analytics — Analytics Logs Data Ingestion | EUR 2.6311/GB (paid meter also has zero-rated meter) | **illustration only:** 1 billed GB | EUR 2.631 |
| Key Vault Standard — Operations | EUR 0.0264/10,000 ops | **illustration only:** 1,000 ops | EUR 0.00264 |
| Container Apps — **Environment Private Endpoint** | EUR 0.1258/hour | **if feature provisioned continuously**: 730 hours | **EUR 91.834** |
| Container Apps — Environment Management Hour | EUR 0.1258/hour | **possible additional configured charge**: 730 hours | **EUR 91.834** |

Direct meter IDs: B1ms `5e31969e-0b91-5186-81a1-7475fabe1262`; storage `36845e2a-736f-5a9d-af4e-b2dc7547a06f`; Container Apps private endpoint `3d952ec1-3455-54fe-86ed-0ae4a5864088`; environment management `763af336-b491-5b72-b7b9-9965af0bc588`; Basic registry `5c9e7a65-5784-494c-9718-7749d4075dd9`. Meter effective dates are recorded by the live API; these are prices observed **as of the query date**, not claims that every rate originated on that date.

**Caveats:** Log Analytics may include free benefits, so do not assume 1 GB is necessarily payable or zero-cost. Container Apps Consumption provides 180,000 free vCPU-seconds, 360,000 GiB-seconds and 2 million requests per month **shared across the subscription**; remaining entitlement was not read from the Azure billing system. Container Apps' private-endpoint meter applies only if that feature is used. Microsoft also warns about dedicated plan management fees for private endpoints and other networking resources: do not silently assume they are free or double-count a non-enabled feature.

## 2. Scenario arithmetic (EUR, no taxes or customer discounts)

| Scenario | Known retail-meter calculation | Result | Meets <= EUR 20? |
| --- | --- | ---: | --- |
| **A: CI-only synthetic PostgreSQL** | No persistent Azure PostgreSQL/Container Apps; GitHub CI and any separate GitHub billing not in Azure | **EUR 0 Azure resource cost** | **Yes for Azure**, subject to GitHub costs |
| B: B1ms + 32 units storage 24×7 | 730 × 0.0175 + 32 × 0.1205 | **EUR 16.631** | Only this limited pair; not full staging |
| C: B + Basic Azure Container Registry | 16.631 + (730/24) × 0.1466 | **EUR 21.090** | **No**, before app, network, logs, backups, tax |
| D: B + illustration 1 GB paid logs + 1,000 Key Vault ops (without registry) | 16.631 + 2.6311 + 0.00264 | **EUR 19.265** | Leaves < EUR 0.74 for *all* networking/app/backup/tax |
| E: B + continuously enabled Container Apps environment private endpoint | 16.631 + 730 × 0.1258 | **EUR 108.465** | **No**, before Private Link and possible management/networking charges |
| F: Short test, B1ms compute running 120h, 32 billed units storage retained all month | 120 × 0.0175 + 32 × 0.1205 | **EUR 5.956** | A *partial* baseline only; no app/network/quotas |
| G: Short test, B1ms compute running 48h, 32 billed units storage retained all month | 48 × 0.0175 + 32 × 0.1205 | **EUR 4.696** | A *partial* baseline only; requires timely stop/teardown |

**Scenario D is illustrative and cannot be construed as a complete EUR 20 quote.** Backup above included provisioned storage, Private Link resource, DNS, public IP, load balancers, VNet egress, Container Apps app usage, logs, registry, taxes and external provider expenses can add charges. The absence of a numerical value for a mandatory meter is **not** proof of a zero rate. The retail API queried the `westeurope` region; several globally metered networking categories were not returned and must be priced separately before deployment.

### Potential free-account exception — not verified for this subscription

Microsoft's Azure free-account program has historically included **750 hours of B1ms compute and 32 GB storage plus 32 GB backup per month for the first 12 months**. If the actual EA subscription is eligible and the grant is unconsumed, the temporary PostgreSQL retail baseline may be reduced substantially; after expiry charges revert. Eligibility, remaining period and monthly consumption have **not** been verified. Never apply this credit to the quoted scenarios without private Azure billing readback. Importantly, free database allowances do not make private Container Apps endpoint fees free.

## 3. Architecture recommendation

**Preferred now: keep the existing synthetic PostgreSQL GitHub Actions CI, and defer permanent Azure resource creation.** This preserves independent SQL migrations, access-control tests and reproducible integration evidence at **EUR 0 incremental Azure resources** (GitHub Actions costs may apply separately). Perform any Azure runtime/identity testing with read-only preflight and keep production data unconnected.

**For meaningful deployed synthetic staging under EUR 20:** investigate a **timeboxed 24–48-hour environment** with a deterministic full-resource teardown and an explicitly priced private networking topology. A short database compute window looks affordable **in isolation**, but network, Container Apps, backup and residual storage charges can still exceed the ceiling. Do **not** authorize even the timeboxed deployment on the basis of these partial subtotals.

**If 24×7 private Azure staging is a hard requirement:** revise the architecture or raise the budget with explicit operator approval after obtaining all network/private-endpoint, monitoring and storage prices. Do not relax database access security simply to hide costs.

## 4. Next engineering gates, in order

1. **Check the actual EA Azure subscription's Azure Free Account benefits** (particularly B1ms/32 GB), month-to-date usage, remaining entitlement and any negotiated rate; obtain private Azure Cost Management evidence. This is not accessible via the public retail API.
2. **Confirm networking topology** for Container Apps-to-private PostgreSQL. Resolve whether a private endpoint is truly necessary or a different private connection pattern can meet the same security requirements with fewer charges. Include public IP/load balancer, egress/DNS and Private Link where used. Distinguish unavoidable resource fees from conditional features.
3. **Finalize a priced, full-design BOM** (compute/storage/backup, Container Apps capacity and consumption/free allowances, image registry, networking, Key Vault/logging, taxes if applicable); add at least a contingency margin. A priced quote must include SKU availability/quota and any fixed managed environment charges.
4. Create a **separate deployment OIDC identity** with scoped, least-privilege role assignments only if the priced design is accepted. Keep `ea-staging-preflight` Reader identity unchanged.
5. If (and only if) the full quote fits <=EUR20 and exact resource set/period is approved, stage a **synthetic-only** deployment with cost alerts, monitoring, rollback and **resource deletion** (budget alerts alone do not cap spending). Otherwise continue with CI-only and report a feasible alternative or revised budget.

No Azure deployments have been performed as part of this pricing work. No real Gmail/Calendar/Drive/GitHub sync or EA Level 2B/2C promotion is approved.
