# Project Index

This is the canonical navigation page for Syncretic Epistemic Synthesis (SES). Start here when entering the project without prior conversation context.

## Orientation

| Need | Read |
|---|---|
| The founding idea and boundaries | [`../FOUNDING.md`](../FOUNDING.md) |
| Current verified state | [`../STATUS.md`](../STATUS.md) |
| Compact findings ledger | [`../FINDINGS.md`](../FINDINGS.md) |
| Cross-model continuation | [`../HANDOFF.md`](../HANDOFF.md) |
| Releases and structural changes | [`../CHANGELOG.md`](../CHANGELOG.md) |

## Methods

| Layer | Human specification | Machine contract | Implementation |
|---|---|---|---|
| Epistemic synthesis | [`PROTOCOL.md`](PROTOCOL.md) | [`../schema/ses-inquiry-0.1.schema.json`](../schema/ses-inquiry-0.1.schema.json) | [`../syntruth/core.py`](../syntruth/core.py) |
| Legacy decision protocol (reproduction only) | [`ACTION_EPISTEMOLOGY.md`](ACTION_EPISTEMOLOGY.md) | [`../schema/decision-pilot-0.1.schema.json`](../schema/decision-pilot-0.1.schema.json) | [`../syntruth/decision.py`](../syntruth/decision.py) |
| Bounded decision assurance | [`BOUNDED_DECISION_ASSURANCE.md`](BOUNDED_DECISION_ASSURANCE.md) | [`../schema/decision-assurance-0.2.schema.json`](../schema/decision-assurance-0.2.schema.json) | [`../syntruth/decision_v2.py`](../syntruth/decision_v2.py) |
| Question selection | [`QUESTION_FOUNDRY.md`](QUESTION_FOUNDRY.md) | — | — |
| Finite investigation | [`INVESTIGATION_PROTOCOL.md`](INVESTIGATION_PROTOCOL.md) | [`../schema/investigation-0.1.schema.json`](../schema/investigation-0.1.schema.json) | [`../syntruth/investigation.py`](../syntruth/investigation.py) |
| Agent roles | [`AGENTIC_HARNESS.md`](AGENTIC_HARNESS.md) | [`../schema/agent-artifact-0.1.schema.json`](../schema/agent-artifact-0.1.schema.json) | — |
| Architecture alternatives | [`OPTIONS.md`](OPTIONS.md) | — | — |
| Architecture decisions | [`decisions/README.md`](decisions/README.md) | — | — |

## Maintenance

| Need | Read |
|---|---|
| Repository ownership and release rules | [`../MAINTAINING.md`](../MAINTAINING.md) |
| Contribution checklist | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) |
| Instructions for future agents | [`../AGENTS.md`](../AGENTS.md) |
| Architectural rationale | [`decisions/README.md`](decisions/README.md) |

## Evidence program

| Stage | Location | Status |
|---|---|---|
| Program roadmap | [`../experiments/PROGRAM_ROADMAP.md`](../experiments/PROGRAM_ROADMAP.md) | Living plan |
| Experiment 001: dependence | [`../experiments/001-dependence/`](../experiments/001-dependence/) | Complete, deterministic synthetic result |
| Experiment 002A: provenance | [`../experiments/002-provenance/`](../experiments/002-provenance/) | Complete, deterministic synthetic result |
| Experiment 002B: real corpus | [`../experiments/002-provenance/REAL_CORPUS_PROTOCOL.md`](../experiments/002-provenance/REAL_CORPUS_PROTOCOL.md) | Designed, not run |
| Experiment 003A: decision stress | [`../experiments/003a-decision-stress/`](../experiments/003a-decision-stress/) | Complete synthetic test; 4/7 hypotheses supported |
| Experiment 003B: bounded decision assurance | [`../experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md`](../experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md) | Comparative design draft; not preregistered or run |
| Experiment 003: blinded wind tunnel | [`../experiments/PROGRAM_ROADMAP.md`](../experiments/PROGRAM_ROADMAP.md) | Designed, not run |
| Experiment 004: prospective forecasting | [`../experiments/PROGRAM_ROADMAP.md`](../experiments/PROGRAM_ROADMAP.md) | Designed, not run |
| Experiment 005: field decisions | [`BOUNDED_DECISION_ASSURANCE.md`](BOUNDED_DECISION_ASSURANCE.md) | 0.2 foundation executable; no field study authorized or run |

## Examples and templates

- [003B development interpretation](../experiments/003b-bounded-decision-assurance/DEVELOPMENT_INTERPRETATION.md): two exposed runs; broad comparative study still pending.
- [Finite fault investigation](../examples/fault-investigation.json) and [replay trace](../examples/fault-investigation-results.json): illustrative observations and costs.

- [`../examples/anschluss.json`](../examples/anschluss.json): worked counterfactual inquiry; illustrative judgments, not a historical finding.
- [`../examples/library-outreach-decision.json`](../examples/library-outreach-decision.json): worked low-risk action packet; illustrative judgments, not field data.
- [`../examples/library-outreach-bda.json`](../examples/library-outreach-bda.json): Action 0.2 bounded-assurance packet; illustrative ranges, evidence, challenges, and deficits.
- [`../templates/DECISION_BRIEF.md`](../templates/DECISION_BRIEF.md): human-first worksheet for a real decision pilot.

## External research intake

- [`../research/README.md`](../research/README.md): verification labels and ingestion rules.
- [`../research/INTAKE_TEMPLATE.md`](../research/INTAKE_TEMPLATE.md): reusable packet for subsequent search batches.
- [`../research/intake/001-shared-omission-google-ai/ANALYSIS.md`](../research/intake/001-shared-omission-google-ai/ANALYSIS.md): first AI Mode literature intake, corrections, and novelty assessment for SES-GEM-011.
- [`../research/deep/001-bounded-robustness/report-source.md`](../research/deep/001-bounded-robustness/report-source.md): deep research on typed uncertainty, bounded assurance, adaptive learning, and evaluator overfitting.

## Naming and placement rules

- Root documents answer project-level questions only.
- `docs/` contains stable method descriptions and navigation.
- `schema/` contains interoperable machine contracts.
- `syntruth/` contains dependency-free deterministic reference code.
- `tests/` mirrors implementation modules.
- `scripts/` contains portable repository validation utilities.
- `examples/` contains non-authoritative worked inputs and generated outputs.
- `experiments/NNN-name/` contains preregistration, frozen config, execution log, results, truth gems, and integrity manifest for one study.
- `templates/` contains blank operational forms.
- `research/intake/` contains external reconnaissance, corrected source ledgers, and transfer assessments; AI summaries never enter the findings ledger directly.
- `work/` is reserved for disposable intermediate material and must not be cited as a result.

Completed evidence must never be mixed with proposals. Synthetic results must never be labeled as real-world validation. Generated reports should identify the exact input packet and program version.
