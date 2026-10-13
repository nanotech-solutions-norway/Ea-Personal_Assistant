"""One-shot, read-only validation of an operator-authorized real Bring shipment.

IMPORTANT: Only non-identifying result codes are emitted. Do not print or
persist request URLs, headers, account identifiers, shipment IDs, API responses,
dates, recipient/sender details, or exception bodies.
"""

import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from check_customer_info import RejectRedirects, valid_client_url

BASE_URL = "https://api.bring.com/tracking/api/v2/tracking.json"
MAX_BYTES = 1_000_000
REQUIRED = (
    "BRING_API_UID",
    "BRING_API_KEY",
    "BRING_CLIENT_URL",
    "BRING_REAL_TRACKING_NUMBER",
    "BRING_EXPECTED_CUSTOMER_NUMBER",
)
CUSTOMER_FIELDS = (
    "senderCustomerMasterNumber",
    "senderCustomerNumber",
    "recipientCustomerMasterNumber",
    "recipientCustomerNumber",
)


def diagnose_real_shipment(payload: bytes, requested: str, expected_customer: str):
    """Return only non-identifying diagnostic labels.

    A valid tracking response does not prove that the authenticated Mybring
    user or its company owns the shipment. The tracking status and account
    binding are separate, independently evaluated acceptance gates.
    """
    failed = lambda label: (label, "NOT_VERIFIED", "NOT_ASSESSED", "UNKNOWN")
    response = json.loads(payload)
    if not isinstance(response, dict) or str(response.get("apiVersion")) != "2":
        return failed("INVALID_RESPONSE")
    consignments = response.get("consignmentSet")
    if not isinstance(consignments, list) or not consignments:
        return failed("NOT_FOUND")
    if any(not isinstance(item, dict) or item.get("error") for item in consignments):
        return failed("API_ERROR")

    found = []
    for consignment in consignments:
        packages = consignment.get("packageSet")
        if not isinstance(packages, list) or any(not isinstance(p, dict) for p in packages):
            return failed("INVALID_RESPONSE")
        exact_packages = [p for p in packages if p.get("packageNumber") == requested]
        selected = packages if consignment.get("consignmentId") == requested else exact_packages
        if selected:
            found.append((consignment, selected))

    if not found:
        return failed("NOT_FOUND")
    if len(found) != 1:
        return failed("AMBIGUOUS_MATCH")

    consignment, selected_packages = found[0]
    bools = [consignment.get("isLoggedInSenderOrReceiver")]
    bools.extend(p.get("isLoggedInSenderOrReceiver") for p in selected_packages)
    relationship = (
        "LOGGED_IN_PARTY" if True in bools
        else "NOT_INDICATED" if False in bools
        else "UNKNOWN"
    )

    has_event_status = False
    for package in selected_packages:
        events = package.get("eventSet")
        if not isinstance(events, list):
            return ("STATUS_NOT_VERIFIED", "NOT_VERIFIED", "NOT_ASSESSED", relationship)
        if any(
            isinstance(event, dict)
            and isinstance(event.get("status"), str)
            and re.fullmatch(r"[A-Z_]{3,40}", event["status"])
            for event in events
        ):
            has_event_status = True
    if not has_event_status:
        return ("STATUS_NOT_VERIFIED", "NOT_VERIFIED", "NOT_ASSESSED", relationship)

    # The Tracking v2 examples include these fields but often leave them blank.
    # Do not treat a public tracking response or an API login relationship flag
    # as proof that a specific company customer/master number matches.
    supplied = [
        str(consignment.get(field)).strip()
        for field in CUSTOMER_FIELDS
        if consignment.get(field) not in (None, "")
    ]
    if expected_customer in supplied:
        return ("PASS", "PASS", "CUSTOMER_ID_MATCH", relationship)
    if supplied:
        detail = "NONMATCHING_ACCOUNT_FIELD"
    elif any(field in consignment for field in CUSTOMER_FIELDS):
        detail = "ACCOUNT_FIELDS_EMPTY"
    else:
        detail = "ACCOUNT_FIELDS_ABSENT"
    return ("TENANT_UNVERIFIED", "PASS", detail, relationship)


def validate_real_shipment(payload: bytes, requested: str, expected_customer: str) -> str:
    """Compatibility wrapper: retain the strict final PASS/fail contract."""
    return diagnose_real_shipment(payload, requested, expected_customer)[0]


def valid_input(tracking: str, expected_customer: str) -> bool:
    return bool(
        re.fullmatch(r"[A-Za-z0-9-]{7,80}", tracking)
        and not tracking.upper().startswith("TEST")
        and re.fullmatch(r"[0-9]{6,20}", expected_customer)
    )


def main() -> int:
    if any(not os.environ.get(k) for k in REQUIRED):
        print("BRING_REAL_CHECK=BLOCKED_MISSING_CONFIG")
        return 2
    if not valid_client_url(os.environ["BRING_CLIENT_URL"]) or not valid_input(
        os.environ["BRING_REAL_TRACKING_NUMBER"], os.environ["BRING_EXPECTED_CUSTOMER_NUMBER"]
    ):
        print("BRING_REAL_CHECK=BLOCKED_INVALID_CONFIG")
        return 2
    if any(
        not all(32 <= ord(ch) < 127 for ch in os.environ[key])
        for key in REQUIRED
    ):
        print("BRING_REAL_CHECK=BLOCKED_INVALID_HEADER_VALUE")
        return 2

    tracking = os.environ["BRING_REAL_TRACKING_NUMBER"]
    request = Request(
        BASE_URL + "?" + urlencode({"q": tracking}),
        method="GET",
        headers={
            "Accept": "application/json",
            "X-Mybring-API-Uid": os.environ["BRING_API_UID"],
            "X-Mybring-API-Key": os.environ["BRING_API_KEY"],
            "X-Bring-Client-URL": os.environ["BRING_CLIENT_URL"],
        },
    )
    # Disable ambient proxy variables and reject redirects that might forward
    # the authorization headers to another host.
    opener = build_opener(ProxyHandler({}), RejectRedirects())
    try:
        with opener.open(request, timeout=15) as response:
            if response.status != 200:
                print("BRING_REAL_CHECK=UNEXPECTED_HTTP_STATUS")
                return 3
            payload = response.read(MAX_BYTES + 1)
    except HTTPError as err:
        print(f"BRING_REAL_CHECK=HTTP_{err.code}")
        return 3
    except (URLError, TimeoutError, OSError):
        print("BRING_REAL_CHECK=NETWORK_ERROR")
        return 3
    except Exception:
        print("BRING_REAL_CHECK=UNEXPECTED_ERROR")
        return 3

    if len(payload) > MAX_BYTES:
        print("BRING_REAL_CHECK=RESPONSE_TOO_LARGE")
        return 3
    try:
        status, tracking_result, tenant_detail, relationship = diagnose_real_shipment(
            payload,
            tracking,
            os.environ["BRING_EXPECTED_CUSTOMER_NUMBER"],
        )
    except (UnicodeError, ValueError, TypeError):
        status, tracking_result, tenant_detail, relationship = (
            "INVALID_RESPONSE", "NOT_VERIFIED", "NOT_ASSESSED", "UNKNOWN"
        )

    # Only enumerated labels; never print actual tracking numbers, customer IDs,
    # status descriptions, event dates/locations, user details or response data.
    print("BRING_REAL_TRACKING=" + tracking_result)
    print("BRING_TENANT_DIAGNOSTIC=" + tenant_detail)
    print("BRING_ACCOUNT_RELATIONSHIP_HINT=" + relationship)
    print("BRING_REAL_CHECK=" + status)
    return 0 if status == "PASS" else 4


if __name__ == "__main__":
    sys.exit(main())
