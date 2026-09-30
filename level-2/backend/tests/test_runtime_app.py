import base64
import io
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from ea_runtime.app import create_app
from ea_runtime.auth import AllowAllTestAuthenticator
from ea_runtime.store import InMemoryEventStore
from preflight import REQUIRED


class DenyAuthenticator:
    production_safe = False

    def authorize(self, environ: dict, *, source: str) -> bool:
        return False


def call(app, path, *, method="GET", body=b"", headers=None):
    captured = {}
    environ = {
        "PATH_INFO": path,
        "REQUEST_METHOD": method,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": io.BytesIO(body),
    }
    for key, value in (headers or {}).items():
        environ["HTTP_" + key.upper().replace("-", "_")] = value

    def start_response(status, response_headers):
        captured["status"] = status
        captured["headers"] = response_headers

    response = b"".join(app(environ, start_response))
    captured["body"] = response
    return captured


def ready_env():
    env = {key: "configured" for key in REQUIRED}
    env.update({
        "EA_ENV": "test",
        "EA_LEVEL_2B_ENABLED": "false",
        "EA_EXTERNAL_SEND_ENABLED": "false",
        "EA_EXTERNAL_CALENDAR_ENABLED": "false",
    })
    return env


class RuntimeAppTests(unittest.TestCase):
    def test_health_does_not_imply_readiness(self):
        app = create_app(store=None, authenticator=None, env={})
        self.assertTrue(call(app, "/healthz")["status"].startswith("200"))
        self.assertTrue(call(app, "/readyz")["status"].startswith("503"))

    def test_webhook_fails_closed_without_store(self):
        app = create_app(store=None, authenticator=AllowAllTestAuthenticator(), env=ready_env())
        result = call(app, "/hooks/gmail", method="POST", body=b"{}")
        self.assertTrue(result["status"].startswith("503"))

    def test_webhook_fails_closed_without_authenticator(self):
        app = create_app(store=InMemoryEventStore(), authenticator=None, env=ready_env())
        result = call(app, "/hooks/gmail", method="POST", body=b"{}")
        self.assertTrue(result["status"].startswith("503"))

    def test_gmail_duplicate_is_idempotent(self):
        store = InMemoryEventStore()
        app = create_app(store=store, authenticator=AllowAllTestAuthenticator(), env=ready_env())
        notice = {"emailAddress": "a@example.com", "historyId": "123"}
        body = json.dumps({
            "message": {
                "messageId": "msg-1",
                "data": base64.b64encode(json.dumps(notice).encode()).decode(),
            }
        }).encode()
        first = call(app, "/hooks/gmail", method="POST", body=body)
        second = call(app, "/hooks/gmail", method="POST", body=body)
        self.assertTrue(first["status"].startswith("204"))
        self.assertEqual(first["body"], b"")
        self.assertTrue(second["status"].startswith("200"))
        self.assertEqual(len(store.events), 1)

    def test_calendar_event_persists(self):
        store = InMemoryEventStore()
        app = create_app(store=store, authenticator=AllowAllTestAuthenticator(), env=ready_env())
        result = call(app, "/hooks/calendar", method="POST", body=b"{}", headers={
            "X-Goog-Channel-ID": "c1",
            "X-Goog-Resource-ID": "r1",
            "X-Goog-Resource-State": "exists",
            "X-Goog-Message-Number": "1",
        })
        self.assertTrue(result["status"].startswith("204"))
        self.assertEqual(len(store.events), 1)

    def test_denied_delivery_returns_401(self):
        store = InMemoryEventStore()
        app = create_app(store=store, authenticator=DenyAuthenticator(), env=ready_env())
        result = call(app, "/hooks/calendar", method="POST", body=b"{}", headers={
            "X-Goog-Channel-ID": "c1",
            "X-Goog-Resource-ID": "r1",
            "X-Goog-Resource-State": "exists",
            "X-Goog-Message-Number": "1",
        })
        self.assertTrue(result["status"].startswith("401"))
        self.assertEqual(len(store.events), 0)


if __name__ == "__main__":
    unittest.main()
