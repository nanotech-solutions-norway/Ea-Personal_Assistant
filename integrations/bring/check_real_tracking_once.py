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


def validate_real_shipment(payload: bytes, requested: str, expected_customer: str) -> str:
    """Validate exact shipment identity, company account association and event.

    A public tracking response can succeed for someone else's package.
    Authentication alone is not tenancy proof. We require a returned company
    customer number to equal the independently configured operator-owned number.
    """
    response = json.loads(payload)
    if not isinstance(response, dict) or str(response.get("apiVersion")) != "2":
        return "INVALID_RESPONSE"
    consignments = response.get("consignmentSet")
    if not isinstance(consignments, list) or not consignments:
        return "NOT_FOUND"
    if any(not isinstance(item, dict) or item.get("error") for item in consignments):
        return "API_ERROR"

    found = []
    for consignment in consignments:
        packages = consignment.get("packageSet")
        if not isinstance(packages, list):
            return "INVALID_RESPONSE"
        package_matches = [
            package for package in packages
            if isinstance(package, dict) and package.get("packageNumber") == requested
        ]
        if consignment.get("consignmentId") == requested:
            selected = [p for p in packages if isinstance(p, dict)]
        else:
            selected = package_matches
        if selected:
            found.append((consignment, selected))
    if len(found) != 1:
        return "NOT_FOUND" if not found else "AMBIGUOUS_MATCH"

    consignment, selected_packages = found[0]
    if not any(str(consignment.get(field) or "") == expected_customer for field in CUSTOMER_FIELDS):
        return "TENANT_UNVERIFIED"

    if not selected_packages:
        return "STATUS_NOT_VERIFIED"
    has_event_status = False
    for package in selected_packages:
        events = package.get("eventSet")
        if not isinstance(events, list):
            return "STATUS_NOT_VERIFIED"
        if any(
            isinstance(event, dict)
            and isinstance(event.get("status"), str)
            and re.fullmatch(r"[A-Z_]{3,40}", event["status"])
            for event in events
        ):
            has_event_status = True
    return "PASS" if has_event_status else "STATUS_NOT_VERIFIED"


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
        status = validate_real_shipment(
            payload,
            tracking,
            os.environ["BRING_EXPECTED_CUSTOMER_NUMBER"],
        )
    except (UnicodeError, ValueError, TypeError):
        status = "INVALID_RESPONSE"

    print("BRING_REAL_CHECK=" + status)
    return 0 if status == "PASS" else 4


if __name__ == "__main__":
    sys.exit(main())
