"""Independent post-commit verification for EA's staging source projections.

Read an actual, separately opened database connection AFTER the sink commit.
Failures mean COMMITTED_STATE_UNVERIFIED, not that the commit was rolled back.
Never replay a provider update blindly after a verification failure.
This module performs no provider calls or external writes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from .projection_sink import cursor_scope
from .unified_sync import SourceItem, SyncContractError


class CommittedStateUnverified(SyncContractError):
    """Post-commit evidence is absent or inconsistent; reconcile before retry."""


@dataclass(frozen=True)
class ReadbackReceipt:
    run_id: str
    tenant_scope: str
    source: str
    collection_key: str
    verified_items: int
    persisted_changes: int
    # Intentionally omit provider cursor values from display/logs.


class PostgresProjectionVerifier:
    """Independent DB reader; configure a non-owner, no-BYPASSRLS credential."""

    def __init__(self, dsn: str, *, connect: Callable[[str], Any]):
        if not dsn:
            raise ValueError("PostgreSQL verification DSN required")
        self._dsn = dsn
        self._connect = connect

    @classmethod
    def from_dsn(cls, dsn: str) -> "PostgresProjectionVerifier":
        import psycopg
        return cls(dsn, connect=psycopg.connect)

    def verify(
        self,
        *,
        run_id: str,
        tenant_scope: str,
        source: str,
        collection_key: str,
        next_cursor: str,
        pages_fetched: int,
        changed: int,
        fetched: Iterable[SourceItem],
    ) -> ReadbackReceipt:
        if not run_id or not next_cursor or pages_fetched < 1 or changed < 0:
            raise CommittedStateUnverified("Readback identity or count invalid")
        scope = cursor_scope(tenant_scope, source, collection_key)
        observations = tuple(fetched)
        for item in observations:
            if (item.tenant_scope, item.source, item.collection_key) != (
                tenant_scope, source, collection_key
            ):
                raise CommittedStateUnverified("Observation scope mismatch")

        conn = self._connect(self._dsn)
        try:
            with conn.cursor() as cur:
                # Transaction-local tenant isolation also applies on readback.
                cur.execute("SELECT set_config('ea.tenant_scope', %s, true)", (tenant_scope,))
                cur.execute(
                    "SELECT status,pages_fetched,items_changed,cursor_committed "
                    "FROM ea_sync_runs WHERE run_id=%s AND tenant_scope=%s "
                    "AND source=%s AND collection_key=%s",
                    (run_id, tenant_scope, source, collection_key),
                )
                record = cur.fetchone()
                if record != ("PERSISTED", pages_fetched, changed, True):
                    raise CommittedStateUnverified("Post-commit run ledger mismatch")
                cur.execute(
                    "SELECT cursor_value,tenant_scope,collection_key,valid "
                    "FROM ea_source_cursors WHERE source=%s",
                    (scope,),
                )
                cursor_row = cur.fetchone()
                if cursor_row != (next_cursor, tenant_scope, collection_key, True):
                    raise CommittedStateUnverified("Post-commit cursor mismatch")
                verified = 0
                for item in observations:
                    cur.execute(
                        "SELECT source_revision,state FROM ea_unified_items "
                        "WHERE item_key=%s AND tenant_scope=%s AND source=%s "
                        "AND collection_key=%s",
                        (item.key, tenant_scope, source, collection_key),
                    )
                    row = cur.fetchone()
                    if row is None and item.state == "deleted":
                        # Unknown historical deletions need not become records.
                        continue
                    if row != (item.revision, item.state):
                        raise CommittedStateUnverified("Post-commit item mismatch")
                    verified += 1
            conn.rollback()  # read-only transaction; reset local tenant context
            return ReadbackReceipt(
                run_id=run_id, tenant_scope=tenant_scope,
                source=source, collection_key=collection_key,
                verified_items=verified, persisted_changes=changed,
            )
        except CommittedStateUnverified:
            conn.rollback()
            raise
        except Exception as exc:
            conn.rollback()
            raise CommittedStateUnverified("Post-commit readback unavailable") from exc
        finally:
            conn.close()
