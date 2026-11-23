# Ea P2 — Read-Only Provider Reconciliation Pilot

**Status:** IMPLEMENTED_IN_REPO / READ_ONLY_SYNTHETIC_ADAPTER / NOT_DEPLOYED / NOT_CANONICAL
**Owner:** Ea Personal Assistant
**Work ID:** EA-WORKSTREAM-P2-20261119-01

This code is **not** an autonomous Gmail, CRM or Order Book adapter. It is a pure, deterministic read-only reconciliation function fed normalized metadata collected in a bounded, manually verified connector session. It contains no network access, persistent queue, provider mutations, stored email bodies, real customer identities, prices, secrets or confidential attachments.

## Workstreams covered

- P2-A: technical inbound → Gmail SENT state → CRM and Order Book state comparison.
- P2-B: revised quotation → latest Gmail SENT and attachment metadata → CRM Opportunity, Commercial Order Book and Document_Index currency.

Return values are **observations and proposed correction codes**, not permission to change business records. The function always returns empty `business_writes` and `external_actions`.

Normalized `CaseState` contains status flags and opaque identifiers rather than correspondence contents. A future provider adapter must separately verify complete Gmail threads, current SENT, timezone-aware source timestamps, exact legal entity and source-document provenance, actual quote PDF and user approval before using any extracted value.

## Tests

```sh
python -m unittest discover -s workstreams/p2/tests -p 'test_*.py' -v
```

The new GitHub workflow checks both P1 and P2 pure-function suites and bans supported I/O/network/provider imports in the P2 module. Passing CI is not a deployed runtime or acceptance of Gmail/Drive/CRM integration.

## Authority and boundaries

Apply latest relevant APPROVED/CANONICAL Ea 03A/B/C/D/F, 03I, 05D, 07B, quotation rules, current product truth and accounting boundaries. Gmail owns SENT and attachment state; CRM owns relationship and next actor; Order Book owns commercial transaction, production and document index state. Do not create a fourth concurrent writer.

A later Level 2A correction requires source/target readback, exact field owner, idempotency key, write-ahead logging, current approval and independent provider after-state verification. Level 2B/C HOLD; no sends, invitations, quotation or supplier-PO release, payments or canonical promotion.

See `docs/workstreams/EA_P2_CONTROLLED_READ_ONLY_PILOT_20261119.md` for the redacted evidence mapping and remaining approvals.
