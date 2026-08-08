# 05B — Ea Canonical XLTM Template Usage Rule — 04:05, 08.08.2026

Status: CANONICAL / OPERATOR-INSTRUCTED  
Authority: Explicit operator instruction  
Scope: Quote, Packing List, RFQ and Purchase Order generation

## Purpose

Ea must use the registered canonical Excel macro-enabled templates below whenever the operator requests creation, drafting, recreation, conversion or population of the corresponding document, unless the operator explicitly names another template or requests a different format/layout.

The operator does not need to say "use the template". Requesting the document type is sufficient to trigger the canonical template.

## Canonical template mapping

| Operator intent | Canonical template | Target sheet | Drive file ID |
|---|---|---|---|
| Quote / quotation | `EA_Template_Quote_v1.0.xltm` | `Quote` | `1GNdKJerxGBmJQ75Z6ZmZrCfQA31Sk8Qv` |
| Packing list | `EA_Template_Packing_List_v1.0.xltm` | `Packing list` | `1RP-pUGYwcmZM8v0nyW4N8PHakDfLwWwO` |
| RFQ / request for quote | `EA_Template_RFQ_v1.0.xltm` | `RFQ` | `1_CKn7m-F4AAGkUaeiCRBEf77Xp02xxvO` |
| PO / purchase order | `EA_Template_PO_v1.0.xltm` | `PO` | `1NUitA_ITVS6oz8OK9u7_LaN5v_yOHwHM` |

Canonical Drive folder: `Canonical Document Templates` — ID `19A7iUWZ7WTowDR1TzRsTLmaraxCbIosH`.

## Invocation rule

Apply this rule automatically when the operator requests any semantically equivalent action, including:
- create/draft/generate/recreate a quote or quotation;
- create/draft/generate a packing list;
- create/draft/generate an RFQ or request for quote;
- create/draft/generate a PO or purchase order;
- extract information from attached/source files and create one of those documents;
- convert source information into one of those document types.

## Population workflow

1. Retrieve the corresponding canonical XLTM master from the registered Drive file.
2. Treat the XLTM workbook as authoritative for layout, workbook structure, formulas, validations, images, controls, supporting sheets and VBA.
3. Apply `05A_EA_DOCUMENT_TEMPLATE_RECREATION_CONVERSION_STATIC_RULES_0349_08082026.md` for extraction, source precedence, no-invention, formula preservation and validation.
4. Populate only transaction/project-specific fields required by the operator/source material.
5. Preserve formulas and supporting-sheet relationships. Do not flatten formulas into static results.
6. Preserve VBA/macros and macro-enabled format.
7. Save the populated working document as `.xlsm` unless the operator explicitly requests another editable format.
8. Generate PDF only from the designated target sheet when a fixed-layout/final/preview copy is requested.
9. Apply document-specific approved workflows and naming conventions, including quotation-specific approval, reference and filing rules, where applicable.
10. Validate source values, formulas, totals, target-sheet layout and PDF output before handoff.

## Template-specific rules

### Quote
- Use `Quote` as the operator-facing target sheet.
- Supporting product/customer/currency/freight/application-method sheets remain functional dependencies.
- Preserve the existing customer and product lookup/data-validation behavior.
- Existing quotation approval, reference-number, filename and Drive-filing rules remain controlling.

### Packing List
- Use the Quote-workbook-derived `Packing list` template.
- The hidden `Quote` sheet remains the upstream transaction data model; populate/reconcile it when required so delivery data, reference, items and quantities flow into the packing list.
- Preserve `PL-` reference logic and item-weight formulas.

### RFQ
- Use `RFQ` as the target sheet.
- Preserve product lookup, unit/price formulas, transport/carrier validations and supporting workbook sheets.
- Vendor and commercial fields are variable unless a current authoritative source confirms them.

### PO
- Use `PO` as the target sheet.
- The hidden `RFQ` sheet remains an upstream source for vendor/item/reference fields where the workbook relationship requires it.
- Preserve delivery-information, signature/branding and calculation logic.

## Precedence

1. Current explicit operator instruction.
2. Current document-specific APPROVED/CANONICAL workflow or explicitly designated alternative template.
3. This 05B canonical template mapping and usage rule.
4. 05A general document/template static rules.
5. General Ea document/template framework.
6. Verified source evidence.

Do not silently substitute an older workbook, older template, visually similar PDF, or prior populated example for a canonical template.

## Validation gate

Before release, confirm:
- correct canonical template and target sheet used;
- no unintended sample/customer/vendor values remain;
- formulas and validations remain present;
- no visible `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?` or `#N/A` errors;
- arithmetic/totals validate;
- VBA project remains present for macro-enabled output;
- PDF, when requested, contains only the intended target document;
- layout is consistent with the canonical template.

Validation status: `PASS`, `PASS WITH WARNINGS`, or `FAIL`.

## Runtime warning

The canonical template packages have passed structural, formula-error, visual and VBA-binary-preservation validation. Actual VBA/button execution requires Microsoft Excel runtime validation; do not claim macro execution was tested unless it was run in Excel.
