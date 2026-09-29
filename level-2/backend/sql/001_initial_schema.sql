-- Ea Level 2 managed backend foundation
-- PostgreSQL-compatible DDL. No production database is provisioned by this file.

CREATE TABLE IF NOT EXISTS ea_cases (
    case_id TEXT PRIMARY KEY,
    company_contact TEXT,
    gmail_thread_id TEXT,
    latest_actionable_message_id TEXT,
    gmail_draft_id TEXT,
    calendar_event_id TEXT,
    classification TEXT NOT NULL,
    urgency TEXT,
    confidence NUMERIC(5,4),
    suppression_state TEXT,
    next_action TEXT,
    due_at TIMESTAMPTZ,
    dependency_risk TEXT,
    source_revision TEXT,
    state_version BIGINT NOT NULL DEFAULT 1,
    last_verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ea_cases_gmail_thread_uq
    ON ea_cases(gmail_thread_id)
    WHERE gmail_thread_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS ea_actions (
    action_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL REFERENCES ea_cases(case_id),
    action_type TEXT NOT NULL,
    source_id TEXT,
    source_revision TEXT,
    action_revision TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    risk_class TEXT NOT NULL,
    policy_decision TEXT NOT NULL,
    approval_required BOOLEAN NOT NULL DEFAULT FALSE,
    approval_id TEXT,
    status TEXT NOT NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    executed_at TIMESTAMPTZ,
    verified_at TIMESTAMPTZ,
    error_class TEXT,
    error_code TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0,
    CHECK (policy_decision IN ('ALLOW','REQUIRE_APPROVAL','PROHIBIT')),
    CHECK (status IN ('PLANNED','BLOCKED','PENDING_APPROVAL','EXECUTING','EXECUTED','VERIFIED','FAILED','RECONCILE_REQUIRED'))
);

CREATE TABLE IF NOT EXISTS ea_approvals (
    approval_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL REFERENCES ea_cases(case_id),
    action_id TEXT NOT NULL REFERENCES ea_actions(action_id),
    action_type TEXT NOT NULL,
    action_revision TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    approved_by TEXT NOT NULL,
    approved_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    invalidated_reason TEXT,
    CHECK (status IN ('ACTIVE','USED','REJECTED','EXPIRED','INVALIDATED'))
);

CREATE TABLE IF NOT EXISTS ea_audit (
    audit_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    cycle_id TEXT,
    case_id TEXT,
    action_id TEXT,
    policy_version TEXT,
    source_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    classification_before TEXT,
    classification_after TEXT,
    action TEXT,
    risk_class TEXT,
    approval_required BOOLEAN,
    approval_id TEXT,
    tool_result TEXT,
    verification_result TEXT,
    error TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ea_audit_case_idx ON ea_audit(case_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS ea_audit_action_idx ON ea_audit(action_id, timestamp DESC);

CREATE TABLE IF NOT EXISTS ea_source_cursors (
    source TEXT PRIMARY KEY,
    cursor_value TEXT,
    cursor_kind TEXT NOT NULL,
    valid BOOLEAN NOT NULL DEFAULT TRUE,
    last_full_sync_at TIMESTAMPTZ,
    last_incremental_sync_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS ea_watch_registrations (
    watch_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    resource_key TEXT,
    remote_resource_id TEXT,
    expires_at TIMESTAMPTZ,
    state TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (state IN ('ACTIVE','RENEWAL_DUE','EXPIRED','STOPPED','ERROR'))
);

-- Sensitive message bodies/transcripts are intentionally absent.
