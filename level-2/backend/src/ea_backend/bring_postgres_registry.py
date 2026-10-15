"""Read-only PostgreSQL Bring authorization registry, scoped per transaction.

Only host-verified actor issuer/subject/tenant may select registry records.
Application must use a restricted SELECT-only role, FORCE RLS and an
independently protected HMAC key; no actual tracking numbers stored here.

The adapter performs no customer-data updates, Bring calls or secret resolves.
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import timezone
from typing import Callable

from .bring_tenant_gateway import (
    BOOKING_EVIDENCE,
    PrincipalGrant,
    ShipmentProvenance,
    TenantAccount,
)


class RegistrySecurityError(RuntimeError):
    pass


class PostgresBringRegistry:
    """Implement TrustedBringRegistry for one already-authenticated actor.

    Construct ONLY from trusted backend identity context. The DB user must
    never be table owner/superuser/BYPASSRLS; it is granted SELECT only.
    """

    production_safe = True

    def __init__(
        self,
        *,
        connection_factory: Callable,
        actor_issuer: str,
        actor_subject: str,
        tenant_scope: str,
        tracking_hmac_key: bytes,
    ):
        if not callable(connection_factory):
            raise RegistrySecurityError("invalid connection factory")
        if not all(
            isinstance(value, str) and 1 <= len(value) <= 512
            for value in (actor_issuer, actor_subject, tenant_scope)
        ):
            raise RegistrySecurityError("invalid scoped actor configuration")
        if not isinstance(tracking_hmac_key, bytes) or len(tracking_hmac_key) < 32:
            raise RegistrySecurityError("tracking HMAC key unavailable")
        self._connect = connection_factory
        self._actor_issuer = actor_issuer
        self._actor_subject = actor_subject
        self._tenant = tenant_scope
        self._key = tracking_hmac_key

    def _read_one(self, statement: str, args: tuple):
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    # Deny privileged database accounts and missing RLS before
                    # reading any record. Runtime credentials must be SELECT-only.
                    cur.execute(
                        "SELECT rolsuper, rolbypassrls FROM pg_roles "
                        "WHERE rolname = current_user"
                    )
                    role = cur.fetchone()
                    if role is None or role[0] or role[1]:
                        raise RegistrySecurityError("privileged role prohibited")
                    cur.execute(
                        "SELECT row_security_active('ea_bring_principal_grants'::regclass),"
                        " row_security_active('ea_bring_tenant_accounts'::regclass),"
                        " row_security_active('ea_bring_shipment_provenance'::regclass)"
                    )
                    rls = cur.fetchone()
                    if not rls or rls != (True, True, True):
                        raise RegistrySecurityError("registry RLS not enforced")
                    # Scoped only to the current transaction; never SET at
                    # session level. Queries cannot receive client headers.
                    for name, value in (
                        ("ea.actor_issuer", self._actor_issuer),
                        ("ea.actor_subject", self._actor_subject),
                        ("ea.tenant_scope", self._tenant),
                    ):
                        cur.execute("SELECT set_config(%s, %s, true)", (name, value))
                    cur.execute(statement, args)
                    return cur.fetchone()
        except RegistrySecurityError:
            raise
        except Exception:
            # No PII, SQL, tracking references, or connection strings in errors.
            raise RegistrySecurityError("registry read unavailable") from None

    def principal_grant(self, issuer: str, subject: str) -> PrincipalGrant | None:
        if issuer != self._actor_issuer or subject != self._actor_subject:
            return None
        row = self._read_one(
            "SELECT issuer, subject, tenant_scope, permission, customer_number, active "
            "FROM ea_bring_principal_grants "
            "WHERE issuer=%s AND subject=%s AND tenant_scope=%s",
            (issuer, subject, self._tenant),
        )
        return PrincipalGrant(*row) if row else None

    def tenant_account(self, tenant_scope: str) -> TenantAccount | None:
        if tenant_scope != self._tenant:
            return None
        row = self._read_one(
            "SELECT tenant_scope, customer_number, vault_secret_ref, active "
            "FROM ea_bring_tenant_accounts WHERE tenant_scope=%s",
            (tenant_scope,),
        )
        return TenantAccount(*row) if row else None

    def shipment_provenance(
        self, tenant_scope: str, tracking_reference: str
    ) -> ShipmentProvenance | None:
        if tenant_scope != self._tenant or not isinstance(tracking_reference, str):
            return None
        digest = hmac.new(
            self._key,
            (tenant_scope + "\x1f" + tracking_reference).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        row = self._read_one(
            "SELECT tenant_scope, customer_number, evidence_source, reviewed_at, "
            "independently_approved FROM ea_bring_shipment_provenance "
            "WHERE tenant_scope=%s AND tracking_digest=%s",
            (tenant_scope, digest),
        )
        if row is None:
            return None
        return ShipmentProvenance(
            tenant_scope=row[0],
            tracking_reference=tracking_reference,
            customer_number=row[1],
            evidence_source=row[2],
            reviewed_at=row[3].astimezone(timezone.utc),
            independently_approved=row[4],
        )
