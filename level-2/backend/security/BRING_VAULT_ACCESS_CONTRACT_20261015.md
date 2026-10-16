# EA Bring — protected vault read contract (synthetic only)

> **DECISION UPDATE — 2026-10-16:** Azure Key Vault provisioning and production resolver integration are **ON HOLD** by operator direction. For the current *synthetic-only workflow preflight*, GitHub Environment Secrets in existing `bring-pilot` have been selected; see [BRING_GITHUB_SECRETS_STAGING_20261016.md](./BRING_GITHUB_SECRETS_STAGING_20261016.md). This legacy Key Vault contract and adapter remain dormant and must NOT be treated as approved deployment requirements for the current preflight. Runtime Bring authorization and production synchronization remain disabled. No GitHub workflow can silently replace the server-side, tenant-bound credential resolver.

**Status:** CODE_ONLY / KEY_VAULT_NOT_PROVISIONED / PRODUCTION_SYNC_DISABLED

This change follows operator-reported local Entra access-token validation success
on 15 Oct 2026. Entra tokens and user claims were not uploaded to GitHub.

## Authority and sequence

1. Independently verify an Entra API access token (signed v2 token, correct
   tenant/audience, allowed desktop client and delegated bring.tracking.read).
2. Load a verified actor's server-side tenant grant and independently approved
   shipment evidence from the restricted PostgreSQL registry.
3. Run the existing fail-closed authorize_tracking_read gate. Current policy
   remains PROHIBIT / ReadGateConfig.enabled=False; no runtime route exists.
4. Only a trusted backend tool implementation can pass the internally generated
   ScopedTrackingPermit to ScopedBringVaultResolver. It must never accept a
   fabricated permit from an HTTP request, user-supplied JSON, LLM or webhook.
5. Resolver checks exact, preapproved vault host and secret reference, then
   fetches only ONE named secret through a fixed user-assigned managed identity.
   No list-secrets operations, Azure CLI, interactive login or DefaultAzureCredential
   fallback.
6. The protected Key Vault secret value has a JSON shape containing exactly:
   api_uid, api_key, client_url. All values are treated as secret data and
   never logged. client_url is a valid HTTPS URL.
7. A separate future Bring adapter must make one read-only request using
   this memory-only bundle with redirects disabled and sanitized outcome codes.
   No API calls, response caching, tracking synchronization or account writes
   are part of this PR.

## Key Vault deployment planning — NOT YET AUTHORIZED

- Create an EA-specific Key Vault (not shared with AtlasOrbit) in the approved
  staging resource group, only after the 48-hour all-in EUR20 cost, quota,
  topology and teardown gates have passed.
- Use Key Vault Azure role-based access control, least-privilege secret read
  scope for a dedicated **EA runtime user-assigned managed identity**, and
  separate secret creation/rotation permissions. The current GitHub OIDC Reader
  principal must not be promoted to deployer or secret reader.
- Restrict networking and avoid unrestricted public Key Vault access; ensure
  the Container Apps network and identity can reach the selected vault without
  incurring unpriced Private Link/NAT/egress costs.
- In each tenant account registry row, save only the allowlisted
  https://<vault-name>.vault.azure.net/secrets/<name> reference.
  Store no plaintext Bring credentials in the public repository.
- Provision an independent >=32-byte HMAC secret for the booking registry
  and rehearse rotation/re-indexing separately; do not re-use the Bring API key
  as the digest key.
- Real secret bundle values must originate from the operator's private Bring
  configuration, not demo fixtures or public Github files.
- Prior to enabling runtime, independently test wrongly scoped managed
  identities, wrong tenant/vault references, revoked grants, wrong shipment
  references, attempts to select alternate vaults, Key Vault 403/404/429,
  secret rotation, timeout and log redaction.
- A public GitHub repository must never contain downloaded credentials,
  raw API requests/responses, individual tracking references or database dumps.

## Security limitations

A Python dataclass alone is not a cryptographic capability. The trusted
server-side route must create ScopedTrackingPermit only after real Entra and
registry authorization; otherwise callers able to construct it can bypass
policy and choose approved vault paths. Do not expose the resolver through a
standalone endpoint. Vault-scoping controls constrain blast radius but are
not sufficient to prove tenant authorization.

The code's tests use synthetic secret and vault names, with mocked clients.
No Azure token, workload identity, vault, PostgreSQL staging deployment,
permission assignment, live Bring API connection or production tenant isolation
test has been exercised by this stage.

Project gates still required before any paid Azure staging:
- Full private topology priced with all managed public IP, load balancer,
  VNet/private DNS, Container Apps, PostgreSQL, Key Vault, logs/egress and
  taxes within EUR20, or independently documented acceptable alternative.
- Scope-restricted deployment identity separate from preflight Reader.
- Timeboxed synthetic-only staging, data protection and complete teardown
  with post-delete ARM and actual spend readback.

**Operational default:** NO_DEPLOYMENT / NO_LIVE_SYNC / NO_PAID_RESOURCE_CREATE.
