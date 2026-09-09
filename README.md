# Ea Personal Assistant

Repository for the Ea Personal Assistant model configuration, deployment files, validation evidence, operational controls and future managed automation design.

## Purpose

Ea is intended to operate as:

- a private Custom GPT runtime;
- a ChatGPT Project operating environment;
- a version-controlled protocol and validation system;
- an optional Level 2 managed automation layer only if separately approved.

## Repository structure

```text
active-source/              # Compact current Project source set + manifest and approved overlays
archive/phase-packages/     # Full phase-package archive/build evidence
validation/                 # QA results, release gates, validation trackers
config/custom-gpt/          # Custom GPT instruction block, knowledge list, starters
config/project/             # Project instruction block and source list
level-2/                    # Future backend/MCP/automation design; HOLD
docs/decisions/             # Architecture decisions and approved choices
docs/pending-review/        # Items awaiting operator approval
docs/canonical-rules/       # Approved canonical Ea rules
```

## Operating rule

Use `active-source/` as the compact source-of-truth set for ChatGPT Project operation. Keep archive material as build evidence/reference unless explicitly promoted. Current explicit operator instructions and later approved/canonical overlays supersede conflicting older material.

## Current status — 09.09.2026

- Level 1 baseline: **APPROVED for use** (06.07.2026).
- Post-approval canonical additions and runtime changes remain subject to targeted validation/readback; this does not revoke the approved baseline.
- Current hourly email-watch runtime source: `active-source/07B_EA_EMAIL_DRAFT_FOLLOWUP_WATCH_CURRENT_1810_25082026.md`.
- Known operator-deleted Gmail drafts are controlled by `active-source/03D_EA_MANUAL_DRAFT_DELETION_SUPPRESSION_RULE_1111_09092026.md`.
- Live `Ea Business Email Watch` remains enabled and hourly; canonical `condition_watch` versus live `exact_schedule` is `CONTROL_PLANE_DRIFT / PENDING_REVIEW` and must not be silently resolved.
- Level 2 remains **HOLD** and requires separate explicit operator approval before planning or implementation.

See `RELEASE_MANIFEST.md`, `active-source/12_EA_MASTER_INDEX.md`, `active-source/ea_optimized_source_manifest.json` and `docs/EA_CLEANUP_RUN_1728_09092026.md` for current control state.
