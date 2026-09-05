# Interpretation of the first investigation development milestone

Status: descriptive development evidence; 2026-09-04.
Sources: [budget-three report](development-results/report.md),
[budget-two report](development-results-budget2/report.md),
[protocol](DEVELOPMENT_PROTOCOL.md), [extension](BUDGET2_EXTENSION.md).

## What ran

Each run uses 120 public cases under five private evaluator regimes and six
policies: 600 case-regime episodes, 3,600 policy executions per run. Both runs
reuse public case seeds. The second was designed after seeing the first; these
are two development runs, not two independent confirmations.

## Results relevant to the design decision

Under accurate models and budget two, mean net utility is 5.225 for immediate
choice, 6.119 fixed review, 6.278 random review, 7.508 entropy selection,
8.023 myopic value-of-information and 8.267 sequential lookahead.
Sequential minus myopic is +.244, descriptive paired 95% bootstrap interval
[-.469, 1.157]. Extra planning has not established an advantage over the strongest
simple comparator. It uses about 8.0 planner nodes per episode versus 1.9.

When all parties know tests are uninformative, myopic, sequential and entropy
stop without investigation. Fixed/random spend budget and lose utility.
When only the evaluator knows the tests are uninformative, myopic scores .312
and sequential .042, versus 5.225 for immediate choice. This difference between
disclosed and hidden unreliability is a central boundary.

With reversed test likelihoods, immediate choice scores 5.225 while myopic
scores -5.302 and sequential -5.365. More investigation amplifies the erroneous
observation model.

In the absent-mechanism regime every selected nonbaseline action has actual
severe-loss probability .35. Neither policy introduces the missing hypothesis.
Further investigation adds cost without reducing this harm. The generator
deliberately makes this limit severe; it does not estimate its field frequency.

## What these results do not establish

- No novel general algorithm or new scientific mechanism was discovered.
- The selector did not learn the diagnostic accuracy of its tests.
- Supplied finite alternatives are not open-world hypothesis discovery.
- The three-test fixed/random/entropy equality is order invariance after buying
  the whole menu, not evidence that selection never matters.
- Low predicted risk versus high actual conditional-state risk is an evaluator
  discrepancy statistic, not a formal calibration test. It can occur even with
  a correctly specified probabilistic model.
- Bootstrap intervals are descriptive and unadjusted across comparisons.
- The oracle gets the true state for free; regret uses it as an upper bound.
- Outcome-tail means are averaged per episode, not pooled CVaR.
- This milestone fixes outcome-risk semantics in the new protocol, but does not
  estimate epistemic distributions over those risks.
- Real investigator cost, human understanding and institutional benefit are untested.

## Retain, revise, defer

Retain explicit costs, posteriors, traces, family restrictions, outcome mixtures
and feasible-action selection. Retain myopic as the default; keep sequential as
an experimental comparator. Do not promote additional planning depth from these
results.

Revise the next research question toward validating observation models: can
independent calibration evidence detect when a proposed test is unreliable,
and can that evidence improve the choice to investigate or stop? Then investigate
actual model expansion. Both require separate designs; neither is implemented here.

Keep the broader BDA comparisons (SMAA, RDM, evidence-failure auditing, human review)
on the program roadmap. This narrow slice does not stand in for that full study.

## Bounded development observations

DEV-003B-001: In this generator, useful stopping saves investigation cost when
the supplied no-information model is correct.

DEV-003B-002: Sequential planning did not establish improvement over one-step
planning; extra compute remains unjustified by this development comparison.

DEV-003B-003: Misleading likelihoods and absent hypotheses can overwhelm gains
from investigation selection. These are designed stress boundaries, not novel
theorems or estimates of real-world prevalence.

