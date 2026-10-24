# AI Lead & Revenue Intelligence

An end-to-end lead analytics project combining predictive conversion modeling, model interpretation, lead prioritization, and expected-commission ranking.

## What is included

- `notebooks/01_data_prep.ipynb` — dataset inspection
- `notebooks/02_data_transform.ipynb` — data preparation and 70/15/15 split
- `notebooks/03_Building_model.ipynb` — logistic regression, random forest and XGBoost comparison; isotonic calibration
- `notebooks/04_SHAP.ipynb` — interpretation of the underlying classifier (not calibrated probabilities)
- `notebooks/06_Model_Evaluation.ipynb` — held-out evaluation and prioritization analysis
- `notebooks/07_Revenue_Intelligence.ipynb` — probability-versus-illustrative-expected-commission prioritization and example scoring
- `src/lead_scoring_utils.py` — shared preprocessing and feature utilities
- `models/lead_scoring_pipeline_v2.joblib` — corrected, previously verified saved model bundle
- `images/` — SHAP illustrations
- `data/dashboard_ready/` — aggregate held-out summaries and qualification-time scenario

The historical troubleshooting notebook and superseded model bundles are intentionally omitted from this public-facing copy.

## Model evaluation and prioritization results

The verified held-out test contains **1,386** records, of which **534** converted (38.53%). Using probability thresholds Hot ≥0.70, Warm ≥0.40, and Cold <0.40:

| Tier | Leads | Historical conversions | Conversion rate |
|---|---:|---:|---:|
| Hot | 403 | 331 | 82.13% |
| Warm | 269 | 119 | 44.24% |
| Cold | 714 | 84 | 11.76% |

The top 20% of held-out leads (278) had an observed conversion rate of approximately **87.41%**, or **2.27×** the overall baseline. These results are based on held-out historical records.

For a capacity of 100 leads, ranking by expected commission instead of conversion probability produced approximately **$1.529M versus $1.011M** in summed expected commissions, based on illustrative commission inputs. The **$518.6K difference** compares modeled scenarios, not actual revenue earned.

The qualification-time scenario assumes **10 minutes per lead** rather than using measured staff time.

## Setup and reproducibility

1. Create a Python environment and run `pip install -r requirements.txt`.
2. Download the [Lead Scoring Dataset from Kaggle](https://www.kaggle.com/datasets/amritachatterjee09/lead-scoring-dataset) and place `Lead_Scoring_dataset.csv` at `data/raw/Lead_Scoring_dataset.csv`, subject to Kaggle’s applicable terms.
3. Launch Jupyter from the `notebooks/` directory, so the existing relative paths resolve as written.
4. Run notebooks `01` → `02` → `03`, then `04` and `05` as appropriate. The revenue notebook (`06`) additionally expects a locally generated `data/dashboard_ready/lead_scores_dashboard.xlsx` with its required score and illustrative commission columns; this workbook is **not distributed** here.
5. The included saved V2 model is for inspecting the previously verified result; serialized Python models should only be loaded from trusted sources and may require matching dependency versions.

**Reproducibility notes:** The original Kaggle dataset and lead-level data exports are not included in this repository. The revenue-intelligence notebook requires a locally generated workbook containing lead scores and illustrative commission values. Package versions were not pinned from the original training environment, so re-running the analysis may produce different results.

## Methodology and limitations

Commission values and qualification-time inputs are illustrative assumptions; the associated estimates are not measured revenue or time savings.

- Split: stratified 70% training, 15% validation, 15% test (random state 42).
- Model selection was based on validation ROC-AUC. Isotonic calibration used the same validation split, which is a limitation and may introduce optimistic selection/calibration bias; test evaluation was held out.
- The corrected V2 saved model was previously checked against held-out dashboard scores (within 0.0001); its reported Brier score was approximately **0.139682**.
- SHAP explanations describe the uncalibrated classifier output, **not** expected commission or the isotonic calibration mapping.
- Probability thresholds and lead ranking are demonstration choices; there is no evidence here of real-world deployment, prospective validation, profitability, or transferability to another industry.
- No historical conversion labels for a new client's data are supplied; this model should not be used as a ready-made commercial scoring system.

## Dataset source

This project uses the **Lead Scoring Dataset**, published by **Amrita Chatterjee** on Kaggle:

https://www.kaggle.com/datasets/amritachatterjee09/lead-scoring-dataset

Kaggle lists the dataset license as **Unknown**. The original CSV and row-level derivative exports are therefore not redistributed in this repository. To reproduce the analysis, obtain the dataset directly from Kaggle and place it in `data/raw/` as described above, subject to the source's applicable terms.
