# 003B investigation development evaluation

Exposed development generator; descriptive results, not independent confirmation.
Net utility charges actual investigation and specified delay costs. CPU cost is reported
as planner nodes separately. Outcome tail is the mean of per-episode lower-tail means.

| Regime | Policy | Net utility | Cost | Steps | Severe loss probability | False low-risk | Planner nodes |
|---|---|---:|---:|---:|---:|---:|---:|
| matched | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| matched | fixed | 6.537 | 4.953 | 3.00 | 0.023 | 0.025 | 0.0 |
| matched | random | 6.537 | 4.953 | 3.00 | 0.023 | 0.025 | 0.0 |
| matched | entropy | 6.537 | 4.953 | 3.00 | 0.023 | 0.025 | 0.0 |
| matched | myopic | 7.980 | 1.889 | 1.33 | 0.027 | 0.025 | 2.3 |
| matched | sequential | 8.297 | 1.950 | 1.46 | 0.024 | 0.025 | 36.3 |
| disclosed_no_signal | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | fixed | 0.272 | 4.953 | 3.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | random | 0.272 | 4.953 | 3.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | entropy | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | myopic | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 1.0 |
| disclosed_no_signal | sequential | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 31.0 |
| hidden_no_signal | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| hidden_no_signal | fixed | -2.083 | 4.953 | 3.00 | 0.054 | 0.058 | 0.0 |
| hidden_no_signal | random | -2.083 | 4.953 | 3.00 | 0.054 | 0.058 | 0.0 |
| hidden_no_signal | entropy | -2.083 | 4.953 | 3.00 | 0.054 | 0.058 | 0.0 |
| hidden_no_signal | myopic | 0.394 | 1.903 | 1.34 | 0.058 | 0.100 | 2.3 |
| hidden_no_signal | sequential | 0.401 | 1.986 | 1.47 | 0.057 | 0.117 | 36.3 |
| reversed | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| reversed | fixed | -9.244 | 4.953 | 3.00 | 0.088 | 0.100 | 0.0 |
| reversed | random | -9.244 | 4.953 | 3.00 | 0.088 | 0.100 | 0.0 |
| reversed | entropy | -9.244 | 4.953 | 3.00 | 0.088 | 0.100 | 0.0 |
| reversed | myopic | -5.332 | 1.769 | 1.24 | 0.085 | 0.142 | 2.2 |
| reversed | sequential | -5.240 | 1.819 | 1.32 | 0.086 | 0.175 | 36.2 |
| omitted | stop | -27.415 | 0.000 | 0.00 | 0.350 | 1.000 | 0.0 |
| omitted | fixed | -32.368 | 4.953 | 3.00 | 0.350 | 0.917 | 0.0 |
| omitted | random | -32.368 | 4.953 | 3.00 | 0.350 | 0.917 | 0.0 |
| omitted | entropy | -32.368 | 4.953 | 3.00 | 0.350 | 0.917 | 0.0 |
| omitted | myopic | -29.318 | 1.903 | 1.34 | 0.350 | 0.933 | 2.3 |
| omitted | sequential | -29.401 | 1.986 | 1.47 | 0.350 | 0.942 | 36.3 |

## Paired comparisons

Sequential minus comparator. Percentile bootstrap intervals are descriptive,
paired across cases and unadjusted for multiple comparisons.

| Regime | Comparator | Net difference | 95% interval |
|---|---|---:|---|
| matched | stop | 3.072 | 1.064 to 4.894 |
| matched | fixed | 1.760 | 0.333 to 3.180 |
| matched | random | 1.760 | 0.333 to 3.180 |
| matched | entropy | 1.760 | 0.333 to 3.180 |
| matched | myopic | 0.317 | -0.548 to 1.337 |
| disclosed_no_signal | stop | 0.000 | 0.000 to 0.000 |
| disclosed_no_signal | fixed | 4.953 | 4.701 to 5.224 |
| disclosed_no_signal | random | 4.953 | 4.701 to 5.224 |
| disclosed_no_signal | entropy | 0.000 | 0.000 to 0.000 |
| disclosed_no_signal | myopic | 0.000 | 0.000 to 0.000 |
| hidden_no_signal | stop | -4.825 | -7.506 to -2.395 |
| hidden_no_signal | fixed | 2.483 | 1.092 to 3.783 |
| hidden_no_signal | random | 2.483 | 1.092 to 3.783 |
| hidden_no_signal | entropy | 2.483 | 1.092 to 3.783 |
| hidden_no_signal | myopic | 0.007 | -0.808 to 0.993 |
| reversed | stop | -10.465 | -13.129 to -7.903 |
| reversed | fixed | 4.004 | 3.046 to 5.065 |
| reversed | random | 4.004 | 3.046 to 5.065 |
| reversed | entropy | 4.004 | 3.046 to 5.065 |
| reversed | myopic | 0.092 | -0.760 to 1.018 |
| omitted | stop | -1.986 | -2.222 to -1.733 |
| omitted | fixed | 2.968 | 2.706 to 3.243 |
| omitted | random | 2.968 | 2.706 to 3.243 |
| omitted | entropy | 2.968 | 2.706 to 3.243 |
| omitted | myopic | -0.082 | -0.237 to 0.060 |

## Scope

Known finite model and supplied likelihoods; exposed generator; no novelty or field validation
The omitted mechanism is absent from every public hypothesis set.
No method can assign posterior mass to it. Trace samples expose predictions and updates.
Strong performance with supplied accurate likelihoods does not establish how to obtain those likelihoods.
