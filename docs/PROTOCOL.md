# SES Inquiry Protocol 0.1

## Purpose

The protocol is a portable representation of an inquiry. Version 0.1 supports probabilistic hypotheses, multiple model perspectives, dependence-grouped evidence, declared robustness uncertainty, and human-readable metadata.

## Required top-level fields

- `protocol_version`: currently `0.1`.
- `inquiry`: the inquiry contract.
- `hypotheses`: mutually exclusive hypotheses for the current numerical engine.
- `models`: perspectives with weights and hypothesis-specific priors.
- `evidence`: observations with reliability and conditional likelihoods.

## Inquiry contract

The `inquiry` object requires:

- `title`
- `question`
- `claim_type`
- `cutoff`
- `horizon`
- `resolution_criteria`

Optional fields include `scope`, `ethical_note`, and `limitations`.

## Hypotheses

Each hypothesis has a unique `id`, a `label`, and optional `description`. Version 0.1 assumes the hypotheses are mutually exclusive and collectively exhaustive enough for a useful comparison. Include an “other/model incomplete” hypothesis when that assumption is doubtful.

## Models

Each model contains:

- `id` and `label`;
- positive `weight`;
- `priors`, a probability for every hypothesis; and
- optional `assumptions`.

The engine normalizes model weights and priors. Models may represent disciplinary perspectives, causal theories, or independently produced forecasts.

## Evidence

Each evidence item contains:

- `id` and `description`;
- `independence_group`, identifying common data or citation ancestry;
- `reliability` in `[0,1]`;
- `likelihoods`, with `P(evidence | hypothesis)` in `(0,1)` for every hypothesis;
- optional `source`, `directness`, `available_at_cutoff`, and `distortions`.

Evidence in the same independence group is aggregated as a reliability-weighted mean log-likelihood. This intentionally prevents multiple derivatives of one source from counting as fully independent confirmations. It is a conservative heuristic, not a settled statistical model.

## Robustness

An optional `robustness` object controls deterministic Monte Carlo perturbation:

- `samples`
- `seed`
- `reliability_jitter`
- `prior_concentration`
- `model_weight_jitter`

The engine reports the 5th and 95th percentiles of ensemble posterior probabilities. These intervals measure sensitivity to declared input uncertainty, not the full uncertainty of the real world.

## Challenges and translations

`challenges`, `translations`, `constraints`, and `values` may be recorded for auditability. Version 0.1 renders challenges but does not automatically convert them into numerical penalties. This is deliberate: unvalidated natural-language objections should not silently modify probabilities.

## Output semantics

- `ensemble posterior`: weighted average of per-model posteriors.
- `disagreement`: normalized Jensen-Shannon divergence among model posteriors.
- `leverage`: maximum change in any ensemble posterior when one evidence group is omitted.
- `robust core`: the same hypothesis ranks first in every model and its 5th-percentile ensemble estimate remains above every rival’s 95th-percentile estimate.
- `contested shell`: material model disagreement, overlapping sensitivity intervals, or high-leverage assumptions.

## Non-goals of version 0.1

- automatic determination of whether a source is authentic;
- automatic causal identification;
- general handling of overlapping hypotheses;
- normative aggregation;
- autonomous web research;
- replacement of disciplinary review; or
- certification that a numerical input is well calibrated.
