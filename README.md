# Ea Personal Assistant

Repository for the Ea Personal Assistant model configuration, deployment files, validation evidence, operational controls and managed automation design.

## Purpose

Ea operates as:

- a private assistant runtime configuration;
- a ChatGPT Project operating environment;
- a version-controlled protocol and validation system;
- a Level 2A controlled internal automation architecture, with Level 2B/2C separately gated.

## Repository structure

```text
active-source/              # Compact current Project source set + approved overlays
archive/phase-packages/     # Full phase-package archive/build evidence
validation/                 # QA results, release gates, validation trackers
config/custom-gpt/          # Runtime-compatible instruction and knowledge configuration
config/project/             # Project instruction and source configuration
config/personal-finance/    # Personal Finance Senior Advisor schemas
knowledge/finance/          # Personal Finance Senior Advisor protocol/instructions/specification
level-2/                    # Managed backend; Level 2A active scope, 2B/2C gated
docs/decisions/             # Architecture decisions and approved choices
docs/pending-review/        # Items awaiting operator approval
registers/                  # Capability and operational registers
```

## Operating rule

Use `active-source/` as the compact source-of-truth set for ChatGPT Project operation. Keep archive material as build evidence/reference unless explicitly promoted. Current explicit operator instructions and later approved/canonical overlays supersede conflicting older material.

## Current status — 06.10.2026

- Level 1 baseline: **APPROVED for use**.
- Level 2A: **ACTIVE** for controlled internal autonomy.
- Level 2B and Level 2C: **HOLD** pending separate validation and explicit promotion.
- Personal Finance Senior Advisor: **APPROVED / ACTIVE capability**.
- Personal finance routes through `active-source/04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md`.
- Personal-finance protocol, core instructions and specification are mirrored under `knowledge/finance/`.
- Restricted financial execution remains **R4 human-only**.
- Real user-specific financial records are intentionally excluded from this public repository.
- Current hourly email-watch runtime source remains `active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`.
- Known operator-deleted Gmail drafts remain controlled by `active-source/03D_EA_MANUAL_DRAFT_DELETION_SUPPRESSION_RULE_1111_09092026.md`.

See `RELEASE_MANIFEST.md`, `active-source/12_EA_MASTER_INDEX.md`, `active-source/ea_optimized_source_manifest.json` and the current validation records for control state.
