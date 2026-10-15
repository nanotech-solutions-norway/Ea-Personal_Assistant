"""Fail-closed tenant authorization gate for future read-only Bring tracking.

This module performs NO HTTP, vault access, database I/O, logging, or writes.
It is not wired into the EA runtime yet: default posture remains DISABLED.

All identity assertions and shipment provenance must originate from trusted,
backend-controlled verifier and registry implementations, NEVER user headers,
public Tracking v2 payloads, model responses or uploaded screenshots alone.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

READ_SCOPE = "bring.tracking.read"
BOOKING_EVIDENCE = "authenticated_mybring_booking"
_KV_REF = re.compile(
    r"https://[a-z0-9-]+\.vault\.azure\.net/secrets/[A-Za-z0-9-]+"
)
_REF = re.compile(r"[A-Za-z0-9-]{7,80}")


@dataclass(frozen=True)
class VerifiedIdentity:
    issuer: str
    subject: str
    audience: str
    expires_at: datetime


@dataclass(frozen=True)
class PrincipalGrant:
    issuer: str
    subject: str
    tenant_scope: str
    permission: str
    customer_number: str
    active: bool = False


@dataclass(frozen=True)
class TenantAccount:
    tenant_scope: str
    customer_number: str
    vault_secret_ref: str
    active: bool = False


@dataclass(frozen=True)
class ShipmentProvenance:
    tenant_scope: str
    tracking_reference: str
    customer_number: str
    evidence_source: str
    reviewed_at: datetime
    independently_approved: bool = False


@dataclass(frozen=True)
class ReadGateConfig:
    issuer: str
    audience: str
    enabled: bool = False
    maximum_evidence_age_days: int = 30


@dataclass(frozen=True)
class ScopedTrackingPermit:
    """Internal-only result; never expose this or vault path to clients/logs."""

    tenant_scope: str
    tracking_reference: str
    credential_ref: str
    read_only: bool = True


class IdentityVerifier(Protocol):
    production_safe: bool

    def verify(self, bearer_token: str, *, expected_audience: str) -> VerifiedIdentity:
        """Cryptographically verify OIDC JWT and reject invalid signatures/claims."""


class TrustedBringRegistry(Protocol):
    production_safe: bool

    def principal_grant(self, issuer: str, subject: str) -> PrincipalGrant | None: ...

    def tenant_account(self, tenant_scope: str) -> TenantAccount | None: ...

    def shipment_provenance(
        self, tenant_scope: str, tracking_reference: str
    ) -> ShipmentProvenance | None: ...


class BringAuthorizationDenied(PermissionError):
    """Reason codes are safe for sanitized audit; never contain identifiers."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def _deny(reason: str) -> None:
    raise BringAuthorizationDenied(reason)


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        _deny("INVALID_TIME_EVIDENCE")
    return value.astimezone(timezone.utc)


def authorize_tracking_read(
    *,
    bearer_token: str,
    requested_tenant: str,
    tracking_reference: str,
    config: ReadGateConfig,
    verifier: IdentityVerifier,
    registry: TrustedBringRegistry,
    now: datetime | None = None,
) -> ScopedTrackingPermit:
    """Allow only a registered principal, company and pre-approved shipment.

    An authenticated token without an approved principal grant is insufficient.
    A company-owned shipment without an authenticated principal is insufficient.
    Public Bring status or a sender/receiver flag is NEVER an authorization input.
    """
    if not isinstance(config, ReadGateConfig) or config.enabled is not True:
        _deny("FEATURE_DISABLED")
    if (
        not config.issuer
        or not config.audience
        or not 1 <= config.maximum_evidence_age_days <= 365
        or not getattr(verifier, "production_safe", False)
        or not getattr(registry, "production_safe", False)
    ):
        _deny("TRUSTED_COMPONENT_UNAVAILABLE")
    if not isinstance(bearer_token, str) or not bearer_token.strip():
        _deny("IDENTITY_UNVERIFIED")
    if not isinstance(requested_tenant, str) or not requested_tenant.strip():
        _deny("INVALID_TENANT")
    if not isinstance(tracking_reference, str) or not _REF.fullmatch(tracking_reference):
        _deny("INVALID_TRACKING_REFERENCE")

    when = _utc(now if now is not None else datetime.now(timezone.utc))
    try:
        identity = verifier.verify(bearer_token, expected_audience=config.audience)
    except Exception:
        _deny("IDENTITY_UNVERIFIED")
    if (
        not isinstance(identity, VerifiedIdentity)
        or not identity.subject
        or identity.issuer != config.issuer
        or identity.audience != config.audience
        or _utc(identity.expires_at) <= when
    ):
        _deny("IDENTITY_UNVERIFIED")

    try:
        grant = registry.principal_grant(identity.issuer, identity.subject)
        account = registry.tenant_account(requested_tenant)
        provenance = registry.shipment_provenance(requested_tenant, tracking_reference)
    except Exception:
        _deny("TRUSTED_REGISTRY_UNAVAILABLE")

    if (
        not isinstance(grant, PrincipalGrant)
        or grant.active is not True
        or grant.issuer != identity.issuer
        or grant.subject != identity.subject
        or grant.tenant_scope != requested_tenant
        or grant.permission != READ_SCOPE
    ):
        _deny("TENANT_ACCESS_DENIED")
    if (
        not isinstance(account, TenantAccount)
        or account.active is not True
        or account.tenant_scope != requested_tenant
        or not re.fullmatch(r"[0-9]{6,20}", account.customer_number)
        or grant.customer_number != account.customer_number
        or not _KV_REF.fullmatch(account.vault_secret_ref)
    ):
        _deny("ACCOUNT_BINDING_UNVERIFIED")
    if (
        not isinstance(provenance, ShipmentProvenance)
        or provenance.tenant_scope != requested_tenant
        or provenance.tracking_reference != tracking_reference
        or provenance.customer_number != account.customer_number
        or provenance.evidence_source != BOOKING_EVIDENCE
        or provenance.independently_approved is not True
    ):
        _deny("SHIPMENT_PROVENANCE_UNVERIFIED")

    reviewed = _utc(provenance.reviewed_at)
    if reviewed > when or when - reviewed > timedelta(days=config.maximum_evidence_age_days):
        _deny("SHIPMENT_EVIDENCE_STALE")

    return ScopedTrackingPermit(
        tenant_scope=requested_tenant,
        tracking_reference=tracking_reference,
        credential_ref=account.vault_secret_ref,
    )
