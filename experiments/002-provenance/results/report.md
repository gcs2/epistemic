# Recovering hidden evidence families

> Confirmatory synthetic-pilot report. Structural recovery is evaluated against hidden generated ancestry.

- **Cells:** 108
- **Generated cases:** 17,280
- **Configuration SHA-256:** `b0ed7fbad790f3f91a45174a102eac3956ebc408e56be03645d8acc5040eb2d8`

## Overall provenance recovery

| Method | Precision | Recall | F1 | False independence | False dependence | Source-count error |
|---|---:|---:|---:|---:|---:|---:|
| Oracle | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| All Independent | 100.0% | 0.0% | 0.0% | 100.0% | 0.0% | 233.0% |
| All One | 14.5% | 100.0% | 24.5% | 0.0% | 100.0% | 82.5% |
| Citation | 100.0% | 40.4% | 48.2% | 59.6% | 0.0% | 124.2% |
| Text | 61.1% | 76.3% | 51.0% | 23.7% | 28.8% | 62.1% |
| Hybrid | 61.2% | 86.7% | 59.1% | 13.3% | 30.7% | 45.1% |

## Downstream truth estimation

| Method | Brier | Log loss | Accuracy | Confidently wrong | Sharpness |
|---|---:|---:|---:|---:|---:|
| Oracle | 0.06257 | 0.20569 | 91.4% | 1.27% | 0.4106 |
| Citation | 0.07977 | 0.36496 | 89.9% | 4.29% | 0.4455 |
| All Independent | 0.08759 | 0.52339 | 89.5% | 6.00% | 0.4625 |
| Hybrid | 0.08770 | 0.30255 | 89.2% | 1.64% | 0.3611 |
| Text | 0.08872 | 0.32515 | 89.1% | 2.25% | 0.3736 |
| All One | 0.14194 | 0.46352 | 89.5% | 0.00% | 0.1530 |

## Preregistered hypotheses

| Hypothesis | Result | Registered contrast |
|---|---|---|
| H1 | **Supported** | citation aggregate precision = 1.0000 |
| H2 | **Supported** | citation recall at completeness 0/0.5/0.9 = 0.0000/0.3694/0.8425 |
| H3 | **Supported** | text recall at paraphrase 0/0.4/0.8 = 1.0000/0.9670/0.3230 |
| H4 | **Supported** | text false-dependence at contamination 0.1/0.5 = 0.0000/0.5768 |
| H5 | **Not supported** | recall hybrid/citation/text = 0.8671/0.4040/0.7633; hybrid precision = 0.6123 |
| H6 | **Not supported** | recoverable hybrid − all-independent Brier = -0.003512; 95% interval [-0.013027, 0.006741] |
| H7 | **Supported** | nontrivial hybrid − oracle Brier = 0.025127; 95% interval [0.019773, 0.030825] |
| H8 | **Supported** | all-one − oracle Brier = 0.079366; 95% interval [0.074089, 0.084529] |

## Interpretation boundary

This pilot asks whether observable inheritance signals can recover a known hidden graph. It does not establish performance on natural prose, multi-parent claims, false citations, strategic source laundering, or real human and agent workflows.
