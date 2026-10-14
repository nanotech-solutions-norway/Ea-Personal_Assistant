# EA Azure staging — operator approval and read-only preflight handoff
**Decision received:** 13 October 2026  
**Status:** `OPERATOR_APPROVED / AZURE_ACCESS_NOT_YET_VERIFIED / NOT_DEPLOYED`  
**Scope:** private, single-tenant, synthetic-only EA Level 2A; West Europe; new EA-specific resource group; maximum EUR 20/month.

## Verified facts versus assertions
- GitHub PR #54 **MERGED** (commit `ef226f7d2e60769777a0c43ac1519a1c9198bbbd`); original design and safety files are on `main`.
- Operator **supplied an Azure subscription UUID**, attested the EUR 20 budget was validated, and separately **granted staging deployment authorization**.
- Subscription UUID is **not committed to this public repository**. Use the protected GitHub Actions environment or an authorized private operator handoff.
- Azure subscription ownership, identity federation, RBAC, quota, region/SKU availability, actual price breakdown and real cost containment **not independently verified from Azure** in this connector session.
- No Azure resources, Google backend OAuth, GitHub production webhook, customer data replication or paid services were created here.
- This authorization does **not** approve live provider synchronization, external calendar changes, mail sends, real customer data ingestion, Level 2B/2C promotion or any spending above EUR 20/month.

## Stage 1 — Set up an OIDC-protected GitHub environment (manual administrator setup)

Repository: `nanotech-solutions-norway/Ea-Personal_Assistant`

1. In GitHub **Settings → Environments**, create **`ea-staging-preflight`**.
2. Restrict deployment branches/tags to **`main`**; enable required reviewer where eligible. Do not weaken the existing branch-protection rules.
3. Under *environment variables*, set:
   - `AZURE_SUBSCRIPTION_ID` = the exact UUID supplied privately by the operator (not printed in public repository files).
   - `AZURE_TENANT_ID` = the verified Azure/Microsoft Entra *Directory (tenant) ID* for that subscription. This is **not** the subscription UUID.
   - `AZURE_CLIENT_ID` = a specific Azure app/managed identity client ID approved for read-only GitHub OIDC access, not the principal object ID.
4. In Microsoft Entra, configure an app registration or user-assigned managed identity with a federated identity credential:
   - Issuer `https://token.actions.githubusercontent.com`
   - Subject `repo:nanotech-solutions-norway@215678827/Ea-Personal_Assistant@1289533798:environment:ea-staging-preflight`
   - Audience `api://AzureADTokenExchange`
   - Ensure the subject's exact case matches the GitHub OIDC token.
5. Grant this preflight identity **Reader** rights on the selected Azure subscription or an appropriately restricted scope sufficient to read subscription/provider metadata. Grant nothing beyond least-privileged inspection. Keep **deployer credentials separate** and do not grant Contributor to the read-only preflight identity.
6. On `main`, manually run **Actions → EA Azure staging — read-only identity preflight → Run workflow**. It will check that the configured subscription is enabled, tenant matches and West Europe is listed; it reports provider registration states and will perform **no resource creation**.

Workflow file: `.github/workflows/ea-azure-staging-readonly-preflight.yml`. It is intentionally `workflow_dispatch` only, with no push/cron triggers, no Azure deployment command and no provider synchronization.

The ChatGPT GitHub and Drive connectors **do not** provide Azure Resource Manager authentication. This file cannot prove cloud access until the protected OIDC environment is configured and the run actually succeeds.

## Stage 2 — Accept cost/RBAC evidence BEFORE a first deployment
1. Attach or record the operator's actual all-in West Europe cost calculation *privately* (SKU, replicas, PostgreSQL compute + >=32 GiB storage, VNet/DNS/egress, Key Vault, logs, backups, registry, VAT/other charges).
2. Verify the named subscription pricing/free grants independently and compare monthly forecast in EUR with the **EUR 20 ceiling**. `budget.operator_budget_validated_attestation=true` does not replace an itemized quote or cloud bill.
3. Separate real RBAC and deployment identity checks from identity sign-in. Read-only login merely proves authentication and metadata access; it does not authorize a particular resource deployment.
4. Identify actual West Europe SKUs and quotas. A provider registration state of `Registered` does not prove that a given SKU is available.
5. If all-in estimated spend is above EUR 20 or unknown, stop. Continue with disposable PostgreSQL/GitHub Actions synthetic integration; request an explicitly revised technical or budget plan.
6. When accepting the quote, confirm its expiration, monitoring, teardown and practical spend containment. **Azure budgets alert but do not stop charges.**

## Stage 3 — Later authorized infrastructure work (not yet executed)
- Allocate **`rg-ea-stg-westeurope`** only after the prerequisite gates pass.
- Create dedicated private network, managed PostgreSQL, secrets, runtime and least-privileged identities. Avoid sharing resources, tokens or customer data with AtlasOrbit and ACSEE.
- Run SQL migrations 001–005 under migration identity; prove restricted role and legacy-table isolation.
- Enable no external provider webhooks, watches or OAuth until synthetic `/readyz`, DB RLS, independent commit readback, authentication and rollback tests pass.
- Require **separate approval** for any read-only real-provider test or eventual production/Level 2B/2C activation.

## Verification checklist
- [x] PR #54 merged; design files exist in `main`
- [x] Subscription supplied by operator (stored outside public repo)
- [x] EUR 20 budget validation attested by operator
- [x] Operator authorizes priced EA synthetic staging deployment
- [x] Protected-environment manual OIDC preflight workflow prepared in review PR
- [ ] Preflight environment variables and federated identity established
- [ ] Azure OIDC read-only workflow run PASS, tenant/ownership independently verified
- [ ] Authorized administrator confirms deployment RBAC
- [ ] Actual itemized West Europe <=EUR 20/month quote independently verified and preserved
- [ ] Resource group actually created and cost budget alerts configured
- [ ] Staging DB/runtime network, security, RLS and synthetic E2E verified
- [ ] Backend provider grants independently authorized and live sync explicitly approved

**Stop state:** `CLOUD_PREFLIGHT_PENDING / NO_AZURE_DEPLOYMENT / NO_LIVE_SYNC / LEVEL_2B_2C_HOLD`.

References: [GitHub OIDC with Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure) and [Azure Cost Management budget alerts](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets).

## UPDATE — 15 October 2026: OIDC and registration verification

The earlier `CLOUD_PREFLIGHT_PENDING` checklist above is historical. Azure identity checks and provider registrations are now **independently verified** via [GitHub Actions run 38655941349 (attempt 2)](https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38655941349). The deployed GitHub OIDC subject uses immutable numeric owner/repository IDs; the original name-based `sub` example is superseded above.

The subscription and tenant matched; Azure OIDC login, West Europe location and four namespaces `Microsoft.App`, `Microsoft.DBforPostgreSQL`, `Microsoft.KeyVault`, `Microsoft.Network` all passed. **Remaining:** actual subscription SKU/quota, Reader-vs-deployer RBAC distinction, documented all-in EUR20 estimate, any Azure resources, private DB/runtime, restricted role, synthetic staging E2E. All external real-provider synchronization and Level 2B/2C remain HOLD. Read-only SKU follow-up: [EA_AZURE_SKU_COST_GATE_20261015.md](./EA_AZURE_SKU_COST_GATE_20261015.md).
