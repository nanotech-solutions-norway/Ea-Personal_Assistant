# EA Bring — one-time real shipment acceptance (staging only)

**State:** PENDING_REAL_SHIPMENT_VALIDATION / PRODUCTION_SYNC_HOLD

## Purpose and limitations

The authenticated Tracking v2 smoke test succeeded with a synthetic package
(GitHub run 38369633072). It does not validate any real company shipment.

Bring Tracking API can provide public tracking details even when the API user is
not the sender or recipient. A successful HTTP 200 alone is not sufficient
proof of company authorization. The new one-shot check requires:

- A unique exact match for the provided real package or consignment number.
- An explicit match for the company's configured customer number in the
  shipment sender or recipient customer/master number fields.
- At least one event carrying a valid machine-readable status.
- No response bodies, identifiers, contacts, dates, locations or credential
  values emitted to job logs or artifacts.

If provider response fields needed to prove the company association are
redacted, the validation fails closed as TENANT_UNVERIFIED. A sender/receiver
relationship boolean alone does not establish the specific expected tenant.

This is a staged company-account confirmation only, not an end-to-end test of
the EA production identity/RBAC or tenant isolation layer.

## Operator setup: add exactly two new Environment secrets

Use the secured GitHub settings link:
https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/settings/environments

Select **bring-pilot → Environment secrets → New secret**. Enter:

1. BRING_REAL_TRACKING_NUMBER: one real Bring tracking/package/consignment
   number belonging to your own company and explicitly approved for this test.
   Do not select a personal or third-party parcel. Never send this number via
   ChatGPT, PR comments, workflow dispatch inputs or public code.
2. BRING_EXPECTED_CUSTOMER_NUMBER: your company customer number from the private
   Mybring ApiCustomers.csv export. Treat it as protected configuration; never
   commit the CSV or the number to this public repository.

Existing secret keys BRING_API_UID and BRING_API_KEY and existing variable
BRING_CLIENT_URL remain unchanged. Restrict environment deployment to main
and require approval when supported.

## Runbook

1. Verify new PR CI and branch rules have passed, and merge via protected main.
2. Save the two new Environment secrets using GitHub settings.
3. Open:
   https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/actions/workflows/bring-real-shipment-validation.yml
4. Choose Run workflow → main → Run workflow. Approve bring-pilot if prompted.
5. Inspect the status marker in the one-shot read-only live job:

   - BRING_REAL_CHECK=PASS: exact shipment, expected company customer ID and a
     status event confirmed.
   - BRING_REAL_CHECK=TENANT_UNVERIFIED: no explicit customer-ID match in data.
     Investigate via privately authenticated account-scoped Bring source; do
     not override the evidence gate.
   - BRING_REAL_CHECK=NOT_FOUND or AMBIGUOUS_MATCH: invalid unique match.
   - BRING_REAL_CHECK=STATUS_NOT_VERIFIED: no acceptable event status.
   - BRING_REAL_CHECK=BLOCKED_MISSING_CONFIG: required secret missing.
   - BRING_REAL_CHECK=API_ERROR, HTTP_401, HTTP_403, HTTP_429, NETWORK_ERROR:
     provider API or network could not satisfy acceptance.

Only PASS plus an overall successful workflow count as bounded acceptance.

## Hold boundaries

No scheduled polling, real shipment persistence, cross-tenant data mixing,
production integration, bookings, invoice access or external writes are
enabled. A one-time GitHub-hosted Actions staging job does not replace the
approved managed Azure EA backend with Key Vault, authenticated tenant mapping,
encrypted storage, durable audit, rate-limit/backoff and tenant RLS tests.

Documentation: https://developer.bring.com/api/tracking/
