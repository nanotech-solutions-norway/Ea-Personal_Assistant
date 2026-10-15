# EA Azure staging — free-account entitlement verification gate (15 Oct 2026)

**Decision state:** `FREE_ACCOUNT_ELIGIBILITY_UNVERIFIED / PRIVATE_BILLING_EVIDENCE_PENDING / NO_DEPLOYMENT`.

## Source-backed eligibility rule

Microsoft's Azure free-account program can provide (for eligible new accounts in their first 12 months) **750 hours of PostgreSQL Flexible Server B1ms, 32 GB database storage and 32 GB backup storage per month**. Credits and usage allowances are **per eligible subscription**, time-limited and not automatically applicable to any subscription simply because the database SKU is available.

Official Microsoft reference: https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/check-free-service-usage

Microsoft specifically explains that the subscription overview's **Top free services by usage** / **Free services for 12 months** table appears only for free-account subscriptions with such benefits. The usage table can be delayed 1–2 days and may not appear until resources are used. If the table is absent, Microsoft instructs that free-service benefits are not available for the selected subscription.

## Automated read-only verification created

- Workflow `.github/workflows/ea-azure-free-benefits-readonly.yml`: on PR, validate offline classifier tests only. On an explicitly operator-dispatched **main** run, obtain existing protected `ea-staging-preflight` Reader OIDC identity and read **only**:
  - `GET /subscriptions/{id}/providers/Microsoft.Billing/billingProperty/default?api-version=2024-04-01` — Microsoft subscription billing type (Free/Paid/etc.).
  - `GET /subscriptions/{id}/providers/Microsoft.BillingBenefits/freeServices?api-version=2026-06-01` — listed explicit billing benefits.
- Executed code never prints raw billing account IDs, customer details, billing profiles, subscription UUIDs or Azure token values. No raw billing data is uploaded as an artifact. Only coarse categorical statuses appear in GitHub Actions public logs.
- These APIs may return 403 (Reader access is not sufficient in the subscription/billing agreement), 404 (unsupported endpoint/benefit form) or empty results. **None** alone disproves the free 12-month entitlement; a free billing type likewise **does not** prove unused B1ms quota. Do not grant Contributor or Owner to the existing preflight identity.
- The new `Microsoft.BillingBenefits` API may not represent legacy free-account allowances; treat a missing PostgreSQL record as `INCONCLUSIVE`.
- Recorded statuses do not include numeric free credits or remaining usage; portal readback by account owner may still be required.

### Manual execution after this PR has merged to main

```powershell
gh workflow run ea-azure-free-benefits-readonly.yml --repo nanotech-solutions-norway/Ea-Personal_Assistant --ref main
gh run list --repo nanotech-solutions-norway/Ea-Personal_Assistant --workflow ea-azure-free-benefits-readonly.yml --limit 1
```

Follow with `gh run view <RUN_ID> --repo nanotech-solutions-norway/Ea-Personal_Assistant`.

### Definitive verification fallback (private Azure Portal)

Open https://portal.azure.com -> **Subscriptions** -> select the **EA** subscription -> check **Free services for 12 months**. Confirm the exact PostgreSQL Flexible Server B1ms compute meter, 32 GB database meter, 32 GB backup meter, remaining eligibility **expiry**, used / remaining monthly units and whether another workload shares the benefit. Do not save screenshots with names/subscription identifiers in the public repository. The free-services table may lag actual usage by 1–2 days.

## Cost-containment decision matrix

| Verified fact | Decision |
| --- | --- |
| Direct portal confirms active 750h B1ms/32GB storage/32GB backups and unused allowance | Recalculate **time-limited** database subtotal with benefits; do **not** infer private Container Apps networking is also free. Require all-in priced secure BOM <= EUR 20/month, quota, deployer RBAC and teardown before deployment. |
| Direct portal shows no Free services table / entitlement expired | **No free allowance** may be counted. Retail B1ms + assumed storage baseline EUR 16.631/month alone; original always-on architecture remains blocked. Use synthetic CI or price a full 24–48h test deployment. |
| OIDC workflow returns Free billing type but no quantified B1ms benefit | **NOT VERIFIED.** Portal proof required. Do not mark `budget.estimate_verified` true. |
| Billing APIs are forbidden/not supported/no benefit record visible | **INCONCLUSIVE.** No additional Azure permissions or resource creation by inference; private portal evidence required. |
| Complete all-in quote > EUR 20, even if some free benefits apply | **DO NOT DEPLOY.** Retain synthetic disposable PostgreSQL GitHub CI until a different fully-priced architecture or budget is expressly approved. |

## Next safe engineering phase

1. Verify private eligibility from approved Azure billing source, not from retail prices.
2. If free benefits exist, calculate expected **base case + expired-benefit case** with the complete secure topology, and put future billing-expiry risk on a calendar/check.
3. Treat explicit billed Container Apps **Environment Private Endpoint** retail meter of EUR 0.1258/hour (EUR 91.834/730h) as a conditional feature: don't include it unless topology requires that feature; equally don't claim a feature-free alternative without examining required private networking and security controls.
4. Design a short-lived synthetic deployment with *explicit* duration, automated **delete** path, backups/networking prices, no live integrations, and separate scoped deployer role. Keep the original `ea-staging-preflight` identity Reader.
5. Do not create resources, activate EA Level 2B/2C or start any real Gmail/Calendar/Drive/Bring/GitHub ingestion without separate access and deployment gates.

Evidence: [retail-price assessment](./EA_AZURE_RETAIL_COST_ESTIMATE_20261015.md) and [live pricing probe](./pricing/azure_retail_meter_probe.py). All-in cost verified: **false**; Azure resources created: **none**.

## Observed result — protected manual run on 15 October 2026

**GitHub Actions [run 38717508118](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38717508118): SUCCESS** (billing-read job and offline classifier tests passed; immutable OIDC login and subscription/tenant checks succeeded).

Sanitized status returned by the live job:
- `billing_property_access: READ_OK`
- `billing_type_signal: NONFREE_BILLING_TYPE_FREE_SERVICES_STILL_POSSIBLE`
- `billing_benefits_access: UNAVAILABLE_OR_UNAUTHORIZED`
- `pg_benefit_record_signal: INCONCLUSIVE`
- `twelve_month_postgresql_b1ms_750h_and_32gb_entitlement: NOT_INDEPENDENTLY_VERIFIED`
- `unused_monthly_entitlement_and_credit_balance: NOT_INDEPENDENTLY_VERIFIED`
- `deployment_authorized: False`

**Decision:** a successfully executed workflow does not mean free services were verified. The subscription billing-property read succeeded and indicated a non-free billing type, which does not exclude a surviving 12-month benefit after upgrading from a trial. The separate free-service benefits read was unavailable or unauthorized under Reader; no amount, eligibility, expiration or usage can be established. Keep the public retail baseline unchanged and full-cost/paid deployment gates closed.

**Only outstanding operator-side fact:** inspect the actual EA subscription **Overview** in https://portal.azure.com → **Subscriptions** → select EA subscription → **Top free services by usage** → **View all free services**. The table's presence, exact PostgreSQL compute/storage/backup meter names, usage/limits and free-benefit expiration are decisive; if the table is absent, Microsoft's official guidance says free-service benefits are not available for that subscription. No account numbers, invoice details or billing screenshots should be put in the public GitHub repository. See https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/check-free-service-usage . Do not broaden the Reader role merely to get the BillingBenefits API to return data.

If the table is absent or ineligible, evaluate either (a) existing CI-only PostgreSQL synthetic tests with no additional Azure infrastructure spend or (b) a complete independently priced **timeboxed** 24–48-hour staging proposal. An all-in cost estimate and actual quotas are still needed before deploying (b). Free benefits, if present, do not eliminate paid private networking.
