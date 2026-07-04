# Ea Personal Assistant

Repository for the Ea Personal Assistant model configuration, deployment files, validation evidence, and future managed automation design.

## Purpose

Ea is intended to operate as:

- a private Custom GPT runtime;
- a ChatGPT Project operating environment;
- a version-controlled protocol and validation system;
- an optional Level 2 managed automation layer for live transcription, write-back, and scheduled processing.

## Recommended repository structure

```text
active-source/              # Compact 13-file active Project source set + manifest
archive/phase-packages/     # Full 89-file phase package archive
validation/                 # QA results, release gates, validation trackers
config/custom-gpt/          # Custom GPT instruction block, knowledge list, starters
config/project/             # Project instruction block and source list
level-2/                    # Backend, MCP, automation, schema and capture requirements
docs/decisions/             # Architecture decisions and approved choices
docs/pending-review/        # Items awaiting user approval
docs/canonical-rules/       # Approved canonical Ea rules
```

## Operating rule

Use `active-source/` as the compact source-of-truth set for the ChatGPT Project. Keep the 89-file package under `archive/phase-packages/` as build evidence and reference material, not as active Project files.

## Status

Current status: **repository skeleton created; source files pending manual upload**.
