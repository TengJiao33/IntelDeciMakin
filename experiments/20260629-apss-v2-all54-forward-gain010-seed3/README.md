# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v1
- Runtime Seconds: 51.74

## Configuration

- groups: `synthetic_structure_recovery, monotone_classification, polish_research_units, qs_university_rankings, wine_quality, education_evaluation, health_risk_evaluation, toc_uco_ordinal_classification`
- seeds per dataset: `3`
- ridge alpha: `1.0`
- max interactions: `4`
- interaction selection: `forward`
- interaction candidate pool: `40`
- interaction gain threshold: `0.01`
- complexity lambda: `0.02`

## Files

- `split_results.csv`: every dataset/seed/model result.
- `summary_by_dataset_model.csv`: mean/std summary.
- `apss_selection_frequencies.csv`: selected base model frequencies.
- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.

## APSS Selection Frequencies

| group | dataset_id | selected_base_model | count | frequency |
| --- | --- | --- | --- | --- |
| education_evaluation | higher_education_students_performance | M4_sparse_interaction | 3 | 1.0000 |
| education_evaluation | student_performance_math_no_prior_grades | M4_sparse_interaction | 3 | 1.0000 |
| education_evaluation | student_performance_math_with_prior_grades | M4_sparse_interaction | 1 | 0.3333 |
| education_evaluation | student_performance_math_with_prior_grades | M5_full_flexible | 2 | 0.6667 |
| education_evaluation | student_performance_portuguese_no_prior_grades | M4_sparse_interaction | 2 | 0.6667 |
| education_evaluation | student_performance_portuguese_no_prior_grades | M5_full_flexible | 1 | 0.3333 |
| education_evaluation | student_performance_portuguese_with_prior_grades | M4_sparse_interaction | 2 | 0.6667 |
| education_evaluation | student_performance_portuguese_with_prior_grades | M5_full_flexible | 1 | 0.3333 |
| health_risk_evaluation | maternal_health_risk | M1_linear_additive | 1 | 0.3333 |
| health_risk_evaluation | maternal_health_risk | M3_nonmonotone_additive | 1 | 0.3333 |
| health_risk_evaluation | maternal_health_risk | M4_sparse_interaction | 1 | 0.3333 |
| monotone_classification | mcs_bcc | M4_sparse_interaction | 2 | 0.6667 |
| monotone_classification | mcs_bcc | M5_full_flexible | 1 | 0.3333 |
| monotone_classification | mcs_cev | M1_linear_additive | 2 | 0.6667 |
| monotone_classification | mcs_cev | M4_sparse_interaction | 1 | 0.3333 |
| monotone_classification | mcs_cpu | M4_sparse_interaction | 1 | 0.3333 |
| monotone_classification | mcs_cpu | M5_full_flexible | 2 | 0.6667 |
| monotone_classification | mcs_dbs | M1_linear_additive | 1 | 0.3333 |
| monotone_classification | mcs_dbs | M2_monotone_additive | 1 | 0.3333 |
| monotone_classification | mcs_dbs | M4_sparse_interaction | 1 | 0.3333 |
| monotone_classification | mcs_era | M1_linear_additive | 3 | 1.0000 |
| monotone_classification | mcs_esl | M1_linear_additive | 2 | 0.6667 |
| monotone_classification | mcs_esl | M4_sparse_interaction | 1 | 0.3333 |
| monotone_classification | mcs_lev | M1_linear_additive | 3 | 1.0000 |
| monotone_classification | mcs_mmg | M1_linear_additive | 3 | 1.0000 |
| monotone_classification | mcs_mpg | M1_linear_additive | 2 | 0.6667 |
| monotone_classification | mcs_mpg | M4_sparse_interaction | 1 | 0.3333 |
| polish_research_units | polish_research_units_all | M1_linear_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_all | M4_sparse_interaction | 2 | 0.6667 |
| polish_research_units | polish_research_units_hs | M1_linear_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_hs | M2_monotone_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_hs | M3_nonmonotone_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_njn | M1_linear_additive | 2 | 0.6667 |
| polish_research_units | polish_research_units_njn | M3_nonmonotone_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_nz | M1_linear_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_nz | M4_sparse_interaction | 1 | 0.3333 |
| polish_research_units | polish_research_units_nz | M5_full_flexible | 1 | 0.3333 |
| polish_research_units | polish_research_units_si | M3_nonmonotone_additive | 1 | 0.3333 |
| polish_research_units | polish_research_units_si | M4_sparse_interaction | 2 | 0.6667 |
| polish_research_units | polish_research_units_ta | M4_sparse_interaction | 1 | 0.3333 |
| polish_research_units | polish_research_units_ta | M5_full_flexible | 2 | 0.6667 |
| qs_university_rankings | qs_2020_top500_common6 | M1_linear_additive | 2 | 0.6667 |
| qs_university_rankings | qs_2020_top500_common6 | M5_full_flexible | 1 | 0.3333 |
| qs_university_rankings | qs_2022_top500_common6 | M1_linear_additive | 2 | 0.6667 |
| qs_university_rankings | qs_2022_top500_common6 | M5_full_flexible | 1 | 0.3333 |
| qs_university_rankings | qs_2026_top500_all10 | M2_monotone_additive | 1 | 0.3333 |
| qs_university_rankings | qs_2026_top500_all10 | M5_full_flexible | 2 | 0.6667 |
| qs_university_rankings | qs_2026_top500_common6 | M4_sparse_interaction | 2 | 0.6667 |
| qs_university_rankings | qs_2026_top500_common6 | M5_full_flexible | 1 | 0.3333 |
| synthetic_structure_recovery | synthetic_mixed_structure | M5_full_flexible | 3 | 1.0000 |
| synthetic_structure_recovery | synthetic_monotone_additive | M1_linear_additive | 3 | 1.0000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M3_nonmonotone_additive | 3 | 1.0000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M1_linear_additive | 1 | 0.3333 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M4_sparse_interaction | 1 | 0.3333 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc03_balancescale | M3_nonmonotone_additive | 3 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc03_mammoexp | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc03_mammoexp | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc03_newthyroid | M1_linear_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc03_newthyroid | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc03_tae | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc03_tae | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_car | M4_sparse_interaction | 3 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_childrenanemia | M1_linear_additive | 3 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_gymexercisetracking | M2_monotone_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc04_gymexercisetracking | M3_nonmonotone_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_heartdisease | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc04_heartdisease | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_lestsensors | M3_nonmonotone_additive | 3 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc04_levxsensors | M1_linear_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_levxsensors | M3_nonmonotone_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc04_problematicinternetusage | M3_nonmonotone_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_problematicinternetusage | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc04_support | M1_linear_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_support | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_support | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc04_swd | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc04_swd | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_eucalyptus | M2_monotone_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_eucalyptus | M3_nonmonotone_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_eucalyptus | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_lev | M1_linear_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc05_lev | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_nhanes | M2_monotone_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc05_nhanes | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_vlbw | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc05_vlbw | M5_full_flexible | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc05_winequalityred | M2_monotone_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc05_winequalityred | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc06_esl | M1_linear_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc06_esl | M3_nonmonotone_additive | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc06_esl | M4_sparse_interaction | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc08_studentperformance | M4_sparse_interaction | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc08_studentperformance | M5_full_flexible | 1 | 0.3333 |
| toc_uco_ordinal_classification | toc_uco_oc09_era | M1_linear_additive | 3 | 1.0000 |
| toc_uco_ordinal_classification | toc_uco_oc10_melbourneairbnb | M1_linear_additive | 2 | 0.6667 |
| toc_uco_ordinal_classification | toc_uco_oc10_melbourneairbnb | M4_sparse_interaction | 1 | 0.3333 |
| wine_quality | wine_quality_combined | M1_linear_additive | 1 | 0.3333 |
| wine_quality | wine_quality_combined | M4_sparse_interaction | 2 | 0.6667 |
| wine_quality | wine_quality_red | M2_monotone_additive | 3 | 1.0000 |
| wine_quality | wine_quality_white | M4_sparse_interaction | 3 | 1.0000 |

## Synthetic Structure Recovery

| dataset_id | nonmonotone_precision | nonmonotone_recall | nonmonotone_f1 | interaction_precision | interaction_recall | interaction_f1 | false_complexity_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_mixed_structure | 0.8333 | 1.0000 | 0.8889 | 1.0000 | 0.6667 | 0.7778 | 0.3333 |
| synthetic_monotone_additive | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_nonmonotone_marginals | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_sparse_interactions | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.6667 | 0.6667 | 0.0000 |

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions use either train-residual top-K selection or validation-gated forward selection, depending on configuration.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
