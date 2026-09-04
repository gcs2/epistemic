# Cross-Model Handoff

**Checkpoint:** SES 0.6.0 bounded-decision-assurance foundation  
**Canonical project index:** [`docs/INDEX.md`](docs/INDEX.md)  
**Current status:** [`STATUS.md`](STATUS.md)  
**Findings boundary:** [`FINDINGS.md`](FINDINGS.md)

## Mission

Develop Syncretic Epistemic Synthesis into a falsifiable, dependence-aware, multi-model method that improves real inquiry and decision correction without pretending that aggregation eliminates judgment, ethics, or uncertainty.

## Non-negotiable distinctions

1. Repeated reports are not automatically independent evidence.
2. Probability estimates, value judgments, and decision rules must remain separately inspectable.
3. Synthetic validation is not real-world validation.
4. A generated score is not authorization to act.
5. Negative and null results stay in the record.
6. Affected parties need challenge, appeal, and review paths.
7. “Truth gem” claims must be bounded by the test that produced them.

## What exists

- A deterministic evidence-synthesis harness (`syntruth/core.py`).
- Two completed, hash-manifested synthetic experiments.
- A generated-provenance result showing that an intuitively favored hybrid can fail through false transitive merges.
- A real-corpus provenance protocol awaiting data and adjudicators.
- A legacy Action 0.1 engine (`syntruth/decision.py`) retained for Experiment 003A reproduction; do not use it for new live decisions.
- An executable Bounded Decision Assurance 0.2 engine (`syntruth/decision_v2.py`) with explicit consequence bounds, uncertain value weights, evidence records, uncertainty groups, stakeholder constraints, challenge coverage, assurance deficits, lower-tail outcomes, and adaptive-learning commitments.
- A versioned Action 0.2 schema, illustrative packet and generated brief, protocol documentation, behavioral tests, and an architecture decision record.
- Experiment 003A: 96,000 synthetic decision cases showing both useful mechanisms and failures of signed confidence shrinkage, robustness gating, minimax regret, and the registered distributional test.
- Human-readable protocols, JSON contracts, examples, templates, and unit tests.
- A structured external-research intake beginning with the literature around shared omission and false consensus (`research/intake/001-shared-omission-google-ai/`).
- Deep research DR-001 mapping the action problem to decision theory, DMDU, assurance cases, adaptive planning, human factors, and adaptive-evaluation validity (`research/deep/001-bounded-robustness/`).
- A draft comparative Experiment 003B for Bounded Decision Assurance (`experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md`).
- A repository maintenance contract, contribution guide, agent instructions, architecture decision log, and pull-request checklist.

## What the evidence supports

Read [`FINDINGS.md`](FINDINGS.md). In compact form: dependence matters; naive repetition can manufacture confidence; correction can also destroy information; provenance recovery faces a consequential precision–recall tradeoff; and average accuracy can conceal confidently wrong forecasts. These conclusions are currently bounded to synthetic tests.

## What remains unproven

The project has not shown that it reconstructs real evidence ancestry, elicits accurate probabilities or consequence ranges, finds omitted causal explanations, outperforms expert or simpler workflows, or improves decisions in the field. Both library examples are illustrative inputs, not evidence. Action 0.2's unit tests establish implementation properties—not decision efficacy, calibration, completeness, or legitimacy.

## Immediate continuation sequence

1. Run the full validation commands below and repair any failure without weakening tests.
2. Verify Experiment 003A's frozen inputs and result manifest, then read its deviation record and truth gems before changing any claim derived from that study.
3. Review Action 0.2 against its protocol, schema, tests, ADR, and DR-001. Repair semantic or implementation defects without converting qualitative evidence labels into arithmetic.
4. Turn the Experiment 003B design draft into a preregistration and implement its public development generator. Preserve strong baselines, information parity, matched deferral/process cost, component ablations, and protected confirmatory evaluation.
5. Keep Experiment 002B alive as the key external-validity gate for dependence recovery.
6. Prepare—but do not fabricate—a real low-risk pilot packet. A genuine organization, decision owner, affected-party process, baseline, and prospective outcomes are required before calling it a field study.

## Validation commands

Run from this project directory with Python 3.11+:

```powershell
python -m syntruth validate examples/anschluss.json
python -m syntruth decision-validate examples/library-outreach-decision.json
python -m syntruth decide examples/library-outreach-decision.json --output examples/library-outreach-decision-report.md --json examples/library-outreach-decision-results.json
python -m syntruth decision-validate examples/library-outreach-bda.json
python -m syntruth decide examples/library-outreach-bda.json --output examples/library-outreach-bda-report.md --json examples/library-outreach-bda-results.json
python -m syntruth verify experiments/001-dependence/results/MANIFEST.sha256
python -m syntruth verify experiments/002-provenance/results/MANIFEST.sha256
python -m syntruth verify experiments/003a-decision-stress/FROZEN.sha256
python -m syntruth verify experiments/003a-decision-stress/results/MANIFEST.sha256
python -m unittest discover -s tests -v
```

If ordinary `python` is unavailable in the current Codex workspace, use the bundled interpreter path recorded by the host dependency loader.

## Prompt for the next model

> You are continuing Syncretic Epistemic Synthesis at checkpoint 0.6.0. Begin with `AGENTS.md`, `MAINTAINING.md`, and `docs/INDEX.md`, then read `STATUS.md`, `FINDINGS.md`, `HANDOFF.md`, `docs/BOUNDED_DECISION_ASSURANCE.md`, ADR-0002, DR-001, and the Experiment 003B design draft. Run all listed validations before changing claims. Action 0.2 is executable but unvalidated. Your next objective is to critically review its semantics, freeze a falsifiable Experiment 003B preregistration, and implement the public development generator without exposing the protected confirmation evaluator. Keep evidence quality outside consequence arithmetic, preserve Action 0.1 reproduction, and count deferral, elicitation, review, and stakeholder costs. Preserve negative results and never describe simulations, examples, or literature-derived designs as real-world validation. Update tests, status, changelog, findings, and this handoff at the next coherent checkpoint.

## Repository state

The project is an independent Git repository on branch `main`. Remote `origin` points to `https://github.com/gcs2/epistemic.git`. At checkpoint 0.6.0 it has no commits yet and all files are untracked. Repository-local author identity is not configured. Before the initial commit, obtain the intended author name/email, run all validations, inspect `git diff` and `git status`, and describe the research baseline plus 0.2 foundation accurately.
