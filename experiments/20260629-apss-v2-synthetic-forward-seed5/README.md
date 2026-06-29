# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v1
- Runtime Seconds: 0.65

## Configuration

- groups: `synthetic_structure_recovery`
- seeds per dataset: `5`
- ridge alpha: `1.0`
- max interactions: `4`
- interaction selection: `forward`
- interaction candidate pool: `40`
- interaction gain threshold: `0.0`
- complexity lambda: `0.02`

## Files

- `split_results.csv`: every dataset/seed/model result.
- `summary_by_dataset_model.csv`: mean/std summary.
- `apss_selection_frequencies.csv`: selected base model frequencies.
- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.

## APSS Selection Frequencies

| group | dataset_id | selected_base_model | count | frequency |
| --- | --- | --- | --- | --- |
| synthetic_structure_recovery | synthetic_mixed_structure | M5_full_flexible | 5 | 1.0000 |
| synthetic_structure_recovery | synthetic_monotone_additive | M1_linear_additive | 5 | 1.0000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M3_nonmonotone_additive | 4 | 0.8000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M5_full_flexible | 1 | 0.2000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M4_sparse_interaction | 4 | 0.8000 |
| synthetic_structure_recovery | synthetic_sparse_interactions | M5_full_flexible | 1 | 0.2000 |

## Synthetic Structure Recovery

| dataset_id | nonmonotone_precision | nonmonotone_recall | nonmonotone_f1 | interaction_precision | interaction_recall | interaction_f1 | false_complexity_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_mixed_structure | 0.9000 | 1.0000 | 0.9333 | 0.5000 | 0.9000 | 0.6400 | 2.0000 |
| synthetic_monotone_additive | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_nonmonotone_marginals | 1.0000 | 1.0000 | 1.0000 | 0.8000 | 0.8000 | 0.8000 | 0.6000 |
| synthetic_sparse_interactions | 1.0000 | 1.0000 | 1.0000 | 0.5667 | 1.0000 | 0.7200 | 1.6000 |

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions use either train-residual top-K selection or validation-gated forward selection, depending on configuration.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
