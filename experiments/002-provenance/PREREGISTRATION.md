# Experiment 002A Preregistration

## Recovering hidden evidence families from incomplete citations and transformed text

**Protocol version:** 1.0  
**Status:** Confirmatory synthetic-pilot design; to be hash-frozen before full execution  
**Date:** 2026-08-30  
**Framework:** ADEMP

## 1. Place in the research program

Experiment 001 assumed that the ancestry of every evidence item was known. It established that correlated repetition can manufacture confidence, but it did not show that dependence can be detected.

Experiment 002A tests whether provenance-recovery methods can reconstruct hidden source families when:

- citations are incomplete;
- derivative reports transform or omit their parents' language;
- independent reports share topical vocabulary; and
- family sizes vary.

This is still a synthetic study. Unlike Experiment 001, however, the target of inference is the hidden provenance structure itself. Experiment 002B will subsequently replace generated document families with adjudicated real corpora.

## 2. Conceptual basis

The data representation follows the broad logic of the [W3C PROV model](https://www.w3.org/TR/prov-primer/): documents are entities, derivation is an activity, and sources or publishers are agents. This experiment uses only the entity and derivation subset needed for source-family recovery.

Evidence overlap is already a recognized problem in research synthesis. Overviews of systematic reviews use citation matrices and Corrected Covered Area to identify repeated primary studies; methodological guidance emphasizes that overlap must be examined rather than allowing one primary study to receive repeated weight. See [Hennessy and Johnson](https://pmc.ncbi.nlm.nih.gov/articles/PMC8555740/) and the [W3C PROV overview](https://www.w3.org/TR/prov-overview/).

## 3. Research question

> Can observable citation and text-reuse signals recover hidden evidence families accurately enough to improve a downstream probabilistic synthesis?

## 4. Confirmatory hypotheses

**H1 — exact-citation precision.** Citation-component recovery will have pairwise dependency precision of at least 0.98 across all registered cells, because observed citations are generated only within true families.

**H2 — citation missingness.** Citation-component recall will be strictly higher in aggregate at citation completeness 0.90 than at 0.50, and higher at 0.50 than at 0.

**H3 — textual transformation.** Text-similarity recall will decline monotonically in aggregate as paraphrase rate increases from 0 to 0.40 to 0.80.

**H4 — topical collision.** Text-similarity false-dependence rate will be higher in aggregate at topic contamination 0.50 than at 0.10.

**H5 — complementary signals.** Hybrid citation-plus-text recovery will have higher aggregate pairwise recall than either citation-only or text-only recovery, while retaining precision of at least 0.90.

**H6 — downstream utility.** In the recoverable stratum—citation completeness at least 0.50 and paraphrase rate at most 0.40—hybrid recovery will produce lower mean Brier loss than treating all documents as independent.

**H7 — imperfect recovery boundary.** Hybrid recovery will have worse mean Brier loss than oracle-family recovery across all nontrivial registered cells in aggregate. A result of equality would indicate either an unexpectedly sufficient observable signal or a benchmark implementation defect.

**H8 — conservative-collapse cost.** Treating all documents as one evidence family will have worse mean Brier loss than oracle recovery when at least four independent roots exist.

## 5. Data-generating mechanism

### 5.1 Cases and truth

Each case has a binary state `Y ~ Bernoulli(0.5)`. It contains `R` mutually independent root investigations. Root `r` observes:

\[
X_r = s\mu + \epsilon_r,
\]

where `s` is +1 for `Y=1` and −1 for `Y=0`, `mu=0.55`, and `epsilon` is standard normal.

Each root produces a family of one to `M` documents. Every derivative reports `X_r` plus Gaussian transcription noise with standard deviation 0.12. Derivative documents are therefore repeated views of one underlying investigation, not new investigations.

### 5.2 Observable text

Every family receives a set of lineage tokens drawn without replacement from a large vocabulary. Descendants inherit each token unless it is transformed according to the cell's paraphrase rate. Transformation replaces it with a token-specific alias, preserving semantic ancestry while defeating exact-token overlap.

All documents also contain topical tokens shared across independent roots. Topic contamination determines the fraction of the topic vocabulary included in each document, creating accidental similarity without shared ancestry.

The generated text is a bag-of-tokens test medium, not natural prose. That prevents language-model knowledge from entering the gold standard and makes the transformation process exactly auditable.

### 5.3 Observable citations

Each non-root document derives from a randomly selected earlier member of its true family. The parent link is exposed with the cell's citation-completeness probability. No false citations are generated in 002A; false or strategic citations belong to a later stress test.

### 5.4 Registered grid

- cases per cell: 160;
- independent roots: 4 and 10;
- maximum family size: 2, 5, and 10;
- citation completeness: 0, 0.50, and 0.90;
- paraphrase rate: 0, 0.40, and 0.80;
- topic contamination: 0.10 and 0.50;
- signal strength: 0.55;
- transcription-noise standard deviation: 0.12;
- lineage tokens per family: 14;
- topic vocabulary size: 24;
- exact-Jaccard threshold: 0.20;
- random seed: 20260830;
- bootstrap seed: 20260831;
- bootstrap samples: 10,000.

The grid contains 108 cells and 17,280 cases.

## 6. Recovery methods

### M1 — Oracle families

Uses true root-family labels. It is the reference bound.

### M2 — All independent

Assigns every document to a separate family. This represents source-counting without dependence recovery.

### M3 — All one family

Assigns every document to one family. This is the maximally conservative extreme.

### M4 — Citation components

Treats observed citations as undirected edges and returns connected components.

### M5 — Exact-text similarity

Connects documents when exact-token Jaccard similarity is at least 0.20, then returns connected components.

### M6 — Hybrid

Returns connected components of the union of observed citation edges and registered text-similarity edges.

The methods are intentionally simple and interpretable. More sophisticated semantic, temporal, authorship, and graph methods should be compared only after this baseline is frozen.

## 7. Estimands and performance measures

### 7.1 Provenance recovery

For all unordered document pairs:

- true dependence means identical root-family membership;
- predicted dependence means identical recovered-cluster membership.

Report:

- precision;
- recall;
- F1;
- false-independence rate: false negatives divided by true dependent pairs;
- false-dependence rate: false positives divided by true independent pairs;
- relative effective-source-count error: `abs(predicted families − true roots) / true roots`.

Pairs are accumulated within cases and metrics are computed from aggregate counts within each cell. Cell means receive equal weight in cross-cell summaries.

### 7.2 Downstream truth estimation

Within each recovered cluster, average document reports. Treat the cluster mean as one independent evidence observation and sum its Gaussian log-likelihood contribution. Compare the resulting probability with `Y` using:

- Brier loss, primary;
- log loss;
- accuracy;
- confidently-wrong rate at probability at least 0.90 for the false state; and
- sharpness.

This downstream model intentionally makes oracle family averaging appropriate. It tests whether structural recovery is useful, not whether the outcome model is misspecified.

## 8. Analysis rules

- All registered cells and all six methods will be reported.
- H1–H5 use equal-cell aggregate provenance metrics and registered strata.
- H6–H8 use paired cell-level Brier differences with deterministic bootstrap intervals.
- Monotonicity allows deviations smaller than two pooled Monte Carlo standard errors; exact aggregate values will be reported regardless.
- No hypothesis is removed or rewritten after confirmatory results are visible.
- Exploratory threshold sweeps, richer similarity methods, or stress tests with false citations will be stored separately and labeled exploratory.

## 9. Advancement and falsification

Experiment 002A supports moving to real-corpus Experiment 002B if:

1. at least one deployable recovery method improves downstream Brier over all-independent synthesis in the recoverable stratum;
2. its false-dependence and false-independence tradeoff is visible rather than concealed by one score; and
3. the implementation detects the registered failure modes of citation missingness, paraphrase, and topical collision.

It does not support real-world weighting if those conditions hold only with oracle labels.

The central practical claim is weakened if hybrid recovery fails H5 or H6. In that event, SES should represent provenance uncertainty through bounds rather than inferred point clusters.

## 10. Reproducibility

- Standard-library Python only.
- Frozen configuration and preregistration hashes.
- Deterministic results and a separate byte-identical rerun.
- Unit tests for perfect observed citations, all-independent/all-one extremes, pairwise scoring, deterministic generation, and manifest integrity.
- Complete cell-level CSV and machine-readable summaries.

## 11. Limitations declared before execution

- Text is token-generated, not natural language.
- True derivations form disjoint families rather than recombining multiple sources.
- Citations are missing but never false.
- Root investigations have equal reliability and relevance.
- Text similarity uses exact tokens and cannot recognize semantic aliases.
- There are no dates, authors, organizations, or strategic actors.
- Downstream likelihoods are correctly specified.
- Human and agent performance are not tested.

Experiment 002B must use adjudicated real source families; Experiment 002C should add multi-parent synthesis, false citation, circular citation, and adversarial laundering.
