-- Ea Level 2 durable ingestion event store
-- Apply after 001_initial_schema.sql.

CREATE TABLE IF NOT EXISTS ea_ingest_events (
    event_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    cursor_value TEXT NOT NULL,
    resource_key TEXT,
    event_kind TEXT,
    received_at TIMESTAMPTZ NOT NULL,
    processing_status TEXT NOT NULL DEFAULT 'RECEIVED',
    processed_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    error TEXT,
    CHECK (source IN ('gmail','google_calendar')),
    CHECK (processing_status IN ('RECEIVED','PROCESSING','PROCESSED','FAILED','IGNORED'))
);

CREATE INDEX IF NOT EXISTS ea_ingest_events_source_cursor_idx
    ON ea_ingest_events(source, cursor_value);

CREATE INDEX IF NOT EXISTS ea_ingest_events_status_idx
    ON ea_ingest_events(processing_status, received_at);

-- Event rows intentionally store trigger metadata/cursors, not full email bodies
-- or Calendar event bodies. Complete source data is re-read from the authoritative
-- connector/API during case reconciliation.
