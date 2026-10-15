# Bring authorization and tenant-isolation gate — staged backend contract

State: **CODE_CANDIDATE / PRODUCTION_DISABLED**  
Owner: EA Level 2 backend  
Evidence source: operator-approved Mybring booking record and screenshot, reviewed 15 October 2026.

## Security conclusion

Bring's Tracking v2 is publicly trackable and does not reliably identify the
business customer in its response. An API token that can read tracking events
**does not** prove tenant authorization or company ownership.

The prior read-only synthetic test and one real-shipment tracking test have
passed. An independently corroborated Mybring booking and authenticated UI
support provenance of one company shipment. They do not replace a bound,
verified EA requester identity and protected tenant registry.

See:
- https://developer.bring.com/api/tracking/
- https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/issues/48

## Implemented in this change

The pure authorization policy module
src/ea_backend/bring_tenant_gateway.py implements a fail-closed gate with:

1. **Feature disabled by default.** No tenant lookup or provider request is
   allowed when ReadGateConfig.enabled is false.
2. **Authenticated identity.** Accept only a cryptographically verified,
   unexpired OIDC token from the configured issuer/audience, via a production
   identity verifier provided by the trusted backend (not by request input).
3. **Server-side grant.** Derive authorization only from a trusted registry
   mapping the verified issuer/subject to ONE approved tenant and the exact
   bring.tracking.read permission. Ignore client-supplied customer IDs/roles.
4. **Company and credential binding.** The tenant's customer number must match
   the principal grant. The credential reference must resolve to an
   Azure Key Vault secret URI. No secret value is returned by the module.
5. **Shipment provenance.** An exact tracking ID must be on that tenant's
   independently approved authenticated Mybring booking allowlist, with the
   same customer number and fresh evidence. Provider Tracking v2 responses
   and operator screenshots alone are not authorization.
6. **Read-only output.** A ScopedTrackingPermit may be used by a separate,
   trusted tool adapter to retrieve one shipment, without broad enumeration.
7. **Neutral errors.** A denial emits a bounded code, never an account number,
   shipment ID, raw body, token, vault path, or provider credential.

The test suite includes negative cross-tenant attempts in both directions,
forged/expired issuer-audience claims, wrong permission, revoked tenant/grant,
customer mismatch, wrong shipment, wrong provenance, stale evidence,
untrusted verifier/registry, and query-parameter injection.

All current identifiers in code and tests are fictitious synthetic strings.

## Critical limitations: implementation is not deployed

This change does **NOT** add an authenticated Bring read endpoint or route in
runtime/ea_runtime/app.py, and does NOT configure a token verifier, service
principal, Key Vault, persistent registry or PostgreSQL tenant binding.
A Python Protocol with a production_safe flag is a contract, not evidence that
its implementer is secure. Unit-test stubs that set that flag are NOT
production verifiers. The EA backend itself is currently not deployed.

No real customer numbers, shipment identifiers, user emails, passwords,
API keys or booking/screenshot files are committed in this public repository.

The existing policy-matrix.v1.json has no bring.tracking.read action; unknown
actions default to PROHIBIT. Deliberately keep it that way until integration
approval. No GitHub Actions workflow or persistent sync is enabled.

## Required completion evidence before any rollout

**Identity and credential layer:**
- Deploy a real JWT/OIDC verifier validating signing keys, issuer, audience,
  expiration and revocation behavior; reject self-asserted headers.
- Provision an app-controlled tenant/grant/booking registry whose entries
  cannot be written by callers or inferred from tracking API responses.
- Obtain one verified authenticated Mybring booking record and operator
  approval; register the exact customer + tracking association in the
  protected registry, not in repository code or workflow parameters.
- Resolve only the tenant's dedicated read-only Bring credential from
  Key Vault using workload identity. No model/user-provided secret selection.

**Isolation and durability:**
- Enforce tenant ID at the authorized tool boundary and per-transaction DB
  context (SET LOCAL), using a non-owner, non-BYPASSRLS DB role.
- Validate deny paths for anonymous, wrong tenant, mixed tenant, revoked user,
  wrong customer credential, forged token, future/stale booking, repeated
  access after revocation, cross-tenant retrieval and status persistence.
- Verify encrypted retention, idempotent readback, tenant-scoped audit,
  redaction, 429/backoff handling and cost/rate limits.
- Run a true staging integration with TWO isolated test tenants: A must not
  read B's shipment or use B's credential (and vice versa).
- An independently reviewed result must explicitly authorize extending the
  policy matrix; default remains PROHIBIT until that gate.

**Provider rights:**
- Public Tracking v2 permits lookup for publicly trackable shipments.
  Do not claim account-scoped provider authorization unless Bring supplies
  an authenticated company-scoped endpoint/evidence in a separate test.
- Company ownership can be supported by signed booking records; EA tenant
  access control still must be independently enforced in EA.

## Release state

- Policy code / offline unit tests: staged in a branch, CI required.
- True JWT verification: NOT IMPLEMENTED for Bring.
- Persistent grant and shipment evidence registry: NOT IMPLEMENTED.
- Key Vault resolution / account credential separation: NOT IMPLEMENTED.
- Runtime route wired to policy gate: NOT IMPLEMENTED.
- Live two-tenant negative test: NOT RUN.
- Azure deployment/cost approval: NOT REQUESTED by this change.
- Real production polling, event ingestion and storage: **DISABLED**.

Fail-safe state: **TENANT_AUTHZ_PENDING / PRODUCTION_SYNC_HOLD**.
