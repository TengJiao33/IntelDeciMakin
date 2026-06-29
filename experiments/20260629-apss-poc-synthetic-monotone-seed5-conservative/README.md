# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v1
- Runtime Seconds: 0.30

## Configuration

- groups: `synthetic_structure_recovery, monotone_classification`
- seeds per dataset: `5`
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
| monotone_classification | mcs_bcc | M1_linear_additive | 2 | 0.4000 |
| monotone_classification | mcs_bcc | M2_monotone_additive | 1 | 0.2000 |
| monotone_classification | mcs_bcc | M4_sparse_interaction | 2 | 0.4000 |
| monotone_classification | mcs_cev | M1_linear_additive | 5 | 1.0000 |
| monotone_classification | mcs_cpu | M1_linear_additive | 4 | 0.8000 |
| monotone_classification | mcs_cpu | M3_nonmonotone_additive | 1 | 0.2000 |
| monotone_classification | mcs_dbs | M1_linear_additive | 4 | 0.8000 |
| monotone_classification | mcs_dbs | M2_monotone_additive | 1 | 0.2000 |
| monotone_classification | mcs_era | M1_linear_additive | 5 | 1.0000 |
| monotone_classification | mcs_esl | M1_linear_additive | 5 | 1.0000 |
| monotone_classification | mcs_lev | M1_linear_additive | 5 | 1.0000 |
| monotone_classification | mcs_mmg | M1_linear_additive | 5 | 1.0000 |
| monotone_classification | mcs_mpg | M1_linear_additive | 5 | 1.0000 |
| synthetic_structure_recovery | synthetic_mixed_structure | M3_nonmonotone_additive | 3 | 0.6000 |
| synthetic_structure_recovery | synthetic_mixed_structure | M5_full_flexible | 2 | 0.4000 |
| synthetic_structure_recovery | synthetic_monotone_additive | M1_linear_additive | 5 | 1.0000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M3_nonmonotone_additive | 5 | 1.0000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M1_linear_additive | 3 | 0.6000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M4_sparse_interaction | 2 | 0.4000 |

## Synthetic Structure Recovery

| dataset_id | nonmonotone_precision | nonmonotone_recall | nonmonotone_f1 | interaction_precision | interaction_recall | interaction_f1 | false_complexity_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_mixed_structure | 0.9000 | 1.0000 | 0.9333 | 0.4000 | 0.4000 | 0.4000 | 0.2000 |
| synthetic_monotone_additive | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_nonmonotone_marginals | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_sparse_interactions | 1.0000 | 1.0000 | 1.0000 | 0.4000 | 0.4000 | 0.4000 | 0.0000 |

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions are selected from train residual correlations, capped by `max_interactions`.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
