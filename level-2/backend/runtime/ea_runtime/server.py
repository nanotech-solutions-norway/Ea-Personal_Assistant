from __future__ import annotations

import os
from wsgiref.simple_server import make_server

from preflight import check
from .app import create_app
from .bootstrap import build_components


def main() -> None:
    # Staging scaffold. Components are built only when preflight is complete.
    # Any bootstrap/database/auth failure leaves health available while
    # readiness and webhook acknowledgement remain fail-closed.
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    env = dict(os.environ)

    store = None
    authenticator = None
    if check(env).ready:
        try:
            store, authenticator = build_components(env)
        except Exception:
            store = None
            authenticator = None

    app = create_app(store=store, authenticator=authenticator, env=env)
    with make_server(host, port, app) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
