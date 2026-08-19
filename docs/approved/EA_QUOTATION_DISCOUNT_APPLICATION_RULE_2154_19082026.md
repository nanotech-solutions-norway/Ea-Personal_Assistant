# Ea Quotation Discount Application Rule — 21:54, 19.08.2026

**Status:** APPROVED / CANONICAL  
**Authority:** Current explicit operator instruction  
**Subsystem:** Documents / Quotations  
**Scope:** ALL QUOTATIONS

## 1. Discount field is controlling display location

When a quotation includes an approved discount, enter the discount in the existing `Discount` field in the `Terms and conditions` section.

Do not represent a normal quotation discount as a separate negative item line in the invoice/quotation items table unless the operator explicitly instructs otherwise for that specific quotation.

## 2. Product-only discount treatment

When the operator approves a discount that applies only to specified main products:

- reduce the affected product unit prices directly;
- recalculate each affected product subtotal from the discounted unit price and quantity;
- leave transport, freight, dangerous-goods handling, preparation, packaging, administration and other handling/service fees unchanged unless the operator explicitly includes them in the discount;
- do not add a standalone `discount`, `pilot discount`, `rebate` or other negative-value line item;
- recalculate the `Total order value` from the resulting product, transport and handling lines.

## 3. Additional discount on already-discounted product prices

If the quotation already contains approved net product prices that reflect an earlier discount and the operator approves an additional discount:

1. Apply the additional percentage to the currently approved/net product prices, not to freight or handling lines unless explicitly instructed.
2. Round customer-facing unit prices to the quotation currency precision before calculating displayed subtotals, so visible unit price × quantity equals the displayed subtotal.
3. Update the existing `Discount` field to the operator-approved cumulative displayed discount figure when instructed as an additional discount to the previous displayed discount.
4. Do not create a separate discount item to reconcile the difference.

If there is any ambiguity between a cumulative displayed discount and an effective mathematical discount, preserve the operator's explicit wording and seek clarification before external issue.

## 4. Validation gate

Before exporting a discounted quotation, verify all of the following:

- the `Discount` field contains the approved discount display;
- affected product prices have been reduced correctly;
- affected product subtotals equal displayed unit price × quantity;
- freight/transport costs are not discounted unless explicitly approved;
- DG handling/preparation costs are not discounted unless explicitly approved;
- handling/administration/packaging fees are not discounted unless explicitly approved;
- there is no standalone discount line item unless explicitly required;
- total order value equals the sum of all displayed subtotals;
- quotation notes, if used, describe the discount treatment consistently with the item table and do not introduce a second discount mechanism.

## 5. Relationship to existing quotation workflow

This file supplements `docs/approved/EA_QUOTATION_GENERATION_WORKFLOW_1111_05082026.md` and is controlling for discount placement and product-only discount calculations. Current explicit operator instruction remains the highest authority.
