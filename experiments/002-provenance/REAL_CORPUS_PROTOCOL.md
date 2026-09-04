# Experiment 002B Real-Corpus Protocol

## Objective

Determine whether source ancestry in real evidence ecosystems can be adjudicated and recovered with sufficient precision to improve downstream synthesis.

This protocol is a design document, not yet a frozen preregistration. Case acquisition, licensing, adjudicators, and sample size must be secured before freezing.

## 1. Case families

The first portfolio should contain four complementary provenance regimes:

1. **Systematic-review overlap:** reviews that publish their included-primary-study lists, providing an explicit study-by-review matrix.
2. **News text reuse:** original reports, wire stories, press releases, and derivative articles with timestamps and attribution.
3. **Shared administrative data:** reports and papers using the same named dataset, survey wave, registry, or trial population.
4. **Agent common ancestry:** outputs produced from controlled combinations of base model, source packet, upstream summary, and isolated or shared deliberation.

Target at least 25 source sets per regime for a 100-set pilot. A later power analysis determines the confirmatory sample.

## 2. Gold-standard construction

Each set receives independent annotation by:

- one domain specialist;
- one provenance or information-science specialist; and
- a third adjudicator for disagreements.

Annotators identify relationship types rather than forcing a single equivalence label:

- `direct_derivation`;
- `shared_primary_observation`;
- `shared_dataset`;
- `shared_intermediate_summary`;
- `shared_method_only`;
- `topical_similarity_only`;
- `contradicts`;
- `unknown`.

Only relationship types declared dependence-relevant for the downstream claim are collapsed into an effective-family label. The collapse rule is frozen per regime before method evaluation.

Adjudicators see full metadata and source content. Recovery systems receive a standardized view with fields varied by experimental arm.

## 3. Recovery arms

1. Citation/attribution graph only.
2. Exact text reuse only.
3. Semantic similarity only.
4. Metadata and temporal constraints only.
5. Unconstrained hybrid connected components.
6. Precision-first constrained hybrid with bridge-edge review.
7. Human analyst.
8. Human-agent hybrid.

The unconstrained hybrid is retained because Experiment 002A found that it can catastrophically merge components. The constrained method must produce probabilities or abstentions rather than mandatory hard clusters.

## 4. Primary endpoints

- Pairwise precision at a registered recall operating point.
- False-merger rate between independent primary observations.
- Calibration of pairwise dependence probabilities.
- Effective-source-count interval coverage.
- Downstream Brier and log-loss change relative to all-independent and conservative extremes.
- Abstention rate, analyst time, compute cost, and source-access burden.

Because Experiment 002A suggests asymmetric harm, precision and false-merger rate are co-primary; F1 is secondary.

## 5. Required controls

- Separate case-selection, adjudication, and method-development teams.
- Freeze source snapshots and hashes.
- Record licensing and quotation restrictions.
- Blind method developers to confirmatory gold labels.
- Prevent train/test contamination for learned or language-model methods.
- Include hard negatives: independent sources using identical boilerplate or reporting the same public event.
- Include hard positives: paraphrased derivatives with missing attribution.
- Preserve `unknown` rather than forcing adjudicator certainty.
- Publish inter-annotator disagreement and sensitivity to alternative dependence definitions.

## 6. Advancement rule

Proceed to general SES dependence adjustment only if at least one deployable method:

- meets the frozen precision requirement in every regime or abstains;
- improves downstream proper scoring against both naive and conservative baselines;
- produces uncertainty intervals with registered coverage; and
- generalizes to held-out source sets and time periods.

Otherwise, SES must report dependence bounds and route ambiguous bridge edges to human review.

## 7. Immediate acquisition plan

1. Select one openly accessible systematic-review-overlap corpus as the first real pilot.
2. Convert its published citation matrix into W3C-PROV-inspired entities and derivations.
3. Create a sealed train/development/confirmatory split at the review-set level.
4. Implement exact identifier, fuzzy citation, and constrained-graph baselines.
5. Measure how bibliographic ambiguity propagates into effective-source-count error.
6. Only then add natural-language semantic inference.
