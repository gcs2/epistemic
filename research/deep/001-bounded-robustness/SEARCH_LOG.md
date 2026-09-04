# Search Log

Research date: 2026-09-04  
Cutoff used for this research pass: 2026-09-04  
Canonical plan: [`SEARCH_PLAN.md`](SEARCH_PLAN.md)

Search-result snippets were used only to locate sources. The evidence ledger records whether a primary text, authoritative record, or secondary synthesis was inspected.

## Wave 1 — uncertainty semantics and decision alternatives

Queries:

- `decision analysis confidence weighting uncertain consequences impact score signed utility`
- `stochastic multicriteria acceptability analysis uncertain weights original paper`
- `imprecise probabilities decision making maximality E-admissibility review`
- `confidence and decision probability judgments stakes cautiousness`

Yield:

- Found no defensible precedent for multiplying each signed consequence by a scalar evidence-confidence value. This is an absence-of-evidence result, not a novelty claim.
- Found three legitimate but distinct alternatives: represent probability judgments with second-order/imprecise models; explore uncertain criterion values and weight spaces; or make incomplete/cautious choice explicit.
- Identified SMAA-2, Hill's confidence-ranking model, and Nau's indeterminate probabilities as experiment baselines or design constraints.

## Wave 2 — assurance arguments and false confidence

Queries:

- `assurance case confidence quantitative counterexample empirical validation`
- `assured safety arguments separate safety argument confidence argument`
- `eliminative induction assurance case defeaters`
- `probative blindness false assurance safety`
- `assurance case practitioners quantitative confidence methods 2025`

Yield:

- Quantitative confidence propagation has a close analogue to SES's scalar-confidence temptation. Graydon and Holloway found counterexamples and little validating evidence.
- Assured safety arguments separate the primary claim from the argument about why its evidence and inferences are adequate.
- Eliminative induction treats identified reasons for doubt—defeaters—as objects to address, rather than converting all doubt into a probability.
- Practice studies and reviews warn that assurance cases can become costly, opaque, or compliance-oriented. SES must test whether its assurance layer improves outcomes instead of assuming that documentation is beneficial.

## Wave 3 — deep uncertainty and structural omission

Queries:

- `robust decision making scenario discovery model misspecification deep uncertainty original paper`
- `scenario set adequacy robust decision making false robustness`
- `impact of scenario selection on robustness ranking`
- `STPA unsafe control actions causal scenarios completeness validation`
- `DMDU applicability practice limitations institutional organizational context`

Yield:

- RDM and related DMDU methods already reverse “predict then act”: they stress candidate strategies across futures and look for vulnerability clusters.
- Scenario selection can materially change robustness values, and sometimes rankings. A robustness statement is therefore conditional on the scenario-generation and model-boundary process.
- STPA offers a systematic generator of unsafe control actions and causal scenarios. It is useful for SES challenge generation, but it cannot prove open-world completeness.
- Reviews find that DMDU methods can underrepresent organizational, institutional, and individual decision contexts.

## Wave 4 — statistical guarantees and distribution shift

Queries:

- `conformal risk control monotone loss finite sample guarantee`
- `conformal prediction beyond exchangeability distribution drift`
- `robust decision making model misspecification axiomatic`
- `robust optimization ambiguity set misspecification out of sample guarantee`

Yield:

- Conformal risk control demonstrates the right form of scientific claim: a guarantee is tied to a specified loss, sampling scheme, and assumptions.
- Exchangeability violations and distribution drift require modified procedures; the guarantee does not float free of its data-generating conditions.
- These results are design analogies, not validation for SES. SES decisions are not conformal-prediction problems.

## Wave 5 — sequential learning and tail risk

Queries:

- `Dynamic Adaptive Policy Pathways signposts triggers adaptation tipping points original paper`
- `expected value of sample information decision analysis research prioritization`
- `Optimization of Conditional Value-at-Risk Rockafellar Uryasev 2000`
- `prospective hindsight premortem decision quality experiment`

Yield:

- Dynamic Adaptive Policy Pathways supplies an operational language for near-term action, signposts, triggers, and sequenced alternatives.
- Value-of-information methods provide a principled comparison between acting now, learning first, and the cost of a study.
- CVaR/expected shortfall is a useful tail-loss statistic, but it is not a universal moral rule and cannot replace stakeholder-level reporting.
- Premortem evidence was less directly relevant than structured hazard and defeater methods; it was not promoted into the architecture.

## Wave 6 — recursive improvement and evaluator overfitting

Queries:

- `adaptive data analysis reusable holdout original paper`
- `leaderboard overfitting reliable leaderboard original paper`
- `Goodhart law formal taxonomy evaluator gaming`
- `prequential evaluation sequential forecast calibration Dawid`
- `decision support feedback loop empirical evaluation`

Yield:

- Repeatedly changing SES after inspecting the same benchmark makes the benchmark part of development. Standard held-out performance can itself become overfit.
- A dual-loop research program is required: an open development suite and a protected confirmation suite whose cases or seeds are not disclosed to the design loop.
- Prequential evaluation supports scoring predictions and decisions in the order made, before their outcomes are observed.
- Goodhart taxonomies are useful cautionary language, but the actionable controls come from adaptive-data-analysis and benchmark-design work.

## Wave 7 — values, aggregation, and human use

Queries:

- `multi criteria decision analysis double counting criteria additive independence systematic review`
- `utility independence multiattributed consequences original paper`
- `distributional analysis public decisions stakeholder groups`
- `automation bias decision support systematic review`
- `algorithmic decision contestability affected stakeholders`

Yield:

- Additive multi-attribute scoring requires independence assumptions that should be exposed and stress-tested.
- Real applications frequently double-count related criteria; a beautifully precise score can therefore encode a malformed value model.
- Aggregate welfare, distributional effects, and non-compensable constraints should be separate outputs. Equity weights are normative choices, not facts inferred by the harness.
- Human users can abandon correct judgments for erroneous decision-support advice. SES must be evaluated as a human–system process, not solely as a ranking algorithm.

## Wave 8 — direct frontier and overlap search

Queries:

- `"false certification" decision robustness model omission`
- `"robustness certificate" decision making uncertainty scenario set`
- `"scenario set" adequacy robust decision making`
- `structured evidence failure high confidence brittleness certificate`

Yield:

- A September 2026 arXiv preprint, *Counterfactual Fragility Certificates*, is a close frontier neighbor. It records recomputable evidence-failure trajectories for tabular predictions and explicitly calls the object an audit certificate rather than a formal robustness certificate.
- It narrows SES's plausible novelty. Evidence-removal trajectories are not independently new. SES would need to contribute a decision-level, multi-stakeholder, model-coverage, action-and-learning integration and demonstrate added value against this simpler audit method.
- Because the paper is a two-day-old unreviewed preprint at this cutoff, its reported empirical results are treated as provisional.

## Saturation status

The search has reached conceptual saturation for the architecture: two consecutive waves reinforced conditionality, typed uncertainty, and validation hazards without adding a missing major layer. It has **not** reached empirical saturation. The proposed method still needs a comparative benchmark, independent replication, and a real low-risk field pilot before efficacy claims are warranted.
