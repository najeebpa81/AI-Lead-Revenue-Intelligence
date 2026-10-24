# Revenue Scoring Demo — Assumptions

**Project:** AI Lead & Revenue Intelligence  
**Date:** 17 October 2026  
**Currency:** USD (intentional change from the original AED plan)

## Source and scope

- The source `test_scored.csv` has 1,386 education-lead test records: `actual`, `probability`, and `tier`.
- `lead_id` is a synthetic sequential identifier, not a real CRM ID.
- The conversion model was trained on education leads, **not Dubai/UAE real estate leads**.
- No actual commission values were available.

## Synthetic commission assumptions

The five illustrative potential commissions are **USD 3,000, 5,000, 8,000, 12,000 and 20,000**, repeated deterministically across the original row order. No random seed is required.

Original Excel formula: `=CHOOSE(MOD(ROW()-2,5)+1,3000,5000,8000,12000,20000)`.

**Sorting caution:** `ROW()` depends on the current sheet position. If formulas remain live during sorting, commission values may be reassigned. Freeze commission values before sorting, or derive values from a stable ID in a future version.

## Calculations and tie handling

- Expected commission (USD): `probability × illustrative_commission_usd`; Excel `=B2*E2`.
- Probability rank: `=RANK.EQ(B2,$B$2:$B$1387,0)`.
- Revenue rank: `=RANK.EQ(F2,$F$2:$F$1387,0)`.
- Rank difference: `probability_rank - revenue_rank`; Excel `=H2-I2`.
- `RANK.EQ` gives equal scores the same rank, and may skip subsequent rank numbers.
- Positive rank difference means a better numerical revenue rank; negative means a worse one; zero means unchanged.
- `revenue_check` is an arithmetic consistency check, not an independent validation of the model or commission assumptions.

## Observed demonstration results

- Original fields: 1,386 records; zero blanks; zero invalid probabilities; zero tier mismatches.
- Revenue ranking versus probability ranking: **592 improved, 693 dropped, 101 unchanged** (total 1,386).
- Seven leads shared probability rank 1; one lead had revenue rank 1.
- **LEAD-0670:** probability 1.00; illustrative commission USD 20,000; expected commission USD 20,000; probability rank 1; revenue rank 1. This specific record was confirmed in the exported CSV.

| Example | Probability | Illustrative commission | Expected commission | Probability rank → Revenue rank | Change |
|---|---:|---:|---:|---|---:|
| Higher-value opportunity | 31.25% | $20,000 | $6,250 | 675 → 283 | +392 |
| Lower-probability opportunity | ~14.46% | $20,000 | ~$2,891.57 | 890 → 529 | +361 |
| High-probability, low-commission lead | ~95.96% | $3,000 | ~$2,878.79 | 8 → 542 | −534 |
| Another high-probability, low-commission lead | ~92.86% | $3,000 | ~$2,785.71 | 106 → 558 | −452 |
| LEAD-0670 (reference) | 100% | $20,000 | $20,000 | 1 → 1 | 0 |

These examples demonstrate how calculated prioritization changes; they do **not** establish actual revenue uplift.

## Mandatory disclaimer

> **ILLUSTRATIVE REVENUE ESTIMATES ONLY.** Commission amounts are synthetic. No revenue model has been trained or validated. The conversion model was trained on education leads and has not been validated on Dubai/UAE real estate leads. Expected commission is not booked or guaranteed revenue.

## File handling and remaining verification

- Keep `test_scored.csv` unchanged.
- Retain the Excel workbook with formulas as the learning/audit master; use the value-only `revenue_scoring_demo.csv` for Tableau.
- **Before treating the CSV as fully validated**, check all 1,386 records for unique IDs, valid synthetic commission values, expected-commission arithmetic, and rankings recalculated from the exported values. Checking LEAD-0670 alone is insufficient.
- Remove the internal `revenue_check` column and any temporary summary columns from the final dashboard-only dataset if they are not needed.

## One-minute explanation to a sales manager

Our model estimates each lead's chance of converting. We multiply that probability by the potential commission if the lead converts, giving an expected commission. Ranking by this value can promote some lower-probability but higher-value leads, while reducing the priority of some highly likely but low-value leads. It gives the sales team a financial prioritization view alongside conversion probability. In this demo, the commission values are synthetic and the model is not validated on real-estate leads.
