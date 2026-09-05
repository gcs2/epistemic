# Syncretic Epistemic Synthesis (SES)

SES is an experimental protocol and reference program for transparent, multi-model truth-seeking and bounded decision support. It combines dependence-aware evidence, explicit hypotheses, model pluralism, typed uncertainty, adversarial challenge, and prospective learning.

This repository contains the founding document, versioned epistemic and action protocols, completed synthetic experiments, source-backed research, and a deterministic Python reference harness. New readers should begin with the [project index](docs/INDEX.md). Contributors and future models must follow the [maintenance contract](MAINTAINING.md); continuation context is in [HANDOFF.md](HANDOFF.md).

Current checkpoint: **0.7.0**. A finite investigation loop and two public development runs now exist. The runs support keeping one-step planning as the default and expose failure with misleading observations and absent hypotheses. Superiority, field utility and novelty remain unestablished.

## Self-sustaining business initiative

[BIZ-001: business compendium](docs/business/README.md) tracks a service-first
commercialization proposal: customer discovery, plain-language positioning,
sales and marketing, delivery economics, operations, and funding engine research.
Start with its [task ledger](docs/business/TRACKER.md). The initiative is in
planning; no paying market or field advantage is established. SES remains the
internal method name; the public brand and first offer are not yet selected.

## Quick start

Requires Python 3.11 or newer and has no runtime dependencies.

```powershell
python -m syntruth validate examples/anschluss.json
python -m syntruth run examples/anschluss.json --output examples/anschluss-report.md
python -m syntruth benchmark experiments/001-dependence/config.json --output-dir work/001-replay
python -m syntruth provenance-benchmark experiments/002-provenance/config.json --output-dir work/002-replay
python -m syntruth decision-benchmark experiments/003a-decision-stress/config.json --output-dir work/003a-replay
python -m syntruth decision-validate examples/library-outreach-decision.json
python -m syntruth decide examples/library-outreach-decision.json --output examples/library-outreach-decision-report.md
python -m syntruth decision-validate examples/library-outreach-bda.json
python -m syntruth decide examples/library-outreach-bda.json --output examples/library-outreach-bda-report.md --json examples/library-outreach-bda-results.json
python -m syntruth verify experiments/001-dependence/results/MANIFEST.sha256
python -m unittest discover -s tests -v
python -m syntruth investigation-validate examples/fault-investigation.json
python -m syntruth investigate examples/fault-investigation.json
```

The generated report includes:

- ensemble posterior estimates;
- per-model estimates;
- model disagreement;
- robustness intervals under declared uncertainty;
- evidence-group leverage; and
- a robust-core/contested-shell interpretation.

## Project map

- `FOUNDING.md` — philosophical and institutional charter.
- `MAINTAINING.md` — canonical ownership, versioning, release, and anti-clutter rules.
- `CONTRIBUTING.md` and `AGENTS.md` — change requirements for people and future agents.
- `CHANGELOG.md` — curated global release history; Git commits remain the exhaustive technical history.
- `FINDINGS.md` — bounded ledger of established, candidate, and unknown claims.
- `HANDOFF.md` — current cross-model continuation packet and ready-to-use prompt.
- `docs/INDEX.md` — canonical navigation and placement rules.
- `docs/OPTIONS.md` — broad survey of possible products and research directions.
- `docs/PROTOCOL.md` — initial machine-readable inquiry protocol.
- `docs/AGENTIC_HARNESS.md` — role-separated agent orchestration and evaluation design.
- `docs/QUESTION_FOUNDRY.md` — question selection, ten flagship topics, and truth-gem extraction.
- `docs/ACTION_EPISTEMOLOGY.md` — decision, field-learning, and ethics boundary.
- `docs/BOUNDED_DECISION_ASSURANCE.md` — executable Action Protocol 0.2 semantics and limitations.
- `docs/INVESTIGATION_PROTOCOL.md` — choosing, performing and scoring finite investigations.
- `docs/decisions/` — architecture decision records and reversal conditions.
- `schema/` — JSON Schema for interoperable inquiry packets.
- `syntruth/` — reference CLI and synthesis engine.
- `examples/` — worked structured inquiries.
- `templates/` — human-first operational worksheets.
- `tests/` — deterministic behavioral tests.
- `experiments/001-dependence/` — frozen preregistration and executable first benchmark.
- `experiments/002-provenance/` — hidden-source-family recovery benchmark.
- `experiments/003a-decision-stress/` — hidden-tail, misspecification, and decision-rule stress benchmark.
- `experiments/003b-bounded-decision-assurance/` — comparative 0.2 experiment, currently a design draft.
- `research/` — verified literature intake, deep research, and claim-to-source ledgers.
- `experiments/PROGRAM_ROADMAP.md` — the path from synthetic tests to prospective and field validation.

## Method boundary

The program does not independently verify that an input probability, consequence range, causal model, value weight, or challenge set is adequate. Its immediate value is auditability, sensitivity analysis, explicit disagreement, and testable decision discipline. A bounded status is not a universal robustness guarantee and not authorization to act.

Action Protocol 0.1 is retained solely for reproduction and migration comparison. New decision work uses Action 0.2, which keeps evidence quality outside consequence arithmetic and reports conditional performance, stakeholder effects, constraints, assurance deficits, and learning commitments.

## How this repository stays coherent

GitHub commits provide the complete change history. The root changelog summarizes behaviorally and scientifically meaningful releases. Architecture decisions explain durable choices; status and findings have separate canonical ledgers. Breaking protocol changes receive new versioned schemas and engines rather than silently changing old behavior.

Before changing the system:

1. Read the project index, status, findings, handoff, and maintenance contract.
2. Identify the canonical file instead of creating another summary.
3. Add tests and preserve legacy experiment reproducibility.
4. Update documentation, status, changelog, and handoff together at a checkpoint.
5. Run the full validation suite and inspect the repository before committing.

See [`MAINTAINING.md`](MAINTAINING.md) for the complete change classes, placement rules, commit convention, and release checklist.

## Experiment 001 result

The hash-frozen dependence benchmark ran 375,000 simulated trials across 150 registered conditions. All six preregistered mechanism hypotheses were supported:

- naive treatment of correlated duplicates increased Brier loss;
- the penalty increased with duplication and correlation;
- conservative deduplication protected against high dependence;
- conservative deduplication discarded useful information under genuine independence;
- noisy correlation estimates recovered 89.3% of the aggregate oracle improvement; and
- all methods were exactly equivalent when no duplication existed.

See the [confirmatory report](experiments/001-dependence/results/report.md) and bounded [truth-gem ledger](experiments/001-dependence/results/TRUTH_GEMS.md). These are synthetic findings, not evidence that real provenance can already be recovered reliably.

## Experiment 002A result

The source-family recovery benchmark generated 17,280 cases across 108 registered conditions. Six of eight hypotheses were supported. Two central hypotheses failed: an unconditional citation-plus-text hybrid recovered more true relationships but falsely merged too many independent families, and its registered downstream improvement over naive independence was not stable.

Citation-only recovery was incomplete but precise and performed better overall. An exploratory registered-factor split found hybrid recovery highly beneficial under low topical collision and actively harmful under high topical collision. This interaction requires confirmatory replication.

See the [Experiment 002A report](experiments/002-provenance/results/report.md), [truth gems](experiments/002-provenance/results/TRUTH_GEMS.md), and [real-corpus protocol](experiments/002-provenance/REAL_CORPUS_PROTOCOL.md).

## Experiment 003A result

The decision stress test ran 96,000 synthetic cases across 96 registered cells. Four of seven hypotheses were supported. Shared tail omission increased false robustness certification, and multiplying low-confidence negative impacts by confidence increased catastrophe exposure by 0.00689 (paired bootstrap 95% interval 0.00666–0.00713). The registered robustness gate bought some tail protection at an excessive opportunity cost, minimax regret did not improve P90 regret, and the distributional-harm threshold never activated.

See the [Experiment 003A report](experiments/003a-decision-stress/results/report.md), [deviation record](experiments/003a-decision-stress/DEVIATIONS.md), and [truth gems](experiments/003a-decision-stress/results/TRUTH_GEMS.md). Action protocol 0.1 now disables robust certification when it detects the demonstrated signed-confidence hazard.

## Status

The [003B development interpretation](experiments/003b-bounded-decision-assurance/DEVELOPMENT_INTERPRETATION.md)
explains the first investigation results. The [implementation audit](experiments/003b-bounded-decision-assurance/IMPLEMENTATION_AUDIT.md)
distinguishes promised capabilities from implemented behavior. The current engine
can distinguish supplied hypotheses; it cannot discover one outside its model.

Version 0.7 is a research prototype with three completed synthetic experiments and two exposed 003B development runs. BDA 0.2 remains a sensitivity-analysis prototype. Investigation 0.1 adds explicit outcome distributions and an executable finite learning loop. The full BDA comparative study, real-corpus transfer and field validation remain outstanding.

Repository: [github.com/gcs2/epistemic](https://github.com/gcs2/epistemic)
