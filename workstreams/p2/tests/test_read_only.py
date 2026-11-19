"""Ea P2 read-only reconciliation tests: synthetic identifiers, no connectors."""
import unittest
from dataclasses import replace

from workstreams.p2.read_only import (
    CaseState, Message, reconcile_read_only, summarize_codes,
)


def sent(mid="m-out-2", at="2026-11-19T11:55:49+00:00",
         ref="", attached=(), contents_verified=False):
    return Message("synthetic-business-mailbox", "synthetic-thread-01", mid,
                   "SENT", at, attached, contents_verified, ref)


def inbound(mid="m-in-1", at="2026-11-14T03:39:27+00:00"):
    return Message("synthetic-business-mailbox", "synthetic-thread-01", mid,
                   "INBOUND", at)


def technical():
    return CaseState(
        pilot_id="PILOT-TECH-A", crm_key="EA-TEST-LEAD-A",
        order_key="EA-TEST-ORDER-A", order_record_crm_link="",
        crm_next_actor="NTSN", order_next_actor="EXTERNAL",
        crm_claims_unsent_draft=True, crm_last_source_message="m-old-draft",
        order_last_source_message="m-out-2", sent=(sent(),),
        inbound=(inbound(),), source_coverage="BOUNDED_PARTIAL",
        full_customer_thread_checked=True,
    )


def quotation():
    return CaseState(
        pilot_id="PILOT-QUOTE-B", crm_key="EA-TEST-OPP-B",
        order_key="EA-TEST-ORDER-B", order_record_crm_link="EA-TEST-OPP-B",
        crm_next_actor="NTSN", order_next_actor="EXTERNAL",
        crm_claims_unsent_draft=True, crm_last_source_message="m-old-sent",
        order_last_source_message="m-old-sent",
        order_quote_ref="QUOTE-OLDER",
        document_index_quote_refs=("QUOTE-OLDER",),
        sent=(sent(ref="QUOTE-NEW", attached=("QUOTE-NEW.pdf",)),),
        inbound=(inbound(),), source_coverage="BOUNDED_PARTIAL",
        full_customer_thread_checked=True,
    )


class ReadOnlyReconciliationTests(unittest.TestCase):
    def test_pilot_a_detects_crm_stale_and_missing_typed_link(self):
        report = reconcile_read_only(technical())
        self.assertEqual(report.status, "RECONCILIATION_PROPOSED")
        codes = summarize_codes(report)
        self.assertIn("MISSING_TYPED_CASE_CROSSWALK", codes)
        self.assertIn("CRM_DRAFT_STATE_STALE", codes)
        self.assertIn("CRM_ACTION_OWNER_STALE", codes)
        self.assertIn("SENT_AFTER_LATEST_INBOUND", codes)
        self.assertNotIn("ORDER_ACTION_OWNER_STALE", codes)

    def test_pilot_b_detects_latest_quote_unindexed_but_preserves_old(self):
        report = reconcile_read_only(quotation())
        codes = summarize_codes(report)
        self.assertIn("LATEST_QUOTE_NOT_DOCUMENT_INDEXED", codes)
        self.assertIn("PRESERVE_OLDER_QUOTE_VERSION", codes)
        self.assertIn("QUOTE_ATTACHMENT_METADATA_ONLY", codes)
        self.assertIn("CRM_SOURCE_POINTER_STALE", codes)
        self.assertIn("ORDER_SOURCE_POINTER_STALE", codes)
        self.assertNotIn("MISSING_TYPED_CASE_CROSSWALK", codes)

    def test_no_business_writes_or_external_actions(self):
        for obj in (technical(), quotation()):
            report = reconcile_read_only(obj)
            self.assertEqual(report.business_writes, ())
            self.assertEqual(report.external_actions, ())
            self.assertEqual(report.next_actor, "INTERNAL_REVIEW")

    def test_latest_source_without_content_verified_is_not_approved(self):
        code = summarize_codes(reconcile_read_only(quotation()))
        self.assertIn("QUOTE_ATTACHMENT_METADATA_ONLY", code)
        verified = replace(quotation(),
                           sent=(sent(ref="QUOTE-NEW", attached=("QUOTE-NEW.pdf",),
                                      contents_verified=True),))
        self.assertNotIn("QUOTE_ATTACHMENT_METADATA_ONLY",
                         summarize_codes(reconcile_read_only(verified)))

    def test_previous_document_ref_is_not_mutated(self):
        state = quotation()
        original_refs = state.document_index_quote_refs
        _ = reconcile_read_only(state)
        self.assertEqual(state.document_index_quote_refs, original_refs)

    def test_typed_link_conflict_blocks(self):
        state = replace(quotation(), order_record_crm_link="EA-TEST-OPP-DIFFERENT")
        report = reconcile_read_only(state)
        self.assertEqual(report.status, "BLOCKED_SOURCE_IDENTITY")
        self.assertIn("CONFLICTING_CASE_CROSSWALK", summarize_codes(report))

    def test_case_identity_missing_blocks(self):
        state = replace(technical(), order_key="")
        report = reconcile_read_only(state)
        self.assertEqual(report.status, "SOURCE_IDENTITY_UNVERIFIED")
        self.assertIn("SOURCE_ACCOUNT_KEY_UNVERIFIED", summarize_codes(report))

    def test_no_sent_message_does_not_claim_external_reply(self):
        state = replace(technical(), sent=())
        code = summarize_codes(reconcile_read_only(state))
        self.assertIn("NO_GMAIL_SENT_EVIDENCE", code)
        self.assertNotIn("SENT_AFTER_LATEST_INBOUND", code)

    def test_newer_inbound_does_not_assume_outstanding_reply_complete(self):
        state = replace(technical(), inbound=(inbound(at="2026-11-21T01:00:00Z"),))
        code = summarize_codes(reconcile_read_only(state))
        self.assertIn("NEWER_INBOUND_REQUIRES_REVIEW", code)
        self.assertNotIn("CRM_ACTION_OWNER_STALE", code)

    def test_naive_time_is_not_considered_verified(self):
        state = replace(technical(), sent=(sent(at="2026-11-19T11:55:49"),))
        report = reconcile_read_only(state)
        self.assertIn("SOURCE_TIME_UNVERIFIED", summarize_codes(report))
        self.assertNotIn("SENT_AFTER_LATEST_INBOUND", summarize_codes(report))

    def test_invalid_message_account_key_blocks(self):
        state = replace(technical(), sent=(replace(sent(), account_key=""),))
        self.assertEqual(reconcile_read_only(state).status, "BLOCKED_SOURCE_IDENTITY")

    def test_inverted_gmail_direction_blocks(self):
        state = replace(technical(), sent=(replace(sent(), direction="INBOUND"),))
        self.assertEqual(reconcile_read_only(state).status, "BLOCKED_SOURCE_IDENTITY")

    def test_completely_verified_unchanged_state_is_no_discrepancy(self):
        state = replace(technical(),
                        order_record_crm_link="EA-TEST-LEAD-A",
                        crm_next_actor="EXTERNAL",
                        crm_claims_unsent_draft=False,
                        crm_last_source_message="m-out-2",
                        source_coverage="BOUNDED_COMPLETE")
        report = reconcile_read_only(state)
        self.assertEqual(report.status, "READ_ONLY_NO_DISCREPANCY")
        self.assertEqual(summarize_codes(report), ())

    def test_source_coverage_never_assumed_complete_for_bounded_partial(self):
        self.assertIn("SOURCE_COVERAGE_PARTIAL",
                      summarize_codes(reconcile_read_only(technical())))

    def test_unknown_coverage_value_blocked(self):
        state = replace(technical(), source_coverage="FULL_ENTERPRISE")
        self.assertEqual(reconcile_read_only(state).status, "SOURCE_IDENTITY_UNVERIFIED")

    def test_missing_full_thread_is_flagged(self):
        state = replace(quotation(), full_customer_thread_checked=False)
        self.assertIn("GMAIL_THREAD_INCOMPLETE",
                      summarize_codes(reconcile_read_only(state)))

    def test_duplicate_reconcile_is_stable_and_deduplicated(self):
        a = reconcile_read_only(quotation())
        b = reconcile_read_only(quotation())
        self.assertEqual(a, b)
        codes = summarize_codes(a)
        self.assertEqual(len(codes), len(set(codes)))

    def test_latest_sent_without_verified_quote_ref_holds_claim(self):
        state = replace(quotation(), sent=(sent(attached=("QUOTE-NEW.pdf",)),))
        code = summarize_codes(reconcile_read_only(state))
        self.assertIn("SENT_QUOTE_REFERENCE_UNVERIFIED", code)
        self.assertNotIn("LATEST_QUOTE_NOT_DOCUMENT_INDEXED", code)

    def test_no_quote_document_needed_in_technical_case(self):
        code = summarize_codes(reconcile_read_only(technical()))
        self.assertNotIn("LATEST_QUOTE_NOT_DOCUMENT_INDEXED", code)

    def test_no_source_output_values_exposed_in_finding(self):
        result = reconcile_read_only(quotation())
        serialized = repr(result)
        self.assertNotIn("QUOTE-NEW.pdf", serialized)
        self.assertNotIn("m-old-sent", serialized)


if __name__ == "__main__":
    unittest.main()
