# EA Bring — GitHub Environment Secrets for controlled staging (Key Vault HOLD)

**Decision date:** 2026-10-16
**Scope:** `Ea-Personal_Assistant` only. Applies to **synthetic-only, manually dispatched preflight**. Does NOT approve production Bring integration, real shipment reads, paid Azure deployment or credential migration into an Azure runtime.

## Operator decision

- **Azure Key Vault provisioning and integration: HOLD.** Keep the previously written `bring_vault_credentials.py` as dormant code, for potential future architecture only. No new vault, private endpoint, managed identity, or KV billing is approved. The current `EA_48H_PRIVATE_TOPOLOGY_PROPOSED_20261015.json` remains a non-deployable design; a prospective Key Vault charge is a *conditional exclusion requiring independent validation*, not an automatically marked zero in the authoritative quote.
- **GitHub Environment Secrets: SELECTED for the current Bring preflight.** Reuse the existing GitHub `bring-pilot` environment rather than duplicating live credentials in repository/organization secrets or inventing a new store. Its existing integrations already expect the two secrets and one variable below.
- No real provider connection, no customer tracking numbers, no GitHub-injected secrets in external payloads and no actual data sync are authorized by this switch.

## Operator-managed GitHub environment

Repository: https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant

GitHub → **Settings → Environments → bring-pilot**. Before manually dispatching the preflight:
1. Verify the environment exists, restrict deployments to the protected **`main`** branch, configure required reviewers where supported and block self-review where supported. **Environment configuration/permissions were not readable through the GitHub connector; these protections must be verified by an administrator.** Do not assume controls exist.
2. In **Environment secrets**, create or verify `BRING_API_UID` and `BRING_API_KEY`. Value content is WRITE-ONLY; GitHub cannot show a saved secret back to the assistant. Never place these values in a repository `.env`, a PR, Actions YAML, an issue/comment, Slack, screenshots or logs.
3. In **Environment variables**, create or verify `BRING_CLIENT_URL` (HTTPS URL; no username/password, query-string credentials, fragment or line breaks). It is not an API key but may identify an organization: it is still never echoed by the preflight.
4. Do not add live shipment references, billing payment credentials, tracking-number exports or customer data to this preflight. If the account requires a separate HMAC key for a future PostgreSQL registry, that must be generated independently and handled by a separate reviewed deployment process, **not reused from BRING_API_KEY**.
5. Protect repository administrator access, GitHub Actions workflow changes, environment approval and all secrets from untrusted contributors. A public repo still exposes workflow *source* and execution status, not environment-secret values.

GitHub docs: https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments and https://docs.github.com/en/code-security/reference/secret-security/secret-types .

## Offline validation (safe to run)

New GitHub workflow: `.github/workflows/ea-bring-github-secrets-staging.yml`:
- Pull requests run **synthetic-only unit tests**, with **no `environment`**, no secret references and no provider calls.
- Protected `main` + explicit `workflow_dispatch` triggers a **separate** job referencing only `bring-pilot`. It checks configuration and disabled-production safety flags without printing credential values, connecting to any API or making cloud resource changes. It has `permissions: contents: read` and no Azure OIDC grant.
- It does **not** invoke any of the older `bring-pilot-readonly.yml`, `bring-real-shipment-validation.yml`, or `bring-tracking-smoke.yml` provider tests. Those historical manual workflows may contact Mybring and should remain uninvoked unless separately approved.
- Required output: `EA_GITHUB_SECRETS_STAGING_PREFLIGHT=PASS`, `BRING_PROVIDER_REQUESTS=NONE`, `AZURE_RESOURCE_CREATION=NONE`, `PRODUCTION_BRING_SYNC=DISABLED`.
- Missing/unsafe credentials yield fixed `BLOCKED_...` statuses without exposing secret values.

Operator dispatch **after security/environment controls have been verified**:
```powershell
gh workflow run ea-bring-github-secrets-staging.yml --repo nanotech-solutions-norway/Ea-Personal_Assistant --ref main
gh run list --repo nanotech-solutions-norway/Ea-Personal_Assistant --workflow ea-bring-github-secrets-staging.yml --limit 3
```
Never post or copy the actual `BRING_API_UID`, `BRING_API_KEY` or raw workflow environment to chat/GitHub issues. Report only sanitized `EA_GITHUB_SECRETS_STAGING_PREFLIGHT=...` marker.

## Critical runtime and tenant-isolation boundary

GitHub Actions secrets are available to **workflow jobs** only and cannot be fetched by a running Azure Container Apps replica simply because they exist in GitHub. A future approved deployment, if Key Vault stays on hold, must bridge GitHub environment secrets into **Azure Container Apps app-scoped secrets**, then reference them via a `secretref` environment variable or secure volume mount. Do not pass values in image builds, artifacts, shell history, command-line flags, logs or workflow outputs. Avoid permissions that can `listSecrets` outside the deployment principal. The actual secret injection mechanism and teardown require separate review; **no Azure deployment workflow is added now**.

Current authorization database migration `sql/006_bring_authorization_registry.sql` and `bring_tenant_gateway.py` still require a Key Vault-style tenant-account reference, and the existing runtime gateway remains default-disabled. Therefore this change **DOES NOT make the GH secret provider a compatible runtime credential resolver**. Replacing that key reference and proving tenant-specific credential binding, Entra access-token verification, restricted PostgreSQL RLS and booking provenance is a separate, independently reviewed implementation gate; do not fake a Key Vault URI to bypass it.

For one synthetic staging tenant, GitHub environment credentials are a temporary *workflow secret source*, not a production multi-tenant credential registry. If live multi-tenant Bring access is later approved, a reviewed per-tenant separation and rotation design is mandatory. GitHub secret rotation is not automatic runtime rotation; promotion/redeploy/restart must be separately tested.

Azure docs: https://learn.microsoft.com/en-us/azure/container-apps/security and https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets . Microsoft recommends Key Vault for production secret centralization; the operator-requested GitHub alternative is deliberately limited to controlled staging.

## Mandatory remaining gates

- Private 48-hour Azure all-in price and tax including registry/observability/managed ingress/egress, with <= EUR20 ceiling and enforceable teardown; cost model remains BLOCKED.
- Review of GitHub `bring-pilot` environment required reviewers/main-only access (not verified yet), GH organization permission model and rotation.
- Scope-restricted Azure deployer with independent teardown authority **only if** the cost and access gates are explicitly approved.
- Synthetic-only, cross-tenant negative tests of a future correctly bound runtime secret provider, not just environment variable presence; no unvetted GitHub secret-to-Azure bridging.
- Real signed-token verification and protected tenant registry binding in a deployed API, separate future gate.
- Explicit production approval, never implied by PASS status.

**Current authoritative decision:** `KEY_VAULT_HOLD / GITHUB_ENVIRONMENT_STAGING_SELECTED / GH_SECRET_VALUES_NOT_VERIFIED / NO_AZURE_RESOURCE_CREATION / NO_LIVE_BRING_SYNC`.
