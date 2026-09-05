# Implementation audit and milestone scope

Status: development audit, 2026-09-04. Inspected Action 0.2 at commit 38f8fe4.

| Proposed capability | Implementation evidence | Disposition |
|---|---|---|
| Typed consequence uncertainty | Triangular ranges, independently of qualitative evidence labels | Retain as a sensitivity model |
| Outcome tail protection | States are averaged in _score_once before lower_tail_mean | Distinguish outcome risk from uncertainty in expected value |
| Structural investigation | Challenge status strings determine coverage | Records cannot establish execution; add observable investigation actions |
| Adaptive learning | learning_contract is returned and rendered | Add observations, updates, costs and stopping |
| Stakeholder protection | Constraint is on a worldview-averaged stakeholder score | Label expected-score semantics; new engine measures outcome-level violations |
| Comparison to baseline | Separate marginal fifth percentiles are compared | This is not a paired improvement probability |
| Alternative feasibility | Only mean-leading option gets assurance evaluation | New selector filters feasible actions before ranking |
| Dependence | Shared positive quantiles; provenance labels are metadata | Initial investigation protocol allows one observation per declared family |
| Evaluation independence | All current cases and generators exposed | Development only; independent confirmation still outstanding |
| Repository context | Handoff says no commits, and two manifested experiments | Correct stale context in this checkpoint |

## Reproducible diagnostic

For a known distribution giving +10 with probability .99 and -100 with probability
.01, expected value is +8.9. The mean of the worst 5% of outcomes is -12.
Action 0.2's lower_tail_mean is +8.9 when all declared parameters are fixed:
it measures a tail across expected-score perturbations. The name alone could
invite a wrong interpretation. This is a deterministic counterexample to that
interpretation, not a new statistical finding. Existing arithmetic stays versioned.

## Scope decision

Implement investigation-0.1 as a finite Bayesian investigation model and a narrow
003B development slice. It is not a replacement for the whole BDA architecture.
It can discriminate declared explanations through declared tests. It does not
invent new explanations, validate likelihoods, elicit values, or discover a
truly absent hypothesis. Omitted-state cases deliberately measure that failure.

Unresolved normative disagreements remain explicit values/constraints, not hidden
factual states with an algorithmically discoverable correct answer.

