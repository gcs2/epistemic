# Action Epistemology 0.1: From Claims to Consequences

> **Legacy protocol:** retained for Experiment 003A reproduction and migration comparison. Its signed confidence rule has a demonstrated hazard and must not be used for new live decisions. New work should use the still-unvalidated [`Bounded Decision Assurance 0.2`](BOUNDED_DECISION_ASSURANCE.md).

## Purpose

SES cannot help people merely by producing more elaborate beliefs. Its practical test is whether it helps people choose, learn, correct, and distribute consequences more responsibly. Action protocol 0.1 therefore joins an epistemic model to a bounded decision and an explicit learning contract.

The central loop is:

> question → evidence → alternative worldviews → possible consequences → values → reversible choice → observation → correction

This is not a machine for converting facts into morally compulsory actions. Facts, values, and decision rules remain separate and visible.

## The four ledgers

Every action packet maintains four ledgers that must not be collapsed.

1. **World ledger:** mutually distinguishable scenarios and each worldview's probabilities over them.
2. **Value ledger:** named stakeholders, criteria, and contestable weights.
3. **Consequence ledger:** conditional impact estimates with confidence and rationale.
4. **Learning ledger:** metric, measurement plan, duration, success rule, stop rules, appeal, and review date.

The output is a decision aid, never authorization. Affected people can dispute an impact, a weight, the scenario set, or the decision process without having to reject the entire analysis.

## Decision standards

The harness reports several different signals because no single scalar deserves sovereignty:

- expected score under the declared mixture of worldviews;
- each worldview's preferred option;
- maximum regret across worldviews;
- sensitivity intervals under declared perturbations;
- probability of ranking first in those perturbations;
- improvement over a named baseline; and
- safety flags for high-risk or irreversible options.

An option is called a **robust candidate for a bounded pilot** only when every worldview prefers it, it wins at least the declared fraction of sensitivity trials, and its lower sensitivity estimate exceeds the baseline's lower estimate. This label still does not justify scaling.

## Why confidence shrinks impacts toward zero

Impact scores range from -100 to 100. The program multiplies each score by its declared confidence. This makes an uncertain dramatic claim count less than an equally dramatic well-supported claim. Zero is an explicit neutral reference point, not a claim that unknown consequences are harmless. Unknown catastrophic possibilities belong in scenarios, challenges, and stop rules rather than being hidden inside a confidence number.

### Post-Experiment 003A warning

Experiment 003A showed that this rule can launder uncertainty when low confidence is attached to negative impacts: multiplying a negative number by a fraction makes the harm look smaller. In the registered positive-tail conditions, catastrophe exposure increased by 0.00689 relative to raw central estimates. Action protocol 0.1 is therefore **not suitable for live decision ranking when any negative impact has confidence below 1.0**. The reference harness now disables robust certification in that condition but retains the score for reproducibility. Action protocol 0.2 must replace signed confidence multiplication with explicit intervals or distributions and downside-aware comparison.

## Minimum ethical gate

The packet is invalid without stop rules, an appeal process, affected-party review, a baseline, and a prospective measurement plan. These are structural prompts, not proof that a process is ethical. Domain governance, consent, privacy, legal review, and independent oversight remain external requirements.

## Suitable first deployments

Begin with decisions that are low-risk, reversible, measurable within weeks or months, and genuinely uncertain: library outreach, nonprofit scheduling, voluntary workplace programs, public-information formats, or research workflow allocation. Do not begin with guilt, diagnosis, military targeting, immigration status, benefits eligibility, or other coercive rights-affecting decisions.

## The field-study test

Before the decision, record what would otherwise happen. Run the smallest useful intervention. Measure intended and adverse outcomes by stakeholder group. At the review date, compare observed results with every worldview's predictions, document implementation failures, update the consequence ledger, and publish null or negative findings. The decisive evidence for SES will be correction and decision improvement in this loop—not the elegance of the report.
