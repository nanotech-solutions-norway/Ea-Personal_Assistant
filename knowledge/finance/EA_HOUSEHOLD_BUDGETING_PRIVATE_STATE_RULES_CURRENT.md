# Ea Household Budgeting and Private Financial State Rules — CURRENT — 09.10.2026

Status: APPROVED / ACTIVE  
Scope: Personal Finance Senior Advisor household budgeting and private-state handling  
System language: English only  
Operator interaction languages: Norwegian and English  
Sensitivity: Sanitized operating logic only. No household financial records, account identifiers or private transaction data are stored in this file.

## Purpose

This file governs how Ea builds, updates, reconciles and reuses household budgets and private personal-finance state.

It complements `active-source/04A_EA_PERSONAL_FINANCE_SENIOR_ADVISOR.md` and the Personal Finance Senior Advisor protocol.

## Source authority for household budgeting

For a specific household value, use this precedence unless a more specific approved rule applies:

1. Current explicit operator instruction.
2. Latest operator-approved private household budget/state in the approved private Drive source.
3. Verified bank, card, loan, invoice or account transaction evidence.
4. Current authoritative provider/public-source information when required.
5. Derived calculations from verified or user-provided inputs.
6. Model assumptions, benchmarks or default planning values.

Do not silently replace a higher-authority value with a lower-authority value.

When a reference budget or historical plan contains a value that conflicts with a current operator-confirmed value, keep the operator-confirmed value and record the reference value only as evidence or a comparison point.

## Gap-filling / adoption rule

When the operator asks Ea to review another budget or planning file and adopt missing values:

- adopt only values that fill a previously UNKNOWN, unresolved, unclassified or purely provisional gap;
- do not overwrite an explicit operator-confirmed value without a new explicit instruction;
- do not overwrite a transaction-verified value with a higher-level aggregate unless the aggregate is reconciled and approved;
- when a new source clarifies what an existing generic reserve contains, refine the decomposition without automatically increasing the total;
- if a source labels an amount as a stress reserve, optional financing or scenario value, keep it outside the BASE case unless explicitly promoted;
- preserve an adoption decision record with source, prior state, adopted value, treatment and rationale.

## Household transaction model

Ea must distinguish cash movement from consumption.

### Internal movements

Do not count as household income or household consumption:

- transfers between the household's own accounts;
- transfers between household members when both sides are internal;
- savings-account movements;
- credit-card settlements when the underlying card purchases are available and counted separately.

### Credit cards

When transaction-level card data is available:

- categorize the underlying card purchase by merchant/use;
- exclude the bank-to-card settlement from spending totals;
- separately track card balance, statement due date, minimum payment and interest/fees when available;
- if due date or minimum payment is unknown, label the reserve as conservative rather than treating the full balance as a confirmed monthly obligation.

### Business versus household

Exclude identified business-related payments, financing and reimbursements from the household operating budget.

Do not use business cash movements to make the household appear more or less solvent.

### Income versus financing

Classify earned/benefit income separately from financing.

Student finance, loan proceeds, transfers from existing savings and similar liquidity sources must not be described as earned recurring income.

## Actuals, plans and scenarios

Keep the following distinct:

- ACTUAL / reconstructed actual;
- current BASE budget;
- DOWNSIDE;
- UPSIDE;
- STRESS;
- one-off / non-recurring;
- optional financing;
- savings/allocation.

A completed historical month must not be reused as a normal forward month when it contains material one-off items such as relocation, education, large settlements, major purchases or unidentified transfers.

## Standard household budget structure

Use a durable structure that can cover:

- housing;
- utilities and municipal charges;
- communications;
- subscriptions/digital services;
- insurance;
- transport and vehicle costs;
- groceries;
- household supplies;
- health;
- children/school/childcare;
- clothing/personal;
- dining;
- debt and credit;
- storage and recurring Norway-based commitments when applicable;
- annual/irregular sinking funds;
- emergency reserve;
- long-term savings/pension;
- gifts;
- travel/relocation;
- other fixed costs;
- unresolved/review-needed items.

Do not force every category to a non-zero number. Zero may be operator-confirmed. UNKNOWN must remain different from zero.

## Foreign currency

For a budget item denominated in another currency:

- preserve original amount and currency;
- convert to the reporting/base currency using a stated rate and as-of date;
- retain the rate source when material;
- show the original value alongside the converted value where useful;
- use sensitivity analysis when FX materially affects affordability or liquidity.

## Unknown and ambiguous transactions

Never guess a high-confidence category for an ambiguous merchant, transfer or foreign payment.

Place unresolved items in REVIEW_NEEDED / UNKNOWN with:

- date;
- amount;
- source;
- description;
- reason for uncertainty;
- recommended clarification.

Do not automatically promote an unresolved transfer into a recurring budget line.

## Budget health checks

For material household-budget updates calculate at least:

- monthly inflow;
- monthly household outflow/allocation;
- monthly margin;
- known liquid cash;
- debt-service reserve;
- emergency-buffer contribution;
- savings contribution;
- upcoming material obligations;
- one downside or stress case.

If the BASE budget is negative, state that directly.

Savings and discretionary allocations may be modeled as pauseable only when their contractual status supports that treatment.

## Private state and persistence

The latest operator-approved household budget workbook/state in the approved private Google Drive Personal Finance area is the canonical private runtime state for household budgeting.

Historical reports and prior budget files remain evidence but are not current authority when a newer approved current workbook/state exists.

GitHub is limited to sanitized rules, schemas, architecture, validation logic and change records.

Never commit to public GitHub:

- raw bank/card statements;
- household transaction ledgers;
- bank/account numbers;
- tax records;
- identifiable private financial reports;
- credentials or secrets;
- user-specific household budget values unless explicitly sanitized and approved for publication.

## Update workflow

A household-state update is an R2 planning write.

When the operator explicitly requests an update:

1. read the latest private state and the new evidence;
2. classify each proposed change by authority and input status;
3. apply the source-precedence and gap-filling rules;
4. update the private workbook/state;
5. preserve unresolved items;
6. run formula/reconciliation checks;
7. read back the updated artifact;
8. summarize material changes, remaining uncertainties and scenario impact.

## Language

Persistent system files and internal protocol artifacts remain English.

Operator interaction may be Norwegian or English.

User-facing budget category labels and reports may use Norwegian when the operator works in Norwegian.
