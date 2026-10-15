"""Bounded, read-only Azure Key Vault Bring credentials adapter.

Not activated in EA runtime. A ScopedTrackingPermit MUST be issued by
authorize_tracking_read after cryptographic identity and protected registry
checks. Never construct a permit from HTTP input, model text or source data.

This module does NOT call Bring or persist credentials.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import urlsplit
from uuid import UUID

from .bring_tenant_gateway import ScopedTrackingPermit


_REF = re.compile(
    r"(https://[a-z0-9][a-z0-9-]{1,22}[a-z0-9]\.vault\.azure\.net)"
    r"/secrets/([A-Za-z0-9-]{1,127})\Z"
)


class BringCredentialUnavailable(RuntimeError):
    """Sanitized failure: never expose secret, tenant, reference, or Azure errors."""

    def __init__(self) -> None:
        super().__init__("BRING_CREDENTIAL_UNAVAILABLE")


@dataclass(frozen=True, repr=False)
class BringCredentialBundle:
    api_uid: str = field(repr=False)
    api_key: str = field(repr=False)
    client_url: str = field(repr=False)


def _valid_header(value: object) -> bool:
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 1024
        and all(32 <= ord(ch) < 127 for ch in value)
    )


def _valid_client_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return bool(
            parsed.scheme == "https"
            and parsed.hostname
            and parsed.username is None
            and parsed.password is None
            and not parsed.query
            and not parsed.fragment
        )
    except (ValueError, TypeError):
        return False


def _parse_bundle(value: object) -> BringCredentialBundle:
    if not isinstance(value, str) or len(value) > 4096:
        raise BringCredentialUnavailable()
    try:
        doc = json.loads(value)
    except (TypeError, ValueError):
        raise BringCredentialUnavailable() from None
    if not isinstance(doc, dict) or set(doc) != {"api_uid", "api_key", "client_url"}:
        raise BringCredentialUnavailable()
    if not all(_valid_header(doc[k]) for k in ("api_uid", "api_key", "client_url")):
        raise BringCredentialUnavailable()
    if not _valid_client_url(doc["client_url"]):
        raise BringCredentialUnavailable()
    return BringCredentialBundle(
        api_uid=doc["api_uid"],
        api_key=doc["api_key"],
        client_url=doc["client_url"],
    )


class ScopedBringVaultResolver:
    """Retrieve exactly one allowlisted secret, only for an authorized permit.

    client_factory(vault_url) must return a trusted object exposing get_secret.
    The permit is an INTERNAL authority object, not a serializable client token.
    """

    def __init__(
        self,
        *,
        approved_vault_urls: frozenset[str],
        client_factory: Callable,
    ) -> None:
        if (
            not isinstance(approved_vault_urls, frozenset)
            or not approved_vault_urls
            or not callable(client_factory)
            or any(not _REF.fullmatch(url + "/secrets/placeholder")
                   for url in approved_vault_urls)
        ):
            raise ValueError("vault resolver is not securely configured")
        self._vaults = approved_vault_urls
        self._client_factory = client_factory

    def resolve(self, permit: ScopedTrackingPermit) -> BringCredentialBundle:
        if (
            not isinstance(permit, ScopedTrackingPermit)
            or permit.read_only is not True
            or not permit.tenant_scope
            or not permit.tracking_reference
            or not isinstance(permit.credential_ref, str)
        ):
            raise BringCredentialUnavailable()
        match = _REF.fullmatch(permit.credential_ref)
        if match is None:
            raise BringCredentialUnavailable()
        vault_url, secret_name = match.groups()
        if vault_url not in self._vaults:
            raise BringCredentialUnavailable()
        try:
            client = self._client_factory(vault_url)
            secret = client.get_secret(secret_name)
            return _parse_bundle(getattr(secret, "value", None))
        except BringCredentialUnavailable:
            raise
        except Exception:
            # Client exceptions sometimes include request URLs; sanitize.
            raise BringCredentialUnavailable() from None


class AzureManagedIdentitySecretClientFactory:
    """Explicit user-assigned managed identity; no CLI/interactive fallbacks.

    Requires azure-identity and azure-keyvault-secrets at deployment.
    Construct from trusted server configuration, NEVER from request headers.
    """

    def __init__(self, *, managed_identity_client_id: str) -> None:
        try:
            parsed = UUID(managed_identity_client_id)
            if str(parsed) != managed_identity_client_id.lower():
                raise ValueError("invalid managed identity GUID")
        except (ValueError, AttributeError, TypeError):
            raise ValueError("invalid managed identity GUID") from None
        self._client_id = str(parsed)

    def __call__(self, vault_url: str):
        try:
            from azure.identity import ManagedIdentityCredential
            from azure.keyvault.secrets import SecretClient
            credential = ManagedIdentityCredential(client_id=self._client_id)
            return SecretClient(vault_url=vault_url, credential=credential)
        except Exception:
            raise BringCredentialUnavailable() from None
