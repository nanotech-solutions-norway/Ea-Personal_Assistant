from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Any


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    PROHIBIT = "PROHIBIT"


@dataclass(frozen=True)
class PolicyResult:
    action: str
    level: str
    decision: Decision
    risk: str
    policy_version: str


def evaluate(matrix: Mapping[str, Any], *, action: str, level: str) -> PolicyResult:
    """Evaluate one action against a deterministic Ea policy matrix.

    Unknown actions fail closed.
    """
    policy_version = str(matrix.get("policy_version", "unknown"))
    default = Decision(str(matrix.get("default", "PROHIBIT")))
    actions = matrix.get("actions", {})
    spec = actions.get(action)

    if not isinstance(spec, Mapping):
        return PolicyResult(action, level, default, "UNKNOWN", policy_version)

    raw = spec.get(level, matrix.get("default", "PROHIBIT"))
    try:
        decision = Decision(str(raw))
    except ValueError:
        decision = Decision.PROHIBIT

    return PolicyResult(
        action=action,
        level=level,
        decision=decision,
        risk=str(spec.get("risk", "UNKNOWN")),
        policy_version=policy_version,
    )


def assert_executable(result: PolicyResult, *, approval_present: bool = False) -> None:
    """Raise unless the action may execute at the tool boundary."""
    if result.decision is Decision.PROHIBIT:
        raise PermissionError(f"{result.action} is prohibited at {result.level}")
    if result.decision is Decision.REQUIRE_APPROVAL and not approval_present:
        raise PermissionError(f"{result.action} requires approval at {result.level}")
