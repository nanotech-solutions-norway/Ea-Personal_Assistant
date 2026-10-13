"""One bounded read-only Google Calendar -> PostgreSQL staging synchronization.

Call ONLY behind an authenticated account/tenant authorization boundary.
The transport is injected by a separate provider credential layer; it must
be Calendar events.list read-only. No watch registration, invitations, edits,
mail sends or autonomous resync after an expired token are supported.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol

from .calendar_source import collect_calendar_events
from .postcommit_readback import ReadbackReceipt
from .unified_sync import SyncContractError


@dataclass(frozen=True)
class AuthorizedCalendarScope:
    tenant_scope: str
    calendar_id: str
    calendar_timezone: str | None

    def validate(self) -> None:
        if not isinstance(self.tenant_scope, str) or not self.tenant_scope.strip():
            raise SyncContractError("Tenant authorization missing")
        if not isinstance(self.calendar_id, str) or not self.calendar_id.strip():
            raise SyncContractError("Calendar authorization missing")


class ProjectionSink(Protocol):
    def capture(self, **kwargs: Any) -> int: ...


class ReadbackVerifier(Protocol):
    def verify(self, **kwargs: Any) -> ReadbackReceipt: ...


def synchronize_calendar_staging(
    *,
    scope: AuthorizedCalendarScope,
    run_id: str,
    list_events: Callable[[dict[str, str]], Mapping[str, Any]],
    sink: ProjectionSink,
    verifier: ReadbackVerifier,
    expected_cursor: str | None,
    mode: str,
    max_pages: int = 100,
) -> ReadbackReceipt:
    """Return success ONLY after durable write and independent readback.

    `mode="full"` allows a first read or a separately authorized 410
    recovery. Never infer deletions from absence without audited evidence
    that the unfiltered, authorized provider inventory is complete.
    `mode="incremental"` requires the prior committed sync token.
    `expected_cursor` MUST come from an authenticated scoped cursor read,
    not from notification payloads. A concurrent cursor mismatch is a
    re-fetch/reconcile condition; no automatic retry here.
    """
    scope.validate()
    if not isinstance(run_id, str) or not run_id.strip():
        raise SyncContractError("Run identifier required")
    if mode not in {"full", "incremental"}:
        raise SyncContractError("Invalid Calendar synchronization mode")
    if mode == "incremental" and (
        not isinstance(expected_cursor, str) or not expected_cursor.strip()
    ):
        raise SyncContractError("Incremental scan requires a committed cursor")
    if not callable(list_events) or sink is None or verifier is None:
        raise SyncContractError("Provider transport, sink and readback required")

    observation = collect_calendar_events(
        tenant_scope=scope.tenant_scope,
        calendar_id=scope.calendar_id,
        calendar_timezone=scope.calendar_timezone,
        list_events=list_events,
        sync_token=expected_cursor if mode == "incremental" else None,
        max_pages=max_pages,
    )
    # Materialize once before calling independent sink / verifier. If the
    # source scan raises, neither persistence nor readback is attempted.
    fetched = observation.items
    changed = sink.capture(
        run_id=run_id, tenant_scope=scope.tenant_scope,
        source="google_calendar", collection_key=scope.calendar_id,
        mode=mode, fetched=fetched, expected_cursor=expected_cursor,
        next_cursor=observation.source_cursor,
        pages_fetched=observation.pages_fetched, all_pages_fetched=True,
        complete_full_inventory=False,
    )
    # A verification error means the commit MAY ALREADY EXIST. Do not rerun
    # the same provider fetch without first reconciling the committed cursor.
    return verifier.verify(
        run_id=run_id, tenant_scope=scope.tenant_scope,
        source="google_calendar", collection_key=scope.calendar_id,
        next_cursor=observation.source_cursor,
        pages_fetched=observation.pages_fetched,
        changed=changed, fetched=fetched,
    )
