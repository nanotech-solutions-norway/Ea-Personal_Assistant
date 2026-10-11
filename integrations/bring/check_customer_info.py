"""Read-only, single-request Mybring connection check. No credential or customer logging."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

API_URL = "https://api.bring.com/customer-info/customers"
REQUIRED = ("BRING_API_UID", "BRING_API_KEY", "BRING_CLIENT_URL")
MAX_RESPONSE_BYTES = 1_000_000


class RejectRedirects(HTTPRedirectHandler):
    """Never forward secret-bearing headers to a redirect destination."""

    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def valid_client_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return (
            parsed.scheme == "https"
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and all(32 <= ord(character) < 127 for character in value)
        )
    except ValueError:
        return False


def customer_count(payload: bytes) -> int:
    """Validate shape without logging, exporting, or persisting account data."""
    doc = json.loads(payload)
    if not isinstance(doc, dict) or not isinstance(doc.get("customers"), list):
        raise ValueError("Customer Info response has unexpected shape")
    if not all(isinstance(customer, dict) for customer in doc["customers"]):
        raise ValueError("Customer Info response contains an unexpected item")
    return len(doc["customers"])


def main() -> int:
    missing = [key for key in REQUIRED if not os.environ.get(key)]
    if missing:
        print("BRING_CHECK=BLOCKED_MISSING_CONFIG (" + ",".join(missing) + ")")
        return 2
    if not valid_client_url(os.environ["BRING_CLIENT_URL"]):
        print("BRING_CHECK=BLOCKED_INVALID_CLIENT_URL")
        return 2

    if any(not all(32 <= ord(character) < 127 for character in os.environ[key]) for key in REQUIRED):
        print("BRING_CHECK=BLOCKED_INVALID_HEADER_VALUE")
        return 2

    request = Request(
        API_URL,
        method="GET",
        headers={
            "Accept": "application/json",
            "X-Mybring-API-Uid": os.environ["BRING_API_UID"],
            "X-Mybring-API-Key": os.environ["BRING_API_KEY"],
            "X-Bring-Client-URL": os.environ["BRING_CLIENT_URL"],
        },
    )
    opener = build_opener(RejectRedirects())
    try:
        with opener.open(request, timeout=15) as response:
            if response.status != 200:
                print("BRING_CHECK=UNEXPECTED_HTTP_STATUS")
                return 3
            payload = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as error:
        # HTTP status only. Never print response bodies or request headers.
        print(f"BRING_CHECK=HTTP_{error.code}")
        return 3
    except (URLError, TimeoutError, OSError):
        print("BRING_CHECK=NETWORK_ERROR")
        return 3
    except Exception:
        print("BRING_CHECK=UNEXPECTED_ERROR")
        return 3

    if len(payload) > MAX_RESPONSE_BYTES:
        print("BRING_CHECK=RESPONSE_TOO_LARGE")
        return 3
    try:
        count = customer_count(payload)
    except (ValueError, UnicodeDecodeError):
        print("BRING_CHECK=INVALID_RESPONSE")
        return 3

    if count == 0:
        print("BRING_CHECK=AUTHENTICATED_NO_CUSTOMER_ACCESS")
        return 4

    print("BRING_CHECK=PASS (read-only access confirmed; customer data not logged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
