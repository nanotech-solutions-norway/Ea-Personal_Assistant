#!/usr/bin/env python3
"""Private subscription-specific ACA price-sheet read (public-safe summary ONLY).

Requires prior protected GitHub OIDC Azure/login using the immutable Reader.
HTTP GET only. Azure errors, tokens, subscription IDs, offer data, invoices,
meter metadata beyond allowlisted units and raw JSON are never logged.
No deployment, grant changes or billing export is performed.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

UUID = re.compile(r"^[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")
ARM_HOST = "management.azure.com"
API_VERSION = "2024-08-01"
MAX_PAGES = 8
METER_IDS = {
    "ACA_ACTIVE_VCPU_SECOND": "0426badc-b719-5201-b141-b2d5c4943b7d",
    "ACA_ACTIVE_GIB_SECOND": "3ba64b1c-cb46-5ee0-b086-a68736392ac0",
    "ACA_HTTP_REQUESTS_MILLION": "b110d175-46b6-5bbc-adde-cf3438ed87f0",
}
# These canonical public meter GUIDs are previously supported by retail evidence.
UNIT_EXPECTED = {
    "ACA_ACTIVE_VCPU_SECOND": {"1 Second"},
    "ACA_ACTIVE_GIB_SECOND": {"1 GiB Second"},
    "ACA_HTTP_REQUESTS_MILLION": {"1M"},
}


def safe_next_url(url: str, sub: str) -> bool:
    if not isinstance(url, str) or len(url) > 4096:
        return False
    p = urlsplit(url)
    expected = f"/subscriptions/{sub.lower()}/providers/microsoft.consumption/pricesheets/default"
    return (
        p.scheme == "https"
        and p.hostname == ARM_HOST
        and p.port is None
        and p.username is None
        and p.password is None
        and p.path.lower() == expected
        and p.query.lower().count("api-version=") == 1
        and p.fragment == ""
    )


def normalize_row(row: object) -> tuple[str, str, str, str] | None:
    if not isinstance(row, dict):
        return None
    meter_id = str(row.get("meterId", "")).lower()
    name = next((label for label, key in METER_IDS.items() if meter_id == key), None)
    if name is None or row.get("unitOfMeasure") not in UNIT_EXPECTED[name]:
        return None
    currency = row.get("currencyCode")
    if currency != "EUR":
        return None
    unit_price = row.get("unitPrice")
    if isinstance(unit_price, bool) or not isinstance(unit_price, (int, float, str)):
        return None
    try:
        rate = Decimal(str(unit_price))
    except (InvalidOperation, ValueError):
        return None
    if not rate.is_finite() or rate < 0:
        return None
    # The free allowance is shared across the subscription. IncludedQuantity
    # in a price sheet is not remaining current-month usage.
    included = row.get("includedQuantity")
    valid_included = included is not None and not isinstance(included, bool)
    try:
        incl = str(Decimal(str(included))) if valid_included else "UNKNOWN"
    except (InvalidOperation, ValueError):
        incl = "UNKNOWN"
    return name, str(rate), str(row["unitOfMeasure"]), incl


def extract_allowlisted_prices(pages: list[object]) -> dict:
    rates: dict[str, set[tuple[str, str, str]]] = {k: set() for k in METER_IDS}
    malformed = False
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("properties"), dict):
            malformed = True
            break
        items = page["properties"].get("pricesheets")
        if not isinstance(items, list):
            malformed = True
            break
        for row in items:
            entry = normalize_row(row)
            if entry:
                name, price, unit, included = entry
                rates[name].add((price, unit, included))
    if malformed:
        return {"status": "MALFORMED_RESPONSE", "rates": {}}
    summary = {}
    for key, found in rates.items():
        if not found:
            summary[key] = {"status": "NOT_RETURNED"}
        elif len(found) == 1:
            rate, unit, included = next(iter(found))
            summary[key] = {
                "status": "ACCOUNT_PRICE_CANDIDATE_ZERO_NOT_PROOF_FREE" if Decimal(rate) == 0 else "ACCOUNT_PRICE_CANDIDATE",
                "eur_per_unit": rate,
                "unit": unit,
                "price_sheet_included_quantity_NOT_REMAINING_BALANCE": included,
            }
        else:
            summary[key] = {"status": "AMBIGUOUS_MULTIPLE_PRICE_SHEET_TIERS", "candidate_count": len(found)}
    return {"status": "ACCOUNT_PRICE_SHEET_READ_BUT_NOT_DEPLOYMENT_APPROVAL", "rates": summary}


# Only permit these fixed classifications in public GitHub logs. Azure CLI
# stderr must NEVER be included in a diagnostic, because it may contain
# account IDs, resource identifiers, request URIs or tenant-specific text.
AZURE_FAILURES = {
    "AuthorizationFailed": "AUTHORIZATION_FAILED",
    "Forbidden": "FORBIDDEN",
    "Unauthorized": "UNAUTHORIZED",
    "InvalidAuthenticationToken": "AUTHENTICATION_TOKEN_INVALID",
    "ResourceNotFound": "RESOURCE_NOT_FOUND",
    "NotFound": "NOT_FOUND",
    "SubscriptionNotFound": "SUBSCRIPTION_NOT_FOUND",
    "NoRegisteredProviderFound": "PROVIDER_NOT_AVAILABLE",
    "InvalidApiVersionParameter": "UNSUPPORTED_API_VERSION",
    "InvalidResourceType": "UNSUPPORTED_RESOURCE_TYPE",
    "FeatureNotSupported": "FEATURE_NOT_SUPPORTED",
    "BadRequest": "BAD_REQUEST",
    "MethodNotAllowed": "METHOD_NOT_ALLOWED",
}


def classify_azure_cli_failure(stderr: object) -> str:
    """Allowlisted error code ONLY, not raw Azure response or exception."""
    if not isinstance(stderr, str):
        return "UNAVAILABLE_OR_UNAUTHORIZED"
    code = re.search(r"\(([A-Za-z]+)\)", stderr[:32768])
    if code and code.group(1) in AZURE_FAILURES:
        return AZURE_FAILURES[code.group(1)]
    # Some versions of Azure CLI emit HTTP status without a service code.
    if re.search(r"\b(?:HTTP(?: Error)?|StatusCode)\s*[:= ]\s*403\b", stderr):
        return "HTTP_403"
    if re.search(r"\b(?:HTTP(?: Error)?|StatusCode)\s*[:= ]\s*404\b", stderr):
        return "HTTP_404"
    if re.search(r"\b(?:HTTP(?: Error)?|StatusCode)\s*[:= ]\s*400\b", stderr):
        return "HTTP_400"
    return "UNAVAILABLE_OR_UNAUTHORIZED"


def read_page(url: str) -> dict | None:
    try:
        r = subprocess.run(
            ["az", "rest", "--method", "get", "--url", url,
             "--only-show-errors", "--output", "json"],
            capture_output=True, text=True, timeout=90, check=False,
        )
        if r.returncode:
            return {"_ea_safe_error": classify_azure_cli_failure(r.stderr)}
        return json.loads(r.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def read_private_pricesheet(sub: str, fetcher=read_page) -> dict:
    if not UUID.fullmatch(sub):
        return {"status": "BLOCKED_INVALID_SUBSCRIPTION_CONFIG", "rates": {}}
    base = (f"https://{ARM_HOST}/subscriptions/{sub}"
            f"/providers/Microsoft.Consumption/pricesheets/default")
    url = base + f"?api-version={API_VERSION}&%24expand=meterDetails&%24top=1000"
    pages = []
    for _ in range(MAX_PAGES):
        if not safe_next_url(url, sub):
            return {"status": "BLOCKED_UNTRUSTED_NEXT_LINK", "rates": {}}
        page = fetcher(url)
        if not isinstance(page, dict):
            return {"status": "UNAVAILABLE_OR_UNAUTHORIZED", "rates": {}}
        if "_ea_safe_error" in page:
            code = page["_ea_safe_error"]
            if code not in set(AZURE_FAILURES.values()) | {"HTTP_403", "HTTP_404", "HTTP_400", "UNAVAILABLE_OR_UNAUTHORIZED"}:
                code = "UNAVAILABLE_OR_UNAUTHORIZED"
            return {"status": code, "rates": {}}
        pages.append(page)
        props = page.get("properties")
        if not isinstance(props, dict):
            return {"status": "MALFORMED_RESPONSE", "rates": {}}
        next_link = props.get("nextLink")
        if not next_link:
            result = extract_allowlisted_prices(pages)
            result["pages_read"] = len(pages)
            return result
        url = next_link
    return {"status": "INCOMPLETE_PAGINATION", "rates": {}}


def main() -> int:
    sub = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
    result = read_private_pricesheet(sub)
    # Entire public stdout contains only allowlisted service rates and statuses.
    print("EA_ACA_SUBSCRIPTION_BILLING_READ=" + result["status"])
    for name, item in result.get("rates", {}).items():
        print(name + "=" + json.dumps(item, sort_keys=True))
    if "pages_read" in result:
        print("PAGES_READ=" + str(result["pages_read"]))
    print("SUBSCRIPTION_FREE_ALLOWANCE_REMAINING=NOT_VERIFIED")
    print("AZURE_DEPLOYMENT_AUTHORIZED=FALSE")
    print("BRING_PRODUCTION_SYNC_ENABLED=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
