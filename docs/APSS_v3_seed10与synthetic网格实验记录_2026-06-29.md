# APSS v3: seed10 full-benchmark run and synthetic grid record

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: run + descriptive validation
- Origin Date: 2026-06-29
- Verification Status: ANALYZED
- Version Label: apss_v3_seed10_grid_record_v1

## Purpose

This round continues the APSS proof-of-concept experiment after publishing the project repository. The goal is not to claim a final paper result, but to check whether the adaptive preference-structure selector remains stable when:

1. the all-benchmark run is expanded from 3 seeds to 10 seeds;
2. the interaction-gain threshold is varied;
3. the complexity penalty is tested on synthetic structure-recovery data.

## Commands

Full 54-dataset run, sensitive interaction gate:

```powershell
python scripts/run_apss_poc.py --groups synthetic_structure_recovery monotone_classification polish_research_units qs_university_rankings wine_quality education_evaluation health_risk_evaluation toc_uco_ordinal_classification --seeds 10 --interaction-selection forward --interaction-candidate-pool 40 --interaction-gain-threshold 0.005 --complexity-lambda 0.02 --out-dir experiments/20260629-apss-v3-all54-forward-gain005-lam002-seed10
```

Full 54-dataset run, more conservative interaction gate:

```powershell
python scripts/run_apss_poc.py --groups synthetic_structure_recovery monotone_classification polish_research_units qs_university_rankings wine_quality education_evaluation health_risk_evaluation toc_uco_ordinal_classification --seeds 10 --interaction-selection forward --interaction-candidate-pool 40 --interaction-gain-threshold 0.01 --complexity-lambda 0.02 --out-dir experiments/20260629-apss-v3-all54-forward-gain010-lam002-seed10
```

Synthetic-only parameter grid:

```powershell
python scripts/run_apss_poc.py --groups synthetic_structure_recovery --seeds 20 --interaction-selection forward --interaction-candidate-pool 40 --interaction-gain-threshold <0.005|0.01> --complexity-lambda <0.02|0.05> --out-dir experiments/20260629-apss-v3-synthetic-grid-<config>-seed20
```

## Output Directories

- `experiments/20260629-apss-v3-all54-forward-gain005-lam002-seed10`
- `experiments/20260629-apss-v3-all54-forward-gain010-lam002-seed10`
- `experiments/20260629-apss-v3-synthetic-grid-gain005-lam002-seed20`
- `experiments/20260629-apss-v3-synthetic-grid-gain010-lam002-seed20`
- `experiments/20260629-apss-v3-synthetic-grid-gain005-lam005-seed20`
- `experiments/20260629-apss-v3-synthetic-grid-gain010-lam005-seed20`

## Full Benchmark Results

Macro mean over 54 dataset-level summaries:

| Run | APSS accuracy | APSS macro-F1 | APSS balanced acc. | APSS ordinal MAE | APSS within-one | APSS complexity | M1 ordinal MAE | Delta vs M1 MAE | Better / tie / worse vs M1 | Equals-or-better best baseline | Mean delta vs best baseline |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gain=0.005, lambda=0.02 | 0.6663 | 0.6190 | 0.6463 | 0.4630 | 0.9188 | 0.9562 | 0.5146 | -0.0517 | 36 / 5 / 13 | 10 / 54 | +0.0105 |
| gain=0.010, lambda=0.02 | 0.6651 | 0.6178 | 0.6450 | 0.4641 | 0.9189 | 0.8873 | 0.5146 | -0.0505 | 36 / 6 / 12 | 12 / 54 | +0.0101 |

Reading:

- APSS improves over the simple linear-additive M1 baseline on average, especially by ordinal MAE.
- APSS is not an oracle selector on the held-out test split. It equals or beats the best baseline only on 10-12 of 54 datasets, depending on the threshold.
- Therefore the current evidence supports a cautious claim: APSS can adapt structure and usually does not sacrifice predictive accuracy relative to a simple additive baseline. It does not yet support a broad "always best accuracy" claim.

## Selection Frequencies

Seed-level APSS selected-model proportions over the full benchmark:

| Run | M1 linear | M2 monotone | M3 nonmonotone | M4 sparse interaction | M5 full flexible |
|---|---:|---:|---:|---:|---:|
| gain=0.005, lambda=0.02 | 0.2870 | 0.0630 | 0.1000 | 0.3833 | 0.1667 |
| gain=0.010, lambda=0.02 | 0.3148 | 0.0667 | 0.1148 | 0.3500 | 0.1537 |

Reading:

- The selector does not collapse to one fixed formula. It chooses additive, nonmonotone, sparse-interaction, and flexible forms across datasets/seeds.
- Increasing the interaction-gain threshold slightly reduces complex interaction choices and increases M1 choices.

## Synthetic Structure Recovery

All-54 run, synthetic subset only:

| Run | Nonmonotone precision | Nonmonotone recall | Nonmonotone F1 | Interaction precision | Interaction recall | Interaction F1 | False complexity count |
|---|---:|---:|---:|---:|---:|---:|---:|
| gain=0.005, lambda=0.02 | 0.9625 | 1.0000 | 0.9750 | 0.9208 | 0.9375 | 0.9208 | 0.2750 |
| gain=0.010, lambda=0.02 | 0.9500 | 1.0000 | 0.9667 | 0.9458 | 0.8875 | 0.9025 | 0.1750 |

Synthetic-only 20-seed grid:

| Config | Nonmonotone F1 | Interaction precision | Interaction recall | Interaction F1 | False complexity count |
|---|---:|---:|---:|---:|---:|
| gain=0.010, lambda=0.02 | 0.9792 | 0.9292 | 0.9062 | 0.9083 | 0.1625 |
| gain=0.005, lambda=0.02 | 0.9833 | 0.8938 | 0.9312 | 0.9046 | 0.2875 |
| gain=0.005, lambda=0.05 | 0.9625 | 0.6896 | 0.6938 | 0.6879 | 0.1750 |
| gain=0.010, lambda=0.05 | 0.9625 | 0.6896 | 0.6812 | 0.6829 | 0.1375 |

Reading:

- The main positive evidence is structure recovery, not only predictive metrics.
- `lambda=0.05` is too conservative: it suppresses true interaction structure and sharply lowers interaction F1.
- `lambda=0.02` is currently the better default.
- `gain=0.005` is more sensitive, with higher recall and slightly better interaction F1 in the all-54 run, but more false complexity.
- `gain=0.010` is more conservative, with slightly lower interaction recall but fewer false-complexity selections.

## Anomalies

- No crash or missing output files.
- Python emitted pandas optional dependency warnings: installed `numexpr` and `bottleneck` versions are older than pandas' preferred versions. The experiment completed, but the environment should be cleaned before formal reproduction.

## Current Interpretation Boundary

This round strengthens three points:

1. APSS is empirically meaningful as an adaptive structure selector: the selected structure changes across datasets and seeds instead of reducing to a single fixed model.
2. Synthetic recovery provides a clearer benchmark than real decision datasets alone: nonmonotonicity and interaction can be checked against known ground truth.
3. Complexity control is a real methodological issue, not an implementation detail. Too strong a penalty erases true interactions; too weak a gate increases false complexity.

This round does not yet prove:

1. APSS is the best predictive model across all datasets.
2. APSS's real-data discovered structures are substantively correct.
3. The current M0-M5 baselines are sufficient for a paper-level benchmark.

## Next Experimental Needs

- Add a structure-acceptability summary rather than only selected-model frequency.
- Compare against stronger non-MCDA predictive baselines, at least random forest / gradient boosting / ordinal logistic where applicable.
- Move from single train/validation/test splits to repeated CV or nested CV for the final benchmark.
- Decide whether the paper's core claim is accuracy improvement, structure recovery, or adaptive decision-method selection. Current evidence favors structure recovery plus adaptive method selection, not pure accuracy dominance.
