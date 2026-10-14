# EA Azure staging — provider verification and SKU/cost gate (15 Oct 2026)

**Status:** `OIDC_VERIFIED / FOUR_PROVIDERS_REGISTERED / SKU_AND_ALL_IN_QUOTE_PENDING / NOT_DEPLOYED`  
**Scope:** one private synthetic-only EA tenant, `westeurope`, dedicated proposed `rg-ea-stg-westeurope`, maximum **EUR 20/month**; no live provider synchronization; EA Level 2B/2C HOLD.

## Evidence independently checked

- Original identity workflow on `main`: https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38655941349
- **Rerun attempt 2:** result `success`, GitHub OIDC immutable subject accepted by Microsoft Entra, Azure CLI login PASS, approved subscription ID/tenant identity matched, active subscription `Enabled`, `westeurope` present.
- Exact provider registration states in independent run's logs:
  - `Microsoft.App`: `Registered`
  - `Microsoft.DBforPostgreSQL`: `Registered`
  - `Microsoft.KeyVault`: `Registered`
  - `Microsoft.Network`: `Registered`
- Operator had separately granted *synthetic staging* deployment authorization and attested budget validation; this **does not** verify the precise current cloud costs.
- Azure resources created by read-only workflow: **none**. Connected GitHub/Google Drive tools do not confer Azure ARM write access.
- Immutable OIDC subject matches the Entra federated credential with numeric GitHub owner/repository IDs and the `ea-staging-preflight` environment. Do not revert to name-based subject.

## Next permitted execution: manual read-only West Europe SKU check

Workflow: `.github/workflows/ea-azure-staging-sku-readonly.yml`, available on `main` only after this PR merges.

The job uses the same protected `ea-staging-preflight` environment and OIDC Reader identity. It fails closed on an unregistered provider, reads PostgreSQL Flexible Server West Europe SKU metadata with `az postgres flexible-server list-skus --location westeurope`, and reports the candidate Burstable identifiers. It **cannot** prove subscription quota availability, account-specific actual EUR charges or approval to create resources. It never creates a resource group, server, app, secret, role assignment, OAuth grant or budget object.

Run manually:
```powershell
gh workflow run ea-azure-staging-sku-readonly.yml --repo nanotech-solutions-norway/Ea-Personal_Assistant --ref main
gh run list --repo nanotech-solutions-norway/Ea-Personal_Assistant --workflow ea-azure-staging-sku-readonly.yml --limit 1
```

## Remaining hard deployment gates

1. Capture the previously attested budget calculation **as an itemized, authoritative actual subscription quote**, preferably private Drive documentation. Specify PostgreSQL Burstable compute hours/SKU, >=32 GiB disk, backup retention, Container Apps vCPU/memory/request assumptions and remaining subscription-wide free grant, Key Vault operations, private VNet/DNS/NAT/endpoint/egress, registry, monitoring/logging, any paid supporting services, taxes, and recurring cross-cloud expenses.
2. Verify West Europe SKU output; confirm actual subscription-specific quota/capacity and private network design. Region/provider registration is not SKU/capacity proof.
3. Require computed all-in EUR/month **<=20** for the specified operating duration, plus a practicable teardown / fail-closed stop plan. Azure budgets are **alerts**, not a guarantee against charges; PostgreSQL service stop does not remove all costs and may restart after seven days.
4. Keep OIDC preflight Reader separate from any prospective deployment identity. Before actual infrastructure creation, establish least-privileged deployer ARM rights and verify resource scopes. Do not widen preflight identity permissions.
5. When gates 1–4 are evidenced, create a separately gated synthetic-only deployment workflow/plan; perform final security review, do not enable backend provider OAuth or live syncing.

### Cost-safe alternative when the quote cannot fit EUR 20/month

Retain the current disposable PostgreSQL GitHub Actions synthetic CI and read-only cloud checks, rather than provisioning always-on PostgreSQL / private networking. Another architecture or higher budget requires explicit operator choice. No architecture adjustment is silently approved.

## Reference documentation

- https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server#az-postgres-flexible-server-list-skus
- https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices
- https://learn.microsoft.com/en-us/azure/container-apps/billing
- https://learn.microsoft.com/en-us/azure/postgresql/configure-maintain/concepts-limits
- https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets
