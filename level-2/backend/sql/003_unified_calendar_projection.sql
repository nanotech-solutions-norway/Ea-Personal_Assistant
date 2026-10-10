-- Ea cross-platform projection. Apply after 001 and 002.
-- Private managed PostgreSQL ONLY. Never mirror rows into public GitHub/Drive.
CREATE TABLE IF NOT EXISTS ea_unified_items (
    item_key TEXT PRIMARY KEY,
    tenant_scope TEXT NOT NULL,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_revision TEXT NOT NULL,
    item_kind TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('active','deleted')),
    display_title TEXT,
    due_at TIMESTAMPTZ,
    timezone TEXT,
    last_verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_scope, source, source_id)
);
CREATE INDEX IF NOT EXISTS ea_unified_items_due_idx
    ON ea_unified_items (tenant_scope, due_at) WHERE state = 'active';
CREATE TABLE IF NOT EXISTS ea_unified_links (
    tenant_scope TEXT NOT NULL,
    commitment_id TEXT NOT NULL,
    item_key TEXT NOT NULL REFERENCES ea_unified_items(item_key),
    evidence_kind TEXT NOT NULL CHECK (evidence_kind IN ('operator_confirmed','canonical_case_id','verified_source_reference')),
    verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_scope, commitment_id, item_key)
);
CREATE TABLE IF NOT EXISTS ea_sync_runs (
    run_id TEXT PRIMARY KEY,
    tenant_scope TEXT NOT NULL,
    source TEXT NOT NULL,
    collection_key TEXT NOT NULL,
    mode TEXT NOT NULL CHECK (mode IN ('full','incremental','manual_snapshot')),
    status TEXT NOT NULL CHECK (status IN ('STARTED','CAPTURED','PERSISTED','READBACK_PASS','BLOCKED','FAILED')),
    pages_fetched INTEGER NOT NULL DEFAULT 0,
    collection_complete BOOLEAN NOT NULL DEFAULT FALSE,
    items_changed INTEGER NOT NULL DEFAULT 0,
    cursor_committed BOOLEAN NOT NULL DEFAULT FALSE,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ea_sync_runs_scope_idx
    ON ea_sync_runs(tenant_scope,source,collection_key,started_at DESC);
-- Isolation is mandatory at query and authorization layer. Add DB RLS in deployment
-- against tenant identity; repository DDL alone is not a safe multi-tenant service.
