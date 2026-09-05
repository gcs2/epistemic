# Decision rules under shared misspecification and hidden tails

## Scope

Experiment 003A contains 96,000 synthetic cases across 96 registered cells. It tests decision-rule mechanics under known generating truth; it is not real-world validation.

## Aggregate performance

| Method | True value | Mean regret | P90 regret | Harmful choice | Catastrophe exposure | Affected harm | Baseline selected |
|---|---:|---:|---:|---:|---:|---:|---:|
| oracle_expected | 15.617 | 0.000 | 0.000 | 0.00% | 2.71% | 0.00% | 0.02% |
| baseline | 0.000 | 15.617 | 23.841 | 0.00% | 0.00% | 0.00% | 100.00% |
| declared_raw | 14.800 | 0.817 | 3.056 | 0.33% | 2.58% | 0.00% | 2.77% |
| confidence_shrink | 14.948 | 0.668 | 2.340 | 0.69% | 2.81% | 0.00% | 1.78% |
| minimax_regret | 14.800 | 0.817 | 3.071 | 0.34% | 2.58% | 0.00% | 2.64% |
| robustness_gate | 13.241 | 2.376 | 9.094 | 0.32% | 2.39% | 0.00% | 19.34% |

## Registered hypotheses

- **H1: supported.**
- **H2: supported.**
- **H3: supported.**
- **H4: supported.**
- **H5: not supported.**
- **H6: not supported.**
- **H7: not supported.**

## Central stress findings

- Robustness-gate certified-non-oracle rate with the tail included: 7.01%; with the tail omitted: 8.29%.
- Confidence-shrink minus declared-raw catastrophe exposure when negative confidence is 0.4: 0.0069.
- With tails included, the robustness gate reduced catastrophe exposure by 0.0076, but increased mean regret by 1.879; the allowed regret increase was 1.331, so H5 failed.
- Minimax-regret P90 regret was 3.649 versus 3.643 for declared raw; H6 failed.
- The affected-party harm threshold never activated for any method. H7 therefore failed uninformatively and cannot support a distributional conclusion.
- See `summary.json` and `cells.csv` for all registered contrasts; no cell was selected for favorability.

## Interpretation boundary

The oracle is unavailable in practice. A rule can appear stable because every declared view shares the same missing state, impact error, or value omission. Robustness to declared perturbations is conditional robustness—not protection against the unknown model space.
