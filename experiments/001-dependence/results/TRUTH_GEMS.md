# Experiment 001 Truth Gems

These are bounded outputs of a synthetic experiment, not universal declarations about real evidence systems. Their machine-readable records are in `truth-gems.json`.

## SES-GEM-001 — Count independent origins, not repetitions

When evidence items share a correlated origin, their effective evidential count is smaller than their nominal count. In the registered simulation, the naive penalty rose with duplication and correlation, reaching a Brier-loss difference of 0.04710 at correlation 0.95 and maximum duplication 16.

**Boundary:** real dependence groups and correlations were supplied by the generator rather than inferred.

## SES-GEM-002 — Dependence correction is conditional

Conservative deduplication protected strongly under high dependence, but harmed performance when observations were genuinely independent. Binary “duplicate/not duplicate” treatment should therefore give way to estimated dependence, intervals, or explicit sensitivity analysis.

**Boundary:** the crossover point is model- and domain-dependent.

## SES-GEM-003 — Imperfect dependence knowledge can still be useful

The registered noisy correlation estimator recovered 89.3% of the aggregate Brier improvement separating naive synthesis from the oracle. Perfect provenance may not be necessary, though real errors will be less friendly than the simulated unbiased noise.

**Boundary:** real source-mapping errors may be biased, strategic, and correlated with the claim.

## SES-GEM-004 — Accuracy hides manufactured confidence

Naive and oracle classification accuracy differed by only 0.50 percentage points, yet naive log loss was 1.60 times larger and it was confidently wrong 4.55 times as often. A truth system can appear nearly as “accurate” while being substantially worse at knowing when it might be wrong.

**Boundary:** decision-specific losses still matter; proper scoring is not the only evaluation.

## SES-GEM-005 — The real bottleneck is now empirical

Experiment 001 establishes what dependence does under a known model. It does not establish that source ancestry and effective correlation can be recovered in real scholarly, media, intelligence, or multi-agent systems. That is the central question for Experiment 002.

This is an **ignorance gem**: a precise boundary that prevents a successful simulation from being inflated into an unsupported cultural claim.
