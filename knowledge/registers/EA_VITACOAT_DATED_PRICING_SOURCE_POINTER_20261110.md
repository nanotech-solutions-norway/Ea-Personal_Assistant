# VitaCoat dated commercial evidence pointer — 10.11.2026

Status: **PENDING_REVIEW / INTERNAL SOURCE ROUTING ONLY**  
Scope: Ea product pricing evidence and quote preparation; no public/customer-facing price authorization.

## Restricted source of prices

- Restricted NTSN Google Sheet: `Ea Product Register — CSV import 16.10.2026`.
- Updated tabs: `Historical Quote Evidence` (new dated entries 23–34) and `Price Change Alerts` (new entries 14–16).
- Evidence dates: 28.10.2026 (historical NTSN customer quote, hard-surface/textile); 30.10.2026 (Nano4You manufacturer ready-to-use channel offer); 03.11.2026 (Richard/CitroxBio intermediary ready-to-use channel offer); 04.11.2026 (superseded preliminary trial quotation).
- Pricing values, private customer identities, and acquisition costs **must remain in the access-controlled register and underlying private correspondence**, not this public repository.

## Product boundaries and release gates

1. VitaCoat hard-surface and VitaCoat textile are distinct formulations. Do not propagate one SKU's price to another.
2. Ready-to-use litre prices cannot be converted to a 160 kg solvent-mixable concentrate drum price without supplier-certified composition, density, dilution yield, and mass/volume basis.
3. Current supplier correspondence indicates hard-surface concentrate supply may not be feasible. No general bulk concentrate list price is approved.
4. Keep manufacturer, intermediary, customer-specific quotations and proposed sample prices in separate scopes. Do not override general list price, import defaults, or historical evidence.
5. Confirm commercial route, latest supplier quotation, pack, lead time, incoterm, freight, customs/dangerous-goods status, tax treatment and customer-specific discount authority before external issue.

## Verification

- Google Sheets: 12 added historical evidence entries and 3 price-alert entries; connector readback on 10.11.2026 confirmed the target ranges.
- Operational ledger: `operations/ledgers/EA-PRICE-20261110-01.jsonl` (redacted workstream events).
- Classification: PENDING_REVIEW (not APPROVED/CANONICAL).

## Supplier update 18.11.2026 — VitaCoat Textile Coating (pending review)

- A newer supplier-specific, dated ready-to-use textile offer exists in the original restricted Gmail conversation. Supplier reports availability of a water-based, solvent-free ready-to-use 1 L bottle and a potential direct UK supply route. This does **not** establish a general retail or NTSN sell price, an industrial 360 kg quoted bulk rate, a validated concentrate option or a revised hard-surface quote.
- The 18.11.2026 **special offer price** and transaction-specific details are entered solely in the restricted `NanoTech Solutions Norway AS — Product Register — 16.11.2026` under `VitaCoat Supplier Evidence`; technical separation and linked original documents are under `VitaCoat Technical Evidence`.
- Supplier TDS (17.10.2023), MSDS (27.07.2022) and flyer supplied 18.11.2026 are preserved in NTSN Product Truth Archive: [TDS](https://drive.google.com/file/d/1IEAYIL-dCfxx1X3xeMXn_rW05ve6CDvw/view), [MSDS](https://drive.google.com/file/d/1tQnGT3w4eOCoQbPf5sDgpl2FdVMKtp_c/view), [Flyer](https://drive.google.com/file/d/1wnNdpzZpBzgUTCQBPum7IR0QgxV9KK5J/view). Existing NTSN-branded TDS/SDS remain retained.
- Status: `PENDING_REVIEW_TECHNICAL` + `PENDING_REVIEW_COMMERCIAL` + `PENDING_REVIEW_REGULATORY`. The historic MSDS contains organic-solvent/explosive-vapour wording in conflict with the 2026 solvent-free supplier message, and lacks verified current CLP/DG release. Do not use this correspondence to infer regulatory safety, import clearance, concentrate readiness, industrial master-batch suitability, density or durability.
- Product identity: VitaCoat Textile Coating and VitaCoat Hard-Surface Coating are **distinct**. The 2026 textile offer does not replace any pricing evidence for the hard-surface coating. Do not overwrite historical or base price lists.
- Private source-of-truth record: `Choose_Coating/knowledge/ntsn-product-register/products.jsonl`, ID `NTSN-VITACOAT-TEXTILE`, staged under a review PR; not an approval of external claims.
