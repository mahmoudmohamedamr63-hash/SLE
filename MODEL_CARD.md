# Model Card — SLE (Lupus) Gene-Expression Classifier

*Following the model card format proposed by Mitchell et al., 2019
("Model Cards for Model Reporting").*

## Model Details
- **Developed by:** [your name] — portfolio/learning project.
- **Model type:** Logistic Regression (binary classifier).
- **Inputs:** 4 standardized gene-expression values — IFIT3, IFIH1, CXCL10, STAT2.
- **Output:** Predicted class (SLE / Healthy) + predicted probability.
- **Version:** 1.0 — trained on `data/clean_data.csv`.

## Intended Use
- **Intended use:** Educational / portfolio demonstration of an ML
  classification pipeline (data cleaning, leakage-free evaluation, model
  comparison, interpretability, deployment) applied to a biomedical dataset.
- **Out-of-scope use:** This model is **not validated for clinical use** and
  must not be used to diagnose, rule out, or make any treatment decision
  about SLE or any other condition, for any real patient. It has not been
  reviewed by a medical professional or validated on an independent
  clinical cohort.

## Training Data
- 210 samples (105 SLE, 105 Healthy) with 4 gene-expression features.
- Data-quality issues found and corrected: inconsistent label casing,
  a mostly-empty identifier column (see `README.md` → Data section).
- No demographic information (age, sex, ethnicity) was present in the
  source data, so the model's behavior across subpopulations is unknown.

## Evaluation
- Stratified 80/20 train/test split; scaler fit on the training fold only.
- Metrics on held-out test set: accuracy, precision, recall/sensitivity,
  specificity, F1, ROC-AUC, PR-AUC, and Brier score (calibration) — see
  `models/metrics_report.json`.
- 95% confidence intervals via bootstrap resampling (`src/04_bootstrap_ci.py`).
- 5-fold stratified cross-validation on the training fold, run inside a
  `Pipeline(scaler, model)` so the scaler is refit per fold — no leakage
  from validation folds into scaling statistics.
- Nested cross-validation (`src/05_nested_cv.py`): outer 5-fold for the
  performance estimate, inner 3-fold `GridSearchCV` for hyperparameter
  selection, so the reported score isn't inflated by tuning against the
  same folds it's evaluated on.
- Ablation study (`src/06_ablation_study.py`): all 15 non-empty subsets of
  the 4 genes were evaluated under the same protocol. Every single gene
  alone already separates the two classes perfectly in this dataset — see
  README "Results" for what that does and doesn't imply.
- Coefficient bootstrap CIs, permutation importance, and partial dependence
  plots (`src/07_interpretability.py`) — a model-agnostic cross-check that
  the logistic regression coefficients aren't an artifact of collinearity
  among the four co-regulated genes.
- **External validation:** no independent cohort is currently available.
  `src/08_external_validation.py` is ready to run against one when it
  exists (`--data path/to/cohort.csv`) without any code changes.

## Deployment / Serving Behavior
- The API (`api/main.py`) returns `model_score` (this model's own output),
  not a labeled "probability" — the field name and the response disclaimer
  are both explicit that this is not a clinical probability.
- Every prediction includes an `out_of_distribution` flag: if any input
  feature is more than 3 standard deviations from the training-set mean
  (using the fitted `StandardScaler`'s own statistics), the response flags
  it so a caller doesn't treat an extrapolated prediction as equally
  trustworthy to an in-distribution one.

## Limitations
- **The four biomarkers are perfectly separable between classes in this
  dataset** (no overlap in any single feature — see `figures/feature_boxplots.png`).
  This is not typical of real-world clinical measurements and means the
  reported 100% metrics reflect this dataset's characteristics, not a
  guarantee of performance on new, independently collected samples.
- Sample size (210) is small for a heterogeneous autoimmune disease with
  multiple known subtypes; no external validation cohort was available.
- The model was not tested for fairness/bias across demographic subgroups,
  since no such data was available.

## Ethical Considerations
- SLE disproportionately affects women and certain ethnic groups; any real
  deployment of a similar model would need subgroup-level evaluation before
  use, which this project does not perform.
- False negatives in a real diagnostic context could delay treatment; false
  positives could cause unnecessary patient anxiety and testing. Given the
  lack of clinical validation here, this model should not influence either
  outcome for a real person.

## How to Cite / Reuse
This project is for demonstration purposes. If adapting the code for a
real clinical or research use case, an independent, IRB-reviewed dataset
and clinical collaborator are required before any patient-facing use.
