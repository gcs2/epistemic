# Contributing

SES is both software and a research record. A contribution is complete only when its behavior, evidence status, and documentation agree.

Start with [`MAINTAINING.md`](MAINTAINING.md) and the [`project index`](docs/INDEX.md). Open a focused change, preserve unrelated work, and do not alter frozen experiment artifacts except through an explicit deviation and regenerated manifest.

## Local validation

Requires Python 3.11 or newer.

```powershell
python -m unittest discover -s tests -v
python -m syntruth validate examples/anschluss.json
python -m syntruth decision-validate examples/library-outreach-decision.json
python -m syntruth decision-validate examples/library-outreach-bda.json
python -m syntruth verify experiments/001-dependence/results/MANIFEST.sha256
python -m syntruth verify experiments/002-provenance/results/MANIFEST.sha256
python -m syntruth verify experiments/003a-decision-stress/FROZEN.sha256
python -m syntruth verify experiments/003a-decision-stress/results/MANIFEST.sha256
```

Experiment 003A has separate frozen-input and result manifests. Verify both before changing its implementation, artifacts, or claims.

## Pull-request standard

State:

- the failure mode or question being addressed;
- the semantic change;
- how it was tested;
- which claims or artifacts changed;
- backwards-compatibility implications; and
- what remains unproven.

Code style is deliberately dependency-light and explicit. Avoid adding a library where a small, auditable standard-library implementation is sufficient.
