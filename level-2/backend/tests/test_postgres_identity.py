"""Malformed catalog response denials; actual SQL is exercised by dual-PG CI."""
import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.postgres_identity import read_postgres_identity, IDENTITY_SQL, OTHER_CONNECT_SQL
from ea_backend.single_tenant_session import TenantSessionDenied


class CatalogConnection:
    def __init__(self, row=('synthetic_db','synthetic_role',False,False,False), peers=()):
        self.row, self.peers, self.queries = row, peers, []
        self.closed = False
    def cursor(self):
        return self
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False
    def execute(self, query):
        self.queries.append(query)
    def fetchone(self):
        return self.row
    def fetchall(self):
        return self.peers


class PostgresIdentityTests(unittest.TestCase):
    def test_reads_only_fixed_catalog_selects_and_preserves_unsafe_evidence(self):
        conn = CatalogConnection(row=('synthetic_db','synthetic_role',False,True,True),
                                 peers=[('postgres',),('synthetic_peer',)])
        result = read_postgres_identity(conn)
        self.assertEqual(conn.queries,[IDENTITY_SQL,OTHER_CONNECT_SQL])
        self.assertTrue(all(query.startswith('SELECT ') for query in conn.queries))
        self.assertTrue(result.bypass_rls and result.owns_application_tables)
        self.assertEqual(result.other_connectable_databases,frozenset({'postgres','synthetic_peer'}))
        self.assertFalse(conn.closed)

    def test_missing_or_malformed_identity_denied_before_peer_query(self):
        for row in (None, (), ('db','role',False,False),
                    ('db','role','false',False,False), ('','role',False,False,False),
                    {'database_name':'db'}, ('db','role',False,False,None)):
            conn = CatalogConnection(row=row)
            with self.subTest(row=type(row).__name__), self.assertRaises(TenantSessionDenied):
                read_postgres_identity(conn)
            self.assertEqual(conn.queries,[IDENTITY_SQL])

    def test_malformed_peer_evidence_denied(self):
        for peers in (None, {'db':True}, [None], [('db','extra')], [(None,)], [('',)], ['db']):
            with self.subTest(peers=type(peers).__name__), self.assertRaises(TenantSessionDenied):
                read_postgres_identity(CatalogConnection(peers=peers))


if __name__ == '__main__':
    unittest.main()
