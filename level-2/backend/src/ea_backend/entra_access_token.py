"""Single-tenant Microsoft Entra v2 *access-token* verifier for EA Bring reads.

Never accept ID tokens, Graph access tokens, user-chosen issuers/JWKS URLs,
unsigned JWTs or client-provided role/tenant assertions as authorization.
No secret values or token/claim contents are logged.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from uuid import UUID

from .bring_tenant_gateway import VerifiedIdentity, READ_SCOPE


def _guid(value: str) -> str:
    """Require a canonical UUID to prevent arbitrary authority URLs."""
    if not isinstance(value, str):
        raise ValueError("invalid configured GUID")
    parsed = UUID(value)
    if str(parsed) != value.lower() or len(value) != 36:
        raise ValueError("invalid configured GUID")
    return str(parsed)


class EntraAccessTokenVerifier:
    """Cryptographically validate delegated tokens to the EA application API.

    - Tenant-specific, pinned Entra v2 authority and signing JWKS.
    - Only RS256: no alg negotiation from caller tokens.
    - Exact issuer, audience, tenant ID, calling client app ID and OID.
    - Requires delegated scp=bring.tracking.read; app-only/ID tokens denied.
    - No token or claim values logged on validation errors.
    - PyJWT JWKS cache can refresh on unrecognized signing kid.
    """

    production_safe = True

    def __init__(
        self,
        *,
        tenant_id: str,
        api_audience: str,
        authorized_client_ids: tuple[str, ...],
        required_scope: str = READ_SCOPE,
    ):
        self.tenant_id = _guid(tenant_id)
        if not isinstance(api_audience, str) or not api_audience.strip():
            raise ValueError("API audience is mandatory")
        if not isinstance(required_scope, str) or required_scope != READ_SCOPE:
            raise ValueError("Bring delegated read scope is mandatory")
        if not authorized_client_ids or not isinstance(authorized_client_ids, tuple):
            raise ValueError("calling client allowlist is mandatory")
        self.allowed_clients = frozenset(_guid(x) for x in authorized_client_ids)
        self.audience = api_audience
        self.required_scope = required_scope
        self.issuer = f"https://login.microsoftonline.com/{self.tenant_id}/v2.0"
        self.jwks_url = (
            f"https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys"
        )
        try:
            from jwt import PyJWKClient
        except ImportError as exc:
            raise RuntimeError("PyJWT[crypto] must be installed for Entra verification") from exc
        self._jwks = PyJWKClient(
            self.jwks_url, cache_jwk_set=True, lifespan=3600, timeout=5
        )

    def verify(self, bearer_token: str, *, expected_audience: str) -> VerifiedIdentity:
        if (
            not isinstance(bearer_token, str)
            or not 1 <= len(bearer_token) <= 12000
            or expected_audience != self.audience
        ):
            raise ValueError("unverified access token")
        try:
            import jwt

            header = jwt.get_unverified_header(bearer_token)
            if (
                not isinstance(header, dict)
                or header.get("alg") != "RS256"
                or not isinstance(header.get("kid"), str)
                or not 1 <= len(header["kid"]) <= 256
            ):
                raise ValueError("unsupported token header")

            signing_key = self._jwks.get_signing_key_from_jwt(bearer_token)
            # Microsoft documents key-level issuer for v2 key sets. When
            # provided, it must also match this *tenant-specific* issuer.
            key_issuer = getattr(signing_key, "_jwk_data", {}).get("issuer")
            if key_issuer is not None and key_issuer.replace(
                "{tenantid}", self.tenant_id
            ) != self.issuer:
                raise ValueError("unexpected signing-key issuer")
            if signing_key.key_type != "RSA":
                raise ValueError("non-RSA signing key")

            claims = jwt.decode(
                bearer_token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience,
                options={
                    "require": [
                        "iss", "aud", "exp", "nbf", "iat", "tid",
                        "oid", "azp", "ver", "scp", "sub"
                    ],
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": True,
                    "verify_iss": True,
                },
                leeway=0,
            )
            if claims.get("ver") != "2.0":
                raise ValueError("unexpected token version")
            if _guid(claims.get("tid", "")) != self.tenant_id:
                raise ValueError("wrong token tenant")
            oid = _guid(claims.get("oid", ""))
            if _guid(claims.get("azp", "")) not in self.allowed_clients:
                raise ValueError("calling application not allowed")
            scopes = claims.get("scp")
            if not isinstance(scopes, str) or self.required_scope not in scopes.split():
                raise ValueError("delegated read scope missing")
            if not isinstance(claims.get("sub"), str) or not claims["sub"]:
                raise ValueError("subject missing")
            if type(claims.get("exp")) not in (int, float):
                raise ValueError("expiry claim invalid")
            # Use tenant-scoped OID, not mutable email or an untrusted header.
            return VerifiedIdentity(
                issuer=self.issuer,
                subject=oid,
                audience=self.audience,
                expires_at=datetime.fromtimestamp(claims["exp"], tz=timezone.utc),
            )
        except Exception as exc:
            # Do not propagate provider/HTTP/JWT exception text (may contain
            # source metadata). Callers receive one sanitized denial.
            raise ValueError("unverified access token") from None
