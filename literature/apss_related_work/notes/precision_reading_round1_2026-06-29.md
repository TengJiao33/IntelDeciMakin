# APSS related work precision reading - round 1

Date: 2026-06-29

Purpose: precision-read the papers most likely to collide with APSS. The goal is not to summarize politely, but to decide what we can no longer claim, what remains open, and which baselines become mandatory.

## Bottom line

The broad statement "traditional MCDA methods do not learn and only use preset formulas" is too weak and partly false. The stronger and more defensible statement is:

> Existing preference-learning / preference-disaggregation work often learns parameters, criteria, preference directions, or interactions from assignment/preference examples, but usually within a pre-specified interpretable model family. The remaining APSS space is adaptive selection and governance among competing preference-structure hypotheses, with explicit control of false complexity.

This changes our innovation target. We should not sell APSS as "first to learn interactions" or "first to select criteria." Those are already covered. We need to sell it as "learning one layer up": deciding which preference structure is warranted by data, not only estimating a fixed structure.

## Paper 1: IJCAI2023SparseInteractions

Source: https://www.ijcai.org/proceedings/2023/0421.pdf

Local PDF: `literature/apss_related_work/papers/2023_IJCAI_Learning_preference_models_with_sparse_interactions_of_criteria.pdf`

Extracted text: `literature/apss_related_work/extracted_text/2023_IJCAI_Learning_preference_models_with_sparse_interactions_of_criteria.txt`

### What problem does it solve?

It targets multicriteria aggregation where criteria may interact. The authors explicitly argue that interactions create a combinatorial learning problem: possible interaction subsets grow exponentially with the number of criteria. This directly overlaps with our "interaction discovery" language.

Evidence anchors:

- Abstract: lines 10-33 say the paper learns decision models whose interaction pattern is revealed from preference data.
- Lines 74-78 quantify the combinatorial explosion: for 10 criteria there are over 1000 possible interactions, for 20 criteria over one million.
- Lines 101-108 state that no prior restriction is made on possible interaction groups and useful groups emerge from preference data.

### How does it work?

The model family is capacity-based aggregation: multilinear utility and Choquet integral variants. Interactions are encoded by Mobius masses. The method uses iterative reweighted least squares for sparse recovery, plus dualization for scalability.

Key design:

- Input: preference / indifference examples over alternatives, not ordinary class labels.
- Learned object: sparse interaction coefficients in a fixed capacity-based aggregation family.
- Complexity control: sparsity penalty over interaction terms.
- Monotonicity: can be enforced, but with additional constraints and constraint generation.

### What evidence does it provide?

The experiments are synthetic but strong for their intended claim.

- Lines 764-780: synthetic preference data generated from sparse Mobius vectors; 500 training examples and 1000 test examples; noise added; Gurobi used.
- Lines 801-804: D-IRLS can learn more than 4 million coefficients at n = 22 in under 450 seconds, with generalization comparable to exact solving.
- Lines 826-839: sparse large-interaction models outperform 2-additive and 3-additive restrictions in test error under their setting.
- Lines 882-901: conclusion says future work includes learning the interaction functions themselves, which they call a model selection problem.

### Collision with APSS

Very high.

We cannot claim:

- "No one learns interactions from data."
- "No one lets interaction structures emerge."
- "Existing methods must predefine pairwise interaction only."

What remains:

- Their model family is still fixed: capacity-based aggregation with chosen interaction-function forms.
- They work mainly on preference-example aggregation, not general sorting/ranking-to-sorting benchmarks.
- They do not select among additive vs nonmonotone vs MRSort-like vs interaction families as competing explanations.
- Their future-work note on learning interaction functions is a warning: if we frame APSS as general model-family selection, this paper is the closest conceptual neighbor.

### Mandatory baseline / comparison implication

We need at least one sparse-interaction baseline. If reproducing D-IRLS exactly is too heavy, we need a transparent approximate baseline such as sparse polynomial / pairwise interaction logistic or sparse Choquet-like learner, and we must cite IJCAI 2023 as the stronger formal method.

## Paper 2: PDARegularization2025

Source: https://arxiv.org/pdf/2505.20111

Local PDF: `literature/apss_related_work/papers/2025_Preference_disaggregation_criteria_selection_regularization.pdf`

Extracted text: `literature/apss_related_work/extracted_text/2025_Preference_disaggregation_criteria_selection_regularization.txt`

### What problem does it solve?

It targets the fact that DMs may not actually use all criteria. It proposes embedded criteria selection in preference disaggregation: infer both the selected criteria and the additive value function from decision examples.

Evidence anchors:

- Lines 13-31: abstract defines embedded criteria selection using empirical error and generalization error.
- Lines 87-107: additive value function is adopted; simplicity is defined by deviation from linearity and number of marginal value functions.
- Lines 554-575: introduces 0-1 variables indicating whether each criterion is selected.
- Lines 732-752: defines complexity as a combination of slope variation and number of selected criteria.

### How does it work?

The model family is additive value function / UTA-like preference disaggregation. The paper rewrites the additive value function with binary criterion-selection variables and solves mixed-integer linear formulations.

Key design:

- Input: holistic decision examples / preference information from DM.
- Learned object: selected criteria plus marginal value functions.
- Complexity control: slope deviation from linearity plus number of selected marginal functions.
- Objective: trade off empirical fit and model complexity.
- Output: supporting criteria sets, streamlined supporting criteria sets, core/redundant criteria.

### What evidence does it provide?

The paper uses a green supplier selection example and formal propositions. It is more method-conceptual than broad benchmark empirical.

Important anchors:

- Lines 883-900: objective combines empirical error and generalization error; parameter C controls the trade-off.
- Lines 1121-1139: model has dual role of preference learning and criteria selection.
- Lines 1921-1959: conclusion restates that it infers criteria and value function from limited decision examples.
- Lines 1991-2000: future work says interactions and stability of supporting criteria sets remain open.

### Collision with APSS

Very high for "criteria selection" and "complexity/generalization trade-off."

We cannot claim:

- "No one treats unused criteria as a learnable issue."
- "No one combines preference disaggregation with regularization."
- "No one treats complexity as part of MCDA learning."

What remains:

- Their aggregation structure is additive and monotonic.
- Interactions are explicitly future work.
- Stability of selected supporting criteria sets is explicitly future work.
- They do not treat structure-family selection as the object; they select criteria inside a chosen additive family.

### Mandatory baseline / comparison implication

APSS must include a criteria-selection additive baseline. Otherwise reviewers can say our "adaptive criteria discovery" is just a weaker version of this paper. A practical baseline can be L1/logistic additive selection or MILP-style additive selection if feasible.

## Paper 3: MRSortNonMonotone2021

Source: https://arxiv.org/pdf/2107.09668

Local PDF: `literature/apss_related_work/papers/2021_Learning_MRSort_from_non_monotone_data.pdf`

Extracted text: `literature/apss_related_work/extracted_text/2021_Learning_MRSort_from_non_monotone_data.txt`

### What problem does it solve?

It extends inverse MRSort learning to settings where criteria are not necessarily monotone. Instead of assuming every criterion is gain/cost, it allows gain, cost, single-peaked, and single-valley criteria and learns the type from assignment examples.

Evidence anchors:

- Lines 10-16: abstract states that it learns preference directions together with MRSort parameters.
- Lines 70-72: criteria can be maximized, minimized, single-peaked, or single-valley.
- Lines 341-355: Inv-MRSort computes weights, majority level, profiles, and extends to multiple criterion types.
- Lines 359-367: the MIP computes criterion nature, weights, majority level, and frontiers.

### How does it work?

The model family is MRSort. The structure is expanded inside MRSort by allowing per-criterion type variables. It is still not selecting among arbitrary MCDA families.

Key design:

- Input: assignment examples.
- Learned object: MRSort parameters plus criterion preference type.
- Optimization: MIP maximizing restored assignment examples.
- Scope: two-category formulation emphasized; extension to more categories discussed.

### What evidence does it provide?

Synthetic:

- Lines 704-736: 200 assignment examples, n in 4 to 9, q unknown-direction criteria in 0 to 4, two categories, 10,000 test alternatives.
- Lines 720-731: metrics are CPU time, generalization restoration accuracy (CAg), and preference direction restoration rate (PDR).
- Lines 761-787: CAg is about 0.90-0.95, average 0.93; PDR falls as criteria and unknown directions increase.
- Lines 797-824: low-importance criteria are hard to type-correctly recover; more data may be needed.

Real-world:

- Lines 825-855: ASA medical dataset; glycemia is expected to be single-peaked.
- Lines 857-897: first two learning sets restore assignments very well but misidentify glycemia as cost.
- Lines 919-940: after selecting a more informative subset, glycemia is recovered as single-peaked.

### Collision with APSS

High for "discovering nonmonotonic criteria."

We cannot claim:

- "Nonmonotonicity has not been learned in MCDA sorting."
- "Criterion direction/type is always assumed manually."

What remains:

- It is MRSort-specific.
- It needs informative data; high predictive restoration can coexist with wrong structure recovery.
- It documents exactly our concern: accuracy alone may hide false preference structure.

This paper is actually useful for our story because it shows why structure recovery metrics matter. In the ASA case, the model can fit assignments while recovering the wrong criterion type until the data become informative enough.

### Mandatory baseline / comparison implication

We need a nonmonotone criterion-type baseline and a structure-recovery metric. Accuracy alone is insufficient.

## Paper 4: Sobrie2019MRSortMonotone

Source: https://olivier.sobrie.be/papers/itor_2019_sobrie_et_al.pdf

Local PDF: `literature/apss_related_work/papers/2019_Sobrie_Mousseau_Pirlot_Learning_monotone_preferences_MRSort.pdf`

Extracted text: `literature/apss_related_work/extracted_text/2019_Sobrie_Mousseau_Pirlot_Learning_monotone_preferences_MRSort.txt`

### What problem does it solve?

It learns a monotone MRSort assignment model from assignment examples at a scale larger than classical MCDA elicitation settings.

Evidence anchors:

- Lines 11-24: abstract defines learning a monotone assignment function using MRSort, comparing against Choquistic Regression and UTADIS.
- Lines 145-168: model-based preference learning uses models with assumptions about preference-relation structure.
- Lines 329-349: MRSort has fixed parameter types; exact MIP minimizes 0/1 loss but scales poorly.

### How does it work?

The model family is MRSort without veto. It learns profiles, criteria weights, and a majority threshold using a metaheuristic that alternates profile search and LP weight/threshold fitting.

Key design:

- Input: assignment examples.
- Learned object: MRSort parameters.
- Structure: fixed monotone majority-rule sorting.
- Baselines: exact MIP when feasible, UTADIS, Choquistic Regression.

### What evidence does it provide?

- Lines 865-901: uses benchmark datasets from ML repositories plus ASA; all attributes treated as monotone.
- Lines 997-1013: evaluates average test 0/1 loss and AUC over 100 random splits.
- Lines 1117-1122: Choquistic Regression clearly wins on MPG and CEV, likely because it can represent interactions.
- Lines 1273-1281: MIP scalability is a problem; metaheuristic handles larger datasets.
- Lines 1352-1404: conclusion emphasizes competitive benchmark behavior and interpretability; also names veto and NCS/capacity interactions as future extensions.

### Collision with APSS

Medium-high.

This paper is not close to APSS in adaptive structure selection, but it kills any claim that "traditional MCDA cannot learn from benchmarks." It also shows a standard experimental pattern: public benchmarks, 0/1 loss, AUC, 100 splits, fixed model comparisons.

What remains:

- MRSort structure is fixed.
- All attributes are treated as monotone.
- When Choquet-style interactions win, the paper interprets it as evidence that some datasets need interaction modeling. It does not automate the choice of when MRSort vs interaction model is warranted.

### Mandatory baseline / comparison implication

MRSort / UTADIS / Choquistic-style baselines are not optional if we write for MCDA/preference-learning reviewers.

## Paper 5: Pelissari2020ChoquetSorting

Source: https://arxiv.org/pdf/2003.12530

Local PDF: `literature/apss_related_work/papers/2020_Pelissari_Duarte_Choquet_capacity_sorting_stochastic_inverse_analysis.pdf`

Extracted text: `literature/apss_related_work/extracted_text/2020_Pelissari_Duarte_Choquet_capacity_sorting_stochastic_inverse_analysis.txt`

### What problem does it solve?

It identifies Choquet capacities for multicriteria sorting problems through stochastic inverse analysis, with uncertainty in decision matrix and limiting profiles. It focuses on sorting rather than ranking.

Evidence anchors:

- Lines 8-19: abstract defines Choquet capacity identification for multicriteria sorting and introduces scenario acceptability / central capacity.
- Lines 31-43: 2-additive capacity reduces parameters while retaining pairwise interaction modeling.
- Lines 44-59: distinguishes supervised, semi-supervised, and unsupervised capacity identification.
- Lines 64-96: contribution is SMAA-S-Choquet plus new descriptive measures for sorting.

### How does it work?

The model family is 2-additive Choquet integral sorting. It is semi-supervised: the DM still provides some indirect preference information, especially interaction signs and optionally Shapley importance relations.

Key design:

- Input: decision matrix, limiting profiles, and indirect preference constraints.
- Learned / identified object: compatible capacity space, scenario acceptability, central capacity vector.
- Structure: Choquet sorting with 2-additive capacity fixed in advance.
- Not a predictive benchmark learner in the same sense as MRSort learning.

Evidence anchors:

- Lines 154-170: decision matrix and limiting profiles must be defined; capacities are identified.
- Lines 162-197: some preference information is required; total lack of information is possible only for Shapley index, not for interaction constraints.
- Lines 346-410: synthetic robustness experiment, not a broad external benchmark.

### Collision with APSS

Medium.

It shows that interaction-aware sorting and capacity identification already exist, but it is not a direct "self-adaptive structure learner." It actually strengthens our differentiation if we say APSS decides whether an interaction-aware model is warranted, while this paper assumes Choquet sorting and identifies compatible capacities under preference constraints.

## Cross-paper synthesis

### Convergence

1. Learning from assignment/preference examples is mature in MCDA-adjacent work.
2. Fixed-family learning is the common pattern: MRSort, additive UTA/PDA, Choquet/capacity.
3. Complexity control already appears in several forms: sparsity, regularization, slope smoothness, reduced criteria, 2-additivity.
4. Accuracy/restoration is a standard metric, but several papers reveal that it is insufficient for structure truth.

### Divergence

1. MRSort papers emphasize interpretable sorting rules and assignment restoration.
2. Choquet papers emphasize interactions and capacity identification.
3. PDA regularization emphasizes criteria parsimony and marginal value simplicity.
4. IJCAI sparse interactions is closer to AI-style scalable structure learning but remains within capacity-based aggregation.

### The key unresolved gap for us

The remaining APSS question should be framed as:

> Given the same decision dataset, can the system adaptively decide which interpretable preference-structure hypothesis is necessary, while avoiding unnecessary nonmonotonicity, criteria selection, or interactions that improve fit only superficially?

That is sharper than "make MADM intelligent." It is also more testable:

- predictive performance: accuracy, macro-F1, ordinal MAE;
- structure recovery: criterion type F1, interaction F1, selected-criteria F1;
- false complexity: spurious nonmonotone criteria / spurious interactions / unnecessary criteria;
- stability: whether the learned structure persists across splits or perturbations.

## Immediate consequences for our paper idea

### Claims we should stop making

- Existing methods are only fixed formulas with no learning.
- Interaction discovery itself is novel.
- Criteria selection itself is novel.
- Nonmonotonicity discovery itself is novel.
- Regularization/complexity trade-off itself is novel.

### Claims that remain defensible

- Existing close works usually learn inside one chosen model family.
- They rarely compare competing interpretable preference-structure families under one adaptive controller.
- They often optimize fit/restoration, but structure correctness and false complexity are under-emphasized as first-class evaluation targets.
- Some papers themselves reveal the problem: high assignment restoration can coexist with wrong recovered structure.

### Stronger APSS innovation candidates after round 1

1. **Adaptive preference-structure governance**: select among additive, criteria-sparse, nonmonotone, and interaction-aware explanations rather than estimating one fixed family.
2. **False-complexity control**: treat unnecessary discovered structure as a decision-explanation error, not merely as statistical overfit.
3. **Structure-truth benchmark protocol**: evaluate predictive utility and recovered preference structure jointly across synthetic and public ordinal decision datasets.

The third one is still not enough as a standalone "method innovation," but it becomes powerful if tied to the method: APSS is designed to decide when added structure is justified.

## Baseline list implied by the literature

- Additive / UTADIS-style monotone learner.
- MRSort fixed-structure learner or a practical approximation.
- Criteria-selection additive learner.
- Nonmonotone criterion-type learner.
- Sparse interaction learner, ideally Choquet-like or sparse polynomial approximation.
- Black-box ML upper bounds such as random forest / gradient boosting, clearly labeled as predictive baselines rather than MCDA explanations.
- APSS ablations: no structure gate, always-add-interactions, top-K interactions, forward-gain interactions, and stability-controlled interactions.

## Reading queue after this round

1. Belahcene2023SortingPartI/II: map the full sorting model taxonomy and avoid missing an existing "structure selection" family.
2. Bouyssou2020ElectreTRInB: define structure assumptions formally.
3. AutoSklearn2015: boundary between APSS and generic AutoML.
4. Sobrie2012 and Mousseau2000: older parameter-learning lineage for historical positioning.
