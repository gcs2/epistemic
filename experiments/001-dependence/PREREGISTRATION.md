# Experiment 001 Preregistration

## Dependence-aware synthesis under duplicated evidence

**Protocol version:** 1.0  
**Status:** Confirmatory design frozen before the first full benchmark run  
**Date:** 2026-08-11  
**Framework:** ADEMP — aims, data-generating mechanisms, estimands, methods, and performance measures

## 1. Research program

The long-term SES flagship asks:

> Across preregistered resolvable forecasts and blinded retrospective questions, which combination of independent evidence collection, structured model advocacy, dependence mapping, adversarial review, and deterministic synthesis produces the best calibration and error correction per unit of time?

Experiment 001 isolates the first falsifiable mechanism: dependence mapping. It asks whether treating derivative evidence as independent creates avoidable overconfidence and whether cluster-aware aggregation improves probabilistic accuracy.

The study is computational and contains no human participants, private data, live external systems, or model-generated research judgments.

## 2. Background and rationale

Probabilistic forecasts should be evaluated by proper scoring rules, which reward honest probability reporting rather than accuracy alone. The primary metric will be binary Brier loss; log loss is secondary. Proper scoring-rule foundations are described by [Gneiting and Raftery](https://doi.org/10.1198/016214506000001437).

Forecasting tournaments have demonstrated that training, team structure, selection, and aggregation can improve judgment, supporting comparative evaluation rather than argument from prestige. See [Tetlock et al. on forecasting tournaments](https://journals.sagepub.com/doi/10.1177/0963721414534257).

Clustered observations contain fewer effective independent observations than their nominal count suggests. A standard design-effect expression uses within-cluster correlation and cluster size to calculate effective sample size; the conceptual issue is summarized in [Killip, Mahfoud, and Pearce](https://pmc.ncbi.nlm.nih.gov/articles/PMC1466680/).

The simulation is organized with ADEMP because simulation studies can otherwise acquire selective conditions and metrics after results are visible. The framework and the importance of Monte Carlo uncertainty are described by [Morris, White, and Crowther](https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/). OSF explicitly provides a simulation-study preregistration template based on ADEMP and describes preregistration as a time-stamped, read-only plan created before analysis ([OSF guidance](https://help.osf.io/article/330-welcome-to-registrations)). This local document is preparation for, not a substitute for, an external immutable registration.

## 3. Aims

### Primary aim

Estimate how evidence duplication and within-source correlation affect the Brier loss of naive-independent, conservative-deduplicated, correlation-adjusted, and one-per-group synthesis.

### Secondary aims

1. Identify conditions under which conservative dependence grouping discards genuinely independent information.
2. Measure whether noisy correlation estimates retain most of the oracle adjustment’s benefit.
3. Quantify overconfident error, calibration error, log loss, and classification accuracy.
4. establish deterministic, reusable benchmark infrastructure for later SES ablations.

## 4. Confirmatory hypotheses

**H1 — duplication penalty.** When within-group correlation is positive and groups contain duplicates, naive-independent synthesis will have worse mean Brier loss than oracle correlation-adjusted synthesis.

**H2 — monotonic amplification.** The relative Brier disadvantage of naive-independent synthesis will increase with both maximum duplication and within-group correlation, averaged over other registered conditions.

**H3 — conservative protection.** When correlation is high (`rho >= 0.75`) and maximum duplication is at least 4, conservative deduplication will have lower Brier loss and a lower rate of confidently wrong predictions than naive-independent synthesis.

**H4 — independence cost.** When within-group correlation is zero and maximum duplication exceeds 1, conservative deduplication will have worse Brier loss than naive-independent synthesis because it discards independent information.

**H5 — estimation utility.** With registered correlation-estimation noise, estimated-correlation synthesis will outperform naive-independent synthesis in mean Brier loss across cells with positive correlation and duplication, but underperform the oracle.

**H6 — no-duplication equivalence.** When every group contains exactly one item, all registered aggregation rules except estimation noise should produce numerically identical predictions. Because the denominator is one, estimation noise also has no effect; therefore all five methods should be identical up to floating-point tolerance.

## 5. Data-generating mechanisms

### 5.1 Outcomes

Each trial has a binary true state `Y`, sampled from `Bernoulli(base_rate)` with registered base rate 0.5.

### 5.2 Independent evidence groups

Each trial contains `G` independent latent evidence groups. Group sizes are sampled uniformly from the integers 1 through `D`, where `D` is the cell’s maximum duplication.

### 5.3 Correlated observations

For item `j` in group `g`:

\[
X_{gj}=s\mu+\sigma\left(\sqrt{\rho}Z_g+\sqrt{1-\rho}\epsilon_{gj}\right),
\]

where:

- \(s=+1\) when `Y=1` and \(s=-1\) when `Y=0`;
- \(\mu\) is registered signal strength;
- \(\sigma=1\);
- \(Z_g\) and \(\epsilon_{gj}\) are independent standard normal variables; and
- \(\rho\) is within-group correlation.

Different groups are independent. The joint log-likelihood ratio for an equicorrelated group is:

\[
LLR_g=\frac{2\mu}{\sigma^2}\frac{\sum_j X_{gj}}{1+(m_g-1)\rho}.
\]

The denominator is the cluster design effect. This makes the oracle posterior analytically available.

### 5.4 Registered grid

- trials per cell: 2,500;
- independent evidence groups: 3, 8, 20;
- maximum duplicates: 1, 2, 4, 8, 16;
- within-group correlation: 0, 0.25, 0.50, 0.75, 0.95;
- signal strength: 0.25, 0.75;
- standard deviation: 1;
- base rate: 0.5;
- correlation-estimation standard deviation: 0.15;
- random seed: 20260811.

This produces 150 cells and 375,000 trials. All registered cells will be reported.

## 6. Estimands

The primary estimand is the paired difference in mean Brier loss between each method and oracle correlation-adjusted synthesis, overall and within registered grid strata.

Secondary estimands are paired differences in:

- binary log loss;
- classification accuracy at threshold 0.5;
- expected calibration error using ten equal-width bins;
- rate of confidently wrong predictions, defined as assigning at least 0.90 probability to the false state; and
- forecast sharpness, measured as mean absolute distance from 0.5.

Monte Carlo standard errors will be calculated for mean Brier and log loss.

## 7. Methods compared

### M1 — Oracle correlation-adjusted

Uses the true `rho` in the design-effect denominator. This is the data-generating-model optimum and a reference bound, not a deployable SES method.

### M2 — Estimated-correlation

Uses a group-specific estimate `rho_hat`, created by adding zero-mean Gaussian error with standard deviation 0.15 to true `rho` and clipping to `[0, 0.999]`.

### M3 — Conservative deduplication

Assumes within-group correlation of one, so each group contributes its mean observation. This matches SES 0.1’s conservative independence-group heuristic.

### M4 — Naive independent

Assumes correlation zero and sums every item as an independent contribution.

### M5 — One per group

Uses only the first observation from every group. This avoids duplication but wastes within-group replication.

All methods use the true base rate and the same observed trials.

## 8. Performance measures and analysis

### 8.1 Primary analysis

For every cell and method, compute mean Brier loss. Aggregate cell means with equal cell weight so cells with identical registered trial counts remain equally represented. Report method-minus-oracle differences and percent change relative to naive-independent synthesis.

H1 is supported if naive Brier exceeds oracle Brier across all positive-correlation, duplicated cells in aggregate and the paired cell-level bootstrap 95% interval excludes zero.

H2 is evaluated by reporting the naive-minus-oracle Brier difference over the complete `rho × maximum duplication` grid. Monotonicity is considered supported when row- and column-averaged differences are nondecreasing apart from differences smaller than two Monte Carlo standard errors.

H3–H5 are evaluated through registered stratified contrasts. H6 uses exact numerical comparison with absolute tolerance `1e-12`.

### 8.2 Uncertainty

Simulation Monte Carlo standard errors are primary for within-cell means. Across-cell paired uncertainty will use a deterministic bootstrap with 10,000 resamples and seed `20260812`. No null-hypothesis significance test will substitute for effect sizes.

### 8.3 Multiplicity

The six hypotheses are mechanism tests rather than interchangeable discoveries. All are reported; no claims will be selected solely by a significance threshold. Exploratory analyses are labeled separately.

## 9. Success, failure, and interpretation rules

The central SES dependence claim is provisionally supported if H1, H3, and H4 all hold. H4 is essential: a method that always discounts evidence can appear safe merely by remaining uncertain. A useful method must reveal both its protection and its opportunity cost.

The claim is weakened if:

- naive synthesis matches or beats dependence-aware synthesis under high correlation and duplication;
- conservative grouping does not sacrifice performance when evidence is actually independent, suggesting a coding or DGM error; or
- estimated correlation performs worse than both extremes across most positive-correlation cells.

No synthetic result establishes that real citation or agent dependence can be identified accurately. It establishes only the consequences of dependence and misclassification under declared models.

## 10. Reproducibility controls

- Python standard library only.
- Fixed seed and complete configuration committed with the protocol.
- Deterministic CSV, JSON, and Markdown outputs.
- Unit tests for no-duplication equivalence, perfect-correlation equivalence, posterior normalization, and run determinism.
- Full cell results retained; no condition omitted because it is inconvenient.
- Code changes after the frozen hash will be recorded in `DEVIATIONS.md`.

## 11. Prospective extension boundary

This preregistration governs only the synthetic benchmark. Retrospective historical cases and prospective human/agent experiments require separate frozen protocols, data-governance review, and—where humans are participants—appropriate ethics review.

## 12. Known limitations before observing results

- Binary states are easier than open-world hypothesis generation.
- Evidence groups are known perfectly; real provenance is incomplete.
- Equicorrelation is a simplification.
- Signals are conditionally Gaussian and correctly specified.
- Sources do not deceive strategically.
- Model pluralism, red-teaming, translation, and human legitimacy are not tested here.
- Brier and log loss measure probabilistic accuracy, not explanatory value or decision justice.

These limitations define the next experiments rather than invalidate this one.
