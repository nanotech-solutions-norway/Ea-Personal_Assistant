from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

REQUIRED = (
    "DATABASE_URL",
    "WEBHOOK_BASE_URL",
    "GOOGLE_CLOUD_PROJECT",
    "GMAIL_PUBSUB_TOPIC",
    "EA_SECRET_STORE",
    "EA_AUDIT_DESTINATION",
)

FORBIDDEN_TRUE_AT_LEVEL_2A = (
    "EA_LEVEL_2B_ENABLED",
    "EA_EXTERNAL_SEND_ENABLED",
    "EA_EXTERNAL_CALENDAR_ENABLED",
)


@dataclass(frozen=True)
class PreflightResult:
    ready: bool
    missing: tuple[str, ...]
    unsafe_flags: tuple[str, ...]


def check(env: Mapping[str, str] | None = None) -> PreflightResult:
    values = dict(os.environ if env is None else env)
    missing = tuple(k for k in REQUIRED if not values.get(k, "").strip())
    unsafe = tuple(
        k for k in FORBIDDEN_TRUE_AT_LEVEL_2A
        if values.get(k, "").strip().lower() in {"1", "true", "yes", "on"}
    )
    return PreflightResult(
        ready=not missing and not unsafe,
        missing=missing,
        unsafe_flags=unsafe,
    )


if __name__ == "__main__":
    result = check()
    print(f"ready={result.ready}")
    if result.missing:
        print("missing=" + ",".join(result.missing))
    if result.unsafe_flags:
        print("unsafe_flags=" + ",".join(result.unsafe_flags))
    raise SystemExit(0 if result.ready else 2)
