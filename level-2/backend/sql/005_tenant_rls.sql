-- 005: Enforcement-grade tenant isolation for EA staging projections.
-- Apply after 001-004, as the migration/owner role, not the restricted runtime role.
-- FORCE RLS protects table owners; SUPERUSER/BYPASSRLS still bypasses RLS.
-- Never run the EA application as a superuser, table owner or BYPASSRLS role.
-- A missing transaction-scoped ea.tenant_scope must DENY access by default.

ALTER TABLE ea_source_cursors
    ADD COLUMN IF NOT EXISTS tenant_scope TEXT;
ALTER TABLE ea_source_cursors
    ADD COLUMN IF NOT EXISTS collection_key TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS ea_unified_items_tenant_item_uq
    ON ea_unified_items(tenant_scope, item_key);
-- Prevent a tenant's link row from pointing at another tenant's projection.
ALTER TABLE ea_unified_links
    ADD CONSTRAINT ea_unified_links_tenant_fk
    FOREIGN KEY (tenant_scope, item_key)
    REFERENCES ea_unified_items(tenant_scope, item_key);

ALTER TABLE ea_unified_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_unified_items FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS ea_unified_items_scope ON ea_unified_items;
CREATE POLICY ea_unified_items_scope ON ea_unified_items
    USING (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''))
    WITH CHECK (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''));

ALTER TABLE ea_unified_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_unified_links FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS ea_unified_links_scope ON ea_unified_links;
CREATE POLICY ea_unified_links_scope ON ea_unified_links
    USING (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''))
    WITH CHECK (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''));

ALTER TABLE ea_sync_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_sync_runs FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS ea_sync_runs_scope ON ea_sync_runs;
CREATE POLICY ea_sync_runs_scope ON ea_sync_runs
    USING (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''))
    WITH CHECK (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''));

ALTER TABLE ea_source_cursors ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_source_cursors FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS ea_source_cursors_scope ON ea_source_cursors;
CREATE POLICY ea_source_cursors_scope ON ea_source_cursors
    USING (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''))
    WITH CHECK (tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), ''));

-- Existing legacy cursor rows have NULL tenant_scope and intentionally become
-- invisible to restricted workers until explicitly reconciled/retired.
-- This migration does NOT secure legacy ea_cases, ea_actions, ea_approvals,
-- ea_audit, ea_watch_registrations, or ea_ingest_events. Those tables require
-- separate single-tenant isolation or explicit tenant-scoped migrations.
-- Do not activate a shared multi-tenant service on the legacy tables.
