# EA Bring read-only authentication pilot

**Scope:** Internal, operator-owned account only. Staging / PENDING_REVIEW for production.

## Purpose

Confirm that a user-created Mybring API key can perform exactly one authorized,
read-only GET to Bring's Customer Info API, without emitting customer records,
credentials, response bodies or request headers into GitHub logs or artifacts.

Source: https://developer.bring.com/api/customerinfo/

## Environment setup

In GitHub repository `nanotech-solutions-norway/Ea-Personal_Assistant`, create
an Environment named `bring-pilot`, restricted to the `main` branch and
with required-reviewer protection when available.

Environment **secrets**:
- `BRING_API_UID`: Mybring user's login email
- `BRING_API_KEY`: the Mybring user API key

Environment **variable**:
- `BRING_CLIENT_URL`: the verified public integration identifier,
  initially `https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant`
  for this repository-run pilot.

Never commit key material or personal/customer information. Do not paste
the key into ChatGPT or open GitHub issues.

## Gates

1. Review and merge the pull request after standard CI passes.
2. Check environment branch restrictions and authorized reviewer protection.
3. GitHub Actions -> **EA Bring read-only API pilot** -> **Run workflow** on `main`.
4. Review **only** the result marker:
   - `BRING_CHECK=PASS`: GET returned authorized nonempty customer collection.
   - `BRING_CHECK=HTTP_401`: authentication failed (check UID/key).
   - `BRING_CHECK=HTTP_403`: rights/access may be insufficient.
   - `BRING_CHECK=AUTHENTICATED_NO_CUSTOMER_ACCESS`: no customer account access.
   - `BRING_CHECK=BLOCKED_MISSING_CONFIG`: required secret/variable not available.
5. Never infer that shipment tracking, invoicing, or subsequent data sync is
   enabled from a successful Customer Info check; those require separate scopes
   and authorization/acceptance tests.

No schedule, API write, automation promotion, customer record export, or
external file write-back is enabled by this workflow.

## Protected-main merge gate

The `main` branch is governed by the active repository ruleset
`EA Personal Assistant — Protect main (CI + PR)`. Do not merge this pilot
until GitHub displays all four required PR checks as passing on the
current head or test-merge commit. Keep `bring-pilot` scoped to `main`.

This documentation does not attest that any Bring API credential-backed
request has run. Only a subsequently recorded manual Actions run and its
`BRING_CHECK` status constitute live-authentication evidence.
