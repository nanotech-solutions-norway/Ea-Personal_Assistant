# Ea Label Creation Register — 12:10, 31.07.2026

Status: ACTIVE_OPERATIONAL_REGISTER / REGULATORY_RELEASE_PENDING_REVIEW  
Scope: Brother P-touch label creation, `.lbx` output, CLP/REACH source handling, validation and file tracking.

## 1. Current operating configuration

| Field | Approved operating setting |
|---|---|
| Primary authoring software | Brother P-touch Editor |
| Primary editable format | `.lbx` |
| Default label dimensions | 62 mm width × 102 mm length |
| Default orientation | Vertical / portrait |
| Default nominal quantity | 500 ml unless the user specifies another quantity |
| Preferred construction | Editable text objects; embedded images only for required pictograms or when an image-based version is explicitly requested |
| Default language | English unless explicitly instructed otherwise |
| Preview requirement | Generate a PNG preview for each `.lbx` |
| Package requirement | Provide individual files and a ZIP package |
| Naming rule | Use only the user-approved product name on customer-facing labels |
| Legacy/source names | May be used internally as source references only; do not expose them on the label unless the user explicitly approves a quoted source name |

## 2. Source and regulatory controls

1. Use the latest verified SDS as the primary source for classification, pictograms, signal word, H-statements, P-statements, supplemental statements, UFI and supplier details.
2. Do not infer a hazardous or non-hazardous classification from marketing materials, technical sheets or old labels.
3. Where the SDS is old, incomplete, conflicts with another source, leaves the UFI blank, or does not match the intended private-label product identifier or supplier, classify the label as `PENDING_REVIEW`.
4. Regulatory, CLP, REACH, poison-centre, UFI, dangerous-goods and market-placement conclusions remain `QUALIFIED_REVIEW_REQUIRED`.
5. The product identifier shown on the label must match the current SDS used for market placement.
6. For hazardous products, group pictograms, signal word, hazard statements and precautionary statements together and preserve the exact SDS wording.
7. For products not classified as hazardous in the supplied SDS, do not add hazard pictograms, a signal word or H-statements without a current classification source.
8. Before release, verify local-language requirements for the market where the product will be sold.
9. Open every `.lbx` in Brother P-touch Editor and confirm dimensions, print margins, text wrapping, clipping, object editability and printer/media compatibility.
10. A generated label is a controlled draft until operator review and, where applicable, qualified chemical/regulatory review are complete.

## 3. Label layout rules established in this workstream

- Default page: 62 mm × 102 mm portrait.
- Use the largest practical font while maintaining complete, unclipped text.
- Product name is the largest text element.
- Nominal quantity is placed at the upper or lower right according to template geometry.
- Safety text is grouped under clear headings.
- Supplier and emergency details are placed in a separate lower section.
- Pictograms are embedded as individual images only when required by the current SDS.
- An image-based label version must cover the complete label area.
- Text-based versions must remain editable in P-touch Editor.

## 4. Label history

| Product | Format | Dimensions | Construction | Classification source status | Register status |
|---|---|---:|---|---|---|
| Hirec PFW9 | `.lbx` | 62 × 102 mm | Editable text; separate image version created | Source SDS used | Generated; final release review required |
| Hirec PFS10 | `.lbx` | 62 × 102 mm | Editable text with required GHS pictograms | Source SDS used | Generated; final release review required |
| Hirec-R | `.lbx` | 62 × 120 mm | Editable text with required GHS pictograms | Source SDS used; UFI unresolved | Generated; `PENDING_REVIEW` |
| TextileCoat65 | `.lbx` | 62 × 102 mm | Editable text; no pictograms added | Uploaded source SDS dated 18.02.2008 | Generated draft; `PENDING_CURRENT_SDS_AND_CLP_REVIEW` |
| FabricCoat37 | `.lbx` | 62 × 102 mm | Editable text; no pictograms added | Uploaded source SDS dated 15.02.2008 | Generated draft; `PENDING_CURRENT_SDS_AND_CLP_REVIEW` |

## 5. Current product-specific instructions

### TextileCoat65

- Use only the product name `TextileCoat65`.
- Do not display the source trade name or source brand.
- Use the 62 mm × 102 mm portrait text template.
- No pictograms, signal word or H-statements were added because the supplied SDS does not classify the preparation as hazardous.
- Include source-supported handling, first-aid, frost-protection, spill and disposal information.
- Status: `PENDING_CURRENT_SDS_AND_CLP_REVIEW`.

### FabricCoat37

- Use only the product name `FabricCoat37`.
- Do not display the source trade name or source brand.
- Use the 62 mm × 102 mm portrait text template.
- No pictograms, signal word or H-statements were added because the supplied SDS does not classify the preparation as hazardous.
- Include source-supported handling, first-aid, frost-protection, environmental and disposal information.
- Status: `PENDING_CURRENT_SDS_AND_CLP_REVIEW`.

## 6. Release gate

A label may move from draft to release-ready only after:

- a current SDS matching the exact product identifier is available;
- the EU/EEA supplier identity and contact details are confirmed;
- classification and labelling are reviewed under the current CLP regime;
- UFI and poison-centre notification requirements are resolved where applicable;
- language requirements are confirmed for each target market;
- the `.lbx` opens correctly in P-touch Editor;
- a physical print test confirms dimensions, readability and no clipping;
- operator approval is recorded.

## 7. Current decision classification

| Decision | Status |
|---|---|
| 62 × 102 mm portrait as default label geometry | APPROVED_BY_CURRENT_USER_INSTRUCTION |
| Brother P-touch `.lbx` as primary editable output | APPROVED_BY_CURRENT_USER_INSTRUCTION |
| Editable text objects as default construction | APPROVED_BY_CURRENT_USER_INSTRUCTION |
| `TextileCoat65` and `FabricCoat37` as exclusive customer-facing names | APPROVED_BY_CURRENT_USER_INSTRUCTION |
| Current regulatory release of labels based on 2008 SDS files | PENDING_REVIEW / QUALIFIED_REVIEW_REQUIRED |
