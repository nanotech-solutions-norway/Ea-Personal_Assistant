# EA: October 2026 Azure Container Apps Consumption billing — priced vs account-unknown

**Research date:** 15 October 2026
**Scope:** Ea-Personal_Assistant, West Europe, pure ACA Consumption, max 48-hour synthetic-only pilot; no Bring provider calls, no Azure deployment, EUR20 inclusive ceiling.
**Evidence classification:** OFFICIAL BILLING_RULES_CONFIRMED / SOME_EUR_RETAIL_RATES_CONFIRMED / ACCOUNT_SPECIFIC_PRICE_SHEET_PENDING / FREE_GRANT_REMAINING_UNKNOWN.

## Confirmed Microsoft consumption-plan billing logic

Per https://learn.microsoft.com/en-us/azure/container-apps/billing:
- **180,000 vCPU-seconds**, **360,000 GiB-seconds** and **2 million billable requests** are free **per subscription per calendar month**, **shared with all running ACA apps/jobs**. Remaining usable credit cannot be inferred from the allowance maximum. A non-free Azure subscription can still have relevant ACA plan grants.
- Active vCPU/GiB-second allocation is metered; scaled-to-zero has zero application CPU/memory usage cost. Jobs are charged at the active consumption rate while running; jobs have no request charges.
- Custom VNet may create separately charged managed public egress IP and Standard LB; see https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks. Free compute units do **not** automatically waive these charges.

## Public rate evidence as of 15 Oct 2026

Real historical GitHub Azure Retail Prices API queries:
- https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38722335284
- https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38714329616

West Europe EUR selected price observations:
- **ACA Standard Requests**: EUR0.4928 per 1,000,000 requests.
- **ACA Standard vCPU Active Usage**: returned **EUR0.0 per second** with meter GUID `0426badc-b719-5201-b141-b2d5c4943b7d`.
- **ACA Standard Memory Active Usage**: returned **EUR0.0 per GiB-second** with meter GUID `3ba64b1c-cb46-5ee0-b086-a68736392ac0`.
- **ACA Standard Requests meter GUID**: `b110d175-46b6-5bbc-adde-cf3438ed87f0`.

**Important:** The ZERO catalog compute lines do not prove that PAYG above the shared subscription allowance is EUR0. They may represent a free/non-billable meter or inadequacy in public retail rows; they are not affirmative evidence for an unconditionally free application. Do NOT mark `container_apps_usage` priced EUR0 in the approved quote.

Context-only published US-region active rates:
- Microsoft technical article https://techcommunity.microsoft.com/blog/appsonazureblog/understanding-idle-usage-in-azure-container-apps/4419197 reports **USD 0.000024 per active vCPU-second** and **USD 0.000003 per active GiB-second** (article uses an imprecise memory unit description; cross-check with official GiB-second billing).
- The latest West Europe EUR unit rates and subscription price sheet MUST be verified separately. Do **not** perform arbitrary USD→EUR currency conversion or represent these US rates as contracted EUR prices.

## Applied to current proposed workload

Proposed bounds from `EA_48H_SYNTHETIC_USAGE_ENVELOPE_PROPOSED_20261015.json`:
- vCPU active allocation: 0.25 × 7,200s = **1,800 vCPU-s**
- Memory: 0.5GiB × 7,200s = **3,600 GiB-s**
- Requests: 10,000 × EUR0.4928/1M = **EUR0.004928** *if all billable*.
- Context-only US reference compute cost fully paid: USD(1,800 × 0.000024 + 3,600 × 0.000003) = **USD0.054**, NOT West Europe EUR account pricing.

Remaining free allowance must be checked against other subscription ACA workloads; none assumed in authoritative cost envelope. This small CPU/RAM load could fit in the monthly grant *if unconsumed*, but **no proof exists that the grant is unused**.

## Secure account-specific rate lookup (no deploy)

New safe probe: `pricing/azure_aca_subscription_price_readonly.py`, triggered only from protected `main` by `.github/workflows/ea-azure-aca-subscription-price-readonly.yml`.

It uses the **existing** `ea-staging-preflight` environment, OIDC principal with immutable **Reader** permission, calls the official subscription price sheet by **Azure ARM GET** per:
https://learn.microsoft.com/en-us/rest/api/consumption/price-sheet/get?view=rest-consumption-2024-08-01

The script:
- Pins the protected `AZURE_SUBSCRIPTION_ID`, accepts only https://management.azure.com **same-subscription** page URLs (max eight pages).
- Retains only three **allowlisted ACA meter GUIDs**, exact EUR currency and approved units; suppresses raw billing rows, offer/billing account IDs, personal/customer info, subscription IDs and authentication failures.
- Prints one of `ACCOUNT_PRICE_SHEET_READ_BUT_NOT_DEPLOYMENT_APPROVAL`, `UNAVAILABLE_OR_UNAUTHORIZED`, `BLOCKED_UNTRUSTED_NEXT_LINK`, `INCOMPLETE_PAGINATION`, `MALFORMED_RESPONSE` or `BLOCKED_INVALID_SUBSCRIPTION_CONFIG`.
- A price sheet with zero-price item reports `ACCOUNT_PRICE_CANDIDATE_ZERO_NOT_PROOF_FREE`, not `FREE_ENTITLEMENT_VERIFIED`.
- No programmatic role assignment; if Reader lacks price sheet privilege or the billing agreement does not expose the API, result stays **INCONCLUSIVE**, NOT a reason to elevate the GitHub Reader credential.
- Pricesheet `includedQuantity` is **not** the remaining current month shared ACA grant. This probe cannot establish free-grant *remaining balance*, VAT invoice status, full topology/billing or permission to deploy.

Run manually from GitHub Actions page under `EA Azure ACA subscription price sheet (read only)` → **Run workflow**, branch `main`; or from a logged-in Windows GitHub CLI:

    gh workflow run ea-azure-aca-subscription-price-readonly.yml --ref main
    gh run list --workflow ea-azure-aca-subscription-price-readonly.yml --limit 3

Review **only** sanitized job lines: `EA_ACA_SUBSCRIPTION_BILLING_READ` and `ACA_*` statuses. NEVER copy raw token/private invoices into public GitHub.

If price sheet read is unavailable due to insufficient billing access, a separately authorized billing admin may privately export their existing subscription's Price Sheet or Cost Management report from the Azure Portal. DO NOT alter `ea-staging-preflight` Reader or create an additional app until this need is reviewed.

## Consequences for EUR20 cost ceiling

Even if a price-sheet API returns concrete positive CPU/memory EUR rates, a release quote still needs private Key Vault network access, all managed auxiliary resources, exact taxes, recurring/teardown charges, actual resource quota/capacity and independent signoff.

**No automatic changes to the 20-component cost template**. `container_apps_usage` remains UNVERIFIED; existing template remains BLOCKED, `deployment_authorized=false`, `BRING_PRODUCTION_SYNC_DISABLED`.
