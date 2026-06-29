# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v2
- Runtime Seconds: 2.13

## Configuration

- groups: `synthetic_structure_recovery`
- seeds per dataset: `20`
- ridge alpha: `1.0`
- max interactions: `4`
- interaction selection: `forward`
- interaction candidate pool: `40`
- interaction gain threshold: `0.01`
- complexity lambda: `0.05`

## Files

- `split_results.csv`: every dataset/seed/model result.
- `summary_by_dataset_model.csv`: mean/std summary.
- `apss_selection_frequencies.csv`: selected base model frequencies.
- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.

## APSS Selection Frequencies

| group | dataset_id | selected_base_model | count | frequency |
| --- | --- | --- | --- | --- |
| synthetic_structure_recovery | synthetic_mixed_structure | M3_nonmonotone_additive | 13 | 0.6500 |
| synthetic_structure_recovery | synthetic_mixed_structure | M5_full_flexible | 7 | 0.3500 |
| synthetic_structure_recovery | synthetic_monotone_additive | M1_linear_additive | 20 | 1.0000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M3_nonmonotone_additive | 20 | 1.0000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M1_linear_additive | 11 | 0.5500 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M4_sparse_interaction | 9 | 0.4500 |

## Synthetic Structure Recovery

| dataset_id | nonmonotone_precision | nonmonotone_recall | nonmonotone_f1 | interaction_precision | interaction_recall | interaction_f1 | false_complexity_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_mixed_structure | 0.7750 | 1.0000 | 0.8500 | 0.3083 | 0.3000 | 0.2983 | 0.5500 |
| synthetic_monotone_additive | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_nonmonotone_marginals | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_sparse_interactions | 1.0000 | 1.0000 | 1.0000 | 0.4500 | 0.4250 | 0.4333 | 0.0000 |

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions use either train-residual top-K selection or validation-gated forward selection, depending on configuration.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
