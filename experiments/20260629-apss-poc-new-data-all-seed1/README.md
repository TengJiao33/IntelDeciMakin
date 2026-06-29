# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v1
- Runtime Seconds: 2.27

## Configuration

- groups: `education_evaluation, health_risk_evaluation, toc_uco_ordinal_classification`
- seeds per dataset: `1`
- ridge alpha: `1.0`
- max interactions: `2`
- complexity lambda: `0.05`

## Files

- `split_results.csv`: every dataset/seed/model result.
- `summary_by_dataset_model.csv`: mean/std summary.
- `apss_selection_frequencies.csv`: selected base model frequencies.
- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.

## APSS Selection Frequencies

| group | dataset_id | selected_base_model | count | frequency |
| --- | --- | --- | --- | --- |
| education_evaluation | higher_education_students_performance | M1_linear_additive | 1 | 1.0000 |
| education_evaluation | student_performance_math_no_prior_grades | M4_sparse_interaction | 1 | 1.0000 |
| education_evaluation | student_performance_math_with_prior_grades | M3_nonmonotone_additive | 1 | 1.0000 |
| education_evaluation | student_performance_portuguese_no_prior_grades | M1_linear_additive | 1 | 1.0000 |
| education_evaluation | student_performance_portuguese_with_prior_grades | M1_linear_additive | 1 | 1.0000 |
| health_risk_evaluation | maternal_health_risk | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc03_balancescale | M3_nonmonotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc03_mammoexp | M4_sparse_interaction | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc03_newthyroid | M2_monotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc03_tae | M3_nonmonotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_car | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_childrenanemia | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_gymexercisetracking | M2_monotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_heartdisease | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_lestsensors | M3_nonmonotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_levxsensors | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_problematicinternetusage | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_support | M4_sparse_interaction | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_swd | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc05_eucalyptus | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc05_lev | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc05_nhanes | M2_monotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc05_vlbw | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc05_winequalityred | M2_monotone_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc06_esl | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc08_studentperformance | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc09_era | M1_linear_additive | 1 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc10_melbourneairbnb | M1_linear_additive | 1 | 1.0000 |

## Synthetic Structure Recovery

_No synthetic structure diagnostics._

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions are selected from train residual correlations, capped by `max_interactions`.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
