# EA Unified Calendar — Private billing-evidence collection gate
**Time:** 14:36, 15.10.2026 (Europe/Madrid)  
**Classification:** read-only engineering/AUTO_APPROVED; price and deployment decisions PENDING_REVIEW  
**Scope:** EA Personal Assistant **only** (not AtlasOrbit), West Europe, one private synthetic-only EA tenant, max **€20/month inclusive of applicable taxes**, 48-hour proposed cloud timebox. **NO DEPLOYMENT.**

## Verified baseline / why this gate matters

- [PR #73](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/73) confirmed MERGED on GitHub on 15.10.2026. The expanded public catalog search found **one zero-valued West Europe Consumption meter each** for active Container Apps CPU and memory; **zero positive matches**. This observation is not evidence that the subscription's usage is free.
- Microsoft states ACA Consumption charges by vCPU-seconds, GiB-seconds and HTTP requests; monthly free grants are shared by subscription and may be exhausted. Custom VNet may add separate charges. [Official billing rules](https://learn.microsoft.com/en-us/azure/container-apps/billing).
- Microsoft's [MCA billing schema](https://learn.microsoft.com/en-us/azure/cost-management-billing/dataset-schema/price-sheet-mca) says `unitPrice` reflects contracted billing rate (as distinct from market price), with `meterId`, `productOrderName`, `priceType`, `meterRegion`, tier and billing-profile scope. Currency on retail API results is a reference; it does not determine the operator's actual billing agreement. [Billing relationship](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/understand-billing-tenant-relationship).

## New private evidence tool

[`pricing/private_billing_evidence.py`](./pricing/private_billing_evidence.py) reads a **locally held MCA billing-profile price sheet CSV**. It matches known ACA active CPU/memory meter IDs, rejects wrong profile/region/tier/currency/price type, stale price-sheet periods, NaN/negative values and ambiguous/zero rates. It prints only counters and stage, **never** a private `unitPrice`, `billingProfileId`, subscription ID, filename path, bearer token or row contents.

Important boundaries:
- No network calls, Azure RBAC changes, account login or billable resources. Public GitHub Actions runs **synthetic fixture tests only**.
- Input must be a `*.csv` file **outside the Git checkout**; scripts reject files placed inside the repository. Do not commit or upload the price sheet, screenshots, raw Azure billing account IDs or JSON containing identifiers to public GitHub/Drive, or into ChatGPT.
- The script is a **candidate sanity check**, not independent account-authenticity, remaining subscription free-grant verification, tax validation or release approval. Even a perfect price sheet keeps `deployment_authorized=false`.
- Supported parser is **MCA CSV** only. If the real Azure billing agreement is Enterprise Agreement, CSP/partner or a free/trial offer with no corresponding billing-profile CSV, this parser is **not applicable**. Record `NOT_APPLICABLE / PRIVATE BILLING TYPE NOT VERIFIED` rather than forcing a fake MCA price sheet or changing billing ownership.

## Optional operator-only Microsoft portal evidence step

Only if actual EA subscription is governed by a Microsoft Customer Agreement and the authenticated user **already has billing-profile Reader/Owner/Contributor/Invoice Manager permission**:

1. Open the private [Azure portal](https://portal.azure.com) and locate **Cost Management + Billing**. Verify it is the **EA Personal Assistant subscription's billing profile**, not AtlasOrbit or an unrelated/family subscription. Do not paste identifiers into GitHub or chat.
2. Under the billing profile, select **Download usage and prices** (under Shortcuts) and **Download Azure price sheet for current month and year**. If Microsoft delivers a ZIP, extract the CSV to a private folder such as `%USERPROFILE%\Documents\EA-private-billing\`, **outside** the repository. See [Microsoft portal steps](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/ea-pricing).
3. In an ordinary, local PowerShell session, set the billing-profile identifier **locally** (do not add it to GitHub Secrets; no reason to share with this review):
   ```powershell
   $env:EA_PRIVATE_BILLING_PROFILE_ID = Read-Host "EA-specific Azure billing profile ID"
   cd "$HOME\Ea-Personal_Assistant"
   py -3 .\level-2\backend\deployment\pricing\private_billing_evidence.py --input "$HOME\Documents\EA-private-billing\pricesheet.csv"
   Remove-Item Env:\EA_PRIVATE_BILLING_PROFILE_ID -ErrorAction SilentlyContinue
   ```
4. Review the **sanitized** status; expected unresolved result is permitted. In particular `ONE_PRIVATE_POSITIVE_CANDIDATE_NEEDS_INDEPENDENT_REVIEW` remains only a local candidate; `UNRESOLVED_ZERO_OR_MULTIPLE_TARIFFS` is not evidence of free service. For an MCA price-sheet CSV that omits required columns or is too large (>25 MiB), the script refuses to evaluate. Do not manually invent missing columns or price fields.
5. Keep the original CSV/ZIP private and separate from all GitHub paths. Cost/account identities remain local. To proceed with an independent cost review, share only the high-level status flags (not IDs or private rates), or use a separately approved private confidential review channel.

Azure's **resource/subscription Reader** does not itself establish **billing-profile price-sheet access**. Do not elevate the immutable EA OIDC Reader. If portal pricing access is denied, record the blocker; request billing-profile read authority through the normal Microsoft billing administration process, not a deployment role.

## Remaining release prerequisites (unchanged)

- Identify exact subscription/contract billing terms and applicable effective prices and conversion currency; verify the account's remaining monthly ACA free allocation rather than silently deducting it.
- Independently price full network management, PostgreSQL compute and full-month storage, backup excess, DNS, LB rules/data, managed public IP, ACA runtime and requests, ACR, Key Vault, logs and egress, taxes and contingency under the 48h horizon **including residual charges after teardown**.
- Independently validate deletion of the **managed ACA infrastructure resource group**, IP, LB, PostgreSQL storage/backup, DNS, logs, registry and other resources with scope-safe procedures. Azure Cost Management budgets issue alerts but are **not hard spending caps**. [Microsoft documentation](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-create-budget-bicep).
- Check actual PostgreSQL B1ms provisioning capacity, private networking, least-privilege deployer plan, independent review and approval **separately** before any Azure write actions.

**Decision:** `BILLING_SUBSCRIPTION_PRICING_PENDING_PRIVATE_EVIDENCE` / `ALL_IN_EUR20_HOLD` / `CLOUD_DEPLOYMENT_NOT_AUTHORIZED` / `LIVE_PROVIDER_SYNC_HOLD` / `EA_LEVEL2B_2C_HOLD`. Continue no-charge disposable PostgreSQL CI. Existing EA OIDC Reader remains Reader.
