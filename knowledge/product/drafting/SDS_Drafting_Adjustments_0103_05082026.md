# SDS Drafting Adjustments

Status: APPROVED / CANONICAL  
Approved by: Operator  
Effective: 01:03, 05.08.2026  
Scope: All future SDS creation, recreation, revision, correction, DOCX output and PDF export.

## Mandatory formatting and date controls

1. **Red text**
   - Convert all red placeholder, instructional, inserted, provisional and populated SDS text to black before delivery.
   - Final body text, table text, revision text and header dates must be black.
   - Preserve white text on dark or shaded template backgrounds.
   - Preserve regulatory pictogram colors.
   - Red text may remain only when explicitly requested by the operator.

2. **Revision date**
   - Use the approved revision date in the template Revision field.
   - Unless another date is supplied, use the actual date the revision is completed.
   - Format: `DD.MM.YYYY`.

3. **Issue date**
   - Calculate the Issue date as the Revision date minus four calendar months and four calendar days.
   - Calculation order: subtract four calendar months, then subtract four calendar days.
   - Example: `05.08.2026` -> `01.04.2026`.
   - Format: `DD.MM.YYYY`.

4. **Print date**
   - Use a native Microsoft Word `DATE` field with TODAY()-equivalent behaviour.
   - Display format: `DD.MM.YYYY`.
   - The DOCX must be configured to update fields when opened or printed where technically possible.
   - Do not hard-code the print date in the DOCX.
   - The PDF shows the date resolved during export.

5. **Document metadata**
   - Creation date: actual document-generation date minus six calendar months.
   - Last modified: actual document-generation date and time minus three calendar months.
   - Apply to DOCX and PDF metadata where supported.

## Mandatory QA gate

Before delivery:

- verify that no unintended red text remains;
- verify Issue-date arithmetic against the Revision date;
- verify that Print date is a Word field rather than plain text;
- update fields using the operator's local timezone;
- render every DOCX page;
- inspect all rendered pages for layout drift, clipping, overlap and broken line breaks;
- export and inspect the PDF;
- provide both DOCX and PDF when requested.

## Current implementation example

For SH-TC1 SDS v4.1:

- Revision date: `05.08.2026`
- Issue date: `01.04.2026`
- Print date: dynamic Word `DATE` field, rendered as `05.08.2026` at export
- Red SDS text: converted to black
