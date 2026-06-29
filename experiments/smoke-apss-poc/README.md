# APSS Proof-of-Concept Run

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run
- Verification Status: ANALYZED
- Version Label: apss_poc_v1
- Runtime Seconds: 0.04

## Configuration

- groups: `synthetic_structure_recovery`
- seeds per dataset: `2`
- ridge alpha: `1.0`
- max interactions: `4`
- complexity lambda: `0.02`

## Files

- `split_results.csv`: every dataset/seed/model result.
- `summary_by_dataset_model.csv`: mean/std summary.
- `apss_selection_frequencies.csv`: selected base model frequencies.
- `synthetic_structure_recovery.csv`: structure recovery diagnostics for synthetic datasets.

## APSS Selection Frequencies

| group | dataset_id | selected_base_model | count | frequency |
| --- | --- | --- | --- | --- |
| synthetic_structure_recovery | synthetic_monotone_additive | M1_linear_additive | 2 | 1.0000 |
| synthetic_structure_recovery | synthetic_nonmonotone_marginals | M3_nonmonotone_additive | 2 | 1.0000 |

## Synthetic Structure Recovery

| dataset_id | nonmonotone_precision | nonmonotone_recall | nonmonotone_f1 | interaction_precision | interaction_recall | interaction_f1 | false_complexity_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_monotone_additive | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| synthetic_nonmonotone_marginals | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

## Notes

- This is a lightweight proof-of-concept, not the formal paper experiment.
- Models are thresholded score models implemented with `numpy/pandas` only.
- M3/M5 non-monotonicity detection is based on derivative sign changes in quadratic marginal terms.
- M4/M5 interactions are selected from train residual correlations, capped by `max_interactions`.
- APSS selection minimizes validation ordinal MAE plus a small complexity penalty.
