# Bench Data Prepared for Adaptive Preference-Structure Learning

This folder contains a first reproducible data base for the adaptive MCDA/MADM preference-structure project.

## Layout

- `data/raw/`: unchanged source files downloaded or copied from local literature assets.
- `data/processed/`: normalized CSV files with a common convention.
- `data/metadata/bench_manifest.csv`: source, size, criteria, label, and benchmark-role metadata.
- `data/metadata/bench_summary_by_group.csv`: group-level counts.
- `data/metadata/bench_quality_report.md`: row/criteria/class counts and missing-value checks.

## Processed CSV convention

- `alternative_id`: row identifier.
- `dataset_id`: processed dataset identifier.
- `g1`, `g2`, ...: numeric criteria for modeling.
- `class_index`: ordered class integer; larger means more preferred.
- `class_label`: `Cl1`, `Cl2`, ...

Some application datasets keep additional descriptive columns such as `subset`, `rank`, `wine_type`, or `original_quality`.

## Benchmark roles

1. `synthetic_structure_recovery`: generated data with known latent structures. Use this layer to test whether a method recovers monotonicity, non-monotonicity, and sparse interactions.
2. `monotone_classification`: public IJOC ordered-class benchmarks with gain-type normalized criteria. Use this layer to test whether a method avoids unnecessary complexity on monotone data.
3. `polish_research_units`: official ordered labels for Polish research units. Use as the main MCDA-like real application benchmark.
4. `qs_university_rankings`: QS ranks converted into five ordered classes. Use as an external-ranking application benchmark, not as objective ground truth.
5. `education_evaluation`: UCI student-performance datasets and higher-education performance evaluation. Use as education-oriented ordered evaluation benchmarks.
6. `health_risk_evaluation`: UCI Maternal Health Risk. Use as a risk-stratification benchmark with interpretable clinical measurements.
7. `wine_quality`: UCI wine quality ordered labels. Use as a likely non-linear/non-monotonic ordered-class benchmark.
8. `toc_uco_ordinal_classification`: original ordinal-classification datasets from TOC-UCO. Use as a broad generalization layer rather than a MCDA-specific evidence layer.

## Regeneration

First prepare raw data:

```powershell
.\scripts\download_bench_raw_data.ps1
```

Then regenerate processed data and metadata:

```powershell
& 'C:\Users\22433\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -s .\scripts\prepare_bench_data.py
```
