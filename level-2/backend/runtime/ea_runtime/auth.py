from __future__ import annotations

from typing import Protocol


class RequestAuthenticator(Protocol):
    def authorize(self, environ: dict, *, source: str) -> bool:
        """Return True only for an authenticated delivery from the expected source."""


class AllowAllTestAuthenticator:
    """Test-only authenticator. Never production-authorized."""

    production_safe = False

    def authorize(self, environ: dict, *, source: str) -> bool:
        return True
