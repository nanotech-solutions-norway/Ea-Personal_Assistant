# Level 2 Managed Automation

Status: LEVEL_2A_ACTIVE / MANAGED_BACKEND_FOUNDATION_IMPLEMENTED_IN_REPOSITORY / NOT_DEPLOYED  
Level 2B: HOLD  
Level 2C: HOLD

The managed backend foundation now lives in:

- `level-2/backend/README.md`
- `level-2/backend/sql/`
- `level-2/backend/policy/`
- `level-2/backend/schemas/`
- `level-2/backend/ingestion/`
- `level-2/backend/security/`
- `level-2/backend/staging/`
- `level-2/backend/validation/`

The foundation covers persistent case/audit state, deterministic policy, idempotency, source→sink controls, Gmail/Calendar incremental ingestion contracts, least-privilege identity separation, and Level 2B.1 staging.

It does not deploy cloud infrastructure or activate Level 2B/2C.

Meeting/audio capture remains a separate privacy/consent-controlled future capability and is not enabled by the backend foundation.
