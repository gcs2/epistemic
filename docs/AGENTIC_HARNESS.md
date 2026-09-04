# Agentic Harness Design

## Objective

The agentic harness should accelerate research while preserving independence, provenance, dissent, and human accountability. Its unit of work is an SES inquiry packet, not an unstructured chat transcript.

## Design axioms

1. **Artifacts over impressions.** Every agent produces structured claims, citations, assumptions, or challenges.
2. **Role separation.** Discovery, advocacy, criticism, synthesis, and audit should not be performed invisibly by one context window.
3. **Measured independence.** Different role prompts are not sufficient evidence of independent judgment, especially when agents share a base model or sources.
4. **No silent weighting.** Agents can recommend priors, likelihoods, and source reliabilities, but these remain labeled proposals until accepted through the inquiry’s governance procedure.
5. **Provenance by default.** Every artifact records agent/model identity, operating instructions, source lineage, time, and parent artifacts.
6. **Reproducible synthesis.** Given an accepted inquiry packet and random seed, the numerical layer must be rerunnable without an LLM.
7. **Dissent preservation.** Minority models and unresolved objections survive into the final report.

## Reference workflow

```text
Question
  -> Framer packet
  -> parallel scouts and stakeholder mappers
  -> provenance/dependence graph
  -> competing model advocates
  -> translator and causal modeler
  -> red team and missing-hypothesis search
  -> methodologist quality review
  -> human checkpoint for accepted inputs
  -> deterministic synthesis engine
  -> auditor reproduction
  -> public report + minority reports + disconfirmation plan
```

## Roles and contracts

### Framer

**Input:** natural-language question.  
**Output:** inquiry contract, claim type, scope, cutoff, horizon, resolution rule, candidate hypotheses, value-bearing choices.  
**Must not:** assign final probabilities or exclude a live rival without explanation.

### Evidence scouts

Use multiple scouts divided by discipline, geography, language, or source type.

**Output per source:** bibliographic identity, stable locator or snapshot, extracted claims, direct quotations within legal limits, method, population, date, conflicts of interest, and proposed dependence group.  
**Must not:** treat search-result ranking as evidentiary weight.

### Provenance mapper

Builds a directed graph from observations through datasets, publications, reviews, and claims. Flags common data ancestry, citation copying, retractions, and circular citation.

### Model advocates

Each advocate receives the common evidence corpus and one hypothesis or theoretical model. It constructs the strongest coherent case, identifies expected observations, and states what would falsify the position.

Advocates should be isolated from one another until initial submissions are complete. A second round allows direct rebuttal.

### Translator

Constructs explicit mappings among disciplinary terms. For every proposed shared latent construct, it records overlap, non-equivalence, measurement implications, and lost context.

### Causal modeler

Creates one or more causal graphs, identifies interventions and confounders, and distinguishes observed associations from assumed mechanisms. For counterfactuals, it tests minimal rewrite and actor coherence.

### Methodologist

Reviews measurement, design, sampling, identification, statistics, archival context, and generalizability. It recommends—but does not secretly apply—reliability adjustments.

### Skeptic/red team

Searches for:

- absent hypotheses;
- evidence that would reverse the ranking;
- strategic deception and publication bias;
- incoherent combinations of premises;
- unmodeled feedback and opponent adaptation;
- duplicated evidence;
- category errors; and
- normative choices disguised as empirical ones.

### Stakeholder steward

Identifies people affected by the inquiry, solicits relevant situated knowledge, flags harmful framing, and distinguishes inclusion from veto over empirical findings.

### Synthesizer

Transforms accepted judgments into the SES protocol. It must provide a change log from every model recommendation to the accepted numerical input.

### Auditor

Runs validation and synthesis from a clean environment, checks source accessibility and hashes, verifies dependence assignments, and attempts to reproduce the report. Ideally it uses a different organization or model family from the producing agents.

## Execution state machine

An inquiry moves through explicit states:

1. `DRAFT`
2. `FRAMED`
3. `EVIDENCE_OPEN`
4. `MODELS_OPEN`
5. `ADVERSARIAL_REVIEW`
6. `INPUTS_PROPOSED`
7. `HUMAN_ACCEPTED`
8. `SYNTHESIZED`
9. `AUDITED`
10. `PUBLISHED`
11. `UPDATED` or `RESOLVED`

Transitions require signed artifacts. High-consequence inquiries may require multiple approvals at `HUMAN_ACCEPTED` and `PUBLISHED`.

## Agent artifact envelope

Every agent output should eventually use an envelope similar to:

```json
{
  "artifact_id": "content-addressed-id",
  "inquiry_id": "stable-inquiry-id",
  "role": "evidence_scout",
  "producer": {
    "system": "provider/model/version",
    "configuration_hash": "...",
    "operator": "institution-or-pseudonym"
  },
  "created_at": "ISO-8601 timestamp",
  "parents": ["artifact-id"],
  "claims": [],
  "sources": [],
  "uncertainties": [],
  "conflicts": [],
  "signature": "optional-verifiable-signature"
}
```

## Orchestration strategies

### Fixed pipeline

Predictable, inexpensive, and easy to audit. Best for early benchmarks. Weak at responding to unexpected inquiry structure.

### Blackboard architecture

Agents post structured artifacts to a shared inquiry graph and claim bounded tasks. Flexible and extensible, but requires strong permissions and loop controls.

### Debate tournament

Pairs advocates and critics, then advances unresolved claims to stronger review. Useful for discriminating arguments, but risks rewarding rhetoric.

### Market or scoring mechanism

Agents allocate confidence or tokens to claims. Potentially useful after calibration data exist; premature markets will quantify uncalibrated imitation.

### Adaptive scientific workflow

The system chooses the next task by expected value of information. This is the most epistemically efficient target architecture but depends on credible probability models and test costs.

**Recommended progression:** fixed pipeline -> blackboard with bounded tasks -> value-of-information scheduling.

## Preventing synthetic monoculture

The harness should calculate a diversity profile based on:

- model family and training lineage where known;
- prompting and tool differences;
- source-corpus overlap;
- shared upstream summaries;
- correlation on blinded benchmark errors;
- institutional and disciplinary origin; and
- language and geographic coverage.

Outputs from agents with highly correlated histories should be placed in the same effective dependence group, even when their prose disagrees.

## Human checkpoints

Human review is most valuable at:

- framing and resolution criteria;
- inclusion of affected perspectives;
- acceptance of source authenticity;
- causal assumptions;
- priors and likelihood elicitation;
- normative tradeoffs;
- publication of high-risk claims; and
- adjudication of appeals.

The goal is not generic “human in the loop.” It is targeted human authority at points where legitimacy, tacit knowledge, and responsibility matter.

## Evaluation suite

Before public deployment, compare variants on:

1. **Resolution accuracy:** Brier/log score on prospective questions.
2. **Calibration:** observed frequency against stated probability.
3. **Dependency resistance:** performance when one source is copied many times.
4. **Misinformation resistance:** planted forged or strategically framed evidence.
5. **Hypothesis recall:** whether the true or best-supported model enters the candidate set.
6. **Minority preservation:** whether a correct dissenting model survives majority pressure.
7. **Causal recovery:** blinded cases with known generating structures.
8. **Value of information:** ability to select discriminating next evidence.
9. **Reproducibility:** agreement between independent runs from the same accepted packet.
10. **Legibility:** whether users can accurately explain why the system reached its result.

## Safety and abuse cases

Special procedures are required for inquiries involving private persons, medical or legal decisions, targeted persuasion, intelligence operations, ongoing violence, biosecurity, or claims likely to produce harassment. Provenance transparency can conflict with confidential-source protection; the protocol must support sealed evidence whose existence and reviewing authority are auditable without public disclosure.

An SES report must never imply that computational synthesis transfers moral or legal responsibility away from decision-makers.

## Minimal implementation plan

1. Store agent artifacts as versioned JSON files.
2. Add source records and SHA-256 snapshots.
3. Add a provenance DAG and dependency-group suggestions.
4. Implement role-specific task adapters behind one provider-neutral interface.
5. Require agents to emit schema-valid proposals.
6. Add a human review diff for accepting or rejecting proposals.
7. Invoke the existing deterministic engine only after acceptance.
8. Run an auditor process from the accepted packet.
9. Evaluate on blinded retrospective cases before autonomous source acquisition.

The current reference CLI implements step 7 and establishes the inquiry format around which the other steps can be built.
