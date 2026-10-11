# \ea-update — Ea Personal Controlled Update Protocol

**Release:** EA-PERSONAL-BETA-0.1.0

## Purpose

Update an installed Ea Personal beta release without overwriting customer-specific preferences or silently changing authority.

## Procedure

1. Identify installed release from the current manifest.
2. Identify candidate release from a supplied approved AtlasOrbit release package.
3. Verify candidate package completeness.
4. Compare:
   - runtime rules;
   - workflows;
   - app requirements;
   - approval boundaries;
   - onboarding/profile schema;
   - breaking changes.
5. Present a concise change summary.
6. Preserve customer-specific profile/preferences unless the candidate explicitly defines a migration.
7. Do not import arbitrary current GitHub `main` content.
8. After the user authorizes the update, replace only release-controlled sources/configuration.
9. Run `\validate-ea` for material changes.
10. If validation fails, mark `BETA_SUSPENDED` for affected capabilities and restore the last validated release where technically possible.

## Non-breaking update

May proceed after user confirmation when:
- no permission expansion;
- no new consequential-action authority;
- no customer-state schema migration;
- no removed capability relied on by the customer.

## Breaking/high-risk update

Requires explicit acknowledgement when it changes:
- permissions/action scope;
- data/memory behavior;
- connected apps;
- retention/export behavior;
- legal/financial operating boundaries;
- customer-state schema.

## Rollback

Record the last validated release ID before update. Rollback restores release-controlled configuration only and must not erase customer-owned data unless the customer explicitly requests deletion.
