"""Offline migration readiness contract; never authorizes or applies SQL.

Architecture S/M requires an explicit owning-project decision. Evidence is
supplied by the caller and must be independently verified before deployment.
"""
from dataclasses import dataclass

LEGACY_TABLES = frozenset({
    'ea_cases', 'ea_actions', 'ea_approvals', 'ea_audit',
    'ea_watch_registrations', 'ea_ingest_events',
})
REQUIRED_PROOFS = frozenset({
    'restricted_role', 'source_cursor_scope', 'same_tenant_references',
    'approval_case_binding', 'replay_denial', 'rollback_readback',
    'unattributed_rows_quarantined',
})


@dataclass(frozen=True)
class MigrationContract:
    version: int
    architecture: str
    decision_reference: str
    table_inventory: frozenset[str]
    proofs: frozenset[str]
    shared_runtime: bool = False
    forced_rls_tables: frozenset[str] = frozenset()
    dedicated_database_verified: bool = False


def migration_blockers(contract: MigrationContract) -> tuple[str, ...]:
    """Return deterministic blockers; an empty result is NOT deployment authority."""
    # Dataclass annotations do not validate runtime values. In particular,
    # bool is an int subclass and nonempty strings are truthy: neither proves
    # the contract version nor a verified isolation assertion.
    if type(contract) is not MigrationContract:
        return ('malformed_contract',)
    if (type(contract.version) is not int
            or type(contract.architecture) is not str
            or type(contract.decision_reference) is not str
            or type(contract.shared_runtime) is not bool
            or type(contract.dedicated_database_verified) is not bool):
        return ('malformed_contract',)
    for values in (contract.table_inventory, contract.proofs, contract.forced_rls_tables):
        if type(values) is not frozenset or not all(type(value) is str for value in values):
            return ('malformed_contract',)
    blockers = []
    if contract.version != 1:
        blockers.append('unsupported_contract_version')
    if contract.architecture not in ('S', 'M') or not contract.decision_reference.strip():
        blockers.append('owner_architecture_decision_required')
    if contract.table_inventory != LEGACY_TABLES:
        blockers.append('legacy_table_inventory_mismatch')
    blockers.extend('missing_proof:' + item for item in sorted(REQUIRED_PROOFS - contract.proofs))
    if contract.architecture == 'S':
        if contract.shared_runtime or not contract.dedicated_database_verified:
            blockers.append('single_tenant_database_isolation_required')
    if contract.architecture == 'M' and not LEGACY_TABLES <= contract.forced_rls_tables:
        blockers.append('all_legacy_tables_require_force_rls')
    return tuple(blockers)
