# SES Action Protocol 0.2: Bounded Decision Assurance

## Status and purpose

Action Protocol 0.2 is an executable research prototype. It replaces Action Protocol 0.1's signed confidence multiplication with typed uncertainty and a bounded assurance case. It has unit and invariance tests but has not passed Experiment 003B, independent replication, or a field trial.

Its output answers:

> Given these declared scenarios, probability views, value ranges, consequence bounds, dependence groups, constraints, challenges, and unresolved deficits, which option—if any—meets the stated status rule?

It does not answer:

> Which option is universally best, safe, legitimate, or authorized?

## Why 0.2 is a new protocol

Action 0.1 attached a confidence value to every signed impact and multiplied the two. Experiment 003A showed that low confidence in a negative impact moves the harm toward zero and can increase tail exposure. Changing a threshold cannot repair that semantic error, so 0.2 receives a new schema and engine. Action 0.1 remains available only for reproduction and comparison.

## Typed ledgers

### Decision contract

Defines the owner, question, evidence cutoff, horizon, and named baseline. Ownership is accountability metadata, not permission for the program to act.

### State and model ledger

`scenarios` defines the represented state space. Each `worldview` declares a central scenario-probability vector and an optional concentration controlling perturbation around that vector. A worldview has a weight range rather than one privileged fixed weight.

Scenario probabilities sum to one *inside the declared scenario space*. This does not imply that the space is complete.

### Value ledger

Criteria and stakeholders use `{low, central, high}` weight ranges. Every simulation draws and normalizes these weights. The current engine is still additive and therefore does not solve preference interactions or interpersonal comparison. Non-compensable protections belong in `constraints`, not merely in large weights.

### Consequence ledger

Every option × scenario × stakeholder × criterion cell declares:

- a bounded triangular estimate `{low, central, high}` on the -100 to 100 illustrative scale;
- an `uncertainty_group`; and
- one or more `evidence_ids`.

Cells in the same uncertainty group share a sampled quantile, preserving a simple declared positive dependence rather than treating all cells as independent. This is a transparent first model, not a general copula or causal dependence engine.

Evidence quality does not alter these numbers. If weaker evidence justifies wider bounds, the analyst must state and defend those wider bounds explicitly.

### Evidence ledger

Evidence records source, independence group, qualitative quality, and status. The arithmetic never multiplies consequences by these labels. Weak or contested evidence produces warnings for the leading option; refuted evidence produces a blocker.

### Structural challenge ledger

Challenges have a type, method, and status:

- `tested`: the declared challenge was executed;
- `bounded`: its scope was explicitly examined but not fully testable; or
- `open`: it remains unresolved.

The assurance policy lists required challenge types. Missing required types block a favorable bounded status. Challenge presence is not proof of completeness or quality.

### Assurance-deficit ledger

Deficits identify missing evidence, coverage, inference, implementation, value, or external-validity problems. They have severity and status. The packet explicitly chooses which open severities block status. An accepted deficit stays visible; acceptance is a human governance judgment, not evidence that the deficit disappeared.

### Constraint ledger

Version 0.2 initially implements a minimum stakeholder-score constraint with an allowed violation probability. It is deliberately separate from aggregate welfare so benefits to one group cannot automatically erase a protected group's shortfall.

### Learning ledger

Records measurement, review date, success rule, monitoring triggers, stop rules, appeal, and affected-party review. Version 0.2 renders these commitments but does not yet optimize the expected value of information or simulate trigger dynamics.

## Computation

For each deterministic Monte Carlo draw, the engine:

1. samples worldview, stakeholder, and criterion weights from declared triangular ranges;
2. samples each worldview's probability vector when a concentration is provided;
3. samples consequence cells using one shared quantile per uncertainty group;
4. computes per-worldview, aggregate, and unweighted stakeholder-specific option scores;
5. records the first-ranked option, regret, and constraint violations; and
6. aggregates the declared sensitivity distribution.

For each option it reports:

- central and mean score;
- 5th, 50th, and 95th percentiles;
- lower-tail mean at the declared alpha;
- first-rank acceptability;
- mean regret;
- mean result for each stakeholder;
- worst stakeholder mean;
- constraint-violation probabilities; and
- probability of exceeding the baseline.

These are induced sensitivity distributions, not frequentist confidence intervals and not guarantees outside the packet.

## Bounded statuses

Statuses are rule-based descriptions:

- `blocked`: a required challenge is missing, a configured open deficit blocks, candidate evidence is refuted, a constraint exceeds its allowed violation probability, or the candidate is high-risk/irreversible;
- `pilot-eligible`: no blocker exists, the candidate exceeds the first-rank threshold, and its 5th percentile exceeds the baseline's 5th percentile;
- `conditionally-preferred`: no blocker exists and first-rank acceptability meets the threshold, but the stricter pilot comparison does not;
- `exploratory`: the declared ranking is too unstable for either label.

No status authorizes action or scaling. Domain governance can impose stricter rules.

## Known limitations

1. Triangular ranges can create false precision and require defensible elicitation.
2. Shared quantiles model only a simple positive dependence structure.
3. Additive criteria can double-count outcomes or violate preference independence.
4. The scenario set can omit important mechanisms, groups, and states.
5. Challenge records can become performative checkboxes.
6. The current constraint family is narrow.
7. Learning commitments are rendered but not optimized.
8. Human interpretation may produce automation bias.
9. Favorable status rules have not been calibrated against real consequences.

These limitations are targets for Experiment 003B, not footnotes to be ignored.

## Machine contract and implementation

- Schema: [`../schema/decision-assurance-0.2.schema.json`](../schema/decision-assurance-0.2.schema.json)
- Engine: [`../syntruth/decision_v2.py`](../syntruth/decision_v2.py)
- Example: [`../examples/library-outreach-bda.json`](../examples/library-outreach-bda.json)
- Generated brief: [`../examples/library-outreach-bda-report.md`](../examples/library-outreach-bda-report.md)
- Behavioral tests: [`../tests/test_decision_v2.py`](../tests/test_decision_v2.py)
- Design rationale: [`decisions/0002-bounded-decision-assurance.md`](decisions/0002-bounded-decision-assurance.md)
- Comparative experiment: [`../experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md`](../experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md)

## Migration from 0.1

There is no automatic confidence-to-range conversion because such a conversion would encode an unsupported calibration rule. Migrate by re-eliciting or re-estimating each consequence bound, creating explicit evidence records, assigning uncertainty groups, declaring required challenges and deficits, and specifying constraints. Preserve the original 0.1 packet for comparison.
