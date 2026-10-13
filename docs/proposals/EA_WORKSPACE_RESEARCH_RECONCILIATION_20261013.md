# EA Personal Assistant — ChatGPT Workspace Research Adoption Reconciliation (13 October 2026)

**State:** STAGED/PENDING_REVIEW in EA PR #43, subordinate to AtlasOrbit's single Plugin proposal. Level 2A internal/read-only only. **No external writes or live managed sync** as a result of this document.

## Research received
`Deep Research — ChatGPT-Native Desktop Workspace, AtlasOrbit & EA Personal Assistant — 04:06, 12.10.2026` (DOCX + Markdown). Source archived under AtlasOrbit Drive `05_Research_Sources`:
- Google Docs converted original: https://docs.google.com/document/d/18obFepNmf5eYdtjbTR8WZb0HFVmrMTHVKpCMIshwvgE/edit
- Original Markdown: https://drive.google.com/file/d/1VVuGiXKPIWQNPjSNaO2l9VP7y0sinW5Q/view

Research recommendations for EA: **one AtlasOrbit Plugin**, governed EA module, read-only calendar/inbox/task/commitment/source-health screens, provider authority/freshness/identity, exact approval separation; no Sites-based private-data hub or autonomous calendar/email actions. The workspace should *consume* EA backend read models; it must not become a competing source of truth.

## Reconciliation of outdated 12 Oct research statement
The research says EA engineering was paused. That statement was valid for the 11 Oct snapshot but is superseded by the operator's explicit **13 Oct resumption**.
- EA PR #50 merged: read-only Calendar staging worker + independent PostgreSQL post-commit readback, with synthetic tests.
- EA PR #51 merged: engineering continuation checkpoint corrected.
- EA PR #54 OPEN/NOT MERGED: West Europe staging architecture **planning only**, EUR20/month ceiling, one private EA tenant, new resource-group design, Azure subscription **not yet supplied**, no priced quote. CI passed but GitHub merge protection rejected the merge.
- No managed EA cloud backend, separate Google OAuth workload, Gmail/Drive/GitHub provider watches, running production cursors or continuous live synchronization were deployed by those PRs.

This is a **separate EA private staging proposal** from AtlasOrbit's D-071 production cloud baseline (Azure Norway East); do not mix subscriptions, budgets, tenant identities or cloud resources without explicit consent.

## Safe UI domain adapter contract
- Backend obtains tenant/principal/account from authenticated authorization and resolves per-source entitlement. UI strings never become identity authority.
- Calendar events: Google Calendar; separate commitments retain EA/AtlasOrbit ledger IDs; never imply the commitment was created as a Calendar event.
- Inbox: Gmail thread/draft metadata, correct sender alias, deleted-draft suppression 03D, hygiene 03F, limited content/purpose; no provider send action.
- GitHub and Drive: source-qualified exact resource/URL/revision, freshness, observed/reconciled timestamp; a notification is only a reconciliation trigger.
- Health: report NOT_CONNECTED / UNVERIFIED / STALE / VERIFIED_READ_ONLY only after genuinely verified backend/provider evidence.
- ChatGPT native Tasks, chats, Projects: no universal export/change feed is proven; display UNVERIFIED or UNSUPPORTED until supported consented integration is demonstrated.
- Actions: no generic arbitrary commands, no `email.send`, `calendar.modify`, payment/share/delete, or EA Level 2B/2C capabilities. R3 needs exact approved revision; R4 is human only.

## Related staged artifacts
- AtlasOrbit PR #115: https://github.com/nanotech-solutions-norway/atlasorbit/pull/115
- React synthetic workspace: `atlasorbit/apps/workspace-ui/` (PR #115 branch)
- Read-only identity/provenance/tool contracts and negative tests: `atlasorbit/prototypes/chatgpt-workspace-shell/workspace-contracts.mjs` and `test-contracts.mjs`
- EA PR #43: https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/43
- EA deployment planning PR #54: https://github.com/nanotech-solutions-norway/Ea-Personal_Assistant/pull/54

## Verification and subsequent gates
1. **Now:** stage EA read-only domain-contract review; preserve existing approved 07C 07:00 Europe/Oslo briefing and independent email watch unchanged.
2. **Next:** verify AtlasOrbit PR #115 synthetic UI build, accessibility, platform version; do not claim installed Plugin/MCP UI.
3. **Later:** separately authorized read-only EA backend API, tenant/role/entitlement mapping, source/provenance readback, stale/expiry/duplicate test and ACSEE negative paths.
4. **Cloud gate:** provide EA Azure subscription and complete EUR20 quote; receive explicit deployment authorization. **Do not provision paid Azure resources** from this proposal.
5. **Release gates:** A-111/A-173/A-110/A-316 review, privacy/EEA, offboarding, rollback and customer UAT; Level 2B/2C HOLD. No architecture promotion without operator/repository review decision.

**Outcome:** Research adopted as reviewable engineering guidance, not as permission for live sync, provider writes, second commercial Plugin, secrets or customer data. The operator's request to implement the report authorizes safe synthetic engineering/documentation work, not the separately gated consequential operations.
