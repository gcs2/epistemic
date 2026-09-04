# Deep Research Search Plan: Bounded Robustness and Recursive Improvement

Status: active  
Research question: Can SES replace scalar confidence-weighting with a bounded, falsifiable robustness-and-assurance architecture that improves decisions under consequence uncertainty, structural omission, stakeholder conflict, and distribution shift?

## Decision this research must support

Choose among:

1. **Parameter reform** — retain Action Protocol 0.1 and change weights, thresholds, or gates.
2. **Architectural reform** — retain the SES workflow but replace its action-ranking and certification layer.
3. **Full overhaul** — replace the central synthesis method because its abstractions cannot support valid claims.

The recommendation must identify what evidence would reverse it. Success is not a persuasive essay; it is a defensible method change plus a preregistrable experiment capable of showing that the change fails.

## Search ladder

Each question is searched through the following levels. Later levels deliberately seek evidence against the emerging design.

| Level | Purpose | Query pattern |
|---|---|---|
| L0 — vocabulary | Find the disciplines' own terms | `[problem description] terminology review` |
| L1 — foundations | Locate original formal models and assumptions | `[method] original paper theorem assumptions` |
| L2 — failure modes | Find counterexamples and boundary conditions | `[method] invalid counterexample failure empirical validation` |
| L3 — operationalization | Find procedures, data structures, and measurable outputs | `[method] handbook implementation algorithm case study` |
| L4 — comparison | Identify strongest simple and domain-specific baselines | `[task] benchmark comparison baseline decision support` |
| L5 — evaluation | Find validation designs and outcome measures | `[method] prospective validation calibration field experiment` |
| L6 — disconfirmation | Search the negation of the emerging conclusion | `scalar confidence valid`, `assurance cases ineffective`, `robust decision making criticism`, `scenario discovery false positive` |
| L7 — transfer | State exactly what transfers to SES and what does not | Internal claim-to-source mapping; no analogy is treated as validation |

## Research lanes and current gap matrix

| Lane | Current evidence | Gap that remains | Next search / test |
|---|---|---|---|
| Signed confidence transformation | Algebra and Experiment 003A show that multiplying a negative impact by confidence moves the harm toward zero. Decision-theory searches have not found a sound precedent for this cellwise operation. | Absence from search is not proof of novelty; determine whether an equivalent rule has a recognized interpretation. | Search multi-attribute utility, evidence discounting, Bayesian shrinkage, and imprecise utility for signed outcomes and counterexamples. |
| Consequence uncertainty | Stochastic multicriteria acceptability analysis (SMAA) represents uncertain measurements and weights as distributions; imprecise probability permits sets of models and incomplete rankings. | Mapping verbal evidence quality to a calibrated distribution may simply relocate subjectivity. | Compare explicit intervals, elicited distributions, and abstention; test misspecified and adversarial uncertainty sets. |
| Structural omission / model coverage | Robust Decision Making (RDM) searches futures for vulnerabilities; STPA systematically generates unsafe control actions and causal scenarios. | No method can certify that the challenge set contains all important states. Coverage is conditional and may be gamed. | Search scenario discovery validation, unknown unknowns, red-teaming recall, and hazard-analysis completeness claims. |
| Assurance and defeaters | Assurance-case research supports separating the primary claim from confidence in its support and recording unresolved defeaters. Quantitative confidence schemes have produced implausible results and have little empirical validation. | Assurance cases can become costly documentation rituals and still inherit subjective judgments. | Search empirical effectiveness, inter-rater reliability, defeater taxonomies, and assurance-case maintenance costs. |
| Tail harm and stakeholder protection | Robust/minimax regret methods address model uncertainty; coherent tail-risk measures address loss distributions. | Tail metrics can hide distributional harm, depend on arbitrary thresholds, and conflict with expected value. | Compare CVaR, regret, stochastic dominance, worst-group shortfall, and explicit rights/constraint approaches. |
| Adaptive action and learning | Dynamic adaptive policy pathways use signposts, triggers, and reversible sequences; value-of-information methods price learning. | Triggers may be late, noisy, strategically manipulated, or more costly than the uncertainty they resolve. | Search adaptive pathways validation, trigger design, option value, EVSI/EVPI, and delayed-harm cases. |
| Certification under shift | Conformal risk control provides finite-sample guarantees under stated assumptions; work beyond exchangeability shows how guarantees must change under shift. | SES decisions are not exchangeable prediction tasks; importing the language of guarantees could overclaim. | Use conformal methods only as a design analogy for explicit assumptions and coverage tests; seek direct decision-theoretic guarantees. |
| Recursive self-improvement | Frozen preregistrations and replication protect against some hindsight bias. | An SES that repeatedly optimizes against its own benchmark can overfit the evaluator and manufacture apparent progress. | Search adaptive data analysis, reusable holdouts, Goodhart effects, prequential evaluation, benchmark saturation, and evaluator gaming. |
| Human and institutional use | Decision aids must affect actions, appeals, accountability, and learning—not merely scores. | A technically improved ranker may add burdens, centralize value judgments, or be ignored. | Search field evaluations, decision-aid adoption, contestability, auditability, and organizational accident literature. |

## Candidate source families

Priority is given to original papers, official handbooks, standards, systematic reviews, and prospective evaluations.

- Decision under deep uncertainty: Robust Decision Making, info-gap, minimax regret, Dynamic Adaptive Policy Pathways.
- Multicriteria uncertainty: SMAA, imprecise probabilities/utilities, stochastic dominance, sensitivity analysis.
- Safety engineering: assurance cases, eliminative induction, STPA, safety cases for models and machine learning.
- Statistical validity: calibration, selective prediction, conformal risk control, distribution shift, adaptive data analysis.
- Decision learning: value of information, sequential decisions, reversible pilots, prequential evaluation.
- Institutions and ethics: worst-group outcomes, rights/constraints, contestability, audit and accountability.

## Planned query families

Queries are versioned by wave in `SEARCH_LOG.md`. Core templates include:

1. `("confidence" OR evidence quality) signed consequence utility multiplication decision analysis`
2. `stochastic multicriteria acceptability analysis uncertainty weights rank acceptability original paper`
3. `imprecise utility decision making sets of probabilities maximality E-admissibility review`
4. `robust decision making scenario discovery validation vulnerability analysis original paper`
5. `STPA unsafe control actions causal scenarios completeness empirical validation`
6. `assurance case confidence quantitative counterexample empirical effectiveness`
7. `dynamic adaptive policy pathways signposts triggers adaptation tipping points original paper`
8. `expected value of sample information decision analysis research prioritization original paper`
9. `conditional value at risk optimization original paper tail loss decision`
10. `adaptive data analysis reusable holdout benchmark overfitting original paper`
11. `Goodhart law formal taxonomy evaluator gaming measurement target`
12. `prequential evaluation online calibration decision system feedback loop`

For every positive query, run at least one adversarial variant containing terms such as `criticism`, `failure`, `counterexample`, `no improvement`, `invalid`, or `empirical evaluation`.

## Evidence handling

Every material claim in the final report will have:

- a stable claim identifier;
- source type and URL/DOI;
- direct support, indirect analogy, or inference label;
- assumptions and scope;
- contradiction or limitation;
- proposed consequence for SES.

Search-result snippets and AI summaries are discovery aids only. They are not evidence. Sources must be opened and checked directly where accessible.

## Stopping rules

Research may stop when all of the following hold:

1. Every architectural component has at least one primary source and one searched-for counterargument or limitation.
2. The strongest competing methods are specified well enough to serve as experiment baselines.
3. The proposed experiment has preregisterable outcomes, ablations, failure criteria, and no dependence on information unavailable to a real decision maker.
4. Reform versus overhaul can be decided using explicit criteria.
5. Two consecutive search waves add no new architecture component or material falsifier, only examples or restatements.

## Preliminary reform/overhaul criterion

Retain SES's elicitation, provenance, adversarial challenge, and update-loop concepts. Replace Action Protocol 0.1's scalar confidence transformation if research confirms that it lacks a valid decision-theoretic interpretation and fails the benchmark. A full overhaul is warranted only if the broader synthesis workflow cannot outperform transparent simple baselines after costs, deferrals, and stakeholder harms are counted.
