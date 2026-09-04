# Experiment 003A Preregistration

## Decision rules under shared misspecification and hidden tails

**Protocol version:** 1.0  
**Status:** confirmatory design to be hash-frozen before the first full run  
**Date:** 2026-09-04  
**Framework:** ADEMP—aims, data-generating mechanisms, estimands, methods, performance measures

## 1. Purpose and boundary

SES action protocol 0.1 can label an option a “robust candidate for a bounded pilot” when declared worldviews agree, perturbation trials favor it, and its lower sensitivity score exceeds the baseline. Experiment 003A asks whether that mechanism protects decisions when declared beliefs, impacts, and value weights are wrong in known ways.

This is a computational stress test with fully synthetic cases and exact generating truth. It is designed to reveal failure conditions. It does not test real organizations, human legitimacy, causal inference, or field outcomes.

## 2. Primary questions

1. Does a worldview-consensus and sensitivity gate reduce regret or harmful choices relative to ordinary declared expected-score selection?
2. Can common model misspecification create false robustness even when all declared worldviews agree?
3. Does multiplying uncertain impacts by confidence create an optimism bias when the uncertain impacts are negative?
4. When does minimax regret protect against downside at the cost of average value?
5. How much do probability, impact, and stakeholder-weight errors matter separately and jointly?

## 3. Confirmatory hypotheses

**H1—oracle sanity bound.** Oracle expected-value choice will have zero mean expected regret up to floating-point tolerance and no deployable method will have lower regret.

**H2—misspecification penalty.** Averaged over positive-tail cells, declared-raw mean regret will be no lower when probability, impact, or value error is activated than when the corresponding error is zero, holding the registered grid otherwise balanced. The complete contrasts will be reported even if monotonicity fails.

**H3—hidden-tail false robustness.** For positive-tail cells, omitting the tail will increase the robustness gate’s rate of certifying a non-oracle option compared with including the tail.

**H4—uncertainty laundering.** When negative-impact confidence is 0.4 and tail probability is positive, confidence-shrink selection will have greater or equal catastrophe exposure than declared-raw selection in aggregate; it will be considered meaningfully worse if the paired case-level bootstrap interval for the difference excludes zero above.

**H5—gate boundary.** With tails included, the robustness gate will reduce either mean regret or catastrophe exposure relative to confidence-shrink selection without increasing the other by more than 10% of the baseline-to-declared gap. With tails omitted, this joint protection is not expected and will be reported as a boundary, not silently pooled.

**H6—minimax tradeoff.** In included-tail cells with any estimation error, minimax regret will reduce 90th-percentile true regret relative to declared-raw selection, while it may reduce mean true value. Both quantities are co-primary for this hypothesis; downside protection alone is not called universally superior.

**H7—distributional fragility.** Activating stakeholder value shift will increase the rate at which a chosen option’s true expected value for the affected stakeholder falls below the registered harm threshold for at least one deployable scoring method.

## 4. Data-generating mechanism

### 4.1 Cases, states, people, and criteria

Each cell contains 1,000 independent decision cases. Each case has three mutually exclusive states:

- a favorable common state;
- an unfavorable common state; and
- a rare tail state.

The registered tail probability is 0, 0.02, or 0.08. Conditional on not entering the tail, the favorable-state probability is sampled uniformly from 0.35 to 0.75.

There are two stakeholder groups: an affected public with true weight 0.65 and implementing staff with true weight 0.35. There are two criteria: direct benefit with true weight 0.60 and access/burden with true weight 0.40. These weights are normative generator parameters, not claims about correct social values.

### 4.2 Options and true impacts

Every case has:

1. **baseline**, with zero impact in every cell;
2. **balanced**, with moderate common-state gains, moderate operational burdens, and a substantial but smaller tail loss; and
3. **aggressive**, with larger favorable-state gains, mixed unfavorable-state effects, and severe tail losses.

Cell impacts are independently drawn from fixed uniform ranges in the implementation and retained in code. Aggregate option value is the probability-weighted, stakeholder-weighted, criterion-weighted impact. The oracle option maximizes this true expected value. Ties use stable option order.

### 4.3 Probability misspecification

When probability error is zero, declared common-state probabilities equal truth. At error 0.15, each visible state probability is multiplied by a log-normal perturbation with log standard deviation 0.15 and renormalized.

When the tail is included, it remains in the declared state set. When omitted, it is removed and its mass is redistributed proportionally across the common states. All declared worldviews therefore share the omission. This is the direct test of false agreement under a missing hypothesis.

### 4.4 Impact misspecification

When impact error is zero, declared visible-state impacts equal the generated impacts. At error 15, independent zero-mean Gaussian noise with standard deviation 15 is added to each visible impact and clipped to [-100, 100]. Omitted-tail impacts are not represented.

### 4.5 Value misspecification

When value shift is zero, declared stakeholder and criterion weights equal generating weights. At shift 0.5, each weight is multiplied by an independent log-normal perturbation with log standard deviation 0.5 and renormalized within its ledger.

### 4.6 Confidence condition

Positive declared impacts receive confidence 1.0. Negative declared impacts receive registered confidence 1.0 or 0.4. The confidence-shrink method multiplies impact by confidence, matching action protocol 0.1. This factor is not used by declared-raw or oracle choice.

## 5. Registered factorial grid

- tail probability: 0, 0.02, 0.08;
- tail visibility: included, omitted;
- probability-error log SD: 0, 0.15;
- impact-error SD: 0, 15;
- value-shift log SD: 0, 0.5;
- negative-impact confidence: 1.0, 0.4.

The full grid contains 96 cells and 96,000 cases. At tail probability zero, included and omitted visibility are mechanically redundant but retained as implementation and symmetry controls. Every registered cell will be reported.

## 6. Methods

### M1—oracle expected value

Uses true states, probabilities, impacts, and weights. This is a reference bound, not deployable.

### M2—baseline

Always chooses the zero-impact option.

### M3—declared raw

Maximizes expected value from the declared probabilities, impacts, and weights without confidence shrinkage.

### M4—confidence shrink

Maximizes the same declared score after multiplying each impact by its confidence. This isolates the current action-protocol scoring rule.

### M5—minimax regret

Creates registered alternative views around declared state probabilities and stakeholder weights, scores options without confidence shrinkage in each view, and selects the option with the smallest maximum within-view regret. Ties favor the option with higher central declared score, then stable option order.

### M6—robustness gate

Begins with the confidence-shrink leader. It moves away from baseline only if all registered alternative views prefer the same option, that option ranks first in at least 80% of 40 seeded perturbation samples, and the fifth percentile of its sampled declared score exceeds the baseline by the registered zero-point margin. Otherwise it selects baseline. This approximates the executable action-0.1 gate while making the benchmark computationally tractable.

## 7. Outcomes

For every method and cell:

- mean true expected value;
- mean and 90th-percentile regret relative to the oracle option;
- harmful-choice rate, where selected true expected value is below baseline;
- catastrophe exposure, the true probability that the selected option’s aggregate realized state value is at most -50;
- affected-party harm rate, where the selected option’s true expected affected-public value is at most -40;
- baseline selection rate;
- for the robustness gate, certification rate, certified non-oracle rate, and certified harmful rate.

“Catastrophe” and “affected harm” are synthetic threshold labels only; they do not define acceptable real-world risk.

## 8. Analysis

Cell summaries are equally weighted. Confirmatory contrasts use paired case outcomes wherever both methods are evaluated on the same generated case. Uncertainty for aggregate paired mean contrasts is a deterministic case-level bootstrap with 5,000 resamples and seed 20260905. Quantile differences are reported directly and may receive bootstrap intervals if computationally feasible.

H2 is checked by marginal contrasts across the complete grid, separately for probability, impact, and value error. H3–H6 exclude tail-probability-zero cells where specified. H7 compares value-shift conditions across deployable methods.

No single metric establishes superiority. Expected value, regret, tail exposure, distributional harm, deferral, and false certification are retained together.

## 9. Falsifiers and interpretation

The new action gate is weakened if it frequently certifies non-oracle or harmful options, particularly when all views share an omitted tail. Confidence shrinkage must be revised if it increases catastrophe exposure by making uncertain negative impacts less negative. Minimax regret is not called better merely because it defers or sacrifices large ordinary gains.

A successful synthetic gate result would show only that the registered mechanism works under the registered generator. It would not demonstrate accurate real-world probabilities, impact scores, values, scenario completeness, or governance.

## 10. Reproducibility and deviations

- Python standard library only.
- Fixed generator, bootstrap, and sensitivity seeds.
- Configuration and preregistration hash-frozen before the full run.
- Deterministic CSV, JSON, Markdown, and SHA-256 artifacts.
- Unit tests cover configuration validation, deterministic small runs, oracle regret, omission mechanics, and confidence-shrink behavior.
- Any post-freeze correction is recorded in `DEVIATIONS.md`; registered outputs are not deleted because they are unfavorable.

This local hash freeze is an audit mechanism, not an externally timestamped registration.
