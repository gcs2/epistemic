# Experiment 001 Run Log

## Frozen inputs

- Preregistration SHA-256: `BBA3B04B2360F513D2593691ADAD25C5A03A034BDE91EE5C8D404381DB4D37D8`
- Configuration SHA-256: `E1DE74175E3165A4B6D4228D607F771BAECF24AF6039E6C93F9D6207CEB3C81A`
- Confirmatory seed: `20260811`
- Bootstrap seed: `20260812`

## Before the confirmatory run

- The preregistration and configuration were hash-frozen.
- Thirteen tests passed, including determinism, no-duplication equivalence, perfect-correlation oracle/conservative equivalence, dependence-group behavior, protocol validation, and output creation.
- No confirmatory cell output had been inspected.

## Confirmatory execution

- Registered cells: 150.
- Trials per cell: 2,500.
- Total simulated truth-bearing trials: 375,000.
- Methods per trial: 5.
- Full run completed successfully in approximately 23 seconds in the bundled Python 3.12.13 runtime.
- All six preregistered hypotheses were supported.
- No registered conditions were excluded.

## Deterministic replication

The complete benchmark was executed a second time into a separate intermediate directory. SHA-256 hashes matched exactly for:

- `report.md`: `92E9899D6D2A5DEF344BC8D5903B86A5F57ACD8217CCD3CB4EC3B55028322B5B`
- `summary.json`: `0F6FFCE0F3DE4D7D0E97D52AB61714CCF4D8C8C7168BD4ED6E5267449CD55C48`
- `cells.csv`: `83738FBD2A8565C54951A5F783A2425FF659FB29F61D1B39FEDF2AB49E34DE17`

## Post-run validation

- Sixteen tests passed after adding the integrity-verification command.
- Preregistration, configuration, report, summary, cell data, and truth-gem files passed manifest verification.
- Five truth-gem records passed structural checks and all JSON artifacts parsed successfully.
- No deviations from the registered simulation grid, data-generating mechanism, metrics, or hypotheses were recorded.

## Interpretation boundary

The run validates the code against the registered synthetic model. It does not validate real-world provenance recovery, likelihood elicitation, causal inference, model pluralism, human governance, or agent independence. Those limitations remain affirmative targets for Experiments 002–005.
