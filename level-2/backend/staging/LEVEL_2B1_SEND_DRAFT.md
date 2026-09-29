# Level 2B.1 — Approval-Bound Gmail Send Pilot

Status: STAGING_DESIGN_ONLY / LEVEL_2B_HOLD

## Scope

The first Level 2B candidate is deliberately narrow:

**Send one already-created Gmail draft after explicit operator approval of that exact draft revision.**

This design does not activate sending.

## Approval envelope

Approval binds:
- case ID;
- Gmail thread ID;
- Gmail draft ID;
- action type = `gmail.send_existing_draft`;
- exact recipient set;
- subject;
- body hash;
- attachment hashes;
- source revision;
- action revision;
- approval actor;
- approval timestamp;
- optional expiry.

## Execution transaction

1. Retrieve stored approval.
2. Confirm approval is ACTIVE, unexpired and for the same case/action.
3. Re-read Gmail draft.
4. Recompute exact payload hash.
5. If any recipient/body/subject/attachment/source revision changed, invalidate approval and stop.
6. Deterministic policy must return REQUIRE_APPROVAL and approval validation must pass.
7. Generate idempotency key.
8. Check that no verified send exists for the same key.
9. Send exactly the approved draft through the Level 2B execution identity.
10. Read sent-message/thread state.
11. Verify recipient, thread and sent message identity.
12. Mark approval USED and action VERIFIED.
13. Append audit record.

## Fail-closed cases

- draft missing;
- recipient changed;
- body or subject changed;
- attachment set changed;
- source revision changed materially;
- approval expired/rejected/invalidated;
- policy version unavailable;
- ambiguous send result that cannot be reconciled;
- evidence of source→sink prompt injection;
- approval service unavailable.

## Promotion gate

Do not activate Level 2B.1 until:
- separate send-capable execution identity is implemented;
- approval envelope is stored durably;
- hash/revision validation is tested;
- duplicate/ambiguous send tests pass;
- readback of sent message is demonstrated;
- operator explicitly promotes Level 2B.1.

OpenAI human-review pattern reference:
https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
