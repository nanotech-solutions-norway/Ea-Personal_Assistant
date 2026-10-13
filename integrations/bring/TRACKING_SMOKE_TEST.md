# EA Bring Tracking API v2 — authenticated read-only smoke test

**Status:** candidate / pending CI, PR review and first credential-backed acceptance.

## Why this is separate from Customer Info

The Bring Customer Info endpoint (`GET /customer-info/customers`) lists
customer numbers **and their available service products for checkout/booking**.
A successful HTTP 200 response with `customers: []` does not prove that the
API credentials lack Tracking API access. The operator confirms full Mybring
account rights; this must be independently validated per endpoint.

## Exact scope

- A **manual-only** GitHub Actions workflow, not a schedule.
- Reads a single official **synthetic** test identifier:
  `TESTPACKAGEDELIVERED`.
- Request: `GET https://api.bring.com/tracking/api/v2/tracking.json?q=TESTPACKAGEDELIVERED`.
- Uses existing protected GitHub environment `bring-pilot`:
  `BRING_API_UID`, `BRING_API_KEY`, `BRING_CLIENT_URL`.
- Fails closed on HTTP authentication/transport errors, wrong API version,
  nested Bring response errors, wrong package number or missing
  `DELIVERED` event. Prints only `BRING_TRACKING_CHECK=...`.
- No real tracking numbers, customer numbers, account data, email addresses,
  secrets, response bodies or shipping documents in GitHub artifacts/logs.
- No booking, shipment creation, customer account mutation, scheduling,
  invoice access, production sync or persistent webhook registration.

## Acceptance

1. Review PR and confirm required CI checks passed.
2. Merge PR through protected `main` after required approvals/CI.
3. Confirm `bring-pilot` deploy branch restriction allows only `main` and
   requires approval when available.
4. Under GitHub Actions choose **EA Bring Tracking v2 read-only smoke test**,
   select **Run workflow**, choose `main`, and approve environment if asked.
5. Check **Test authenticated synthetic tracking request** logs:
   - `BRING_TRACKING_CHECK=PASS` + workflow success = authenticated synthetic
     Tracking API v2 response validated.
   - `BRING_TRACKING_CHECK=HTTP_401` = authentication rejected.
   - `BRING_TRACKING_CHECK=HTTP_403` = authorization rejected.
   - `BRING_TRACKING_CHECK=API_ERROR` = Bring response contained an
     application-level error despite HTTP 200.
   - `BRING_TRACKING_CHECK=TEST_PACKAGE_MISSING` or
     `TEST_STATUS_MISMATCH` = response did not match test contract.
   - `BRING_TRACKING_CHECK=BLOCKED_MISSING_CONFIG` = environment incomplete.

Passing this synthetic test **does not** authorize access to other shipments.
Separately test one operator-authorized real tracking number through a
protected, tenant-scoped backend before calling production tracking active.

Bring docs:
- https://developer.bring.com/api/tracking/
- https://developer.bring.com/api/testing/
- https://developer.bring.com/api/customerinfo/
