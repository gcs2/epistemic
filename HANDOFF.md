# Cross-Model Handoff

**Checkpoint:** SES 0.7.0 plus BIZ-001 business-initiative documentation
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
- Three completed, hash-manifested synthetic experiments and two exposed 003B development runs.
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

## Commercial initiative continuation

The founder requested a major self-sustaining-business initiative. Read the
[compendium](docs/business/README.md) and [business tracker](docs/business/TRACKER.md).
SES stays the internal method name; outcome-first public language, a service-first
model, and a reporting-workflow offer are proposals, not validated positioning.
The public brand, customer segment, price, operating owners, and budget are unset.

Next commercial action: establish founder access, skills, and time constraints,
then choose a bounded discovery test and private record system. Drafts exist;
no outreach, spending, launch, or research use of customer data is authorized by
the documents. Do not invent leads or mark planned activities complete.
Track commercial outcomes separately from scientific efficacy. Revenue can fund
research only after actual costs, obligations, and an agreed reserve are covered.
Use the business ledger for these tasks, not a duplicate global roadmap.

## Immediate research continuation sequence

Start with the [implementation audit](experiments/003b-bounded-decision-assurance/IMPLEMENTATION_AUDIT.md),
[investigation protocol](docs/INVESTIGATION_PROTOCOL.md) and
[003B interpretation](experiments/003b-bounded-decision-assurance/DEVELOPMENT_INTERPRETATION.md).
Investigation 0.1 is executable; extra lookahead has no established advantage over
one-step planning. Both fail under misleading likelihoods and omitted mechanisms.
The next design target is validation of observation models and then real model
expansion. Do not describe the finite-hypothesis loop as open-world discovery.

1. Run the full validation commands below and repair any failure without weakening tests.
2. Verify Experiment 003A's frozen inputs and result manifest, then read its deviation record and truth gems before changing any claim derived from that study.
3. Preserve the Action 0.2 audit correction: its tail statistics describe expected-score sensitivity. Outcome risk and executable observations live in investigation-0.1.
4. Use the completed 003B development results to design the next falsifiable comparison. Preserve stronger baselines and genuinely independent confirmation for the broader study.
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
python -m syntruth investigation-validate examples/fault-investigation.json
python scripts/check_repository.py
```

If ordinary `python` is unavailable in the current Codex workspace, use the bundled interpreter path recorded by the host dependency loader.

## Prompt for the next model

> Continue SES 0.7.0. Read AGENTS, MAINTAINING, INDEX, STATUS, FINDINGS and this handoff, then the 003B audit and interpretation, investigation protocol, ADR-0003 and DR-001. Verify tests and all manifests. The finite investigation loop is implemented and evaluated on exposed development cases; two-test follow-up reused cases after inspecting the first run. Myopic remains default. Test-model reliability and truly omitted mechanisms are unresolved. The next research design should test whether independent calibration evidence can improve investigation-or-stop decisions, then how new hypotheses enter the model. Preserve the simpler baselines and cost accounting, and avoid presenting finite model discrimination as open-world discovery. Protected confirmation and a real application still require separate work.

## Repository state

Canonical repository: `C:/Users/zephy/Documents/epistemic`, remote
`https://github.com/gcs2/epistemic.git`. On 2026-09-05 its clean local history was
verified to include the 0.7 milestone `f051327`; the previous delivery was applied.
Author identity is configured. This conversation still writes only to its older
workspace, so the business documentation is prepared in an isolated copy and
delivered for import. Verify canonical Git history and remote synchronization
before assuming any new delivery has been applied or pushed. Temporary delivery
and verification directories are not project evidence.
