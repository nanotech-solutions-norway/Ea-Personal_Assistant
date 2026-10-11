"""Staging-only atomic sink for an Ea unified-source projection.

Provider workers and OAuth are deliberately NOT wired. A caller must supply
an authorized, fully paged provider observation. Run behind the EA policy
gateway and a private PostgreSQL database with tenant access controls.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Iterable

from .unified_sync import SourceItem, SyncContractError, plan_sync


class ConcurrentCursorError(SyncContractError):
    """The source cursor changed since the observed fetch began."""


class IncompleteObservationError(SyncContractError):
    """A partial provider result must never advance a source cursor."""


def cursor_scope(tenant: str, source: str, collection: str) -> str:
    if not all(isinstance(v, str) and v.strip() for v in (tenant, source, collection)):
        raise SyncContractError("Missing source cursor scope")
    value = "\x1f".join((tenant, source, collection))
    return "ea:sync:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


class PostgresProjectionSink:
    """Transactional data sink: no network provider calls and no external writes."""

    def __init__(self, dsn: str, *, connect: Callable[[str], Any]):
        if not dsn:
            raise ValueError("PostgreSQL DSN required")
        self._dsn = dsn
        self._connect = connect

    @classmethod
    def from_dsn(cls, dsn: str) -> "PostgresProjectionSink":
        import psycopg
        return cls(dsn, connect=psycopg.connect)

    def capture(
        self,
        *,
        run_id: str,
        tenant_scope: str,
        source: str,
        collection_key: str,
        mode: str,
        fetched: Iterable[SourceItem],
        expected_cursor: str | None,
        next_cursor: str,
        pages_fetched: int,
        all_pages_fetched: bool,
        complete_full_inventory: bool = False,
        operator_attested_snapshot: bool = False,
    ) -> int:
        if not run_id or not next_cursor or not isinstance(pages_fetched, int) or pages_fetched < 1:
            raise SyncContractError("Missing run ID, cursor or source pages")
        if not all_pages_fetched:
            raise IncompleteObservationError("Pagination incomplete; cursor not advanced")
        if complete_full_inventory and mode != "full":
            raise SyncContractError("Only a full observation can certify inventory completeness")
        scope = cursor_scope(tenant_scope, source, collection_key)
        conn = self._connect(self._dsn)
        try:
            with conn.cursor() as cur:
                # Serialize both first-run and subsequent same-scope updates.
                cur.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s, 0))", (scope,))
                cur.execute("SELECT cursor_value FROM ea_source_cursors WHERE source=%s FOR UPDATE", (scope,))
                observed = cur.fetchone()
                current = observed[0] if observed else None
                if current != expected_cursor:
                    raise ConcurrentCursorError("Source cursor stale: re-fetch before applying")

                cur.execute(
                    "SELECT source_id,source_revision,state,item_kind,display_title,due_at,timezone "
                    "FROM ea_unified_items WHERE tenant_scope=%s AND source=%s AND collection_key=%s",
                    (tenant_scope, source, collection_key),
                )
                existing = [
                    SourceItem(
                        tenant_scope=tenant_scope, source=source, source_id=row[0],
                        revision=row[1], state=row[2], kind=row[3], title=row[4],
                        due_at=row[5].isoformat() if hasattr(row[5], "isoformat") else row[5],
                        timezone=row[6], collection_key=collection_key,
                    ) for row in cur.fetchall()
                ]
                plan = plan_sync(
                    existing, tuple(fetched), tenant_scope=tenant_scope, source=source,
                    mode=mode, collection_complete=complete_full_inventory,
                    operator_attested_snapshot=operator_attested_snapshot,
                    collection_key=collection_key,
                )
                for record in (*plan.to_upsert, *plan.to_tombstone):
                    cur.execute(
                        "INSERT INTO ea_unified_items "
                        "(item_key,tenant_scope,source,collection_key,source_id,source_revision,item_kind,"
                        "state,display_title,due_at,timezone,last_verified_at,updated_at) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW()) "
                        "ON CONFLICT(item_key) DO UPDATE SET "
                        "source_revision=EXCLUDED.source_revision,item_kind=EXCLUDED.item_kind,"
                        "state=EXCLUDED.state,display_title=EXCLUDED.display_title,"
                        "due_at=EXCLUDED.due_at,timezone=EXCLUDED.timezone,"
                        "last_verified_at=NOW(),updated_at=NOW() "
                        "WHERE ea_unified_items.tenant_scope=EXCLUDED.tenant_scope "
                        "AND ea_unified_items.source=EXCLUDED.source "
                        "AND ea_unified_items.collection_key=EXCLUDED.collection_key "
                        "AND ea_unified_items.source_id=EXCLUDED.source_id",
                        (record.key, record.tenant_scope, record.source, collection_key, record.source_id,
                         record.revision, record.kind, record.state, record.title,
                         record.due_at, record.timezone),
                    )
                    cur.execute(
                        "SELECT source_revision,state FROM ea_unified_items "
                        "WHERE item_key=%s AND tenant_scope=%s AND source=%s AND collection_key=%s",
                        (record.key, tenant_scope, source, collection_key),
                    )
                    if cur.fetchone() != (record.revision, record.state):
                        raise SyncContractError("Projection readback mismatch; rolling back")

                meta = json.dumps({"source": source, "collection": collection_key}, sort_keys=True)
                cur.execute(
                    "INSERT INTO ea_source_cursors "
                    "(source,cursor_value,cursor_kind,valid,last_full_sync_at,"
                    "last_incremental_sync_at,metadata) "
                    "VALUES (%s,%s,%s,TRUE,CASE WHEN %s THEN NOW() ELSE NULL END,"
                    "NOW(),%s::jsonb) "
                    "ON CONFLICT(source) DO UPDATE SET cursor_value=EXCLUDED.cursor_value,"
                    "cursor_kind=EXCLUDED.cursor_kind,valid=TRUE,"
                    "last_full_sync_at=CASE WHEN %s THEN NOW() ELSE ea_source_cursors.last_full_sync_at END,"
                    "last_incremental_sync_at=NOW(),metadata=EXCLUDED.metadata",
                    (scope, next_cursor, mode, mode == "full", meta, mode == "full"),
                )
                cur.execute(
                    "INSERT INTO ea_sync_runs "
                    "(run_id,tenant_scope,source,collection_key,mode,status,pages_fetched,"
                    "collection_complete,items_changed,cursor_committed,completed_at) "
                    "VALUES (%s,%s,%s,%s,%s,'PERSISTED',%s,%s,%s,TRUE,NOW())",
                    (run_id, tenant_scope, source, collection_key, mode,
                     pages_fetched, complete_full_inventory, plan.changed),
                )
            conn.commit()
            return plan.changed
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
