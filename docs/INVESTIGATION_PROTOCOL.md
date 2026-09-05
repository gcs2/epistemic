# Finite investigation protocol 0.1

Status: executable public-development reference. Uses established Bayesian
experimental design; no new general discovery algorithm is claimed.

## Contract

An investigation packet supplies finite hypotheses and a prior; stakeholder
weights; terminal actions with discrete outcome distributions conditional on
each hypothesis; binary tests with likelihoods, source families, budget units and
costs; a feasible baseline; and outcome-level stakeholder constraints.

The schema is [investigation-0.1](../schema/investigation-0.1.schema.json).
The [engine](../syntruth/investigation.py) additionally validates normalized
probabilities, references, feasibility and finite numeric inputs. Up to eight
tests and eight budget units are supported; exact tree search grows rapidly.

## Semantics

Evidence updates the prior by Bayes' rule using supplied likelihoods. Tests from
distinct families are assumed independent conditional on the hypothesis.
A family can be observed once. Family labels are not automatically verified.

Terminal actions are first filtered for stakeholder constraints:
probability of falling below a named group's floor must not exceed its limit
under the current belief. Expected utility then ranks feasible alternatives.
The baseline must meet each constraint in each declared hypothesis.

Outcome risk is evaluated on the entire discrete mixture of hypotheses and
outcomes. Its lower-tail mean includes a fractional atom at the cutoff. For
.99 probability of +10 and .01 probability of -100, expectation is +8.9 and
the worst-5% outcome mean is -12. This differs from a tail over expected-score
estimates in [Action 0.2](BOUNDED_DECISION_ASSURANCE.md). Constraints and tails
are conditional on the represented model, including its weights and likelihoods.

## Policies

- stop: choose a terminal action immediately.
- fixed: investigate in listed order until the affordable menu is exhausted.
- random: use an explicitly seeded random order.
- entropy: maximize immediate expected entropy reduction per cost, stopping at
  no expected information gain.
- myopic (default): compare stopping with each single investigation's expected
  terminal utility minus its cost.
- sequential: expand the finite observation tree up to the remaining budget,
  allowing further tests or stopping after each observation.

The last two use known value-of-information principles. No inference of a
hypothesis outside the supplied set occurs. Novel causal mechanisms, ambiguous
values, estimated likelihoods, adaptive monitoring and real source acquisition
are outside this first slice. Normative disagreements are not hidden factual
states whose correct answer the system can infer.

Costs combine investigation and any analyst-specified delay costs in the same
utility units as outcomes. CPU cost is reported as planner-node counts separately.
Equal maximum budgets are not matched realized spending; reports show both.

## Running an example

From the repository root:

~~~powershell
python -m syntruth investigation-validate examples/fault-investigation.json
python -m syntruth investigate examples/fault-investigation.json
python -m syntruth investigate examples/fault-investigation.json --method sequential --observations examples/fault-observations.json --output work/investigation-replay.json
~~~

Without observations the command recommends the next test (or stopping).
With observations it replays only the tests selected by the policy. Missing
selected observations and zero-model-probability observations raise explicit
errors. Output records predictions, acquired observations, posteriors, costs,
candidate values and the stopping reason.

## Evidence status and next decision

See [development interpretation](../experiments/003b-bounded-decision-assurance/DEVELOPMENT_INTERPRETATION.md).
Keep myopic as the default. Development results do not justify promoting the more
expensive sequential method or claiming open-world discovery.

Future work should test how likelihoods are validated and how new hypotheses
enter the model. Reusing these exposed cases for independent confirmation is
invalid. Frozen source checks must be run at the recorded experimental revision;
future behavior changes require a new version and evaluation.

