"""Path S transaction foundation; no production wiring or credential handling.

Connection factory, authorization check and effective-identity reader are
trusted injected adapters. Mock identity snapshots are NOT proof of actual
PostgreSQL grants, database isolation or CONNECT privileges. Do not use this
module to certify deployment readiness. Actual database controls remain required.
"""
from contextlib import contextmanager
from dataclasses import dataclass


class TenantSessionDenied(PermissionError):
    pass


class TransactionStateUnknown(RuntimeError):
    """Transaction or cleanup state is unverified; do not blindly replay."""


@dataclass(frozen=True)
class TenantDatabaseBinding:
    tenant_scope: str
    database_name: str
    runtime_role: str


@dataclass(frozen=True)
class EffectiveDatabaseIdentity:
    database_name: str
    runtime_role: str
    superuser: bool
    bypass_rls: bool
    owns_application_tables: bool
    other_connectable_databases: frozenset[str]


class SingleTenantSession:
    """One fixed tenant/database/role boundary, with fresh identity readback.

    The caller must supply authenticated tenant identity, not a request field.
    This is not a SQL sandbox: the application and injected adapters are trusted.
    Returned connections must be dedicated to this transaction until closed.
    """
    def __init__(self, binding, *, connect, read_identity, authorized):
        if type(binding) is not TenantDatabaseBinding or not all(
            type(v) is str and v.strip() for v in (
                binding.tenant_scope, binding.database_name, binding.runtime_role)):
            raise TenantSessionDenied('invalid_fixed_binding')
        if not all(callable(v) for v in (connect, read_identity, authorized)):
            raise TenantSessionDenied('trusted_adapters_required')
        self._binding = binding
        self._connect = connect
        self._read_identity = read_identity
        self._authorized = authorized

    @property
    def binding(self):
        return self._binding

    def _check_tenant(self, tenant):
        if type(tenant) is not str or tenant != self.binding.tenant_scope:
            raise TenantSessionDenied('authenticated_tenant_mismatch')
        if self._authorized(tenant) is not True:
            raise TenantSessionDenied('tenant_revoked_or_unverified')

    def _check_identity(self, conn):
        identity = self._read_identity(conn)
        if type(identity) is not EffectiveDatabaseIdentity:
            raise TenantSessionDenied('effective_identity_required')
        if not all(type(v) is bool for v in (
            identity.superuser, identity.bypass_rls, identity.owns_application_tables)):
            raise TenantSessionDenied('malformed_role_evidence')
        if (type(identity.database_name) is not str or type(identity.runtime_role) is not str
                or type(identity.other_connectable_databases) is not frozenset
                or not all(type(v) is str for v in identity.other_connectable_databases)):
            raise TenantSessionDenied('malformed_database_evidence')
        if (identity.database_name != self.binding.database_name
                or identity.runtime_role != self.binding.runtime_role
                or identity.superuser or identity.bypass_rls or identity.owns_application_tables
                or identity.other_connectable_databases):
            raise TenantSessionDenied('database_or_role_isolation_mismatch')

    @contextmanager
    def transaction(self, authenticated_tenant):
        # Deny wrong/missing tenant before opening a connection or executing SQL.
        self._check_tenant(authenticated_tenant)
        conn = self._connect()
        commit_attempted = False
        primary_error = None
        try:
            self._check_identity(conn)
            self._check_tenant(authenticated_tenant)
            yield conn
            # Re-read identity and revocation before committing application work.
            self._check_identity(conn)
            self._check_tenant(authenticated_tenant)
            commit_attempted = True
            conn.commit()
        except BaseException as exc:
            if commit_attempted:
                # Lost acknowledgement or cancellation can follow a committed write.
                primary_error = TransactionStateUnknown('commit_readback_required_no_retry')
                raise primary_error from exc
            try:
                conn.rollback()
            except BaseException as rollback_exc:
                primary_error = TransactionStateUnknown('rollback_readback_required_no_retry')
                primary_error.add_note('rollback failure class: ' + type(rollback_exc).__name__)
                raise primary_error from exc
            primary_error = exc
            raise
        finally:
            try:
                conn.close()
            except BaseException as close_exc:
                if primary_error is not None:
                    # Preserve the primary denial/cancellation/uncertain-state signal.
                    primary_error.add_note('close failure class: ' + type(close_exc).__name__)
                else:
                    raise TransactionStateUnknown('session_cleanup_readback_required_no_retry') from close_exc
