# APSS Related Work Corpus

This folder stores the local reading corpus for the APSS / adaptive preference-structure learning project.

## Layout

- `papers/`: publicly accessible PDFs downloaded for close reading.
- `metadata/literature_registry.csv`: source registry, research role, and download status.
- `metadata/invalid_downloads/`: attempted downloads that returned HTML or another non-PDF payload.
- `notes/`: reading notes and comparison matrices.

## Why This Corpus Exists

The APSS idea must be compared against nearby work in preference disaggregation, MCDA sorting model learning, ELECTRE/MR-Sort parameter inference, non-monotone preference learning, sparse criteria interactions, criteria selection, and AutoML-style model selection.

The immediate purpose is not citation padding. The purpose is to determine whether APSS has a real research gap:

1. Existing work often learns parameters inside a chosen MCDA model.
2. Some work learns non-monotone preferences or sparse interactions.
3. Some work selects criteria or controls complexity.
4. APSS must therefore be positioned carefully as adaptive preference-structure learning, not merely another parameter-learning module.

## Current Corpus Status

- Valid PDFs: 11
- Invalid/non-PDF attempted downloads: 2
- Important unavailable/landing-page-only records are still listed in the registry.

## Next Reading Pass

For each paper, extract:

- WHY: what bottleneck/problem the paper identifies.
- HOW: what is learned or optimized.
- WHAT: what evidence, data, and metrics are used.
- Structure object: parameter, monotonicity, interaction, criteria subset, model family, or AutoML selection.
- Collision risk with APSS.
- How APSS can be differentiated without overclaiming novelty.

