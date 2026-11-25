# EA CRM Operations Preparation

**Work ID:** EA-CRM-OPS  
**State:** PENDING_REVIEW / NON-DEPLOYED / NO LIVE PROVIDER WRITES

`field_mapping.json` records the 81-field candidate crosswalk from the qualified PR #199 handoff. All 14 identity fields are immutable. Every candidate is disabled. Activities and Audit_Log entries are append-only candidates; Pipeline_6M and Historical_5Y remain read-only until their field ownership is approved. The private spreadsheet ID is deliberately not stored here.

`runtime_controls.py` is an offline reference implementation for three concerns: a hash-chained append-only SQLite event log, an atomic shared-file concurrency lease with renewal/current-token checks, and an ordered read-only provider-first preflight. It has no Google, Gmail, CRM, Order Book, Calendar, network, scheduler or deployment adapter. Production-style use requires separate proof that the chosen durable storage is persistent and shared by every scheduler worker, that the provider writer enforces the lease and conditional revision at the actual write boundary, plus independent provider readback. A local SQLite test is not evidence of scheduler-host durability or provider-side serialization.

The existing Ea Business Email Watch and Ea Order Book Sync schedules, prompts, sender controls and suppression rules are external automation configuration and were not copied or changed here. Level 2B/C and managed sync remain HOLD. This candidate grants no CRM field ownership, provider permission or live write authority.
