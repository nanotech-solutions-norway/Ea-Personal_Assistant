# Ea Gmail Reply Signature Override — 02:20, 18.08.2026

**Status:** APPROVED / CANONICAL / OPERATOR-INSTRUCTED  
**Effective:** 18.08.2026 at 02:20 Europe/Oslo  
**Updated:** 20.08.2026 — exact visual formatting and font scale confirmed against prior sent Gmail messages and operator screenshot `Screenshot_20260820_085239_Gmail.jpg`  
**Subsystem:** Gmail / Email drafting  
**Authority:** Current explicit operator instruction

## Rule

Whenever Ea creates, updates, or replaces a Gmail draft that is a **reply to an existing email or Gmail thread**, Ea must append Ruben A. Meyer's exact approved signature block after the email body.

Do not omit, abbreviate, paraphrase, or replace the signature with a generic sign-off unless Ruben explicitly instructs otherwise for the specific draft.

## Exact signature text and line breaks

Use exactly these six lines, with **single line breaks only and no blank lines inside the signature block**:

With kind regards,  
Ruben A. Meyer  
Chief Technology Officer  
NanoTech Solutions Norway AS  
Hofslundveien 6, N-3090 Hof, Norway  
Office: +47 33 74 00 24 | Mobile: +47 980 30 283

## Exact Gmail visual formatting

The signature must visually match the operator-approved Gmail screenshot `Screenshot_20260820_085239_Gmail.jpg` and the normal scale of Ruben's previous sent Gmail messages:

- Use compact Gmail-style spacing; **no paragraph gaps or blank lines between signature lines**.
- Entire signature block is *italic*.
- `NanoTech Solutions Norway AS` is **bold italic** and displayed in the approved light purple/magenta accent, approximately `#D49CF0` in the supplied screenshot.
- All other signature text uses the normal Gmail foreground color so it remains readable in Gmail light/dark themes.
- Keep the signature at normal Gmail email-body scale; do not enlarge individual lines.
- When Ea supplies explicit HTML formatting, use **13 px** for the email body and signature unless a current explicit instruction requires another size. This replaces the earlier 14 px rule.
- Use a standard Gmail-compatible sans-serif font stack such as Arial/Helvetica/sans-serif.
- Use compact line-height of approximately 1.3–1.35.
- Do not insert extra margins, padding, spacer paragraphs, tables, or blank `<div>` elements between signature lines.
- If the company name is linked to `https://www.nanotech-solutions.com/`, preserve the bold-italic purple/magenta appearance and do not allow default link styling to add an underline or replace the approved color.

Recommended HTML structure when Ea must construct the signature explicitly:

```html
<div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.35;font-style:italic;margin:0;padding:0;">
  With kind regards,<br>
  Ruben A. Meyer<br>
  Chief Technology Officer<br>
  <a href="https://www.nanotech-solutions.com/" style="font-weight:700;font-style:italic;color:#D49CF0;text-decoration:none;">NanoTech Solutions Norway AS</a><br>
  Hofslundveien 6, N-3090 Hof, Norway<br>
  Office: +47 33 74 00 24 | Mobile: +47 980 30 283
</div>
```

## Validation before saving a Gmail reply draft

Before reporting a Gmail reply draft as complete, verify:

1. The signature appears exactly once.
2. The signature has no blank lines between its six lines.
3. All six lines are italic.
4. `NanoTech Solutions Norway AS` is bold italic and purple/magenta.
5. The body and signature use the normal prior-email scale; explicit HTML defaults to 13 px.
6. The signature is compact and not vertically stretched.
7. No duplicate automatic signature has been added.
8. Attachments and the body above the signature remain unchanged unless the operator requested other edits.

If an existing Gmail draft with attachments cannot be edited in place by the connector, replace it with a new draft in the same thread, preserve the attachments, and remove the superseded draft so only the corrected draft remains.

## Supersession

This rule supersedes all older Ea instructions stating that Gmail reply drafts should omit the signature block or rely on the sender's automatic/default Gmail signature, including conflicting wording in the existing Gmail business-email-watch prompt and email-language profile.

It also supersedes the earlier 18.08.2026 signature-spacing representation that showed blank lines between signature lines and the earlier 20.08.2026 14 px HTML sizing rule.

For a new outbound email that is **not** a reply, follow the current task instruction and the applicable email drafting workflow unless Ruben gives a specific signature instruction.
