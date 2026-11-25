"""Synthetic-only EA CRM controls; no provider adapter or deployment is included.

The SQLite event store and lease are suitable for deterministic local testing when
all participants share one durable database file. A scheduled host must separately
prove that such a persistent shared path is available before using this adapter.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping


class EventConflict(RuntimeError):
    """The same idempotency key was reused with different event content."""


class LeaseBusy(RuntimeError):
    """Another unexpired worker owns this workstream lease."""


class StaleLease(RuntimeError):
    """A release was attempted with a stale or incorrect lease token."""


class UnsafeEvent(RuntimeError):
    """An event contains a prohibited payload field or lacks required metadata."""


_REQUIRED_EVENT_FIELDS = {
    "event_id", "work_id", "timestamp_utc", "phase", "action_tier",
    "source_sha", "target_reference", "attempt", "idempotency_key",
    "event_status",
}
_FORBIDDEN_KEYS = {
    "body", "email_body", "customer_email", "customer_name", "customer_data",
    "raw_email", "attachment_bytes", "password", "token", "secret", "api_key",
}


def _check_redacted(value: object, path: str = "event") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in _FORBIDDEN_KEYS:
                raise UnsafeEvent(f"prohibited event field at {path}.{key}")
            _check_redacted(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _check_redacted(child, f"{path}[{index}]")


def _canonical_json(event: Mapping[str, object]) -> str:
    missing = _REQUIRED_EVENT_FIELDS - set(event)
    if missing:
        raise UnsafeEvent(f"missing required event fields: {sorted(missing)}")
    _check_redacted(event)
    return json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class DurableEventLog:
    """Append-only, hash-chained event log with atomic idempotency enforcement."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    work_id TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    previous_sha256 TEXT NOT NULL,
                    entry_sha256 TEXT NOT NULL,
                    UNIQUE(work_id, idempotency_key)
                );
                CREATE TRIGGER IF NOT EXISTS events_no_update
                BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'append-only ledger'); END;
                CREATE TRIGGER IF NOT EXISTS events_no_delete
                BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'append-only ledger'); END;
                CREATE TABLE IF NOT EXISTS leases (
                    work_id TEXT PRIMARY KEY,
                    token TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    acquired_at REAL NOT NULL,
                    expires_at REAL NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        db.execute("PRAGMA busy_timeout=15000")
        return db

    @contextmanager
    def _database(self):
        db = self._connect()
        try:
            yield db
        finally:
            db.close()

    def append(self, event: Mapping[str, object]) -> tuple[bool, str]:
        payload = _canonical_json(event)
        payload_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        with self._database() as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute(
                "SELECT payload_sha256, entry_sha256 FROM events WHERE event_id=? OR (work_id=? AND idempotency_key=?)",
                (str(event["event_id"]), str(event["work_id"]), str(event["idempotency_key"])),
            ).fetchone()
            if existing:
                if existing["payload_sha256"] != payload_sha:
                    db.rollback()
                    raise EventConflict("idempotency key already records different content")
                db.commit()
                return False, str(existing["entry_sha256"])
            previous = db.execute(
                "SELECT entry_sha256 FROM events ORDER BY seq DESC LIMIT 1"
            ).fetchone()
            previous_sha = str(previous["entry_sha256"]) if previous else "0" * 64
            entry_sha = hashlib.sha256(
                (previous_sha + payload_sha).encode("ascii")
            ).hexdigest()
            db.execute(
                "INSERT INTO events(event_id,work_id,idempotency_key,payload,payload_sha256,previous_sha256,entry_sha256) VALUES(?,?,?,?,?,?,?)",
                (str(event["event_id"]), str(event["work_id"]), str(event["idempotency_key"]), payload, payload_sha, previous_sha, entry_sha),
            )
            db.commit()
            return True, entry_sha

    def acquire(self, work_id: str, owner: str, *, ttl_seconds: int = 300, now: float | None = None) -> str:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        moment = time.time() if now is None else now
        token = secrets.token_urlsafe(24)
        with self._database() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT token, expires_at FROM leases WHERE work_id=?", (work_id,)).fetchone()
            if row and float(row["expires_at"]) > moment:
                db.rollback()
                raise LeaseBusy(work_id)
            db.execute(
                "INSERT INTO leases(work_id,token,owner,acquired_at,expires_at) VALUES(?,?,?,?,?) "
                "ON CONFLICT(work_id) DO UPDATE SET token=excluded.token,owner=excluded.owner,acquired_at=excluded.acquired_at,expires_at=excluded.expires_at",
                (work_id, token, owner, moment, moment + ttl_seconds),
            )
            db.commit()
        return token

    def release(self, work_id: str, token: str) -> None:
        with self._database() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT token FROM leases WHERE work_id=?", (work_id,)).fetchone()
            if not row or not secrets.compare_digest(str(row["token"]), token):
                db.rollback()
                raise StaleLease(work_id)
            db.execute("DELETE FROM leases WHERE work_id=?", (work_id,))
            db.commit()

    def renew(self, work_id: str, token: str, *, ttl_seconds: int = 300, now: float | None = None) -> float:
        """Extend a still-current lease; an expired lease cannot be resurrected."""
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        moment = time.time() if now is None else now
        with self._database() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT token, expires_at FROM leases WHERE work_id=?", (work_id,)).fetchone()
            if not row or float(row["expires_at"]) <= moment or not secrets.compare_digest(str(row["token"]), token):
                db.rollback()
                raise StaleLease(work_id)
            expires_at = moment + ttl_seconds
            db.execute("UPDATE leases SET expires_at=? WHERE work_id=?", (expires_at, work_id))
            db.commit()
            return expires_at

    def lease_is_current(self, work_id: str, token: str, *, now: float | None = None) -> bool:
        """Read-only guard for local callers before a bounded operation."""
        moment = time.time() if now is None else now
        with self._database() as db:
            row = db.execute("SELECT token, expires_at FROM leases WHERE work_id=?", (work_id,)).fetchone()
        return bool(row and float(row["expires_at"]) > moment and secrets.compare_digest(str(row["token"]), token))

    def event_count(self) -> int:
        with self._database() as db:
            return int(db.execute("SELECT COUNT(*) FROM events").fetchone()[0])

    def verify_chain(self) -> bool:
        """Check payload digests and append order without mutating the ledger."""
        previous = "0" * 64
        with self._database() as db:
            rows = db.execute(
                "SELECT payload,payload_sha256,previous_sha256,entry_sha256 FROM events ORDER BY seq"
            ).fetchall()
        for row in rows:
            payload = str(row["payload"])
            payload_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            if payload_sha != row["payload_sha256"] or previous != row["previous_sha256"]:
                return False
            expected = hashlib.sha256((previous + payload_sha).encode("ascii")).hexdigest()
            if expected != row["entry_sha256"]:
                return False
            previous = expected
        return True


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    reference: str
    status: str = "VERIFIED"


@dataclass(frozen=True)
class PreflightResult:
    status: str
    provider_results: tuple[CheckResult, ...]
    authority_result: CheckResult | None
    blocked_at: str | None


def provider_first_preflight(
    provider_checks: Iterable[tuple[str, Callable[[], CheckResult]]],
    authority_check: Callable[[], CheckResult],
) -> PreflightResult:
    """Run current provider identity/read checks before secondary authority lookup.

    This function is read-only. A successful result is a preflight signal, not
    authorization to mutate a provider or evidence that a scheduler is deployed.
    """
    checks = tuple(provider_checks)
    if not checks:
        return PreflightResult("BLOCKED", (), None, "NO_PROVIDER_CHECKS")
    provider_results: list[CheckResult] = []
    for name, check in checks:
        try:
            result = check()
        except Exception:
            return PreflightResult("BLOCKED", tuple(provider_results), None, f"PROVIDER_ERROR:{name}")
        provider_results.append(result)
        if not result.ok:
            return PreflightResult("BLOCKED", tuple(provider_results), None, f"PROVIDER_NOT_VERIFIED:{name}")
    try:
        authority_result = authority_check()
    except Exception:
        return PreflightResult("BLOCKED", tuple(provider_results), None, "AUTHORITY_ERROR")
    if not authority_result.ok:
        return PreflightResult("BLOCKED", tuple(provider_results), authority_result, "AUTHORITY_NOT_VERIFIED")
    return PreflightResult("PREFLIGHT_VERIFIED", tuple(provider_results), authority_result, None)
