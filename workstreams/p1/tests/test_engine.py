"""Synthetic-only EA workstream P1 regression tests.

No real mailboxes, files, accounts, supplier prices or external operations.
Run: python -m unittest discover -s workstreams/p1/tests -p 'test_*.py' -v
"""
import unittest

from workstreams.p1.engine import (
    Attachment, Case, Source, StageInput, PROHIBITED_AUTOMATION,
    allowed_operator_choices, attachment_gate, correlate_case, event_key,
    internal_plan, projection_preflight, quote_arithmetic_gate,
    quote_reference_gate, source_gate,
)


def ready(event_type="NEW_LEAD", **overrides):
    settings = dict(
        event_type=event_type, case_id="EA-TEST-CASE-01", identity_verified=True,
        full_thread_and_sent_checked=True, source_gate_passed=True,
        alias_verified=True, reply_anchor_verified=True,
        draft_revision_current=True, customer_disclosure_safe=True,
        quote_source_price_verified=True, quote_reference_qa_passed=True,
        quote_arithmetic_qa_passed=True, quote_layout_qa_passed=True,
        attachment_readback_passed=True,
    )
    settings.update(overrides)
    return StageInput(**settings)


class CorrelationTests(unittest.TestCase):
    def setUp(self):
        self.cases = (
            Case("EA-TEST-CASE-01", {
                "crm_lead_id": "EA-TEST-LEAD-01",
                "crm_opportunity_id": "EA-TEST-OPP-01",
                "gmail_thread_key": "business@example.invalid:thread-01",
            }),
            Case("EA-TEST-CASE-02", {
                "crm_opportunity_id": "EA-TEST-OPP-02",
                "gmail_thread_key": "business@example.invalid:thread-02",
            }),
        )

    def test_exact_cross_workflow_match(self):
        lead = correlate_case({"gmail_thread_key": "business@example.invalid:thread-01"}, self.cases)
        rfq = correlate_case({"crm_opportunity_id": "EA-TEST-OPP-01"}, self.cases)
        self.assertEqual((lead.status, lead.case_id), ("EXACT_MATCH", "EA-TEST-CASE-01"))
        self.assertEqual(rfq.case_id, lead.case_id)

    def test_same_legal_entity_not_an_automatic_merge(self):
        self.assertEqual(correlate_case({"company_name": "SYNTHETIC CO"}, self.cases).status,
                         "INSUFFICIENT_IDENTITY")

    def test_two_opportunities_are_not_merged(self):
        self.assertEqual(correlate_case({
            "crm_opportunity_id": "EA-TEST-OPP-02",
            "gmail_thread_key": "business@example.invalid:thread-01"}, self.cases).status,
            "AMBIGUOUS_CASE")

    def test_conflicting_explicit_and_existing_keys_block(self):
        self.assertEqual(correlate_case({
            "crm_opportunity_id": "EA-TEST-OPP-01",
            "gmail_thread_key": "business@example.invalid:wrong-thread"}, self.cases).status,
            "CONFLICTING_CASE_IDENTIFIERS")

    def test_unknown_explicit_case_is_not_created(self):
        self.assertEqual(correlate_case({"case_id": "EA-MISSING"}, self.cases).status,
                         "UNKNOWN_EXPLICIT_CASE")

    def test_new_source_is_only_candidate(self):
        self.assertEqual(correlate_case(
            {"form_response_key": "form:unseen"}, self.cases).status, "NEW_CANDIDATE_REVIEW")

    def test_unqualified_mailbox_thread_key_is_rejected(self):
        self.assertEqual(correlate_case(
            {"gmail_thread_key": "thread-01"}, self.cases).status, "INVALID_THREAD_KEY")

    def test_source_event_idempotency(self):
        one = event_key("business@example.invalid", "m1", "INBOUND", "EA-TEST-CASE-01")
        self.assertEqual(one, event_key("business@example.invalid", "m1",
                                        "INBOUND", "EA-TEST-CASE-01"))
        self.assertNotEqual(one, event_key("business@example.invalid", "m2",
                                           "INBOUND", "EA-TEST-CASE-01"))
        with self.assertRaises(ValueError):
            event_key("", "m1", "INBOUND", "EA-TEST-CASE-01")


class SourceAndArtifactTests(unittest.TestCase):
    def test_approved_source_with_exact_variant_and_scope(self):
        a = Source("S01", "SurfaceGuard-X", "technical", "r3",
                   "APPROVED", "sha256-abc")
        self.assertEqual(source_gate("SurfaceGuard-X", "technical", [a]), "SOURCE_READY")
        self.assertEqual(source_gate("SurfaceGuard-T", "technical", [a]), "SOURCE_MISSING")

    def test_latest_unapproved_source_does_not_override_approved(self):
        a = Source("S01", "VitaCoat", "technical", "r1",
                   "APPROVED", "sha256-one")
        b = Source("S02", "VitaCoat", "technical", "r2",
                   "PENDING_REVIEW", "sha256-new")
        self.assertEqual(source_gate("VitaCoat", "technical", [a, b]), "SOURCE_READY")

    def test_conflicting_approved_sources_block(self):
        a = Source("S01", "VitaCoat", "SDS", "r1", "APPROVED", "one")
        b = Source("S02", "VitaCoat", "SDS", "r2", "APPROVED", "two")
        self.assertEqual(source_gate("VitaCoat", "SDS", [a, b]),
                         "SOURCE_CONFLICT_PENDING_REVIEW")

    def test_unapproved_source_and_recipient_restriction(self):
        a = Source("S01", "Hirec-R", "technical", "r1",
                   "PENDING_REVIEW", "abc")
        self.assertEqual(source_gate("Hirec-R", "technical", [a]),
                         "SOURCE_UNAPPROVED_OR_RECIPIENT_MISMATCH")
        b = Source("S02", "Hirec-R", "technical", "r2",
                   "APPROVED", "xyz", recipient_fit=False)
        self.assertEqual(source_gate("Hirec-R", "technical", [b]),
                         "SOURCE_UNAPPROVED_OR_RECIPIENT_MISMATCH")

    def test_attachment_actual_readback_matches(self):
        doc = Attachment("file-01", "TDS.pdf", "2026-11", "digest1", True, "APPROVED")
        self.assertEqual(attachment_gate((doc,), (doc,)), "PASS")
        self.assertEqual(attachment_gate((doc,), ()), "ATTACHMENT_COUNT_MISMATCH")
        stale = Attachment("file-01", "TDS.pdf", "2025-08", "digest1", True, "APPROVED")
        self.assertEqual(attachment_gate((doc,), (stale,)), "ATTACHMENT_VERSION_MISMATCH")

    def test_attachment_disclosure_and_unapproved_hold(self):
        planned = Attachment("f1", "internal.pdf", "r1", "sha", False, "APPROVED")
        self.assertEqual(attachment_gate((planned,), (planned,)),
                         "ATTACHMENT_DISCLOSURE_BLOCK")
        pending = Attachment("f1", "tech.pdf", "r1", "sha", True, "PENDING_REVIEW")
        self.assertEqual(attachment_gate((pending,), (pending,)),
                         "ATTACHMENT_UNAPPROVED")

    def test_quote_file_email_printed_ref_alignment(self):
        self.assertEqual(quote_reference_gate("AA-20261119-01", "AA-20261119-01.pdf",
                                              "AA-20261119-01", "AA-20261119-01"), "PASS")
        self.assertEqual(quote_reference_gate("AA-20261119-01", "AA-20261119-02.pdf",
                                              "AA-20261119-01", "AA-20261119-01"),
                         "QUOTE_REFERENCE_MISMATCH")

    def test_quote_arithmetic_is_independent_of_price_authority(self):
        self.assertEqual(quote_arithmetic_gate(("100.00", "50.00"), "150.00",
                                               "15.00", "10.00", "0", "145.00"), "PASS")
        self.assertEqual(quote_arithmetic_gate(("100.00",), "99.00",
                                               "0", "0", "0", "99.00"),
                         "QUOTE_SUBTOTAL_MISMATCH")
        self.assertEqual(quote_arithmetic_gate(("100.00",), "100.00",
                                               "0", "0", "0", "101.00"),
                         "QUOTE_TOTAL_MISMATCH")
        self.assertEqual(quote_arithmetic_gate(("100.00",), "100.00",
                                               "0", "0", "NaN", "100.00"),
                         "QUOTE_ARITHMETIC_INVALID")


class InternalPlanTests(unittest.TestCase):
    def test_stage_a_new_lead_to_unsent_draft_and_crm_proposal(self):
        result = internal_plan(ready())
        self.assertEqual(result.disposition, "INTERNAL_PLAN_READY")
        self.assertIn("PREPARE_IN_THREAD_UNSENT_DRAFT", result.actions)
        self.assertIn("PROPOSE_CRM_ACTIVITY_PROJECTION", result.actions)
        self.assertNotIn("SEND_EMAIL", result.actions)
        self.assertEqual(result.operator_gate, "EXTERNAL_ACTIONS_REQUIRE_NEW_APPROVAL")

    def test_stage_b_rfq_quote_and_draft(self):
        result = internal_plan(ready("RFQ_RECEIVED"))
        self.assertEqual(result.disposition, "INTERNAL_PLAN_READY")
        self.assertIn("PREPARE_INTERNAL_QUOTE", result.actions)
        self.assertIn("RECONCILE_ACTUAL_DRAFT_ATTACHMENT", result.actions)
        self.assertIn("PROPOSE_ORDER_BOOK_DOCUMENT_INDEX_PROJECTION", result.actions)
        self.assertNotIn("ISSUE_QUOTE", result.actions)

    def test_missing_supplier_price_blocks_quote_but_not_lead(self):
        missing = ready("RFQ_RECEIVED", quote_source_price_verified=False)
        self.assertEqual(internal_plan(missing).disposition, "BLOCKED_INTERNAL_PREPARATION")
        self.assertIn("PRICE_SOURCE_UNVERIFIED", internal_plan(missing).blockers)
        self.assertEqual(internal_plan(ready()).disposition, "INTERNAL_PLAN_READY")

    def test_quote_qa_and_missing_attachment_block(self):
        missing = ready("RFQ_RECEIVED", attachment_readback_passed=False,
                        quote_arithmetic_qa_passed=False)
        blockers = internal_plan(missing).blockers
        self.assertIn("QUOTE_ARITHMETIC_FAILED", blockers)
        self.assertIn("ATTACHMENT_READBACK_UNVERIFIED", blockers)

    def test_deleted_draft_suppression_requires_specific_instruction(self):
        result = internal_plan(ready(suppressed_recipient=True))
        self.assertEqual(result.disposition, "SUPPRESSED_03D")
        explicit = internal_plan(ready(suppressed_recipient=True,
                                       explicit_new_draft_instruction=True))
        self.assertEqual(explicit.disposition, "INTERNAL_PLAN_READY")

    def test_espen_always_chat_only(self):
        result = internal_plan(ready(sender_profile="Espen Olsen"))
        self.assertEqual(result.disposition, "CHAT_ONLY_OUTLOOK")
        self.assertEqual(result.actions, ("PREPARE_CHAT_COPY_ONLY",))

    def test_wrong_alias_thread_and_stale_source_block(self):
        result = internal_plan(ready(alias_verified=False,
                                     reply_anchor_verified=False,
                                     draft_revision_current=False))
        self.assertIn("SENDER_ALIAS_UNVERIFIED", result.blockers)
        self.assertIn("THREAD_ANCHOR_UNVERIFIED", result.blockers)
        self.assertIn("STALE_DRAFT_OR_THREAD", result.blockers)

    def test_regulatory_source_conflict_and_attached_draft_block(self):
        result = internal_plan(ready(policies_conflict=True,
                                     existing_draft_with_attachments=True))
        self.assertIn("AUTHORITY_CONFLICT", result.blockers)
        self.assertIn("EXISTING_ATTACHMENT_DRAFT_REPLACEMENT_REQUIRES_RECONCILIATION",
                      result.blockers)

    def test_no_unknown_trigger_or_empty_case_proceeds(self):
        self.assertEqual(internal_plan(ready("UNKNOWN")).disposition, "HOLD")
        self.assertEqual(internal_plan(ready(case_id="")).disposition, "HOLD")

    def test_every_plan_has_no_dangerous_execution_action(self):
        for event in ("NEW_LEAD", "INBOUND_REPLY", "RFQ_RECEIVED"):
            plan = internal_plan(ready(event))
            self.assertTrue(PROHIBITED_AUTOMATION.isdisjoint(plan.actions))
            self.assertEqual(plan.operator_gate, "EXTERNAL_ACTIONS_REQUIRE_NEW_APPROVAL")

    def test_per_work_id_optional_operator_note_is_not_approval(self):
        selected = allowed_operator_choices({
            "W-01": ("HOLD", "please send this anyway"),
            "W-02": ("VERIFY", "Additional product context"),
            "W-03": ("PREPARE", ""),
        })
        self.assertEqual(selected, (("W-02", "VERIFY"), ("W-03", "PREPARE")))
        with self.assertRaises(ValueError):
            allowed_operator_choices({"W-04": ("SEND_EMAIL", "approved")})

    def test_projection_requires_correct_owner_and_readback(self):
        args = ("CRM", "CRM", True, True, False, True)
        self.assertEqual(projection_preflight(*args),
                         "PREPARE_WRITE_UNDER_EXISTING_APPROVED_SCOPE")
        self.assertEqual(projection_preflight("Order_Book", *args[1:]),
                         "FIELD_OWNERSHIP_CONFLICT")
        self.assertEqual(projection_preflight("CRM", "CRM", True, True, True, True),
                         "NO_OP_ALREADY_RECORDED")
        self.assertEqual(projection_preflight("CRM", "CRM", True, True, False, False),
                         "LOGGING_NOT_VERIFIED")
        self.assertEqual(projection_preflight("CRM", "CRM", False, True, False, True),
                         "SOURCE_OR_TARGET_NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
