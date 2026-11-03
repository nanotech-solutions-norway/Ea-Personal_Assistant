"""PostgreSQL-backed Path S proof using only the disposable CI PostgreSQL service.

The fixture creates two temporary databases and two temporary LOGIN roles. It
never connects to a live or cloud database and does not change repository
runtime wiring or application schema.
"""
import os
import pathlib
import sys
import unittest
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ea_backend.single_tenant_session import (
    EffectiveDatabaseIdentity,
    SingleTenantSession,
    TenantDatabaseBinding,
    TenantSessionDenied,
)

DSN = os.environ.get("EA_TEST_DATABASE_URL", "")
TABLE_NAMES = (
    "ea_cases",
    "ea_actions",
    "ea_approvals",
    "ea_audit",
    "ea_watch_registrations",
    "ea_ingest_events",
    "ea_source_cursors",
)


@unittest.skipUnless(DSN, "Disposable PostgreSQL CI service only")
class PathSTwoDisposableDatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import psycopg
        from psycopg import sql

        cls.psycopg = psycopg
        cls.sql = sql
        suffix = uuid.uuid4().hex[:10]
        cls.databases = {
            "synthetic-alpha": "ea_ci_path_s_alpha_" + suffix,
            "synthetic-beta": "ea_ci_path_s_beta_" + suffix,
        }
        cls.roles = {
            "synthetic-alpha": "ea_ci_path_s_alpha_" + suffix,
            "synthetic-beta": "ea_ci_path_s_beta_" + suffix,
        }
        cls.passwords = {
            tenant: uuid.uuid4().hex + uuid.uuid4().hex
            for tenant in cls.databases
        }
        cls.connections = []
        cls.restore_public_connect = []
        with psycopg.connect(DSN, autocommit=True) as admin:
            acl_rows = admin.execute(
                "SELECT d.datname, EXISTS (SELECT 1 FROM aclexplode("
                "COALESCE(d.datacl, acldefault('d', d.datdba))) AS a "
                "WHERE a.grantee = 0 AND a.privilege_type = 'CONNECT') "
                "FROM pg_database AS d WHERE d.datallowconn"
            ).fetchall()
            cls.restore_public_connect = [name for name, allowed in acl_rows if allowed]
            for name, _allowed in acl_rows:
                admin.execute(
                    cls.sql.SQL("REVOKE CONNECT ON DATABASE {} FROM PUBLIC").format(
                        cls.sql.Identifier(name)
                    )
                )
            for tenant in cls.databases:
                database = cls.databases[tenant]
                role = cls.roles[tenant]
                admin.execute(sql.SQL("CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS PASSWORD {}").format(
                    sql.Identifier(role), sql.Literal(cls.passwords[tenant])
                ))
                admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
                admin.execute(sql.SQL("REVOKE CONNECT ON DATABASE {} FROM PUBLIC").format(sql.Identifier(database)))
                admin.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                    sql.Identifier(database), sql.Identifier(role)
                ))
                with psycopg.connect(
                    psycopg.conninfo.make_conninfo(DSN, dbname=database),
                    autocommit=True,
                ) as db_admin:
                    db_admin.execute("CREATE TABLE ea_cases (case_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
                    db_admin.execute("CREATE TABLE ea_actions (action_id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES ea_cases(case_id), payload TEXT NOT NULL)")
                    db_admin.execute("CREATE TABLE ea_approvals (approval_id TEXT PRIMARY KEY, action_id TEXT NOT NULL REFERENCES ea_actions(action_id))")
                    db_admin.execute("CREATE TABLE ea_audit (audit_id TEXT PRIMARY KEY, action_id TEXT NOT NULL REFERENCES ea_actions(action_id))")
                    db_admin.execute("CREATE TABLE ea_watch_registrations (watch_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
                    db_admin.execute("CREATE TABLE ea_ingest_events (event_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
                    db_admin.execute("CREATE TABLE ea_source_cursors (source_id TEXT PRIMARY KEY, cursor_value TEXT NOT NULL)")
                    db_admin.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(sql.Identifier(role)))
                    db_admin.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO {}").format(sql.Identifier(role)))

    @classmethod
    def tearDownClass(cls):
        if not hasattr(cls, "psycopg"):
            return
        with cls.psycopg.connect(DSN, autocommit=True) as admin:
            for database in cls.databases.values():
                admin.execute(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = %s AND pid <> pg_backend_pid()",
                    (database,),
                )
                admin.execute(cls.sql.SQL("DROP DATABASE IF EXISTS {}").format(cls.sql.Identifier(database)))
            for role in cls.roles.values():
                admin.execute(cls.sql.SQL("DROP ROLE IF EXISTS {}").format(cls.sql.Identifier(role)))
            for database in cls.restore_public_connect:
                admin.execute(
                    cls.sql.SQL("GRANT CONNECT ON DATABASE {} TO PUBLIC").format(
                        cls.sql.Identifier(database)
                    )
                )

    def identity_reader(self, conn):
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user, r.rolsuper, r.rolbypassrls, "
                "EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' "
                "AND tableowner = current_user) "
                "FROM pg_roles AS r WHERE r.rolname = current_user"
            )
            row = cursor.fetchone()
            cursor.execute(
                "SELECT datname FROM pg_database "
                "WHERE datallowconn AND datname <> current_database() "
                "AND has_database_privilege(current_user, datname, 'CONNECT')",
            )
            peers = frozenset(result[0] for result in cursor.fetchall())
        return EffectiveDatabaseIdentity(
            database_name=row[0],
            runtime_role=row[1],
            superuser=row[2],
            bypass_rls=row[3],
            owns_application_tables=row[4],
            other_connectable_databases=peers,
        )

    def connect_as(self, tenant):
        conn = self.psycopg.connect(
            self.psycopg.conninfo.make_conninfo(
                DSN,
                dbname=self.databases[tenant],
                user=self.roles[tenant],
                password=self.passwords[tenant],
                connect_timeout=5,
            )
        )
        self.connections.append(conn)
        return conn

    def guard_for(self, tenant, connect=None):
        return SingleTenantSession(
            TenantDatabaseBinding(
                tenant_scope=tenant,
                database_name=self.databases[tenant],
                runtime_role=self.roles[tenant],
            ),
            connect=connect or (lambda: self.connect_as(tenant)),
            read_identity=self.identity_reader,
            authorized=lambda selected: selected in self.databases,
        )

    def insert_graph(self, conn, tag, payload=None):
        payload = tag if payload is None else payload
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO ea_cases VALUES (%s, %s)", ("case-" + tag, payload))
            cursor.execute("INSERT INTO ea_actions VALUES (%s, %s, %s)", ("action-" + tag, "case-" + tag, payload))
            cursor.execute("INSERT INTO ea_approvals VALUES (%s, %s)", ("approval-" + tag, "action-" + tag))
            cursor.execute("INSERT INTO ea_audit VALUES (%s, %s)", ("audit-" + tag, "action-" + tag))
            cursor.execute("INSERT INTO ea_watch_registrations VALUES (%s, %s)", ("watch-" + tag, payload))
            cursor.execute("INSERT INTO ea_ingest_events VALUES (%s, %s)", ("event-" + tag, payload))
            cursor.execute("INSERT INTO ea_source_cursors VALUES (%s, %s)", ("source-" + tag, "cursor-" + tag))

    def test_each_role_can_connect_only_to_its_assigned_database(self):
        with self.psycopg.connect(DSN) as admin:
            all_databases = [row[0] for row in admin.execute(
                "SELECT datname FROM pg_database WHERE datallowconn"
            ).fetchall()]
            for tenant, peer in (
                ("synthetic-alpha", "synthetic-beta"),
                ("synthetic-beta", "synthetic-alpha"),
            ):
                result = admin.execute(
                    "SELECT has_database_privilege(%s, %s, 'CONNECT')",
                    (self.roles[tenant], self.databases[tenant]),
                ).fetchone()[0]
                denied = admin.execute(
                    "SELECT has_database_privilege(%s, %s, 'CONNECT')",
                    (self.roles[tenant], self.databases[peer]),
                ).fetchone()[0]
                all_access = admin.execute(
                    "SELECT datname FROM pg_database WHERE datallowconn "
                    "AND has_database_privilege(%s, datname, 'CONNECT')",
                    (self.roles[tenant],),
                ).fetchall()
                self.assertTrue(result)
                self.assertFalse(denied)
                self.assertEqual([row[0] for row in all_access], [self.databases[tenant]])
                self.assertEqual(set(all_databases) >= {self.databases[tenant], self.databases[peer]}, True)
        for tenant, peer in (
            ("synthetic-alpha", "synthetic-beta"),
            ("synthetic-beta", "synthetic-alpha"),
        ):
            with self.connect_as(tenant) as conn:
                self.assertEqual(conn.execute("SELECT current_database(), current_user").fetchone(),
                                 (self.databases[tenant], self.roles[tenant]))
            with self.assertRaises(self.psycopg.OperationalError):
                self.psycopg.connect(
                    self.psycopg.conninfo.make_conninfo(
                        DSN,
                        dbname=self.databases[peer],
                        user=self.roles[tenant],
                        password=self.passwords[tenant],
                        connect_timeout=5,
                    )
                )

    def test_same_identifiers_are_isolated_and_replay_is_denied_per_database(self):
        for tenant in self.databases:
            with self.guard_for(tenant).transaction(tenant) as conn:
                self.insert_graph(conn, "same-key", tenant)
        for tenant in self.databases:
            guard = self.guard_for(tenant)
            with guard.transaction(tenant) as conn:
                self.assertEqual(
                    conn.execute("SELECT payload FROM ea_cases WHERE case_id = 'case-same-key'").fetchone()[0],
                    tenant,
                )
                with self.assertRaises(self.psycopg.IntegrityError):
                    self.insert_graph(conn, "same-key")
        self.assertTrue(all(conn.closed for conn in self.connections))

    def test_wrong_tenant_is_denied_before_connection(self):
        opened = []
        guard = self.guard_for("synthetic-alpha", connect=lambda: opened.append(True))
        with self.assertRaises(TenantSessionDenied):
            with guard.transaction("synthetic-beta"):
                self.fail("application work must not run")
        self.assertEqual(opened, [])

    def test_database_identity_drift_denies_before_application_query(self):
        guard = self.guard_for(
            "synthetic-alpha",
            connect=lambda: self.connect_as("synthetic-beta"),
        )
        with self.assertRaises(TenantSessionDenied):
            with guard.transaction("synthetic-alpha") as conn:
                conn.execute("INSERT INTO ea_cases VALUES ('must-not-run', 'synthetic')")
        with self.psycopg.connect(
            self.psycopg.conninfo.make_conninfo(DSN, dbname=self.databases["synthetic-beta"])
        ) as admin:
            self.assertEqual(admin.execute(
                "SELECT count(*) FROM ea_cases WHERE case_id = 'must-not-run'"
            ).fetchone()[0], 0)
        self.assertTrue(self.connections[-1].closed)

    def test_interrupted_write_rolls_back_cursor_and_reference_graph(self):
        tenant = "synthetic-alpha"
        case_id = "interrupt-" + uuid.uuid4().hex
        guard = self.guard_for(tenant)
        with self.assertRaises(RuntimeError):
            with guard.transaction(tenant) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO ea_cases VALUES (%s, %s)", (case_id, "synthetic"))
                    cursor.execute("INSERT INTO ea_source_cursors VALUES (%s, %s)", ("src-" + case_id, "advanced"))
                raise RuntimeError("synthetic interruption")
        with guard.transaction(tenant) as conn:
            self.assertEqual(conn.execute(
                "SELECT count(*) FROM ea_cases WHERE case_id = %s", (case_id,)
            ).fetchone()[0], 0)
            self.assertEqual(conn.execute(
                "SELECT count(*) FROM ea_source_cursors WHERE source_id = %s", ("src-" + case_id,)
            ).fetchone()[0], 0)

