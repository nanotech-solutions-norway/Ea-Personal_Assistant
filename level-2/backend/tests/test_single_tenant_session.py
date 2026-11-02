"""Two fictional in-memory databases; not PostgreSQL privilege acceptance."""
import copy
import pathlib
import sys
import unittest
from dataclasses import replace
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.single_tenant_session import (
    TenantDatabaseBinding, EffectiveDatabaseIdentity, SingleTenantSession,
    TenantSessionDenied, TransactionStateUnknown,
)

TABLES = ('ea_cases','ea_actions','ea_approvals','ea_audit',
          'ea_watch_registrations','ea_ingest_events','ea_source_cursors')


class SyntheticDatabase:
    def __init__(self, name, role):
        self.identity = EffectiveDatabaseIdentity(name, role, False, False, False, frozenset())
        self.rows = {name: {} for name in TABLES}
        self.opens = self.reads = 0
        self.connections = []
    def connect(self):
        self.opens += 1
        conn = SyntheticConnection(self)
        self.connections.append(conn)
        return conn
    def read_identity(self, conn):
        self.reads += 1
        return conn.identity


class SyntheticConnection:
    def __init__(self, db):
        self.db, self.identity = db, db.identity
        self.rows = copy.deepcopy(db.rows)
        self.commits = self.rollbacks = self.closes = 0
        self.ambiguous_commit = False
        self.fail_rollback = self.fail_close = False
    def insert(self, table, key, value):
        if key in self.rows[table]:
            raise ValueError('synthetic_duplicate')
        self.rows[table][key] = value
    def commit(self):
        self.commits += 1
        self.db.rows = copy.deepcopy(self.rows)
        if self.ambiguous_commit:
            raise OSError('synthetic_commit_ack_lost')
    def rollback(self):
        self.rollbacks += 1
        if self.fail_rollback:
            raise OSError('synthetic rollback failure')
        self.rows = copy.deepcopy(self.db.rows)
    def close(self):
        self.closes += 1
        if self.fail_close:
            raise OSError('synthetic close failure')


class SingleTenantSessionTests(unittest.TestCase):
    def setUp(self):
        self.alpha = SyntheticDatabase('synthetic_alpha_db', 'synthetic_alpha_worker')
        self.beta = SyntheticDatabase('synthetic_beta_db', 'synthetic_beta_worker')
        self.enabled = True
        self.guard = self.guard_for(self.alpha, 'synthetic-alpha')
    def guard_for(self, db, tenant, connect=None):
        return SingleTenantSession(TenantDatabaseBinding(tenant, db.identity.database_name, db.identity.runtime_role),
            connect=connect or db.connect, read_identity=db.read_identity,
            authorized=lambda tenant: self.enabled)

    def test_wrong_or_missing_tenant_denied_before_connection_or_identity_sql(self):
        for tenant in ('synthetic-beta', '', None, 1):
            with self.assertRaises(TenantSessionDenied):
                with self.guard.transaction(tenant):
                    self.fail('application query must not run')
        self.assertEqual((self.alpha.opens, self.alpha.reads), (0, 0))

    def test_two_database_legacy_and_cursor_keys_are_isolated_and_replay_denied(self):
        other = self.guard_for(self.beta, 'synthetic-beta')
        for guard, tenant, value in ((self.guard,'synthetic-alpha','alpha'),(other,'synthetic-beta','beta')):
            with guard.transaction(tenant) as conn:
                for table in TABLES:
                    conn.insert(table, 'same-synthetic-key', value)
            with self.assertRaises(ValueError):
                with guard.transaction(tenant) as conn:
                    conn.insert('ea_ingest_events', 'same-synthetic-key', 'duplicate')
        for table in TABLES:
            self.assertEqual(self.alpha.rows[table]['same-synthetic-key'], 'alpha')
            self.assertEqual(self.beta.rows[table]['same-synthetic-key'], 'beta')

    def test_wrong_database_or_role_denied_before_application_queries(self):
        for identity in (self.beta.identity, replace(self.alpha.identity, runtime_role='foreign_role')):
            self.alpha.identity = identity
            with self.assertRaises(TenantSessionDenied):
                with self.guard.transaction('synthetic-alpha'):
                    self.fail('application query must not run')
            conn = self.alpha.connections[-1]
            self.assertEqual((conn.commits,conn.rollbacks,conn.closes),(0,1,1))

    def test_owner_superuser_bypass_and_other_database_connect_denied(self):
        base = self.alpha.identity
        for mutation in ({'superuser':True},{'bypass_rls':True},{'owns_application_tables':True},
                         {'other_connectable_databases':frozenset({'synthetic_beta_db'})},
                         {'superuser':'false'},{'other_connectable_databases':set()}):
            self.alpha.identity = replace(base, **mutation)
            with self.assertRaises(TenantSessionDenied):
                with self.guard.transaction('synthetic-alpha'):
                    self.fail('application query must not run')

    def test_revocation_before_open_and_before_commit_denies(self):
        self.enabled = False
        with self.assertRaises(TenantSessionDenied):
            with self.guard.transaction('synthetic-alpha'):
                self.fail('revoked')
        self.assertEqual(self.alpha.opens,0)
        self.enabled = True
        with self.assertRaises(TenantSessionDenied):
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.insert('ea_cases','case','fictional')
                self.enabled = False
        self.assertEqual(self.alpha.rows['ea_cases'], {})

    def test_identity_drift_before_commit_rolls_back(self):
        with self.assertRaises(TenantSessionDenied):
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.insert('ea_cases','case','fictional')
                conn.identity = self.beta.identity
        self.assertEqual(self.alpha.rows['ea_cases'], {})

    def test_interrupted_transaction_restores_prior_state_and_next_connection_is_fresh(self):
        with self.guard.transaction('synthetic-alpha') as conn:
            conn.insert('ea_source_cursors','source','cursor1')
        with self.assertRaises(RuntimeError):
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.rows['ea_source_cursors']['source'] = 'must-rollback'
                raise RuntimeError('synthetic interruption')
        self.assertEqual(self.alpha.rows['ea_source_cursors']['source'],'cursor1')
        with self.guard.transaction('synthetic-alpha') as conn:
            self.assertEqual(conn.rows['ea_source_cursors']['source'],'cursor1')
        self.assertEqual(len({id(c) for c in self.alpha.connections}),3)
        self.assertTrue(all(c.closes == 1 for c in self.alpha.connections))

    def test_uncertain_commit_is_not_retried_or_claimed_rolled_back(self):
        with self.assertRaises(TransactionStateUnknown):
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.insert('ea_cases','case','fictional')
                conn.ambiguous_commit = True
        self.assertEqual((conn.commits, conn.rollbacks, conn.closes),(1,0,1))
        self.assertEqual(self.alpha.opens,1)
        self.assertEqual(self.alpha.rows['ea_cases']['case'],'fictional')

    def test_cancellation_before_commit_rolls_back_and_closes(self):
        with self.assertRaises(KeyboardInterrupt):
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.insert('ea_cases','case','fictional')
                raise KeyboardInterrupt('synthetic cancellation')
        self.assertEqual((conn.commits,conn.rollbacks,conn.closes),(0,1,1))
        self.assertEqual(self.alpha.rows['ea_cases'],{})

    def test_close_failure_preserves_uncertain_commit_primary_error(self):
        with self.assertRaises(TransactionStateUnknown) as error:
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.ambiguous_commit = conn.fail_close = True
        self.assertEqual(str(error.exception),'commit_readback_required_no_retry')
        self.assertTrue(any('close failure class: OSError' in n for n in error.exception.__notes__))
        self.assertEqual((conn.commits,conn.rollbacks,conn.closes),(1,0,1))

    def test_failed_rollback_signals_uncertain_state_without_masking_cause(self):
        with self.assertRaises(TransactionStateUnknown) as error:
            with self.guard.transaction('synthetic-alpha') as conn:
                conn.fail_rollback = conn.fail_close = True
                raise ValueError('synthetic application failure')
        self.assertEqual(str(error.exception),'rollback_readback_required_no_retry')
        self.assertIsInstance(error.exception.__cause__,ValueError)
        self.assertEqual((conn.commits,conn.rollbacks,conn.closes),(0,1,1))
        self.assertEqual(self.alpha.opens,1)

    def test_unverified_identity_reader_and_nonboolean_authorization_deny(self):
        guard = SingleTenantSession(self.guard.binding, connect=self.alpha.connect,
            read_identity=lambda conn: {}, authorized=lambda tenant: True)
        with self.assertRaises(TenantSessionDenied):
            with guard.transaction('synthetic-alpha'):
                self.fail('unverified identity')
        guard = SingleTenantSession(self.guard.binding, connect=self.alpha.connect,
            read_identity=self.alpha.read_identity, authorized=lambda tenant: 'true')
        opens = self.alpha.opens
        with self.assertRaises(TenantSessionDenied):
            with guard.transaction('synthetic-alpha'):
                self.fail('unverified authorization')
        self.assertEqual(self.alpha.opens,opens)


if __name__ == '__main__':
    unittest.main()
