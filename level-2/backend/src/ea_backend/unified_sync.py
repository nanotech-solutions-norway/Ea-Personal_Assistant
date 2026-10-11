"""Deterministic read-only cross-source projection planner for Ea.

This module performs NO provider I/O and NO writes. Caller must enforce
source authorization, atomic persistence, cursor advancement and readback.
Do not place production payloads in GitHub or Drive.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, Literal

SourceName = Literal["google_calendar", "gmail", "github", "google_drive", "chatgpt_tasks", "chatgpt_projects"]
Mode = Literal["full", "incremental"]

API_SOURCES = frozenset({"google_calendar", "gmail", "github", "google_drive"})
MANUAL_ONLY_SOURCES = frozenset({"chatgpt_tasks", "chatgpt_projects"})
ALL_SOURCES = API_SOURCES | MANUAL_ONLY_SOURCES
STATES = frozenset({"active", "deleted"})


class SyncContractError(ValueError):
    """Invalid or unverified input: fail closed without changing a cursor."""


@dataclass(frozen=True)
class SourceItem:
    """Minimal source projection. Store only in an access-controlled runtime DB."""

    tenant_scope: str
    source: str
    source_id: str
    revision: str
    state: str = "active"
    kind: str = "commitment"
    title: str | None = None
    due_at: str | None = None
    timezone: str | None = None

    @property
    def key(self) -> str:
        return source_key(self.tenant_scope, self.source, self.source_id)


@dataclass(frozen=True)
class SyncPlan:
    tenant_scope: str
    source: str
    mode: str
    to_upsert: tuple[SourceItem, ...]
    to_tombstone: tuple[SourceItem, ...]
    unchanged: int
    full_collection_complete: bool

    @property
    def changed(self) -> int:
        return len(self.to_upsert) + len(self.to_tombstone)


def source_key(tenant_scope: str, source: str, source_id: str) -> str:
    """Stable opaque key; identity includes tenant and provider namespace."""
    if not all(isinstance(v, str) and v.strip() for v in (tenant_scope, source, source_id)):
        raise SyncContractError("Tenant, provider and source ID must be nonempty strings")
    payload = "\x1f".join((tenant_scope, source, source_id))
    return sha256(payload.encode("utf-8")).hexdigest()


def _validate(item: SourceItem, tenant_scope: str, source: str) -> None:
    if item.tenant_scope != tenant_scope or item.source != source:
        raise SyncContractError("Cross-tenant or cross-provider projection rejected")
    if not item.source_id.strip() or not item.revision.strip():
        raise SyncContractError("Missing source identity or revision")
    if item.state not in STATES:
        raise SyncContractError("Unsupported source state")


def plan_sync(
    existing: Iterable[SourceItem],
    fetched: Iterable[SourceItem],
    *,
    tenant_scope: str,
    source: str,
    mode: Mode,
    collection_complete: bool = False,
    operator_attested_snapshot: bool = False,
) -> SyncPlan:
    """Plan idempotent provider-scoped changes; never run external writes.

    Caller fetches every relevant page, validates authorization/freshness, then
    supplies completed observations. An empty/partial response must not erase
    active state. Deleted objects require an explicit tombstone, or a genuinely
    complete full-provider projection. Cross-platform links require independent
    case evidence and are deliberately never inferred from matching titles.
    """
    if source not in ALL_SOURCES or mode not in ("full", "incremental"):
        raise SyncContractError("Unsupported source or synchronization mode")
    if source in MANUAL_ONLY_SOURCES and not operator_attested_snapshot:
        raise SyncContractError("ChatGPT task/Project APIs not established: manual snapshot required")
    if not tenant_scope or not tenant_scope.strip():
        raise SyncContractError("Missing tenant scope")
    if collection_complete and mode != "full":
        raise SyncContractError("Completion-based deletion is only valid for full sync")

    old: dict[str, SourceItem] = {}
    for item in existing:
        _validate(item, tenant_scope, source)
        if item.key in old and old[item.key] != item:
            raise SyncContractError("Conflicting existing identities")
        old[item.key] = item

    new: dict[str, SourceItem] = {}
    for item in fetched:
        _validate(item, tenant_scope, source)
        if item.key in new and new[item.key] != item:
            raise SyncContractError("Conflicting revisions for one source item")
        new[item.key] = item

    upserts: list[SourceItem] = []
    tombstones: list[SourceItem] = []
    unchanged = 0
    for key, item in sorted(new.items()):
        prior = old.get(key)
        if prior == item:
            unchanged += 1
            continue
        if prior is not None and prior.revision == item.revision:
            raise SyncContractError("Changed data under the same source revision")
        if item.state == "deleted":
            if prior is not None and prior.state != "deleted":
                tombstones.append(item)
            else:
                unchanged += 1
        else:
            upserts.append(item)

    # Only complete, unfiltered full scans may infer deletion by absence.
    # A caller must never set collection_complete for a time-windowed Calendar
    # search, Drive folder listing, GitHub issue search or a paginated result.
    if mode == "full" and collection_complete:
        for key, prior in sorted(old.items()):
            if key not in new and prior.state == "active":
                tombstones.append(SourceItem(
                    tenant_scope=prior.tenant_scope,
                    source=prior.source,
                    source_id=prior.source_id,
                    revision="missing-from-complete-full-scan:" + prior.revision,
                    state="deleted",
                    kind=prior.kind,
                ))
    return SyncPlan(
        tenant_scope=tenant_scope,
        source=source,
        mode=mode,
        to_upsert=tuple(upserts),
        to_tombstone=tuple(tombstones),
        unchanged=unchanged,
        full_collection_complete=collection_complete,
    )
