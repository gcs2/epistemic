# Dependence-aware synthesis under duplicated evidence

> Confirmatory synthetic benchmark report. Interpret only within the preregistered data-generating mechanisms.

- **Cells:** 150
- **Simulated trials:** 375,000
- **Configuration SHA-256:** `e1de74175e3165a4b6d4228d607f771baecf24af6039e6c93f9d6207ceb3c81a`

## Overall performance

Lower Brier, log loss, calibration error, and confidently-wrong rate are better. Accuracy is higher-is-better. Cell means receive equal weight.

| Method | Brier | Log loss | Accuracy | ECE | Confidently wrong | Sharpness |
|---|---:|---:|---:|---:|---:|---:|
| Oracle | 0.07509 | 0.23138 | 89.0% | 0.0113 | 0.77% | 0.3894 |
| Estimated | 0.07625 | 0.23552 | 88.8% | 0.0130 | 0.89% | 0.3900 |
| Conservative | 0.08018 | 0.25031 | 88.7% | 0.0300 | 0.48% | 0.3620 |
| Naive | 0.08596 | 0.36973 | 88.5% | 0.0450 | 3.52% | 0.4239 |
| One Per Group | 0.09147 | 0.27965 | 86.4% | 0.0128 | 0.85% | 0.3638 |

## Preregistered hypotheses

| Hypothesis | Result | Registered effect |
|---|---|---|
| H1 | **Supported** | naive − oracle Brier = 0.016973; bootstrap 95% interval [0.012973, 0.021261] |
| H2 | **Supported** | Averaged naive penalty is nondecreasing across registered rho and duplication grids. |
| H3 | **Supported** | high-dependence conservative − naive Brier = -0.030175; confidently-wrong difference = -0.076078 |
| H4 | **Supported** | rho=0 conservative − naive Brier = 0.020006 |
| H5 | **Supported** | estimated − naive Brier = -0.015420; estimated − oracle = 0.001553 |
| H6 | **Supported** | maximum probability spread with one item per group = 0.000e+00 |

## Dependence penalty surface

Values are naive-independent Brier minus oracle Brier. Positive values mean naive synthesis is worse.

| rho \ max duplicates | 1 | 2 | 4 | 8 | 16 |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| 0.25 | 0.00000 | 0.00061 | 0.00253 | 0.00712 | 0.01304 |
| 0.50 | 0.00000 | 0.00288 | 0.00760 | 0.01649 | 0.02580 |
| 0.75 | 0.00000 | 0.00470 | 0.01276 | 0.03040 | 0.03693 |
| 0.95 | 0.00000 | 0.00739 | 0.02087 | 0.03536 | 0.04710 |

## Interpretation

The oracle is advantaged by knowing the true correlation and is a reference bound. Conservative deduplication is intentionally cautious. Its comparison with naive synthesis reveals a real tradeoff: duplicate protection under high dependence versus lost information when grouped observations are independent.

This experiment does not show that real-world dependence groups or correlations can be recovered reliably. That is the subject of later provenance-mapping and retrospective experiments.
