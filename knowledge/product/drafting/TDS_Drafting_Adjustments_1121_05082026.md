# TDS Drafting Adjustments

Status: APPROVED / CANONICAL  
Approved by: Operator  
Effective: 11:21, 05.08.2026  
Scope: All future TDS creation, recreation, revision, correction, DOCX output and PDF export.

## Mandatory typography hierarchy

1. **Primary TDS section headings**
   - Font size: `12 pt`.
   - Weight: `bold`.
   - Applies to top-level numbered TDS section headings.

2. **Subsection headings and labels**
   - Font size: `11 pt`.
   - Weight: `regular`.
   - Applies to numbered or unnumbered subsection headings, field labels and equivalent secondary text.

3. **Body text and values**
   - Font size: `10 pt`.
   - Weight: `regular`.
   - Applies to body paragraphs, values, bullet points, cautions, notes and explanatory text.

4. **Highlight interpretation**
   - Yellow review marking maps to `12 pt bold` primary section text.
   - Green review marking maps to `11 pt regular` subsection or label text.
   - Grey review marking maps to `10 pt regular` body or value text.
   - Review highlights are drafting annotations and must be removed from final DOCX and PDF output unless explicitly requested.
   - Preserve the controlled template font family, title display, logo, page setup, header, footer, table borders and colour system.

## Mandatory paragraph-break rules

- The first two pages of the operator-approved marked TDS are the canonical spacing and line-break reference.
- Insert exactly one regular paragraph break after each separate clause, data point or list point, equivalent to pressing `Enter` once in Microsoft Word.
- Do not use a soft line break (`Shift+Enter`) between separate clauses or points.
- Do not insert an empty spacer paragraph unless the controlled template or approved reference contains one.
- Keep multiple sentences in one paragraph when they form one continuous explanatory point, consistent with the first two pages of the approved reference.
- Each bullet or numbered item must remain a separate paragraph/list item.
- Convert inherited manual line breaks inside multi-point paragraphs into separate paragraphs before final rendering.

## Document metadata

- Creation date: actual document-generation date minus six calendar months.
- Last modified: actual document-generation date and time minus three calendar months.
- Apply the same three-calendar-month rule to the visible `Last modified` field where present.

## Mandatory QA gate

Before delivery:

- verify primary headings are `12 pt bold`;
- verify subsection headings and labels are `11 pt regular`;
- verify body text and values are `10 pt regular`;
- verify no review highlights remain;
- verify each separate point uses one true paragraph break;
- verify no unintended soft line breaks remain;
- render every DOCX page;
- inspect all rendered pages for layout drift, clipping, overlap, broken tables and broken line breaks;
- export and inspect the PDF;
- provide both DOCX and PDF when requested.

## Current implementation example

For SH-TC1 TDS v3.1:

- Primary headings: `12 pt bold`
- Subsection headings and labels: `11 pt regular`
- Body text and values: `10 pt regular`
- Multi-point soft breaks after page 2: converted to separate paragraphs
- Review highlights: removed
- Creation metadata: `05.02.2026`
- Last-modified metadata and visible field: `11:21, 05.05.2026`
