# Initial Collision Map

This file is a starting hypothesis before full PDF-level reading.

## Not New By Itself

- Learning parameters from assignment examples.
- Learning ELECTRE TRI / MR-Sort parameters.
- Allowing non-monotone criteria.
- Learning sparse interactions.
- Selecting criteria with regularization.
- Using validation to choose among predictive models.

## Potentially Defensible APSS Space

APSS may remain defensible if it is framed as:

> adaptive selection among interpretable preference-structure assumptions under a MCDA sorting/ranking-to-sorting task, jointly evaluated by downstream decision performance and structure-recovery diagnostics.

The likely novelty is not a single component. It is the system-level formulation:

1. Hidden structure choice is treated as the research problem.
2. Structure alternatives are MCDA-interpretable rather than arbitrary ML model classes.
3. Complexity is controlled explicitly because unnecessary structure is a decision-explanation error, not only a prediction overfit.
4. Synthetic structure-truth benchmarks are used to test whether discovered structure is real.

## Immediate Reading Priorities

1. `PDARegularization2025`: closest to criteria selection + regularization + generalization.
2. `IJCAI2023SparseInteractions`: closest to interaction learning.
3. `MRSortNonMonotone2021` and `Minoungou2022MRSortSinglePeaked`: closest to non-monotonicity.
4. `Sobrie2019MRSortMonotone`: fixed-structure parameter-learning baseline.
5. `Belahcene2023SortingPartI/II`: map the broader sorting method landscape.

