from __future__ import annotations

import json
from typing import Any, Callable

from .events import EventEnvelope


ConnectFn = Callable[[str], Any]


class PostgresEventStore:
    """Durable PostgreSQL EventStore implementation.

    The connection function is injected for testability. Use from_dsn() in a
    deployment with psycopg installed.
    """

    durable = True

    def __init__(self, dsn: str, *, connect: ConnectFn) -> None:
        if not dsn:
            raise ValueError("PostgreSQL DSN is required")
        self._dsn = dsn
        self._connect = connect

    @classmethod
    def from_dsn(cls, dsn: str) -> "PostgresEventStore":
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("psycopg is required for PostgresEventStore.from_dsn") from exc
        return cls(dsn, connect=psycopg.connect)

    def put_if_absent(self, event: EventEnvelope) -> bool:
        sql = """
            INSERT INTO ea_ingest_events (
                event_id, source, cursor_value, resource_key, event_kind,
                received_at, metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (event_id) DO NOTHING
            RETURNING event_id
        """
        params = (
            event.event_id,
            event.source,
            event.cursor,
            event.resource_key,
            event.event_kind,
            event.received_at,
            json.dumps(event.metadata, sort_keys=True, separators=(",", ":")),
        )
        conn = self._connect(self._dsn)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                inserted = cur.fetchone() is not None
            conn.commit()
            return inserted
        except Exception:
            try:
                conn.rollback()
            finally:
                raise
        finally:
            conn.close()

    def healthcheck(self) -> bool:
        conn = self._connect(self._dsn)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                row = cur.fetchone()
            return bool(row and row[0] == 1)
        except Exception:
            return False
        finally:
            conn.close()
