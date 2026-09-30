from __future__ import annotations

import json
from io import BytesIO
from typing import Callable, Iterable

from preflight import check
from .events import EventValidationError, parse_calendar_headers, parse_gmail_pubsub
from .store import EventStore


StartResponse = Callable[[str, list[tuple[str, str]]], None]


def _response(start_response: StartResponse, status: str, payload: dict) -> Iterable[bytes]:
    body = json.dumps(payload, sort_keys=True).encode("utf-8")
    start_response(status, [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-store"),
    ])
    return [body]


def _read_json(environ: dict) -> dict:
    try:
        size = int(environ.get("CONTENT_LENGTH") or "0")
    except ValueError as exc:
        raise EventValidationError("invalid Content-Length") from exc
    if size <= 0 or size > 1_048_576:
        raise EventValidationError("invalid request body size")
    stream = environ.get("wsgi.input")
    if not hasattr(stream, "read"):
        raise EventValidationError("missing request body")
    raw = stream.read(size)
    try:
        value = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise EventValidationError("invalid JSON") from exc
    if not isinstance(value, dict):
        raise EventValidationError("JSON body must be an object")
    return value


def create_app(*, store: EventStore | None = None, env: dict[str, str] | None = None):
    preflight = check(env)

    def application(environ: dict, start_response: StartResponse):
        path = environ.get("PATH_INFO", "")
        method = environ.get("REQUEST_METHOD", "GET").upper()

        if path == "/healthz":
            return _response(start_response, "200 OK", {"status": "ok", "level": "2A"})

        if path == "/readyz":
            ready = bool(preflight.ready and store is not None)
            status = "200 OK" if ready else "503 Service Unavailable"
            return _response(start_response, status, {
                "ready": ready,
                "preflight_ready": preflight.ready,
                "durable_store_attached": store is not None,
                "missing": list(preflight.missing),
                "unsafe_flags": list(preflight.unsafe_flags),
            })

        if method != "POST":
            return _response(start_response, "405 Method Not Allowed", {"error": "method_not_allowed"})

        if store is None or not preflight.ready:
            return _response(start_response, "503 Service Unavailable", {
                "error": "runtime_not_ready",
                "preflight_ready": preflight.ready,
                "durable_store_attached": store is not None,
            })

        try:
            if path == "/hooks/gmail":
                event = parse_gmail_pubsub(_read_json(environ))
            elif path == "/hooks/calendar":
                headers = {
                    key[5:].replace("_", "-"): value
                    for key, value in environ.items()
                    if key.startswith("HTTP_")
                }
                event = parse_calendar_headers(headers)
            else:
                return _response(start_response, "404 Not Found", {"error": "not_found"})
        except EventValidationError as exc:
            return _response(start_response, "400 Bad Request", {"error": str(exc)})

        inserted = store.put_if_absent(event)
        return _response(start_response, "204 No Content" if inserted else "200 OK", {
            "accepted": True,
            "duplicate": not inserted,
            "event_id": event.event_id,
            "source": event.source,
        })

    return application
