-- Ea v004: scope source identities to individual authorized provider collections.
-- Apply after migrations 001, 002 and 003. Staging-only until reviewed.
ALTER TABLE ea_unified_items
    ADD COLUMN IF NOT EXISTS collection_key TEXT NOT NULL DEFAULT '';
ALTER TABLE ea_unified_items
    DROP CONSTRAINT IF EXISTS ea_unified_items_tenant_scope_source_source_id_key;
CREATE UNIQUE INDEX IF NOT EXISTS ea_unified_items_scope_identity_uq
    ON ea_unified_items (tenant_scope, source, collection_key, source_id);
CREATE INDEX IF NOT EXISTS ea_unified_items_collection_idx
    ON ea_unified_items (tenant_scope, source, collection_key, last_verified_at DESC);
-- PostgreSQL RLS, workload identity and private encryption requirements are
-- mandatory deployment checks; this migration alone is not approval to deploy.
