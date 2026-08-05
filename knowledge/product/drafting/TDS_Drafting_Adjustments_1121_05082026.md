# TDS Drafting Adjustments

Status: APPROVED / CANONICAL  
Approved by: Operator  
Effective: 11:51, 05.08.2026  
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
   - Applies to body paragraphs, values, data lines, bullet points, cautions, notes and explanatory text.

4. **Highlight interpretation**
   - Yellow review marking maps to `12 pt bold` primary section text.
   - Green review marking maps to `11 pt regular` subsection or label text.
   - Grey review marking maps to `10 pt regular` body or value text.
   - Review highlights are drafting annotations and must be removed from final DOCX and PDF output unless explicitly requested.
   - Preserve the controlled template font family, title display, logo, page setup, header, footer, table borders, separator lines and colour system.

## Canonical clause and paragraph-break rules

The first two pages of the operator-approved SH-TC1 TDS supplied on 05.08.2026 are the canonical spacing and paragraph-break reference.

- Treat each heading plus its associated value, paragraph or list as one clause block.
- Put every heading in its own paragraph.
- Put every continuous explanatory point or value in its own paragraph.
- Put every bullet, numbered item or other sub-point in its own paragraph/list item.
- Use one true paragraph break after each sub-point or data line, equivalent to pressing `Enter` once in Microsoft Word.
- Do not place an empty paragraph between consecutive bullets or consecutive data lines inside the same clause block.
- After the final value, paragraph or list item in a clause block, insert exactly one empty paragraph before the next clause heading.
- That one empty paragraph is both the ending space for the previous clause and the beginning space for the next clause.
- Do not insert two empty paragraphs between adjacent clause blocks.
- Preserve intentional section-separator lines and the spacing associated with them.
- Automatic visual wrapping at the right margin is not a paragraph break and must not be recreated manually.
- Do not use soft/manual line breaks (`Shift+Enter` or Word `w:br`) between separate clauses, data points or list items.
- Convert inherited soft breaks and multi-point paragraphs into true separate paragraphs before final rendering.
- Keep multiple sentences in one paragraph only when they form one continuous explanatory point.
- Ensure the first peer item in a list uses the same bullet/number structure and alignment as the succeeding items.
- Do not split one grammatical sentence across multiple bullet items.

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
- verify every separate sub-point is a true paragraph/list item;
- verify every clause block is followed by exactly one empty paragraph, except where an intentional section separator governs spacing;
- verify no duplicate empty paragraphs occur between clause blocks;
- verify no unintended soft/manual line breaks remain;
- compare the completed TDS against the approved first-two-page reference;
- render and inspect every DOCX page;
- export and inspect every PDF page;
- provide both DOCX and PDF when requested.

## Current implementation example

For SH-TC1 TDS v3.1:

- Primary headings: `12 pt bold`
- Subsection headings and labels: `11 pt regular`
- Body text and values: `10 pt regular`
- Canonical clause-block spacing propagated from the approved first two pages
- All separate points stored as true paragraphs/list items
- No Word soft-break elements remain
- Inherited peer-list alignment corrected
- Split contamination sentence merged into one bullet clause
- Review highlights removed
- Output length: `7 pages`
- Creation metadata: `05.02.2026`
- Last-modified metadata and visible field: `11:51, 05.05.2026`
