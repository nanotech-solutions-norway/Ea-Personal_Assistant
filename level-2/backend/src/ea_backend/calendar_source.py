"""Google Calendar Events.list -> normalized EA projection, staging only.

The caller supplies a least-privileged authenticated events.list transport.
This module never obtains tokens, writes calendars, or schedules watches.
See the official Calendar events.list syncToken limitations.
"""
from __future__ import annotations

from datetime import date, datetime, time
from typing import Callable, Mapping, Any
from zoneinfo import ZoneInfo

from .provider_paging import SourcePage, CompletedObservation, collect_source_pages
from .unified_sync import SourceItem, SyncContractError


class CalendarTokenExpired(SyncContractError):
    """Provider reports expired synchronization token (HTTP 410)."""


def _due_at(event: Mapping[str, Any], *, default_timezone: str | None) -> tuple[str | None, str | None]:
    start = event.get("start")
    if not isinstance(start, dict):
        return None, None
    if isinstance(start.get("dateTime"), str) and start["dateTime"].strip():
        return start["dateTime"], start.get("timeZone") or default_timezone
    if isinstance(start.get("date"), str):
        tz = start.get("timeZone") or default_timezone
        if tz:
            try:
                dt = datetime.combine(date.fromisoformat(start["date"]), time.min, ZoneInfo(tz))
            except (ValueError, KeyError) as exc:
                raise SyncContractError("Invalid Calendar all-day date/timezone") from exc
            return dt.isoformat(), tz
    return None, None


def normalize_event(
    event: Mapping[str, Any], *,
    tenant_scope: str,
    calendar_id: str,
    calendar_timezone: str | None,
) -> SourceItem:
    if not isinstance(event, dict):
        raise SyncContractError("Malformed Calendar event")
    event_id, revision = event.get("id"), event.get("etag")
    if not isinstance(event_id, str) or not event_id.strip():
        raise SyncContractError("Calendar event missing ID")
    if not isinstance(revision, str) or not revision.strip():
        raise SyncContractError("Calendar event missing ETag")
    status = event.get("status")
    if status not in ("confirmed", "tentative", "cancelled"):
        raise SyncContractError("Unsupported Calendar event status")
    due, tz = _due_at(event, default_timezone=calendar_timezone)
    return SourceItem(
        tenant_scope=tenant_scope,
        source="google_calendar",
        source_id=event_id,
        revision=revision,
        state="deleted" if status == "cancelled" else "active",
        kind="calendar_event",
        title=event.get("summary") if status != "cancelled" else None,
        due_at=due if status != "cancelled" else None,
        timezone=tz if status != "cancelled" else None,
        collection_key=calendar_id,
    )


def collect_calendar_events(
    *,
    tenant_scope: str,
    calendar_id: str,
    calendar_timezone: str | None,
    list_events: Callable[[dict[str, str]], Mapping[str, Any]],
    sync_token: str | None = None,
    max_pages: int = 100,
) -> CompletedObservation:
    """Collect a complete Google Calendar event source observation.

    Initial call must not restrict by timeMin/timeMax. Incremental calls keep
    the same permitted parameters plus syncToken. On HTTP 410, upstream caller
    must perform a new complete full scan; NEVER clear state beforehand.
    """
    if not tenant_scope or not calendar_id:
        raise SyncContractError("Calendar tenant and calendar ID required")
    if sync_token is not None and not sync_token.strip():
        raise SyncContractError("Invalid sync token")

    def fetch_page(page_token: str | None) -> SourcePage:
        params = {"maxResults": "2500", "showDeleted": "true", "singleEvents": "false"}
        if sync_token is not None:
            params["syncToken"] = sync_token
        if page_token:
            params["pageToken"] = page_token
        try:
            result = list_events(params)
        except CalendarTokenExpired:
            raise
        if not isinstance(result, dict) or not isinstance(result.get("items"), list):
            raise SyncContractError("Invalid Calendar Events.list result")
        next_page = result.get("nextPageToken")
        next_sync = result.get("nextSyncToken")
        if next_page is not None and next_sync is not None:
            raise SyncContractError("Calendar page has both continuation and final sync token")
        items = tuple(normalize_event(e, tenant_scope=tenant_scope, calendar_id=calendar_id,
                                      calendar_timezone=calendar_timezone) for e in result["items"])
        return SourcePage(items=items, next_page_token=next_page, source_cursor=next_sync)

    return collect_source_pages(fetch_page, max_pages=max_pages)
