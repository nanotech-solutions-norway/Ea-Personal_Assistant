#!/usr/bin/env python3
"""Offline-only, fail-closed GitHub Environment Secrets wiring preflight.

This program never connects to Bring, Azure or GitHub APIs. It never prints,
persists, exports, returns or logs any secret value or customer identifier.
It is NOT a runtime Bring credential resolver and grants no tenant authority.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from urllib.parse import urlsplit

REQUIRED = ("BRING_API_UID", "BRING_API_KEY", "BRING_CLIENT_URL")
FORBIDDEN_TRUE = (
    "EA_BRING_PRODUCTION_SYNC_ENABLED",
    "EA_BRING_PROVIDER_CALLS_ENABLED",
    "EA_LIVE_PROVIDER_SYNC_ENABLED",
    "EA_LEVEL_2B_ENABLED",
)
ALLOWED_SOURCE = "github_actions_environment"
TRUE_VALUES = frozenset({"1", "true", "yes", "on"})


def _header_ok(value: object) -> bool:
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 1024
        and bool(value.strip())
        and all(32 <= ord(char) < 127 for char in value)
    )


def _client_url_ok(value: object) -> bool:
    if not _header_ok(value):
        return False
    try:
        parts = urlsplit(value)
        return (
            parts.scheme == "https"
            and bool(parts.hostname)
            and parts.username is None
            and parts.password is None
            and not parts.query
            and not parts.fragment
            and parts.port in (None, 443)
        )
    except (TypeError, ValueError):
        return False


def assess(values: Mapping[str, str]) -> str:
    """Fixed status code only; returns no user input, secret, URL, or exception."""
    if values.get("EA_STAGING_CREDENTIAL_SOURCE") != ALLOWED_SOURCE:
        return "BLOCKED_WRONG_CREDENTIAL_SOURCE"
    if values.get("EA_STAGING_DATA_SCOPE") != "synthetic_only":
        return "BLOCKED_NON_SYNTHETIC_SCOPE"
    if any(str(values.get(name, "")).strip().lower() in TRUE_VALUES
           for name in FORBIDDEN_TRUE):
        return "BLOCKED_LIVE_PROVIDER_OR_PRODUCTION_FLAG"
    if any(not values.get(name) for name in REQUIRED):
        return "BLOCKED_MISSING_GITHUB_ENVIRONMENT_CONFIG"
    if any(not _header_ok(values[name]) for name in REQUIRED):
        return "BLOCKED_INVALID_SECRET_FORMAT"
    if not _client_url_ok(values["BRING_CLIENT_URL"]):
        return "BLOCKED_INVALID_CLIENT_URL"
    return "PASS"


def main() -> int:
    try:
        status = assess(os.environ)
    except Exception:
        status = "BLOCKED_UNEXPECTED_VALIDATION_ERROR"
    print("EA_GITHUB_SECRETS_STAGING_PREFLIGHT=" + status)
    print("BRING_PROVIDER_REQUESTS=NONE")
    print("AZURE_RESOURCE_CREATION=NONE")
    print("PRODUCTION_BRING_SYNC=DISABLED")
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
