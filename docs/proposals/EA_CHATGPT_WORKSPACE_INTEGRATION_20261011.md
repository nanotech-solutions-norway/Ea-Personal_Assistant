# EA Personal Assistant — ChatGPT Workspace Shell Integration — 13:11, 11.10.2026

**State:** PENDING_REVIEW / read-only integration proposal. **Production:** NOT_DEPLOYED. **Scope:** Level 2A internal assistant only. Level 2B/2C HOLD.  
**Related AtlasOrbit staging:** `nanotech-solutions-norway/atlasorbit/docs/proposals/CHATGPT_WORKSPACE_SHELL_FEASIBILITY_20261011.md`, `prototypes/chatgpt-workspace-shell/index.html`.  
**EA governing source:** `active-source/07C_EA_UNIFIED_CALENDAR_DAILY_BRIEFING_20261010.md` and `active-source/12_EA_MASTER_INDEX.md`. No overwrite of these approved/runtime files.

## 1. Purpose and recommended UX

Expose EA as an entitlement-controlled **capability pack of the single AtlasOrbit Plugin** (D-109), not a second EA plugin or independent competing assistant. Initial sidebar "EA Workspace" read-only navigation: Overview, Calendar, Inbox, Tasks, Projects, Approvals and Source Health. Companion `thread` panel shows evidence for the currently discussed item.

The interface is a *view* of EA's approved authorities, not an alternate source of truth:
- Calendar event time and attendance: Google Calendar.
- Business correspondence/drafts: Gmail.
- Engineering/version/release status: verified GitHub commit/PR/run.
- Document/artifact collaboration: Google Drive.
- Commitment identities, dependencies, source freshness: governed EA/AtlasOrbit ledger when actually deployed.
- ChatGPT-native Tasks/chats/projects: show as UNAVAILABLE unless an authorized integration supports reading them; do not infer complete availability.

## 2. Daily briefing compatibility

Preserve the live `Ea Daily Calendar Briefing` as the previously approved native daily task at **07:00 Europe/Oslo** (Madrid same UTC offset on this date). Workspace UI is additional and must **not**:
- replace the daily task,
- replace the independent hourly `Ea Business Email Watch`,
- reactivate older disabled routines,
- start two-way Google Calendar synchronization,
- create invoice, payment or customs calendar entries.

The UI may eventually render the approved daily report structure, provided it can retrieve an authorized, verified output. Do not claim there is a native ChatGPT Tasks/change feed without proven capability.

## 3. Data contracts (proposal)

Read endpoints only for Stage 1:

- `GET /api/workspace/v1/overview` → per-source availability, last checked time, metrics only from verified records.
- `GET /api/workspace/v1/calendar?from=&to=` → Google Calendar events and **separately** non-calendar commitment items, tagged `record_type`.
- `GET /api/workspace/v1/inbox` → authorized follow-up/draft metadata; no message bodies by default.
- `GET /api/workspace/v1/missions` → stable mission/task IDs, approval class, owner, status, due date, blockers.
- `GET /api/workspace/v1/projects` → canonical source-qualified GitHub/Drive evidence.
- `GET /api/workspace/v1/health` → declared/observed/accepted/production-enabled capability statuses; last readback.

Responses must identify `item_id`, `tenant_id` (derived server-side), `provider`, `provider_id`, `source_url`, `source_version`, `last_verified_at`, `authority_status`, `owner`, `timezone`, `status`, `approval_class` when relevant. Never expose provider tokens, secrets, private customer data or unauthorized financial/account records.

## 4. Guardrails and regressions

- Preserve 03D deleted-draft suppression (currently recipient-level); 03F Gmail draft hygiene; historical-thread review and sender/alias restrictions.
- Level 2A may prepare bounded internal material only as explicitly approved; no automatic send, invite, external calendar changes, or sharing/deletion.
- Payments, banking, legal/commercial commitments, and R4 decisions remain human-only.
- Keep customer beta package D-110 distinct; Marita-owned private ChatGPT Project package remains the approved first-UAT fallback, not a production external-memory service.
- Source conflict → PENDING_REVIEW; missing/expired access → visible UNVERIFIED/STALE; sync success requires provider readback, not a UI badge.
- Provider API capability registration and write access require AtlasOrbit A-173 independently of whether UI buttons exist.
- Do not insert new canonical workflow instructions into `active-source/` until this staged proposal passes operator acceptance.

## 5. Implementation and acceptance checklist

1. **COMPLETE:** Source authority and platform capability assessment, matched to D-109 and EA 07C.
2. **STAGED:** AtlasOrbit synthetic workspace HTML + architecture proposal; this file is EA integration staging.
3. **PENDING:** Convert AtlasOrbit HTML into an MCP App UI with global sidebar and thread entrypoints.
4. **PENDING:** Connect accepted, tenant-bound, read-only API. Validate in ACSEE synthetic fixtures and real permission-denial scenarios.
5. **PENDING:** Read-only EA Calendar / Gmail / GitHub / Drive + unified ledger integration with provenance and freshness; do not disturb separate calendar synchronization PR.
6. **PENDING:** Confirm actual plan/workspace and Spanish/EEA availability; OpenAI release notes exclude the expanded Sites beta and public publishing in EEA at launch. Native Sites is not a production private-data dependency, because residency is absent at launch.
7. **PENDING:** Mobile/desktop responsive, keyboard, accessibility, security and authentication UAT.
8. **BLOCKED:** External write operation activation until A-173 provider acceptance and explicit operator promotion.
9. **BLOCKED:** First-customer promotion until D-110/A-316 UAT and data boundary approvals.

## 6. Handoff and operator decision

The present change is a non-authoritative engineering proposal. Approve separately whether to add **EA Workspace** as a UI module in the existing AtlasOrbit Plugin package. No source-of-truth changes, commercial offerings, pricing or newly authorized external operations arise from this proposal. This file must not be interpreted as proof of a running Plugin, Site, backend or synchronization.
