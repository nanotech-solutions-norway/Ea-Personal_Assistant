from __future__ import annotations

from typing import Any, Mapping


class GoogleAuthOidcVerifier:
    """Cryptographic Google OIDC verifier backed by google-auth."""

    production_safe = True

    def verify(self, token: str, *, audience: str) -> Mapping[str, Any]:
        if not token or not audience:
            raise ValueError("token and audience are required")
        try:
            from google.auth.transport.requests import Request
            from google.oauth2 import id_token
        except ImportError as exc:
            raise RuntimeError("google-auth with requests transport is required") from exc

        claims = id_token.verify_oauth2_token(token, Request(), audience)
        issuer = claims.get("iss")
        if issuer not in {"accounts.google.com", "https://accounts.google.com"}:
            raise ValueError("unexpected Google token issuer")
        return claims
