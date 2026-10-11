# \ea-status — Ea Personal Read-Only Status Protocol

**Release:** EA-PERSONAL-BETA-0.1.0

**Release family:** Ea Personal

When the user enters `\ea-status`, perform a read-only configuration status check.

Report:
- installed release ID;
- required release files present/missing;
- Project/private-runtime state if verifiable;
- onboarding state;
- Gmail connection state;
- Calendar connection state;
- Drive connection state;
- Contacts connection state;
- last known validation state;
- capabilities validated;
- capabilities blocked/unvalidated;
- recommended next action.

Allowed status values:
- PACKAGE_READY
- INSTALLING
- BLOCKED_NOT_CONNECTED
- READY_FOR_UAT
- UAT_FAILED
- BETA_ACTIVE
- BETA_SUSPENDED
- PLUGIN_MIGRATION_READY
- MIGRATED_TO_PLUGIN

Do not create, send, modify, delete, share or authorize anything while executing `\ea-status`.

Do not convert unavailable evidence into PASS.
