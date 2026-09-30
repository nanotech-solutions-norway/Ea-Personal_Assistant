from __future__ import annotations

import os
from wsgiref.simple_server import make_server

from .app import create_app


def main() -> None:
    # Staging scaffold only. Durable EventStore and authenticated-delivery
    # adapters are intentionally not auto-created. Without both, readiness is
    # 503 and webhook POSTs fail closed.
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app = create_app(store=None, authenticator=None, env=dict(os.environ))
    with make_server(host, port, app) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
