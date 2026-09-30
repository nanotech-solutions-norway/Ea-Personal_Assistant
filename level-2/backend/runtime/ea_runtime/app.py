from __future__ import annotations

import json
from typing import Callable, Iterable

from preflight import check
from .auth import RequestAuthenticator
from .events import EventValidationError, parse_calendar_headers, parse_gmail_pubsub
from .store import EventStore


StartResponse = Callable[[str, list[tuple[str, str]]], None]


def _response(start_response: StartResponse, status: str, payload: dict | None = None) -> Iterable[bytes]:
    if status.startswith("204"):
        start_response(status, [("Cache-Control", "no-store")])
        return [b""]
    body = json.dumps(payload or {}, sort_keys=True).encode("utf-8")
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


def create_app(
    *,
    store: EventStore | None = None,
    authenticator: RequestAuthenticator | None = None,
    env: dict[str, str] | None = None,
):
    values = dict(env or {})
    preflight = check(values)
    is_test = values.get("EA_ENV", "").strip().lower() == "test"

    def store_ready() -> bool:
        if store is None:
            return False
        if is_test and not getattr(store, "durable", False):
            return True
        if not getattr(store, "durable", False):
            return False
        healthcheck = getattr(store, "healthcheck", None)
        if callable(healthcheck):
            try:
                return bool(healthcheck())
            except Exception:
                return False
        return True

    def auth_ready() -> bool:
        if authenticator is None:
            return False
        return bool(getattr(authenticator, "production_safe", False) or is_test)

    def runtime_ready() -> bool:
        return bool(preflight.ready and store_ready() and auth_ready())

    def application(environ: dict, start_response: StartResponse):
        path = environ.get("PATH_INFO", "")
        method = environ.get("REQUEST_METHOD", "GET").upper()

        if path == "/healthz":
            return _response(start_response, "200 OK", {"status": "ok", "level": "2A"})

        if path == "/readyz":
            s_ready = store_ready()
            a_ready = auth_ready()
            ready = bool(preflight.ready and s_ready and a_ready)
            status = "200 OK" if ready else "503 Service Unavailable"
            return _response(start_response, status, {
                "ready": ready,
                "preflight_ready": preflight.ready,
                "durable_store_ready": s_ready,
                "authenticated_delivery_ready": a_ready,
                "missing": list(preflight.missing),
                "unsafe_flags": list(preflight.unsafe_flags),
            })

        if method != "POST":
            return _response(start_response, "405 Method Not Allowed", {"error": "method_not_allowed"})

        if not runtime_ready():
            return _response(start_response, "503 Service Unavailable", {
                "error": "runtime_not_ready"
            })

        if path == "/hooks/gmail":
            source = "gmail"
        elif path == "/hooks/calendar":
            source = "google_calendar"
        else:
            return _response(start_response, "404 Not Found", {"error": "not_found"})

        if not authenticator.authorize(environ, source=source):
            return _response(start_response, "401 Unauthorized", {"error": "unauthenticated_delivery"})

        try:
            if source == "gmail":
                event = parse_gmail_pubsub(_read_json(environ))
            else:
                headers = {
                    key[5:].replace("_", "-"): value
                    for key, value in environ.items()
                    if key.startswith("HTTP_")
                }
                event = parse_calendar_headers(headers)
        except EventValidationError as exc:
            return _response(start_response, "400 Bad Request", {"error": str(exc)})

        inserted = store.put_if_absent(event)
        if inserted:
            return _response(start_response, "204 No Content")
        return _response(start_response, "200 OK", {
            "accepted": True,
            "duplicate": True,
            "event_id": event.event_id,
            "source": event.source,
        })

    return application
