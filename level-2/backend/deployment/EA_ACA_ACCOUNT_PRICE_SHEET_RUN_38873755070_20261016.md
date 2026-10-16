# EA Azure price-sheet run 38873755070 — diagnostic follow-up

**Run observed:** 16 October 2026, https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/runs/38873755070

- Both jobs **SUCCESS**. The protected Azure OIDC Reader authenticated and selected the expected subscription, and the diagnostic made an Azure ARM GET. However `EA_ACA_SUBSCRIPTION_BILLING_READ=UNAVAILABLE_OR_UNAUTHORIZED`; **no current subscription-specific EUR prices or free-grant balances were retrieved**.
- Azure Consumption Price Sheet GET endpoint and `api-version=2024-08-01` are confirmed in Microsoft's official REST reference: https://learn.microsoft.com/en-us/rest/api/consumption/price-sheet/get?view=rest-consumption-2024-08-01 .
- `Microsoft.Consumption/pricesheets/read` is a documented Azure management-plane action: https://learn.microsoft.com/en-us/azure/role-based-access-control/permissions/management-and-governance . Reader OIDC **must not** be promoted to Contributor or billing data reader automatically.
- For Microsoft Customer Agreement (MCA) billing, an account's downloadable price sheet may belong to its **billing profile**. An authorized billing profile Owner, Contributor, Reader or Invoice Manager can obtain the price sheet **privately** in Azure Portal. Sources: https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/mca-understand-pricesheet and https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/ea-pricing . Do not confuse subscription Reader with MCA billing-profile Reader.

## Code update

The protected manual workflow now classifies only recognized, allowlisted Azure CLI failure code tokens (for example, `AUTHORIZATION_FAILED`, `RESOURCE_NOT_FOUND`, `UNSUPPORTED_API_VERSION` or `UNAVAILABLE_OR_UNAUTHORIZED`). It NEVER includes Azure error text, HTTP payload, subscription GUID, tenant information or sign-in tokens. Missing/unknown errors remain inconclusive. No new Azure identity, role grant, provider call, resource or cost was created.

After PR merging and passing CI, the operator can manually run the workflow again from protected `main`:

```powershell
gh workflow run ea-azure-aca-subscription-price-readonly.yml --repo nanotech-solutions-norway/Ea-Personal_Assistant --ref main
gh run list --repo nanotech-solutions-norway/Ea-Personal_Assistant --workflow ea-azure-aca-subscription-price-readonly.yml --limit 2
```

If it returns `AUTHORIZATION_FAILED` or `FORBIDDEN`, access is insufficient; do **not** change the existing read-only principal or print raw Azure stderr. Instead obtain an authorized **billing-profile** price sheet privately, or request a separately scoped billing-read principal under explicit governance. If it returns resource/API errors, investigate agreement support and backend API. If it returns only `UNAVAILABLE_OR_UNAUTHORIZED`, the cause remains unverified.

**Status:** Account-specific EUR ACA rates remain UNKNOWN; the authoritative 20-category gate remains **4 priced / 16 unverified**. Azure deployment is held at EUR20 including tax. Production Bring synchronization remains DISABLED.
