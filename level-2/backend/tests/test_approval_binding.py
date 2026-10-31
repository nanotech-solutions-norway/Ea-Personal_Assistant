"""Synthetic binding/replay acceptance, not durable DB or live send acceptance."""
import pathlib
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from ea_backend.approval_binding import (
    CaseBinding, ActionBinding, ApprovalBinding, ApprovalBindingDenied, validate_approval_binding,
)
from ea_backend.idempotency import action_revision, approval_payload_hash


class SyntheticReservations:
    """Test-only one-process adapter; no provider calls, durability or recovery claim."""
    def __init__(self):
        self.lock = threading.Lock()
        self.used_approvals = set()
        self.attempts = set()

    def reserve(self, **binding):
        with self.lock:
            key = validate_approval_binding(**binding)
            approval_identity = (binding['authenticated_tenant'], binding['approval'].approval_id)
            if approval_identity in self.used_approvals or key in self.attempts:
                raise ApprovalBindingDenied('replay_or_uncertain_attempt')
            self.used_approvals.add(approval_identity)
            self.attempts.add(key)
            return key


class ApprovalBindingTests(unittest.TestCase):
    def setUp(self):
        now = datetime(2026, 10, 31, 1, tzinfo=timezone.utc)
        revision = action_revision({'synthetic': 'proposal', 'revision': 1})
        digest = approval_payload_hash(action_type='synthetic.preview', recipients=['fiction@example.invalid'],
            subject='Synthetic', body='Fictional', attachment_hashes=[], source_revision='synthetic-v1')
        self.binding = dict(authenticated_tenant='synthetic-alpha',
            case=CaseBinding('synthetic-alpha', 'case-1'),
            action=ActionBinding('synthetic-alpha', 'case-1', 'action-1', 'synthetic.preview', revision, digest),
            approval=ApprovalBinding('synthetic-alpha', 'approval-1', 'case-1', 'action-1',
                'synthetic.preview', revision, digest, 'synthetic-reviewer', now-timedelta(minutes=1), now+timedelta(minutes=1)),
            current_revision=revision, current_payload_hash=digest, now=now)

    def test_malformed_records_have_explicit_denial(self):
        for field in ('case', 'action', 'approval'):
            for invalid in (None, {}, object()):
                with self.subTest(field=field, invalid=type(invalid).__name__):
                    with self.assertRaises(ApprovalBindingDenied):
                        validate_approval_binding(**{**self.binding, field: invalid})

    def test_naive_or_missing_current_time_denied(self):
        for invalid in (None, self.binding['now'].replace(tzinfo=None)):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'now': invalid})

    def test_nonstring_binding_fields_denied(self):
        for entity, field in (('case', 'case_id'), ('action', 'action_type'),
                              ('approval', 'approved_by'), ('approval', 'status')):
            with self.subTest(entity=entity, field=field), self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding,
                    entity: replace(self.binding[entity], **{field: 1})})

    def test_exact_binding_is_deterministic(self):
        self.assertEqual(validate_approval_binding(**self.binding), validate_approval_binding(**self.binding))

    def test_cross_tenant_case_action_approval_and_untrusted_scope_denied(self):
        for field in ('case', 'action', 'approval'):
            with self.subTest(field=field), self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, field: replace(self.binding[field], tenant_scope='synthetic-beta')})
        for scope in ('synthetic-beta', '', None):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'authenticated_tenant': scope})

    def test_approval_cannot_reference_different_case_than_action(self):
        for field in ('case', 'action', 'approval'):
            with self.subTest(field=field), self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, field: replace(self.binding[field], case_id='case-2')})

    def test_action_identity_type_and_missing_principal_denied(self):
        for field, value in (('action_id', 'action-2'), ('action_type', 'synthetic.other'), ('approved_by', ' ')):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'approval': replace(self.binding['approval'], **{field: value})})

    def test_revision_and_payload_mutation_denied(self):
        for entity in ('action', 'approval'):
            for field in ('action_revision', 'payload_hash'):
                with self.subTest(entity=entity, field=field), self.assertRaises(ApprovalBindingDenied):
                    validate_approval_binding(**{**self.binding, entity: replace(self.binding[entity], **{field: '0'*64})})
        for field in ('current_revision', 'current_payload_hash'):
            for value in ('0'*64, '', None, 'malformed'):
                with self.assertRaises(ApprovalBindingDenied):
                    validate_approval_binding(**{**self.binding, field: value})

    def test_expired_future_naive_and_missing_expiry_denied(self):
        now = self.binding['now']
        for mutation in ({'expires_at': now}, {'approved_at': now+timedelta(seconds=1)},
                         {'expires_at': None}, {'approved_at': now.replace(tzinfo=None)}):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'approval': replace(self.binding['approval'], **mutation)})

    def test_revoked_consumed_unknown_and_prohibited_states_denied(self):
        for status in ('USED', 'INVALIDATED', 'EXPIRED', 'REJECTED', 'UNKNOWN'):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'approval': replace(self.binding['approval'], status=status)})
        for mutation in ({'policy_decision': 'PROHIBIT'}, {'policy_decision': 'UNKNOWN'},
                         {'status': 'EXECUTED'}, {'status': 'RECONCILE_REQUIRED'}):
            with self.assertRaises(ApprovalBindingDenied):
                validate_approval_binding(**{**self.binding, 'action': replace(self.binding['action'], **mutation)})

    def test_parallel_duplicate_reservation_has_one_winner(self):
        adapter = SyntheticReservations()
        barrier = threading.Barrier(8)
        def attempt(_):
            barrier.wait()
            try:
                adapter.reserve(**self.binding)
                return True
            except ApprovalBindingDenied:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(attempt, range(8))), 1)
        self.assertEqual(len(adapter.attempts), 1)

    def test_uncertain_after_reservation_does_not_allow_retry(self):
        adapter = SyntheticReservations()
        adapter.reserve(**self.binding)
        # Simulated interruption after reservation: no provider invocation exists.
        with self.assertRaises(ApprovalBindingDenied):
            adapter.reserve(**self.binding)
        self.assertEqual(len(adapter.attempts), 1)

    def test_consumed_approval_cannot_be_rebound_to_another_action(self):
        adapter = SyntheticReservations()
        adapter.reserve(**self.binding)
        rebound = {**self.binding,
            'action': replace(self.binding['action'], action_id='action-2'),
            'approval': replace(self.binding['approval'], action_id='action-2')}
        with self.assertRaises(ApprovalBindingDenied):
            adapter.reserve(**rebound)

    def test_same_approval_id_isolated_across_tenants(self):
        adapter = SyntheticReservations()
        first = adapter.reserve(**self.binding)
        other = {**self.binding, 'authenticated_tenant': 'synthetic-beta'}
        for field in ('case', 'action', 'approval'):
            other[field] = replace(other[field], tenant_scope='synthetic-beta')
        self.assertNotEqual(first, adapter.reserve(**other))


if __name__ == '__main__':
    unittest.main()
