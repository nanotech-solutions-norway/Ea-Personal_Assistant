# Ea Personal Release Manifest — Beta v0.1

release_id: EA-PERSONAL-BETA-0.1.0  
product: Personal AI Assistant  
status: PACKAGE_READY  
release_date: 2026-10-11  
authority: AtlasOrbit D-109 + D-110  
customer_specific_data: prohibited  
azure_required_for_bootstrap_beta: false  
production_external_memory_proven: false  
target_commercial_runtime: AtlasOrbit Plugin + entitlement-controlled Skill Packs

## Required release files

- EA_PERSONAL_RUNTIME.md
- EA_PERSONAL_WORKFLOWS.md
- EA_RELEASE_MANIFEST.md
- INSTALL_EA.md
- VALIDATE_EA.md
- UPDATE_EA.md
- STATUS_EA.md

## Optional customer-facing file

- START_HERE.md

## Supported bootstrap runtime

Customer-owned private ChatGPT Project.

Prefer Project-only memory where the customer's ChatGPT interface supports it.

## Required/optional customer apps

Recommended:
- Gmail
- Google Calendar
- Google Drive

Optional:
- Google Contacts

Web search is used when available/required.

## Installation command

`\install-ea`

## Validation command

`\validate-ea`

## Update command

`\ea-update`

## Status command

`\ea-status`

## Mandatory safety invariants

- No customer password/API key/token in prompts or package files.
- No private customer data written to the public GitHub repository.
- No external send/share/book/delete/permission-changing action without explicit approval in beta.
- No production External Memory claim from Project/Drive continuity alone.
- No silent source conflict merge.
- No PASS status for an unconnected/unverified app.
- No automatic consumption of GitHub `main` as customer runtime authority.

## Beta purpose

Validate:
- installation UX;
- customer-owned Project configuration;
- onboarding;
- source authority;
- Gmail/Calendar/Drive read/draft workflows;
- approval controls;
- update/rollback behavior;
- customer usefulness and friction.

Does not validate:
- production External Memory capacity/recovery/export;
- full AtlasOrbit Plugin entitlement/runtime;
- production Azure substrate;
- unrestricted autonomous external action.

## Initial customer-beta mapping

Marita may be enrolled using this generic release. Her personal state remains in her own authorized ChatGPT/Google surfaces and must not be committed to this repository.

## Release result states

- PACKAGE_READY
- INSTALLING
- BLOCKED_NOT_CONNECTED
- READY_FOR_UAT
- UAT_FAILED
- BETA_ACTIVE
- BETA_SUSPENDED
- PLUGIN_MIGRATION_READY
- MIGRATED_TO_PLUGIN
