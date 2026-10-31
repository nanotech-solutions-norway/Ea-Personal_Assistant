"""Pure proposed approval-binding contract; no DB/provider I/O or execution grant.

Legacy SQL/envelope do not yet supply authenticated tenant/action bindings.
This optional foundation is deliberately not wired into runtime policy. A
qualified durable adapter must atomically reserve the returned binding key.
"""
from dataclasses import dataclass
from datetime import datetime
from hmac import compare_digest

from .idempotency import canonical_json, sha256_hex


class ApprovalBindingDenied(PermissionError):
    """A mismatch or incomplete identity must not authorize any side effect."""


@dataclass(frozen=True)
class CaseBinding:
    tenant_scope: str
    case_id: str


@dataclass(frozen=True)
class ActionBinding:
    tenant_scope: str
    case_id: str
    action_id: str
    action_type: str
    action_revision: str
    payload_hash: str
    policy_decision: str = 'REQUIRE_APPROVAL'
    status: str = 'PENDING_APPROVAL'


@dataclass(frozen=True)
class ApprovalBinding:
    tenant_scope: str
    approval_id: str
    case_id: str
    action_id: str
    action_type: str
    action_revision: str
    payload_hash: str
    approved_by: str
    approved_at: datetime
    expires_at: datetime
    status: str = 'ACTIVE'


def _aware(value):
    return isinstance(value, datetime) and value.tzinfo is not None and value.utcoffset() is not None


def _digest(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def validate_approval_binding(*, authenticated_tenant, case, action, approval,
                              current_revision, current_payload_hash, now):
    """Return an opaque reservation identity after exact binding checks.

    The caller supplies an independently authenticated tenant and freshly
    recomputed revision/hash. This does not authenticate an approver or persist
    consumption. Never treat this return value alone as permission to execute.
    """
    # Reject malformed records through the declared denial boundary rather
    # than incidental attribute errors or duck-typed mutable accessors.
    if (type(case) is not CaseBinding or type(action) is not ActionBinding
            or type(approval) is not ApprovalBinding):
        raise ApprovalBindingDenied('malformed_binding_record')
    if not all(type(value) is str for value in (
            action.action_revision, action.payload_hash, action.policy_decision,
            action.status, approval.action_revision, approval.payload_hash, approval.status)):
        raise ApprovalBindingDenied('malformed_binding_field')
    identities = (authenticated_tenant, case.tenant_scope, action.tenant_scope,
                  approval.tenant_scope, case.case_id, action.case_id, approval.case_id,
                  action.action_id, approval.action_id, action.action_type,
                  approval.action_type, approval.approval_id, approval.approved_by)
    if not all(type(value) is str and value.strip() for value in identities):
        raise ApprovalBindingDenied('missing_binding_identity')
    if not (case.tenant_scope == action.tenant_scope == approval.tenant_scope == authenticated_tenant):
        raise ApprovalBindingDenied('tenant_binding_mismatch')
    if not (case.case_id == action.case_id == approval.case_id):
        raise ApprovalBindingDenied('case_binding_mismatch')
    if (action.action_id, action.action_type) != (approval.action_id, approval.action_type):
        raise ApprovalBindingDenied('action_binding_mismatch')
    if action.policy_decision != 'REQUIRE_APPROVAL' or action.status not in ('PLANNED', 'PENDING_APPROVAL'):
        raise ApprovalBindingDenied('action_not_approval_eligible')
    if approval.status != 'ACTIVE':
        raise ApprovalBindingDenied('approval_not_active')
    if not all(_aware(value) for value in (now, approval.approved_at, approval.expires_at)):
        raise ApprovalBindingDenied('qualified_time_required')
    if not approval.approved_at <= now < approval.expires_at:
        raise ApprovalBindingDenied('approval_time_invalid')
    for expected, observed, approved in (
        (current_revision, action.action_revision, approval.action_revision),
        (current_payload_hash, action.payload_hash, approval.payload_hash),
    ):
        if not all(_digest(value) for value in (expected, observed, approved)):
            raise ApprovalBindingDenied('invalid_binding_digest')
        if not (compare_digest(expected, observed) and compare_digest(expected, approved)):
            raise ApprovalBindingDenied('stale_binding_digest')
    # Structured encoding preserves tuple boundaries even for delimiter-bearing IDs.
    return 'ea:approval:' + sha256_hex(canonical_json([
        authenticated_tenant, case.case_id, action.action_id, action.action_type,
        current_revision, current_payload_hash, approval.approval_id,
    ]))
