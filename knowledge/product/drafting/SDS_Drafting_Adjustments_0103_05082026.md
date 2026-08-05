# SDS Drafting Adjustments

Status: APPROVED / CANONICAL  
Approved by: Operator  
Effective: 11:51, 05.08.2026  
Scope: All future SDS creation, recreation, revision, correction, DOCX output and PDF export.

## Mandatory typography hierarchy

1. **Primary SDS section headings**
   - Font size: `12 pt`.
   - Weight: `bold`.
   - Applies to section banners and equivalent top-level SDS headings.

2. **Subsection headings and labels**
   - Font size: `11 pt`.
   - Weight: `regular`.
   - Applies to subsection headings, field labels, column headings, table labels and equivalent secondary text.

3. **Body text and values**
   - Font size: `10 pt`.
   - Weight: `regular`.
   - Applies to body paragraphs, hazard and precautionary statements, explanatory text, notes, table values and ordinary list content.

4. **Highlight interpretation**
   - Yellow review marking maps to `12 pt bold` primary section text.
   - Green review marking maps to `11 pt regular` subsection or label text.
   - Grey review marking maps to `10 pt regular` body or value text.
   - Review highlights must be removed from the final DOCX and PDF unless explicitly requested.
   - Preserve the controlled font family, page setup, logo, header/footer structure, table widths, borders, shading and regulatory pictogram colours.

5. **Tables and fixed display elements**
   - Section-banner table text uses `12 pt bold`.
   - Column headings and field-label cells use `11 pt regular`.
   - Data and value cells use `10 pt regular`.
   - Do not retain bold placeholder emphasis in body/value cells.
   - The main SDS title, regulatory subtitle and fixed header display elements retain the controlled template display styling.

## Relationship to the TDS spacing rule

- The TDS clause-block blank-line algorithm does not automatically apply to SDS documents.
- Preserve the controlled SDS template paragraph spacing, table continuity and regulatory section flow unless the operator gives a separate SDS line-break instruction.
- Do not add empty paragraphs between table rows, hazard statements or regulatory list items solely to imitate the TDS layout.

## Mandatory formatting and date controls

1. **Red text**
   - Convert all red placeholder, instructional, inserted, provisional and populated SDS text to black before delivery.
   - Final body text, table text, revision text and header dates must be black.
   - Preserve white text on dark or shaded template backgrounds.
   - Preserve regulatory pictogram colours.
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
   - Configure the DOCX to update fields on open or print where technically possible.
   - Do not hard-code the print date.
   - The PDF shows the date resolved during export.

5. **Document metadata**
   - Creation date: actual document-generation date minus six calendar months.
   - Last modified: actual document-generation date and time minus three calendar months.
   - Apply to DOCX and PDF metadata where supported.

## Mandatory QA gate

Before delivery:

- verify primary section headings are `12 pt bold`;
- verify subsection headings and labels are `11 pt regular`;
- verify body text and values are `10 pt regular`;
- verify all table cells follow the same hierarchy;
- verify no review highlights remain;
- verify no unintended red text remains;
- verify Issue-date arithmetic against the Revision date;
- verify the Print date is a native Word field rather than plain text;
- update fields using the operator's local timezone;
- render and inspect every DOCX page;
- export and inspect every PDF page;
- provide both DOCX and PDF when requested.

## Current implementation example

For SH-TC1 SDS v4.1:

- Revision date: `05.08.2026`
- Issue date: `01.04.2026`
- Print date: dynamic Word `DATE` field, rendered as `05.08.2026` at export
- Primary headings: `12 pt bold`
- Subsection headings and labels: `11 pt regular`
- Body text and values: `10 pt regular`
- Table hierarchy validated
- Red SDS text converted to black
- Review highlights removed
- Output length: `22 pages`
- Regulatory status: `DRAFT – PENDING QUALIFIED REGULATORY REVIEW`
