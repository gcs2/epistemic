# Experiment 002A Run Log

## Frozen inputs

- Preregistration SHA-256: `2605CAA66C5661E74B52DE30EEE0ED7647BE4090CD80928371A8E4B056A2BE9C`
- Configuration SHA-256: `B0ED7FBAD790F3F91A45174A102EAC3956EBC408E56BE03645D8ACC5040EB2D8`
- Confirmatory seed: `20260830`
- Bootstrap seed: `20260831`

## Before confirmatory execution

- Twenty-three tests passed.
- The preregistration and configuration were hash-frozen.
- No full-grid output had been inspected.

## Confirmatory execution

- Registered cells: 108.
- Cases per cell: 160.
- Total generated cases: 17,280.
- Methods: 6.
- No cells were excluded.
- Supported hypotheses: H1, H2, H3, H4, H7, H8.
- Not supported: H5 and H6.

The failure of H5 and H6 is retained as a central result. Hybrid recovery increased recall but did not retain the preregistered precision threshold, and its Brier improvement over all-independent synthesis in the recoverable stratum had a bootstrap interval crossing zero.

## Deterministic replication

A separate complete rerun produced identical hashes:

- `report.md`: `9CD50F83439AFF85F7FB69EA98CC6E1996733F98F690848956F502BB01D05D9D`
- `summary.json`: `42D61EF6D1A2DC8674C0F93B06E761CE321CD5F536EBB0F5372AFE54830F358A`
- `cells.csv`: `D62E905C9A010A8897A9110FD7326085513E331EAB04962692988E6E631AD1DE`

## Exploratory analysis

After confirmatory results were inspected, results were stratified by the already-registered topic-contamination factor.

- At contamination 0.10, hybrid precision was 1.0000 and Brier was 0.0685, versus 0.0866 for all-independent synthesis.
- At contamination 0.50, hybrid precision was 0.2245 and Brier was 0.1069, versus 0.0886 for all-independent synthesis.

This interaction is labeled exploratory and requires preregistered replication. It did not alter the confirmatory hypothesis verdicts.

## Deviations

None.
