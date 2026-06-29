# APSS related work reading matrix - round 1

Date: 2026-06-29

| citation_key | WHY problem | HOW method | WHAT evidence | learned object | structure scope | benchmark/data | metrics | APSS collision risk | APSS differentiation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IJCAI2023SparseInteractions | Interactions among criteria are combinatorial and make preference learning complex. | Learn sparse Mobius masses for multilinear utility / Choquet-type models using IRLS and dualization. | Synthetic preference data; scales to more than 20 criteria; D-IRLS comparable to exact solving and better than k-additive restrictions in their tests. | Interaction coefficients / sparse interaction pattern. | Expanded inside a fixed capacity-based aggregation family. | Synthetic pairwise preference/indifference examples; 500 train, 1000 test in reported setup. | Test error, training time, sparsity/coefficients. | Very high: interaction emergence from data is already done. | APSS must move to cross-family structure governance and false-complexity control, not "interaction discovery" alone. |
| PDARegularization2025 | DMs may evaluate alternatives using only a subset of criteria; all-criteria value functions may be overly complex. | Embedded criteria selection in additive PDA using 0-1 variables and regularization. | Formal model plus green supplier example; complexity combines slope deviation and number of marginal value functions. | Selected criteria and additive marginal value functions. | Fixed additive value-function family. | Limited holistic preference / decision examples; illustrative supplier selection case. | Empirical error, generalization/complexity term, supporting criteria sets. | Very high: criteria selection and complexity trade-off are already done. | APSS can combine criteria selection with structure-family choice, interaction/nonmonotonicity, and structure-truth evaluation. |
| MRSortNonMonotone2021 | MRSort learning usually assumes monotone gain/cost criteria, but real criteria may be single-peaked or single-valley. | MIP learns MRSort parameters and criterion type jointly from assignment examples. | Synthetic data with n = 4-9 and unknown criterion types; ASA medical case shows high fit can still recover wrong type unless data are informative. | MRSort weights, majority threshold, profiles, criterion type. | Expanded inside fixed MRSort family. | 200 generated assignment examples plus 10,000 test alternatives; ASA case. | CPU time, CAg, PDR. | High: nonmonotone criterion discovery already exists. | APSS can use this as evidence that structure recovery and false complexity matter beyond accuracy. |
| Sobrie2019MRSortMonotone | Need scalable learning of interpretable monotone sorting models from assignment examples. | Metaheuristic learns MRSort profiles, weights, and majority threshold; compares to MIP, UTADIS, Choquistic Regression. | ML repository datasets plus ASA; 100 random splits; competitive but dataset-dependent. | MRSort parameters. | Fixed monotone MRSort family. | Public monotone classification/sorting benchmarks; ASA. | 0/1 loss, AUC, computing time. | Medium-high: learning MCDA sorting models from benchmarks is established. | APSS should compare against fixed-family learners and decide when MRSort-like assumptions are warranted. |
| Pelissari2020ChoquetSorting | Choquet capacity elicitation is hard in sorting problems, especially with uncertainty. | SMAA-S-Choquet samples compatible 2-additive capacities and produces scenario acceptability / central capacity measures. | Numerical/synthetic example demonstrates scenario analysis and robustness of measures. | Compatible capacity space / scenario central capacities. | Fixed 2-additive Choquet sorting family with preference constraints. | Synthetic/numerical sorting examples; decision matrix and limiting profiles required. | Scenario acceptability, central capacity, sampling variability. | Medium: interaction-aware sorting and capacity identification exist. | APSS can decide whether Choquet-like interaction modeling is needed; this paper assumes it. |

## Cross-paper tension inventory

```yaml
cross_paper_tensions:
  - pair_id: CP-001
    paper_a: "IJCAI2023SparseInteractions"
    paper_b: "PDARegularization2025"
    candidate_basis: "shared construct: complexity-controlled preference learning"
    overlap_topic: "What type of complexity should be controlled?"
    a_finding: "Controls complexity through sparse interaction coefficients in capacity-based models."
    a_evidence_pointer: "precision_reading_round1 > Paper 1"
    b_finding: "Controls complexity through marginal-value smoothness and number of selected criteria."
    b_evidence_pointer: "precision_reading_round1 > Paper 2"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "precision_reading_round1 > Cross-paper synthesis"
    scholar_confirmation: "pending"
  - pair_id: CP-002
    paper_a: "MRSortNonMonotone2021"
    paper_b: "Sobrie2019MRSortMonotone"
    candidate_basis: "shared model family: MRSort"
    overlap_topic: "Whether criterion direction/type is fixed or learned."
    a_finding: "Learns criterion type among gain/cost/single-peaked/single-valley."
    a_evidence_pointer: "precision_reading_round1 > Paper 3"
    b_finding: "Treats benchmark attributes as monotone and learns MRSort parameters."
    b_evidence_pointer: "precision_reading_round1 > Paper 4"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "precision_reading_round1 > Cross-paper synthesis"
    scholar_confirmation: "pending"
  - pair_id: CP-003
    paper_a: "IJCAI2023SparseInteractions"
    paper_b: "Pelissari2020ChoquetSorting"
    candidate_basis: "shared construct: Choquet/capacity interaction modeling"
    overlap_topic: "How interaction-aware capacities are obtained."
    a_finding: "Learns sparse interaction coefficients from preference examples with no prior group restriction."
    a_evidence_pointer: "precision_reading_round1 > Paper 1"
    b_finding: "Identifies compatible 2-additive capacities from decision matrix, limiting profiles, and indirect preference constraints."
    b_evidence_pointer: "precision_reading_round1 > Paper 5"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "precision_reading_round1 > Cross-paper synthesis"
    scholar_confirmation: "pending"
```

Coverage note: 5 papers in this round; 3 candidate pairs recorded. This is a scoped advisory scan, not complete pairwise contradiction detection. The scan prioritizes papers that collide with APSS claims about interaction learning, criteria selection, nonmonotonicity, and fixed-family learning.
