# Experiment 003A Truth Gems

These are bounded outputs of a synthetic decision benchmark. They are not findings about real institutions, correct social values, or the actual frequency of catastrophic decisions.

## SES-GEM-011 — Agreement cannot expose a shared omission

Removing a positive-probability tail state from every declared worldview increased the robustness gate's certified-non-oracle rate from 7.01% to 8.29%. The views agreed partly because they shared the same model boundary.

**Boundary:** the increase is generator- and gate-specific. The experiment tested one explicit omitted state, not open-world hypothesis generation.

## SES-GEM-012 — Confidence shrinkage can launder uncertain harms

When negative impacts had confidence 0.4, multiplying them by confidence increased catastrophe exposure by 0.00689 relative to using their raw central estimates; the paired bootstrap 95% interval was 0.00666 to 0.00713. The rule simultaneously improved average regret in this generator, exposing a real multi-metric tradeoff rather than making it simply “bad.”

**Boundary:** low confidence was assigned selectively to negative impacts. Different uncertainty representations and confidence patterns can reverse the comparison.

## SES-GEM-013 — A safety gate can buy tail protection too expensively

With tails represented, the robustness gate reduced catastrophe exposure from 4.038% to 3.283% relative to confidence-shrink selection. It also increased mean regret from 0.768 to 2.648 and selected baseline in 24.19% of cases. The regret increase of 1.879 exceeded the preregistered allowance of 1.331, so the joint protection hypothesis failed.

**Boundary:** the cost of deferral depends on the baseline, perturbation set, thresholds, and utility generator.

## SES-GEM-014 — Minimax regret is only as useful as its uncertainty set

The registered minimax rule did not reduce downside: P90 regret was 3.649 versus 3.643 for declared-raw choice in included-tail error cells. Its paired mean-regret difference was also indistinguishable from zero under the registered bootstrap interval.

**Boundary:** this tests one small family of probability and stakeholder-weight views. It does not refute minimax regret under richer or better-calibrated uncertainty sets.

## SES-GEM-015 — A metric that never activates teaches nothing

The registered affected-party harm threshold was never crossed by any method. H7 was not supported, but the result does not show distributional robustness; it shows that this generator and threshold were unable to test the claim.

This is an **ignorance gem**. The next benchmark must generate stakeholder-level conflicts and use a sensitive distributional loss rather than rely on a dormant binary threshold.
