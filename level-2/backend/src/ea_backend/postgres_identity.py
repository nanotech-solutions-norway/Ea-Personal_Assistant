"""Read-only PostgreSQL identity adapter for the optional Path S guard.

Uses fixed catalog SELECTs on the supplied already-open trusted connection.
Does not connect, alter roles/ACLs, certify deployment, or wire the live runtime.
Default DB-API tuple rows are required; malformed evidence fails closed.
"""
from .single_tenant_session import EffectiveDatabaseIdentity, TenantSessionDenied

IDENTITY_SQL = (
    "SELECT pg_catalog.current_database(), current_user, r.rolsuper, r.rolbypassrls, "
    "EXISTS (SELECT 1 FROM pg_catalog.pg_class AS c "
    "JOIN pg_catalog.pg_namespace AS n ON n.oid = c.relnamespace "
    "WHERE n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg_toast%' AND c.relkind IN ('r', 'p') "
    "AND pg_catalog.pg_has_role(current_user, c.relowner, 'MEMBER')) "
    "FROM pg_catalog.pg_roles AS r WHERE r.rolname = current_user"
)
OTHER_CONNECT_SQL = (
    "SELECT datname FROM pg_catalog.pg_database "
    "WHERE datallowconn AND datname <> pg_catalog.current_database() "
    "AND pg_catalog.has_database_privilege(current_user, datname, 'CONNECT')"
)


def read_postgres_identity(connection):
    """Return a fresh catalog snapshot; never treat it as immutable IAM proof.

    Ownership covers all non-system tables (including named schemas) and
    all owner-role membership, including NOINHERIT potential SET ROLE access.
    This deliberately rejects membership even when current USAGE is false.
    All connectable peer databases are included, including built-ins.
    Database policy may change after observation; database-enforced permissions
    and independent protected runtime acceptance remain required.
    """
    with connection.cursor() as cursor:
        cursor.execute(IDENTITY_SQL)
        row = cursor.fetchone()
        if (type(row) is not tuple or len(row) != 5
                or not all(type(v) is str and v.strip() for v in row[:2])
                or not all(type(v) is bool for v in row[2:])):
            raise TenantSessionDenied('postgres_identity_readback_invalid')
        cursor.execute(OTHER_CONNECT_SQL)
        peer_rows = cursor.fetchall()
        if type(peer_rows) not in (list, tuple) or not all(
                type(peer) is tuple and len(peer) == 1
                and type(peer[0]) is str and peer[0].strip() for peer in peer_rows):
            raise TenantSessionDenied('postgres_connect_readback_invalid')
    return EffectiveDatabaseIdentity(row[0], row[1], row[2], row[3], row[4],
                                     frozenset(peer[0] for peer in peer_rows))
