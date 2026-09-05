# SES Findings Ledger

This ledger separates findings from aspirations. “Established” always means established within the stated evidence boundary.

## Established in controlled synthetic tests

| ID | Finding | Boundary | Source |
|---|---|---|---|
| SES-GEM-001 | Count independent origins, not repetitions. | Known synthetic source families | [`experiments/001-dependence/results/TRUTH_GEMS.md`](experiments/001-dependence/results/TRUTH_GEMS.md) |
| SES-GEM-002 | Dependence correction must be conditional; deduplication can discard real independent evidence. | Known synthetic dependence settings | same |
| SES-GEM-003 | Imperfect dependence estimates can recover substantial value under a favorable error model. | Simulated noisy estimator only | same |
| SES-GEM-004 | Accuracy can hide manufactured confidence. | Binary synthetic forecasts | same |
| SES-GEM-006 | Provenance recovery is a precision–recall problem. | Generated documents and families | [`experiments/002-provenance/results/TRUTH_GEMS.md`](experiments/002-provenance/results/TRUTH_GEMS.md) |
| SES-GEM-007 | False family mergers can be more damaging than false splits. | Experiment 002A conditions | same |
| SES-GEM-008 | Unconditional edge union can amplify error through transitive closure. | Citation-plus-token clustering tested | same |
| SES-GEM-011 | Agreement cannot expose a state omitted from every declared worldview. | Experiment 003A hidden-tail generator | [`experiments/003a-decision-stress/results/TRUTH_GEMS.md`](experiments/003a-decision-stress/results/TRUTH_GEMS.md) |
| SES-GEM-012 | Signed confidence shrinkage can make uncertain harms look smaller and increase tail exposure. | Experiment 003A selective low-confidence negative impacts | same |
| SES-GEM-013 | A robustness gate can reduce tail exposure yet fail because deferral imposes excessive regret. | Experiment 003A registered joint criterion | same |
| SES-GEM-014 | Minimax regret depends on whether its uncertainty set contains consequential error. | Experiment 003A registered view set | same |

## Promising but not confirmed

| ID | Candidate finding | Needed test |
|---|---|---|
| SES-GEM-009 | Hybrid provenance recovery may help when topical collision is low and harm when it is high. | Preregistered confirmatory replication and real corpus |
| ACTION-CANDIDATE-001 | A choice that survives worldview, value-weight, and impact perturbations may be safer to pilot than an expected-score leader alone. | Comparative retrospective and prospective decision studies |
| ACTION-CANDIDATE-002 | Requiring a baseline, stop rules, appeal, and affected-party review may improve correction and legitimacy. | Human-subject usability and field evaluation |
| SES-GEM-015 | A dormant harm threshold cannot establish distributional safety. | Redesigned synthetic generator with stakeholder conflict |

## Development observations (not confirmatory findings)

The [003B interpretation](experiments/003b-bounded-decision-assurance/DEVELOPMENT_INTERPRETATION.md)
records DEV-003B-001 through DEV-003B-003: cost-aware stopping helps under correct
no-information models; extra lookahead has no established advantage over one-step
planning; misleading likelihoods and absent hypotheses overwhelm selection gains.
These observations come from exposed development generators, including a
post-inspection budget change. They are not promoted to the established ledger.

## Remaining unknowns

- Whether real source ancestry can be recovered precisely enough to improve forecasts.
- Whether SES likelihood judgments are calibrated when elicited from natural evidence.
- Whether SES beats expert panels, forecasting teams, structured single-agent work, or simpler checklists.
- Whether it discovers omitted hypotheses and causal mechanisms reliably.
- Whether its reports improve understanding, trust, correction, or real decisions for affected people.
- Whether the extra time and complexity are worth their cost.

## Interpretation rule

No philosophical rationale, code path, worked example, or attractive report counts as empirical support. Findings enter the established section only through a frozen test with auditable outputs and a clearly bounded claim.
