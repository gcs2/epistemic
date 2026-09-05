# 003B development protocol: selecting investigations

Status: frozen development design before the first full run; NOT confirmation.
The broader DESIGN_DRAFT.md remains the unexecuted program proposal.

## Question and methods

Under the same finite menu, prior, outcome model, family restrictions and maximum
investigation budget, compare stop, fixed-order review, seeded random review,
entropy-gain-per-cost, one-step net value of information (myopic), and finite
lookahead net value of information (sequential). All share the same constrained
terminal choice. The last two are established Bayesian decision methods, not
claims of a new SES algorithm.

Fixed/random/entropy review spend their affordable budget; entropy stops if
expected information gain is numerically zero. Myopic/sequential may stop early
when their expected net improvement is nonpositive. Report actual costs and
budget use; equal maximum budget does not mean equal expenditure.

## Generator and information boundary

Three declared explanations: ordinary condition, source fault, mechanism fault.
Three binary investigations: measurement, source audit, mechanism test.
One observation per independent source family, conditional on the hypothesis.
Four terminal actions: baseline, general intervention, source repair, mechanism
repair. Public prior, costs, signal accuracy and intervention payoffs vary across
cases. Values are fixed normative inputs: public .7, staff .3.

For every generated public case run five regimes:
matched; disclosed_no_signal (all declared/actual likelihoods .5);
hidden_no_signal (actual likelihoods .5 but declared likelihoods unchanged);
reversed (actual likelihoods 1 minus declared);
omitted (fourth actual explanation absent from the public packet).
No private regime label, truth, true likelihood, or true outcome table enters a
policy function. All methods share the pre-sampled actual test outcomes per case.
This common-noise pairing improves comparison; it is not additional evidence.

Conditional outcome mixtures include uncommon severe losses. In omitted cases,
all nonbaseline actions have an unmodeled severe-loss mixture. Baseline remains
available. No algorithm gets a special omitted-state detector.

## Metrics and interpretation

Primary descriptive measure: conditional true expected utility of the terminal
action, minus observed investigation costs (including specified delay).
Secondary: expected regret relative to a clairvoyant terminal-action upper bound;
actual outcome severe-loss probability; mean outcome lower 5% tail per episode;
worst-group expected score; posterior expected utility; latent-state Brier score;
model-assessed low risk (<.05 severe-loss probability) despite actual risk >.10;
baseline rate; steps; explicit cost; planner node count.
Tail means are averaged per episode, NOT pooled population CVaR.
Regret charges investigation but gives the clairvoyant comparator free truth.
Risk is evaluated on gross terminal outcomes; utility subtracts research costs.
CPU node counts are reported separately; no invented utility conversion for compute.

Report each regime, each method, and paired sequential-minus-each-baseline net
utility differences with seeded percentile bootstrap intervals (95%, descriptive,
no multiplicity adjustment). Do not proclaim superiority by cherry-picking an arm,
regime, interval or metric. All regimes receive equal case counts.
Counterexample assertions (tail arithmetic, cost monotonicity, no-information
stopping, budgets, dependence, model/oracle separation) are implementation tests,
not empirical hypotheses.

## Expected failure and decision rule

We expect calibrated lookahead to be useful in some cases and model mismatch to
hurt. These expectations are exposed design beliefs, not confirmatory hypotheses.
If sequential does not materially improve over myopic after compute costs,
retain the simpler method as default. If source/model errors dominate gains,
prioritize likelihood validation and model expansion before more planning depth.

## Execution discipline

Freeze protocol, configuration, engine, generator and schema hashes before the
full development run. Tiny unit fixtures may precede freezing. Any correction
after full output inspection is logged in DEVIATIONS.md and gets a new freeze.
Publish per-episode results and summaries, deterministic replay comparison and
artifact manifest. No protected evaluation is created or claimed in this milestone.

