# EA Bring — Entra v2 identity and PostgreSQL protected registry (phase 2)

**Status: ADAPTERS_STAGED / SYNTHETIC_CI_REQUIRED / DEPLOYMENT_HOLD**

This stage implements real verification **code**, not a deployed identity service or
account authorization decision. It preserves the current default policy
matrix (bring.tracking.read = PROHIBIT) and the Bring provider integration as
manual-only. No paid Azure resources, real customer records, shipping data or
external calls are introduced.

## Architecture and trust boundaries

1. The future *EA API resource server* receives an Entra-issued OAuth2
   **access token**, not an ID token or a Microsoft Graph token.
2. EntraAccessTokenVerifier pins a **single configured Entra workforce tenant**
   (GUID), the EA API audience, allowlisted caller application IDs and
   tenant-specific Microsoft signing JWKS at login.microsoftonline.com.
   Only RS256, v2 tokens, verified issuer/audience/tenant ID, expiration,
   not-before/issued-at, approved calling app, immutable Entra object ID and
   delegated "bring.tracking.read" scope are eligible.
   No arbitrary tenant, JWKS URL, token-provided claims or Graph scopes may
   authorize a Bring read.
3. The existing authorize_tracking_read gate requires a trusted
   verified principal and a server-side tenant/customer grant.
4. PostgresBringRegistry reads three dedicated registry tables using
   a SELECT-only DB principal subject to FORCE ROW LEVEL SECURITY.
   Every DB read sets *transaction-local* actor issuer/subject/tenant
   variables from the trusted backend, never from client headers.
   Sender/recipient customer identifiers are never inferred from the
   public Bring Tracking v2 response.
5. Independently reviewed authenticated Mybring booking evidence associates
   a tenant-owned customer to an exact authorized tracking reference. The
   registry stores an HMAC-SHA256 digest of (tenant, tracking reference), not
   the plaintext package/consignment number. The independent >=32-byte HMAC
   key must be supplied from a protected backend secret store and rotated
   with an explicit re-index/migration process.
6. TenantAccount contains only a Key Vault **reference**, not a plaintext
   Bring API key. A future separate adapter must use trusted workload identity,
   fetch the correct tenant secret, and enforce one read-only request.

## Schema

Migration: sql/006_bring_authorization_registry.sql (run **after 001–005** by
a separate migration owner). New tables:

- ea_bring_tenant_accounts: one company customer number and Key Vault ref per
  authorized tenant, default disabled.
- ea_bring_principal_grants: exact issuer, Entra object ID, tenant and
  bring.tracking.read approval, default disabled.
- ea_bring_shipment_provenance: tenant-bound keyed tracking digest, company
  customer number, approved booking evidence + UTC review timestamp,
  default unapproved.

Each table FORCEs RLS and defaults to no visibility without verified
transaction-local actor context. The runtime DB role must:
- have SELECT only to these tables and schema USAGE;
- have **no SUPERUSER, BYPASSRLS, ownership, CREATE, INSERT, UPDATE or DELETE**;
- be subject to active RLS (checked by the adapter per read);
- be an independently provisioned principal; no secrets in repository code.

**Limit:** Transaction-local settings are under control of a trusted
application SQL connection. Anyone controlling those settings or the
application's verified identity context can defeat this isolation. The adapter
is NOT an authentication service; the caller must verify Entra tokens before
constructing a registry from the trusted issuer/subject. No public HTTP
endpoint is added in this phase.

## Entra configuration NOT YET PROVISIONED

Register a **dedicated EA API** in the intended Microsoft Entra tenant,
configure an application ID URI/audience and expose an admin-consented
delegated scope "bring.tracking.read". Register an authorized client
application ID separately. Do not repurpose the GitHub Actions OIDC identity
used for cloud read-only preflight as an end-user EA API principal.

Real values must come from Entra app registration and remain outside public
GitHub code; the tests use only illustrative UUIDs and offline RSA keys.

Use version 2.0 tenant-specific tokens with RSA-signing keys issued by
Microsoft. The verifier calls only a constructed URL under the pinned
login.microsoftonline.com tenant authority and does not log JWT values or
claims. PyJWT[crypto] is a runtime dependency. Operational rollout requires
key rotation and JWKS availability tests, and upstream token audience/
scope/app-registration confirmation.

## Synthetic acceptance evidence

- Unit suite generates an ephemeral RSA keypair and mock tenant JWKS.
  Checks signature, issuer, audience, token expiry/not-before, tenant,
  authorized client ID, delegated permission, unknown/wrong signing keys,
  unsigned tokens and rejection of foreign app-only roles.
- Disposable PostgreSQL integration suite applies migration 006 and
  provisions an ephemeral restricted role. Two invented tenants A/B have
  distinct grants, customer IDs, vault references and HMAC booking digests.
- Positive and negative lookups are run via actual database RLS; absent
  actor session context, A→B and B→A reads must return no rows. The
  restricted role must fail for table INSERT and RLS policy alteration.
- The existing backend suite/CI still confirms the gateway default is
  disabled and the policy matrix denies Bring runtime access.
- GitHub PR CI results MUST be checked before concluding tests pass.

## Remaining mandatory live gates

1. Confirm exact Entra tenant, resource API and authorized app IDs, register
   intended scope and validate production JWKS key rotation and real
   signed token issuance in a **private** staging runtime.
2. Provision approved tenant/client registrations, immutable principal grants
   and privately reviewed booking evidence with operator approval in an
   access-controlled database; never put real values in GitHub/ChatGPT logs.
3. Provision distinct private PostgreSQL runtime role and Azure Key Vault,
   enable workload identity, and validate correct **per-tenant** secret mapping
   and rotation. No general vault browsing.
4. Add an authenticated EA read-only tool endpoint bound to verified identity
   and authorized tenant. Deny user-selected tenant IDs, unregistered packages,
   replay after grant revocation and any cross-tenant request.
5. Execute live A/B tenant negative tests with restricted runtime connections,
   RLS and post-query redaction/audit. Prove wrong-tenant reads, wrong
   credential access and wrong-shipment access are rejected.
6. Verify TLS, durable audit minimization, encrypted data retention, rate
   limits/429/backoff and cleanup. Get independent authorization for production.
7. **Azure staging cost:** before provisioning, independently validate the
   itemized westeurope all-in price, <= EUR20/month and SKU/quota availability
   under the existing project budget gate. This change does not provision.

**Hard HOLD:** No new endpoint deployed, no Bring real-data sync, no polling,
no extra Mybring permissions or API key rotation, no customer exports.

Sources:
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference
- https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- https://developer.bring.com/api/tracking/
