from __future__ import annotations

import hmac
from typing import Any, Mapping, Protocol


class RequestAuthenticator(Protocol):
    production_safe: bool

    def authorize(self, environ: dict, *, source: str) -> bool:
        """Return True only for an authenticated delivery from the expected source."""


class OidcVerifier(Protocol):
    production_safe: bool

    def verify(self, token: str, *, audience: str) -> Mapping[str, Any]:
        """Verify token signature/issuer/audience and return trusted claims."""


class AllowAllTestAuthenticator:
    """Test-only authenticator. Never production-authorized."""

    production_safe = False

    def authorize(self, environ: dict, *, source: str) -> bool:
        return True


class GoogleDeliveryAuthenticator:
    """Source-specific Google delivery authenticator.

    Gmail Pub/Sub push uses a verified OIDC identity.
    Calendar notifications use the opaque X-Goog-Channel-Token configured
    when the watch channel is created.
    """

    def __init__(
        self,
        *,
        oidc_verifier: OidcVerifier,
        gmail_audience: str,
        gmail_service_account_email: str,
        calendar_channel_token: str,
    ) -> None:
        self._verifier = oidc_verifier
        self._gmail_audience = gmail_audience.strip()
        self._gmail_service_account_email = gmail_service_account_email.strip().lower()
        self._calendar_channel_token = calendar_channel_token
        self.production_safe = bool(
            getattr(oidc_verifier, "production_safe", False)
            and self._gmail_audience
            and self._gmail_service_account_email
            and self._calendar_channel_token
        )

    def authorize(self, environ: dict, *, source: str) -> bool:
        if not self.production_safe:
            return False

        if source == "gmail":
            header = str(environ.get("HTTP_AUTHORIZATION", ""))
            if not header.startswith("Bearer "):
                return False
            token = header[7:].strip()
            if not token:
                return False
            try:
                claims = self._verifier.verify(token, audience=self._gmail_audience)
            except Exception:
                return False
            email = str(claims.get("email", "")).lower()
            verified = claims.get("email_verified")
            return bool(verified is True and hmac.compare_digest(email, self._gmail_service_account_email))

        if source == "google_calendar":
            supplied = str(environ.get("HTTP_X_GOOG_CHANNEL_TOKEN", ""))
            return bool(
                supplied
                and hmac.compare_digest(supplied, self._calendar_channel_token)
            )

        return False
