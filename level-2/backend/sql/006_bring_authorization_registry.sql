-- EA Bring authorization registry. NEW TABLES ONLY; does not migrate provider data.
-- Apply as dedicated migration owner. Never grant runtime INSERT/UPDATE/DELETE.
-- The request identity/tenant settings MUST be set transaction-locally by the
-- trusted backend from a cryptographically verified identity, never headers.
-- Do not connect as table owner, superuser or a BYPASSRLS role.

CREATE TABLE IF NOT EXISTS ea_bring_tenant_accounts (
    tenant_scope TEXT PRIMARY KEY CHECK (length(tenant_scope) BETWEEN 1 AND 128),
    customer_number TEXT NOT NULL CHECK (customer_number ~ '^[0-9]{6,20}$'),
    vault_secret_ref TEXT NOT NULL CHECK (
        vault_secret_ref ~ '^https://[a-z0-9-]+[.]vault[.]azure[.]net/secrets/[A-Za-z0-9-]+$'
    ),
    active BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (tenant_scope, customer_number)
);

CREATE TABLE IF NOT EXISTS ea_bring_principal_grants (
    issuer TEXT NOT NULL,
    subject TEXT NOT NULL,
    tenant_scope TEXT NOT NULL,
    permission TEXT NOT NULL CHECK (permission = 'bring.tracking.read'),
    customer_number TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (issuer, subject, tenant_scope),
    FOREIGN KEY (tenant_scope, customer_number)
      REFERENCES ea_bring_tenant_accounts (tenant_scope, customer_number)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ea_bring_shipment_provenance (
    tenant_scope TEXT NOT NULL,
    tracking_digest TEXT NOT NULL CHECK (tracking_digest ~ '^[0-9a-f]{64}$'),
    customer_number TEXT NOT NULL,
    evidence_source TEXT NOT NULL CHECK (evidence_source = 'authenticated_mybring_booking'),
    reviewed_at TIMESTAMPTZ NOT NULL,
    independently_approved BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (tenant_scope, tracking_digest),
    FOREIGN KEY (tenant_scope, customer_number)
      REFERENCES ea_bring_tenant_accounts (tenant_scope, customer_number)
      ON UPDATE RESTRICT ON DELETE RESTRICT
);

-- FORCE also restricts table owners (though a real runtime owner role is forbidden).
ALTER TABLE ea_bring_tenant_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_bring_tenant_accounts FORCE ROW LEVEL SECURITY;
ALTER TABLE ea_bring_principal_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_bring_principal_grants FORCE ROW LEVEL SECURITY;
ALTER TABLE ea_bring_shipment_provenance ENABLE ROW LEVEL SECURITY;
ALTER TABLE ea_bring_shipment_provenance FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS ea_bring_actor_grant_read ON ea_bring_principal_grants;
CREATE POLICY ea_bring_actor_grant_read ON ea_bring_principal_grants
FOR SELECT USING (
    issuer = NULLIF(current_setting('ea.actor_issuer', true), '')
    AND subject = NULLIF(current_setting('ea.actor_subject', true), '')
    AND tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), '')
);

DROP POLICY IF EXISTS ea_bring_tenant_account_read ON ea_bring_tenant_accounts;
CREATE POLICY ea_bring_tenant_account_read ON ea_bring_tenant_accounts
FOR SELECT USING (
    tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), '')
    AND EXISTS (
        SELECT 1 FROM ea_bring_principal_grants grant_row
        WHERE grant_row.tenant_scope = ea_bring_tenant_accounts.tenant_scope
          AND grant_row.customer_number = ea_bring_tenant_accounts.customer_number
          AND grant_row.active IS TRUE
          AND grant_row.permission = 'bring.tracking.read'
    )
);

DROP POLICY IF EXISTS ea_bring_shipment_provenance_read ON ea_bring_shipment_provenance;
CREATE POLICY ea_bring_shipment_provenance_read ON ea_bring_shipment_provenance
FOR SELECT USING (
    tenant_scope = NULLIF(current_setting('ea.tenant_scope', true), '')
    AND EXISTS (
        SELECT 1 FROM ea_bring_principal_grants grant_row
        WHERE grant_row.tenant_scope = ea_bring_shipment_provenance.tenant_scope
          AND grant_row.customer_number = ea_bring_shipment_provenance.customer_number
          AND grant_row.active IS TRUE
          AND grant_row.permission = 'bring.tracking.read'
    )
);

-- Provision a distinct NOLOGIN group role and restricted LOGIN role privately
-- during deployment; do not include credentials/role grants in this migration.
-- SELECT-only grants are staged/administered independently and must be verified.
-- NO INSERT/UPDATE/DELETE/REFERENCES granted to the runtime role.
