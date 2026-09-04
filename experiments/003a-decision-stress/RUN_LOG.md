# Experiment 003A Run Log

## Frozen inputs

- `PREREGISTRATION.md`: `61CD83654E7A24D82B7A8F5A95877918B303DAB352A2CB99CFFAE5FA03F3A08D`
- `config.json`: `E404B89B5879E4F9E4058DECD21B92EBA679700AEF68F04BBF59AE69435428C3`

Both hashes were recorded in `FROZEN.sha256` before the first full execution.

## Execution history

1. The first 96,000-case execution completed on 2026-09-04.
2. Output inspection identified an H5 result-classification bug: executable analysis used a weaker success rule than the frozen preregistration.
3. The mismatch was recorded in `DEVIATIONS.md`, the evaluator was corrected, and the complete deterministic run was repeated.
4. The corrected result supports H1–H4 and does not support H5–H7.
5. A third complete run reproduced `cells.csv`, `summary.json`, and `report.md` byte-for-byte on 2026-09-04.
6. `results/MANIFEST.sha256` records those generated artifacts plus the human- and machine-readable bounded truth-gem ledgers.

The code uses only the Python standard library. Execution used the Codex bundled Python 3.11+ runtime because `python` was not available on the workspace PATH.
