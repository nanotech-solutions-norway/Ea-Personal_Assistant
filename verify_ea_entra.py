"""Local-only interactive Entra validation (never run in hosted GitHub CI).

Supply three public application identifiers through shell environment variables.
This script never prints access tokens, user claims, IDs or authentication errors.
No environment-specific IDs are committed to this public repository.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from uuid import UUID

ENV_NAMES = (
    "EA_ENTRA_TENANT_ID",
    "EA_API_CLIENT_ID",
    "EA_AUTHORIZED_CLIENT_ID",
)


def _validated_guid(value: str) -> str:
    if not isinstance(value, str) or len(value) != 36:
        raise ValueError("invalid application identifier")
    try:
        parsed = UUID(value)
    except (ValueError, TypeError, AttributeError):
        raise ValueError("invalid application identifier") from None
    if str(parsed) != value.lower():
        raise ValueError("invalid application identifier")
    return str(parsed)


def read_configuration(values: dict[str, str]) -> tuple[str, str, str]:
    """Validate only the configuration shape; never display the values."""
    if any(not isinstance(values.get(key), str) or not values[key].strip() for key in ENV_NAMES):
        raise ValueError("missing Entra configuration")
    return tuple(_validated_guid(values[key].strip()) for key in ENV_NAMES)


def main() -> int:
    try:
        tenant_id, api_client_id, desktop_client_id = read_configuration(dict(os.environ))
    except ValueError:
        print("EA_ENTRA_VALIDATION=BLOCKED_INVALID_CONFIG")
        return 2

    try:
        import msal
        sys.path.insert(0, str((Path(__file__).resolve().parent / "level-2/backend/src").resolve()))
        from ea_backend.entra_access_token import EntraAccessTokenVerifier
    except ImportError:
        print("EA_ENTRA_VALIDATION=BLOCKED_MISSING_DEPENDENCIES")
        return 2

    # Entra interactive sign-in occurs ONLY on the operator's local computer.
    try:
        app = msal.PublicClientApplication(
            client_id=desktop_client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}",
        )
        scope = f"api://{api_client_id}/bring.tracking.read"
        result = app.acquire_token_interactive(scopes=[scope])
    except Exception:
        print("EA_ENTRA_VALIDATION=TOKEN_ISSUANCE_FAILED")
        return 3

    if not isinstance(result, dict) or not result.get("access_token"):
        print("EA_ENTRA_VALIDATION=TOKEN_ISSUANCE_FAILED")
        return 3

    try:
        verifier = EntraAccessTokenVerifier(
            tenant_id=tenant_id,
            api_audience=api_client_id,
            authorized_client_ids=(desktop_client_id,),
        )
        verifier.verify(
            result["access_token"],
            expected_audience=api_client_id,
        )
    except Exception:
        print("EA_ENTRA_VALIDATION=TOKEN_REJECTED")
        return 4

    print("EA_ENTRA_VALIDATION=PASS")
    print("ISSUER=VERIFIED")
    print("AUDIENCE=VERIFIED")
    print("SIGNATURE_AND_SCOPE=VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
