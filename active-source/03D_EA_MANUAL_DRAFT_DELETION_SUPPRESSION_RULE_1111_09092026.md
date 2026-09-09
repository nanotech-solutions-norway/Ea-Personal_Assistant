# Ea Manual Gmail Draft Deletion Suppression Rule — 11:11, 09.09.2026

**Status:** APPROVED / CANONICAL / OPERATOR-INSTRUCTED  
**Authority:** Current explicit operator instruction  
**Effective:** 09.09.2026 at 11:11 Europe/Madrid  
**Scope:** Gmail drafting, business-email watch, CRM/follow-up workflows, scheduled draft preparation and any repeated email-draft generation  
**Level:** Ea Level 1  
**Level 2:** HOLD

## Controlling rule

A Gmail draft that the operator manually deletes must be treated as an intentional suppression signal.

1. Ea must **not automatically recreate, replace or regenerate a new draft to the same recipient** after the operator has manually deleted a draft.
2. This rule applies to normal Gmail drafting workflows, business-email watch routines, CRM/follow-up processing, scheduled draft preparation and any other repeated draft-generation logic.
3. If a later workflow determines that a new draft to the same recipient may be useful or required, Ea must **prompt the operator and ask whether a new draft is required before creating it**.
4. A new explicit operator instruction to draft, reply, prepare or create a Gmail draft to that recipient overrides the suppression for that requested draft; no additional confirmation is required for the specifically requested draft.
5. Ea must not infer manual deletion merely because no draft is present. The suppression rule applies when manual deletion is known from operator instruction or reliable workflow evidence.
6. The suppression applies to draft creation only. It does not close the underlying lead, customer, supplier, partner, project or follow-up case unless separately instructed.
7. Existing approval boundaries remain unchanged: creating a draft does not authorize sending, and external sending still requires explicit approval.

## Conflict handling

This rule overrides any older Ea instruction that would automatically regenerate or replace a missing/deleted Gmail draft for the same recipient without operator confirmation. Other email drafting, historical-context review, source validation, confidentiality and approval rules remain in force.

## Operational handling

When a manually deleted draft is known, classify the draft state as `OPERATOR_DELETED_SUPPRESS_RECREATE` for internal workflow purposes. If a later draft opportunity arises for the same recipient and there is no new explicit operator instruction, return an operator prompt rather than creating the draft.
