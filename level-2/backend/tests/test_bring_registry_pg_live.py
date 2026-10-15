"""Real disposable PostgreSQL validation for Bring registry + FORCE RLS.

Uses ONLY fake tenants/customers/bookings; requires EA_TEST_DATABASE_URL.
"""

import hashlib
import hmac
import os
import pathlib
import sys
import unittest
import uuid
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ea_backend.bring_postgres_registry import PostgresBringRegistry, RegistrySecurityError

DSN = os.getenv("EA_TEST_DATABASE_URL", "")
ACTOR_ROLE = "ea_ci_bring_reader"
ISSUER = "https://login.microsoftonline.com/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa/v2.0"
KEY = b"synthetic-test-hmac-key-not-from-vault-32bytes-minimum"
VAULT_A = "https://synthetic.vault.azure.net/secrets/bring-a"
VAULT_B = "https://synthetic.vault.azure.net/secrets/bring-b"


@unittest.skipUnless(DSN, "Disposable PostgreSQL staging only")
class BringPostgresIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import psycopg
        cls.psycopg = psycopg
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                sql = (ROOT / "sql" / "006_bring_authorization_registry.sql").read_text()
                sql = "\n".join(
                    line for line in sql.splitlines()
                    if not line.lstrip().startswith("--")
                )
                for command in sql.split(";"):
                    if command.strip():
                        cur.execute(command)
                cur.execute(
                    "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ea_ci_bring_reader') "
                    "THEN CREATE ROLE ea_ci_bring_reader NOLOGIN; END IF; END $$"
                )
                cur.execute("GRANT USAGE ON SCHEMA public TO ea_ci_bring_reader")
                cur.execute(
                    "GRANT SELECT ON ea_bring_tenant_accounts, "
                    "ea_bring_principal_grants, ea_bring_shipment_provenance "
                    "TO ea_ci_bring_reader"
                )

    def setUp(self):
        suffix = uuid.uuid4().hex
        self.tenant_a = "synthetic-a-" + suffix
        self.tenant_b = "synthetic-b-" + suffix
        self.subject_a = "synthetic-subject-a-" + suffix
        self.subject_b = "synthetic-subject-b-" + suffix
        self.reference_a = "FAKEPARCEL1234"
        self.reference_b = "FAKEPARCEL5678"
        self.customer_a = "999111222"
        self.customer_b = "111999888"
        self.when = datetime.now(timezone.utc) - timedelta(days=1)
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                for tenant, customer, vault, subject, reference in (
                    (self.tenant_a, self.customer_a, VAULT_A, self.subject_a, self.reference_a),
                    (self.tenant_b, self.customer_b, VAULT_B, self.subject_b, self.reference_b),
                ):
                    cur.execute(
                        "INSERT INTO ea_bring_tenant_accounts "
                        "(tenant_scope, customer_number, vault_secret_ref, active) "
                        "VALUES (%s,%s,%s,TRUE)",
                        (tenant, customer, vault),
                    )
                    cur.execute(
                        "INSERT INTO ea_bring_principal_grants "
                        "(issuer,subject,tenant_scope,permission,customer_number,active) "
                        "VALUES (%s,%s,%s,'bring.tracking.read',%s,TRUE)",
                        (ISSUER, subject, tenant, customer),
                    )
                    digest = hmac.new(
                        KEY, (tenant + "\x1f" + reference).encode(), hashlib.sha256
                    ).hexdigest()
                    cur.execute(
                        "INSERT INTO ea_bring_shipment_provenance "
                        "(tenant_scope,tracking_digest,customer_number,evidence_source,"
                        "reviewed_at,independently_approved) "
                        "VALUES (%s,%s,%s,'authenticated_mybring_booking',%s,TRUE)",
                        (tenant, digest, customer, self.when),
                    )

    def role_factory(self):
        def open_connection():
            conn = self.psycopg.connect(DSN)
            try:
                with conn.cursor() as cur:
                    cur.execute("SET ROLE ea_ci_bring_reader")
                conn.commit()
                return conn
            except Exception:
                conn.close()
                raise
        return open_connection

    def registry(self, *, tenant=None, subject=None, factory=None, key=KEY):
        return PostgresBringRegistry(
            connection_factory=factory or self.role_factory(),
            actor_issuer=ISSUER,
            actor_subject=subject or self.subject_a,
            tenant_scope=tenant or self.tenant_a,
            tracking_hmac_key=key,
        )

    def test_actor_a_can_read_only_a_grant_account_and_booking(self):
        a = self.registry()
        self.assertEqual(a.principal_grant(ISSUER, self.subject_a).tenant_scope, self.tenant_a)
        self.assertEqual(a.tenant_account(self.tenant_a).vault_secret_ref, VAULT_A)
        self.assertEqual(
            a.shipment_provenance(self.tenant_a, self.reference_a).customer_number,
            self.customer_a,
        )

    def test_actor_b_can_read_only_b(self):
        b = self.registry(tenant=self.tenant_b, subject=self.subject_b)
        self.assertEqual(b.principal_grant(ISSUER, self.subject_b).tenant_scope, self.tenant_b)
        self.assertEqual(b.tenant_account(self.tenant_b).vault_secret_ref, VAULT_B)
        self.assertIsNone(b.shipment_provenance(self.tenant_b, self.reference_a))

    def test_actor_a_cannot_fetch_b_by_setting_tenant(self):
        a = self.registry()
        self.assertIsNone(a.tenant_account(self.tenant_b))
        self.assertIsNone(a.shipment_provenance(self.tenant_b, self.reference_b))
        self.assertIsNone(a.principal_grant(ISSUER, self.subject_b))

    def test_actor_b_cannot_fetch_a(self):
        b = self.registry(tenant=self.tenant_b, subject=self.subject_b)
        self.assertIsNone(b.tenant_account(self.tenant_a))
        self.assertIsNone(b.shipment_provenance(self.tenant_a, self.reference_a))
        self.assertIsNone(b.principal_grant(ISSUER, self.subject_a))

    def test_actor_a_claiming_b_tenant_has_no_row(self):
        mismatch = self.registry(tenant=self.tenant_b, subject=self.subject_a)
        self.assertIsNone(mismatch.principal_grant(ISSUER, self.subject_a))
        self.assertIsNone(mismatch.tenant_account(self.tenant_b))
        self.assertIsNone(mismatch.shipment_provenance(self.tenant_b, self.reference_b))

    def test_missing_transaction_context_sees_nothing(self):
        with self.role_factory()() as conn:
            with conn.cursor() as cur:
                for table in (
                    "ea_bring_tenant_accounts",
                    "ea_bring_principal_grants",
                    "ea_bring_shipment_provenance",
                ):
                    cur.execute("SELECT count(*) FROM " + table)
                    self.assertEqual(cur.fetchone()[0], 0)

    def test_reader_cannot_insert_or_update_customer_records(self):
        with self.role_factory()() as conn:
            with conn.cursor() as cur:
                with self.assertRaises(self.psycopg.errors.InsufficientPrivilege):
                    cur.execute(
                        "INSERT INTO ea_bring_tenant_accounts "
                        "(tenant_scope,customer_number,vault_secret_ref) "
                        "VALUES ('forged','999111222',%s)",
                        (VAULT_A,),
                    )

    def test_reader_cannot_disable_rls(self):
        with self.role_factory()() as conn:
            with conn.cursor() as cur:
                with self.assertRaises(self.psycopg.errors.InsufficientPrivilege):
                    cur.execute("ALTER TABLE ea_bring_tenant_accounts DISABLE ROW LEVEL SECURITY")

    def test_plaintext_tracking_reference_not_persisted(self):
        with self.psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT tracking_digest FROM ea_bring_shipment_provenance "
                    "WHERE tenant_scope=%s",
                    (self.tenant_a,)
                )
                digest = cur.fetchone()[0]
        self.assertEqual(len(digest), 64)
        self.assertNotIn(self.reference_a, digest)

    def test_wrong_hmac_key_cannot_find_shipments(self):
        other = self.registry(key=b"other-synthetic-key-has-32-or-more-safe-bytes")
        self.assertIsNone(other.shipment_provenance(self.tenant_a, self.reference_a))

    def test_privileged_db_user_rejected_by_adapter(self):
        unsafe = self.registry(factory=lambda: self.psycopg.connect(DSN))
        with self.assertRaisesRegex(RegistrySecurityError, "privileged role"):
            unsafe.tenant_account(self.tenant_a)


if __name__ == "__main__":
    unittest.main()
