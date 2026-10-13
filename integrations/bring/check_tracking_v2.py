"""EA Bring read-only Tracking v2 smoke test using a synthetic package only.

No customer numbers, real tracking numbers, customer data, response bodies,
secrets, or authentication headers are printed or stored.
"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

from check_customer_info import RejectRedirects, valid_client_url

TEST_TRACKING_NUMBER = "TESTPACKAGEDELIVERED"  # Official Bring test identifier.
TRACKING_URL = (
    "https://api.bring.com/tracking/api/v2/tracking.json"
    "?q=TESTPACKAGEDELIVERED"
)
REQUIRED = ("BRING_API_UID", "BRING_API_KEY", "BRING_CLIENT_URL")
MAX_BYTES = 1_000_000


def validate_synthetic_delivery(payload: bytes) -> str:
    """Return a status code, never customer content, for a v2 tracking response."""
    response = json.loads(payload)
    if not isinstance(response, dict) or str(response.get("apiVersion")) != "2":
        return "INVALID_RESPONSE"

    consignments = response.get("consignmentSet")
    if not isinstance(consignments, list) or not consignments:
        return "INVALID_RESPONSE"

    # Bring can report API errors inside HTTP 200 consignmentSet objects.
    if any(not isinstance(item, dict) or item.get("error") for item in consignments):
        return "API_ERROR"

    for consignment in consignments:
        packages = consignment.get("packageSet")
        if not isinstance(packages, list):
            continue
        for package in packages:
            if not isinstance(package, dict):
                continue
            if package.get("packageNumber") != TEST_TRACKING_NUMBER:
                continue
            events = package.get("eventSet")
            if not isinstance(events, list):
                return "INVALID_RESPONSE"
            if any(
                isinstance(event, dict) and event.get("status") == "DELIVERED"
                for event in events
            ):
                return "PASS"
            return "TEST_STATUS_MISMATCH"

    return "TEST_PACKAGE_MISSING"


def main() -> int:
    missing = [key for key in REQUIRED if not os.environ.get(key)]
    if missing:
        print("BRING_TRACKING_CHECK=BLOCKED_MISSING_CONFIG")
        return 2

    if not valid_client_url(os.environ["BRING_CLIENT_URL"]):
        print("BRING_TRACKING_CHECK=BLOCKED_INVALID_CLIENT_URL")
        return 2

    if any(
        not all(32 <= ord(character) < 127 for character in os.environ[key])
        for key in REQUIRED
    ):
        print("BRING_TRACKING_CHECK=BLOCKED_INVALID_HEADER_VALUE")
        return 2

    request = Request(
        TRACKING_URL,
        method="GET",
        headers={
            "Accept": "application/json",
            "X-Mybring-API-Uid": os.environ["BRING_API_UID"],
            "X-Mybring-API-Key": os.environ["BRING_API_KEY"],
            "X-Bring-Client-URL": os.environ["BRING_CLIENT_URL"],
        },
    )
    try:
        with build_opener(RejectRedirects()).open(request, timeout=15) as response:
            if response.status != 200:
                print("BRING_TRACKING_CHECK=UNEXPECTED_HTTP_STATUS")
                return 3
            payload = response.read(MAX_BYTES + 1)
    except HTTPError as error:
        print(f"BRING_TRACKING_CHECK=HTTP_{error.code}")
        return 3
    except (URLError, TimeoutError, OSError):
        print("BRING_TRACKING_CHECK=NETWORK_ERROR")
        return 3
    except Exception:
        print("BRING_TRACKING_CHECK=UNEXPECTED_ERROR")
        return 3

    if len(payload) > MAX_BYTES:
        print("BRING_TRACKING_CHECK=RESPONSE_TOO_LARGE")
        return 3

    try:
        status = validate_synthetic_delivery(payload)
    except (ValueError, UnicodeError):
        status = "INVALID_RESPONSE"

    print(f"BRING_TRACKING_CHECK={status}")
    return 0 if status == "PASS" else 4


if __name__ == "__main__":
    sys.exit(main())
