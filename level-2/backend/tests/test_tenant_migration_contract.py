"""Synthetic architecture-neutral contract checks; no DB or provider I/O."""
import pathlib
import sys
import unittest
from dataclasses import replace
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.tenant_migration_contract import (
    LEGACY_TABLES, REQUIRED_PROOFS, MigrationContract, migration_blockers,
)
from ea_backend.projection_sink import cursor_scope
from ea_backend.unified_sync import source_key


class TenantMigrationContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = MigrationContract(1, 'M', 'synthetic-owner-decision',
            LEGACY_TABLES, REQUIRED_PROOFS, forced_rls_tables=LEGACY_TABLES)

    def test_unresolved_architecture_denied(self):
        self.assertIn('owner_architecture_decision_required',
            migration_blockers(replace(self.contract, architecture='UNDECIDED')))
        self.assertIn('owner_architecture_decision_required',
            migration_blockers(replace(self.contract, decision_reference=' ')))

    def test_each_legacy_table_must_be_inventoried_and_forced(self):
        for table in LEGACY_TABLES:
            with self.subTest(table=table):
                self.assertIn('legacy_table_inventory_mismatch', migration_blockers(
                    replace(self.contract, table_inventory=LEGACY_TABLES - {table})))
                self.assertIn('all_legacy_tables_require_force_rls', migration_blockers(
                    replace(self.contract, forced_rls_tables=LEGACY_TABLES - {table})))

    def test_each_negative_proof_required(self):
        for proof in REQUIRED_PROOFS:
            self.assertIn('missing_proof:' + proof, migration_blockers(
                replace(self.contract, proofs=REQUIRED_PROOFS - {proof})))

    def test_both_proposals_can_be_evaluated_without_selecting_either(self):
        self.assertEqual(migration_blockers(self.contract), ())
        single = replace(self.contract, architecture='S', forced_rls_tables=frozenset(),
                         dedicated_database_verified=True)
        self.assertEqual(migration_blockers(single), ())
        for candidate in (replace(single, shared_runtime=True),
                          replace(single, dedicated_database_verified=False)):
            self.assertIn('single_tenant_database_isolation_required', migration_blockers(candidate))

    def test_malformed_contract_types_fail_closed(self):
        mutations = (
            {'version': True}, {'version': '1'},
            {'dedicated_database_verified': 'false'}, {'dedicated_database_verified': 1},
            {'shared_runtime': 0}, {'decision_reference': None},
            {'architecture': None}, {'table_inventory': list(LEGACY_TABLES)},
            {'proofs': dict.fromkeys(REQUIRED_PROOFS)},
            {'forced_rls_tables': set(LEGACY_TABLES)},
            {'proofs': frozenset({None})},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertEqual(migration_blockers(replace(self.contract, **mutation)),
                                 ('malformed_contract',))
        for invalid in (None, {}, object()):
            with self.subTest(invalid=type(invalid).__name__):
                self.assertEqual(migration_blockers(invalid), ('malformed_contract',))

    def test_unknown_version_and_extra_table_denied(self):
        self.assertIn('unsupported_contract_version', migration_blockers(replace(self.contract, version=2)))
        self.assertIn('legacy_table_inventory_mismatch', migration_blockers(
            replace(self.contract, table_inventory=LEGACY_TABLES | {'unknown'})))

    def test_cursor_and_projection_identity_separate_tenant_source_collection(self):
        identities = [('synthetic-alpha', 'gmail', 'one'), ('synthetic-beta', 'gmail', 'one'),
                      ('synthetic-alpha', 'google_calendar', 'one'), ('synthetic-alpha', 'gmail', 'two')]
        self.assertEqual(len({cursor_scope(*parts) for parts in identities}), 4)
        self.assertEqual(len({source_key(t, s, 'same-event', c) for t, s, c in identities}), 4)
        self.assertEqual(cursor_scope(*identities[0]), cursor_scope(*identities[0]))


if __name__ == '__main__':
    unittest.main()
