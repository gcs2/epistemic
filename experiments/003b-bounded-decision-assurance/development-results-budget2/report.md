# 003B investigation development evaluation

Exposed development generator; descriptive results, not independent confirmation.
Net utility charges actual investigation and specified delay costs. CPU cost is reported
as planner nodes separately. Outcome tail is the mean of per-episode lower-tail means.

| Regime | Policy | Net utility | Cost | Steps | Severe loss probability | False low-risk | Planner nodes |
|---|---|---:|---:|---:|---:|---:|---:|
| matched | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| matched | fixed | 6.119 | 3.193 | 2.00 | 0.030 | 0.033 | 0.0 |
| matched | random | 6.278 | 3.341 | 2.00 | 0.033 | 0.008 | 0.0 |
| matched | entropy | 7.508 | 2.892 | 2.00 | 0.029 | 0.033 | 0.0 |
| matched | myopic | 8.023 | 1.846 | 1.31 | 0.027 | 0.025 | 1.9 |
| matched | sequential | 8.267 | 1.915 | 1.38 | 0.024 | 0.025 | 8.0 |
| disclosed_no_signal | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | fixed | 2.032 | 3.193 | 2.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | random | 1.884 | 3.341 | 2.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | entropy | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| disclosed_no_signal | myopic | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 1.0 |
| disclosed_no_signal | sequential | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 7.0 |
| hidden_no_signal | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| hidden_no_signal | fixed | -1.196 | 3.193 | 2.00 | 0.058 | 0.083 | 0.0 |
| hidden_no_signal | random | -1.172 | 3.341 | 2.00 | 0.059 | 0.050 | 0.0 |
| hidden_no_signal | entropy | -1.131 | 2.913 | 2.00 | 0.061 | 0.100 | 0.0 |
| hidden_no_signal | myopic | 0.312 | 1.841 | 1.30 | 0.059 | 0.100 | 1.9 |
| hidden_no_signal | sequential | 0.042 | 1.928 | 1.38 | 0.060 | 0.108 | 8.0 |
| reversed | stop | 5.225 | 0.000 | 0.00 | 0.026 | 0.000 | 0.0 |
| reversed | fixed | -6.981 | 3.193 | 2.00 | 0.089 | 0.117 | 0.0 |
| reversed | random | -6.407 | 3.341 | 2.00 | 0.072 | 0.058 | 0.0 |
| reversed | entropy | -6.689 | 2.907 | 2.00 | 0.085 | 0.142 | 0.0 |
| reversed | myopic | -5.302 | 1.739 | 1.23 | 0.085 | 0.133 | 1.9 |
| reversed | sequential | -5.365 | 1.812 | 1.28 | 0.085 | 0.142 | 8.0 |
| omitted | stop | -27.415 | 0.000 | 0.00 | 0.350 | 1.000 | 0.0 |
| omitted | fixed | -30.608 | 3.193 | 2.00 | 0.350 | 0.917 | 0.0 |
| omitted | random | -30.756 | 3.341 | 2.00 | 0.350 | 0.867 | 0.0 |
| omitted | entropy | -30.328 | 2.913 | 2.00 | 0.350 | 0.900 | 0.0 |
| omitted | myopic | -29.256 | 1.841 | 1.30 | 0.350 | 0.908 | 1.9 |
| omitted | sequential | -29.343 | 1.928 | 1.38 | 0.350 | 0.917 | 8.0 |

## Paired comparisons

Sequential minus comparator. Percentile bootstrap intervals are descriptive,
paired across cases and unadjusted for multiple comparisons.

| Regime | Comparator | Net difference | 95% interval |
|---|---|---:|---|
| matched | stop | 3.042 | 0.957 to 4.988 |
| matched | fixed | 2.149 | 0.520 to 3.729 |
| matched | random | 1.989 | 0.125 to 3.902 |
| matched | entropy | 0.759 | -0.272 to 1.946 |
| matched | myopic | 0.244 | -0.469 to 1.157 |
| disclosed_no_signal | stop | 0.000 | 0.000 to 0.000 |
| disclosed_no_signal | fixed | 3.193 | 2.980 to 3.394 |
| disclosed_no_signal | random | 3.341 | 3.122 to 3.550 |
| disclosed_no_signal | entropy | 0.000 | 0.000 to 0.000 |
| disclosed_no_signal | myopic | 0.000 | 0.000 to 0.000 |
| hidden_no_signal | stop | -5.183 | -7.958 to -2.517 |
| hidden_no_signal | fixed | 1.237 | -0.637 to 3.212 |
| hidden_no_signal | random | 1.214 | -0.926 to 3.035 |
| hidden_no_signal | entropy | 1.173 | -0.102 to 2.320 |
| hidden_no_signal | myopic | -0.270 | -0.697 to -0.019 |
| reversed | stop | -10.590 | -13.248 to -8.088 |
| reversed | fixed | 1.616 | -0.085 to 3.178 |
| reversed | random | 1.043 | -0.318 to 2.308 |
| reversed | entropy | 1.325 | 0.375 to 2.166 |
| reversed | myopic | -0.063 | -0.153 to 0.016 |
| omitted | stop | -1.928 | -2.180 to -1.669 |
| omitted | fixed | 1.265 | 1.022 to 1.519 |
| omitted | random | 1.414 | 1.175 to 1.669 |
| omitted | entropy | 0.985 | 0.775 to 1.207 |
| omitted | myopic | -0.087 | -0.202 to 0.013 |

## Scope

Known finite model and supplied likelihoods; exposed generator; no novelty or field validation
The omitted mechanism is absent from every public hypothesis set.
No method can assign posterior mass to it. Trace samples expose predictions and updates.
Strong performance with supplied accurate likelihoods does not establish how to obtain those likelihoods.
