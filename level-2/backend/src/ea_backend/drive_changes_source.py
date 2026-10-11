"""Read-only Google Drive changes.list collector for EA staging.

This module identifies changed file IDs, not resolved folder membership or
the current state of files. The worker must re-fetch permitted metadata and
reconcile Drive permissions before projecting data or tombstoning an item.
Only persist newStartPageToken after all pages and reconciliation succeed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .unified_sync import SyncContractError


class DriveChangeTokenInvalid(SyncContractError):
    """Drive change cursor rejected: require a new source-scoped baseline."""


@dataclass(frozen=True)
class DriveChangesObservation:
    changed_file_ids: tuple[str, ...]
    potentially_removed_file_ids: tuple[str, ...]
    next_start_page_token: str
    pages_fetched: int


def collect_drive_changes(
    *,
    start_page_token: str,
    list_changes: Callable[[dict[str, str]], Mapping[str, Any]],
    max_pages: int = 100,
    max_files: int = 10000,
) -> DriveChangesObservation:
    if not isinstance(start_page_token, str) or not start_page_token.strip():
        raise SyncContractError("Missing Drive starting page token")
    if not 1 <= max_pages <= 1000 or not 1 <= max_files <= 100000:
        raise SyncContractError("Invalid Drive changes limits")
    page_token = start_page_token
    seen: set[str] = {page_token}
    latest_state: dict[str, bool] = {}
    for page in range(1, max_pages + 1):
        request = {
            "pageToken": page_token,
            "pageSize": "1000",
            "includeRemoved": "true",
            "supportsAllDrives": "true",
        }
        response = list_changes(request)
        if not isinstance(response, dict) or not isinstance(response.get("changes"), list):
            raise SyncContractError("Malformed Drive changes response")
        for change in response["changes"]:
            if not isinstance(change, dict):
                raise SyncContractError("Malformed Drive change")
            if change.get("changeType", "file") != "file":
                raise SyncContractError("Non-file Drive changes require separate handling")
            fid = change.get("fileId")
            if not isinstance(fid, str) or not fid.strip():
                raise SyncContractError("Drive change missing fileId")
            removed = change.get("removed", False)
            if not isinstance(removed, bool):
                raise SyncContractError("Malformed Drive removal flag")
            # Last change for one file ID wins; never infer a deletion merely
            # because an item did not appear in the change feed.
            latest_state[fid] = removed
            if len(latest_state) > max_files:
                raise SyncContractError("Drive file cap exceeded")
        continuation = response.get("nextPageToken")
        if continuation is None:
            next_cursor = response.get("newStartPageToken")
            if not isinstance(next_cursor, str) or not next_cursor.strip():
                raise SyncContractError("Missing terminal newStartPageToken")
            changed = sorted(key for key, removed in latest_state.items() if not removed)
            removed = sorted(key for key, was_removed in latest_state.items() if was_removed)
            return DriveChangesObservation(tuple(changed), tuple(removed), next_cursor, page)
        if not isinstance(continuation, str) or not continuation.strip() or continuation in seen:
            raise SyncContractError("Invalid or cyclic Drive nextPageToken")
        seen.add(continuation)
        page_token = continuation
    raise SyncContractError("Drive changes pagination incomplete")
