# Ea Release Manifest

Status: LEVEL_1_APPROVED / LEVEL_2A_ACTIVE / PERSONAL_FINANCE_CAPABILITY_APPROVED

## Active source folder

`active-source/`

The current compact active-source set includes the approved Personal Finance Senior Advisor domain source:

- `active-source/04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md`

## Personal Finance Senior Advisor

Implementation sources:

- `knowledge/finance/PERSONAL_FINANCE_ADVISOR_PROTOCOL_CURRENT.md`
- `knowledge/finance/PERSONAL_FINANCE_ADVISOR_CORE_INSTRUCTIONS.md`
- `knowledge/finance/PERSONAL_FINANCE_ADVISOR_SPECIFICATION_CURRENT.md`
- `knowledge/finance/EA_HOUSEHOLD_BUDGETING_PRIVATE_STATE_RULES_CURRENT.md`
- `config/personal-finance/financial_state.schema.json`
- `config/project/EA_PROJECT_INSTRUCTION_BLOCK.md`
- `config/custom-gpt/EA_CUSTOM_GPT_INSTRUCTION_BLOCK.md`
- `config/custom-gpt/EA_CUSTOM_GPT_KNOWLEDGE_FILE_LIST.md`

Governance:

- R0/R1 analysis and preparation are allowed within authorized scope.
- R2 planning writes require explicit operator instruction and readback.
- R3 consequential external financial actions require exact operator approval.
- R4 transfers, payments, trades, borrowing, account actions, financial/legal signing, ownership changes and credential/security changes remain human-only.
- No user-specific raw financial records are included in this repository release.
- Household budget state is private Drive state; GitHub stores only sanitized operating rules, schemas and validation logic.
- Household budgeting uses explicit operator input > latest approved private state > verified transaction evidence > derived values > assumptions.

## Validation

Personal-finance static integration validation:

- workflow: `.github/workflows/ea-personal-finance-validation.yml`
- result on 06.10.2026: **PASS**
- Security baseline: **PASS**
- CodeQL: **PASS**

Live/synthetic finance regression using synthetic or explicitly approved user data remains a separate acceptance layer before high-impact production reliance.

## Level 2 status

- Level 2A: ACTIVE for controlled internal autonomy.
- Level 2B: HOLD.
- Level 2C: HOLD.

Personal-finance integration does not expand Level 2 authority.

## Release gate

The Personal Finance Senior Advisor repository integration is approved and active as an Ea capability. Live ChatGPT runtime/project configuration remains dependent on the available ChatGPT configuration surface and source loading.
