# Deep Research Report: From Scalar Confidence to Bounded Decision Assurance

**Research ID:** DR-001-bounded-robustness  
**Cutoff:** 2026-09-04  
**Status:** completed research pass; method proposal not yet validated  
**Audience:** SES designers, researchers, reviewers, and future models  
**Canonical evidence records:** [`SEARCH_PLAN.md`](SEARCH_PLAN.md), [`SEARCH_LOG.md`](SEARCH_LOG.md), [`claim-source-ledger.json`](claim-source-ledger.json)

## Executive answer

The best next move is **architectural reform, not parameter tuning and not a full project reset**.

SES should retain its strongest ideas—provenance, multiple explicit perspectives, adversarial challenge, bounded claims, reversible pilots, and correction—but replace Action Protocol 0.1's decision layer. Multiplying a signed impact by confidence is not merely imperfect calibration. It confuses two different questions:

1. How good or bad would the consequence be if the claim is correct?
2. How uncertain are we about that consequence claim?

For a negative impact, multiplication by a confidence fraction makes the harm numerically smaller. Experiment 003A showed the practical consequence inside its synthetic generator: selective low confidence on harms increased catastrophe exposure. The literature offers formal ways to represent uncertain probabilities, criteria values, weights, and model ambiguity, but this research found no sound basis for using one scalar as a universal discount on signed consequences.

The proposed replacement is **SES Action Protocol 0.2: Bounded Decision Assurance (BDA)**. It does not issue a universal “robust” verdict. It produces a conditional, recomputable case stating:

- which option performs acceptably;
- over which declared models, scenarios, values, and perturbations;
- by which outcome measures;
- which evidence and inference defects remain unresolved;
- which important spaces were not tested;
- what reversible action or information-gathering step is justified now; and
- which signposts trigger review, escalation, or stopping.

This is potentially a useful and publishable synthesis, but it is **not yet a breakthrough finding**. Decision Making under Deep Uncertainty, SMAA, imprecise probability, assurance cases, STPA, value-of-information analysis, and adaptive policy pathways already contain most individual components. A new contribution would have to be demonstrated in the integration and evaluation: lower false assurance under shared omission and evidence failure, better downside and stakeholder outcomes at comparable deferral cost, and better learning over time than strong transparent baselines.

The immediate scientific product should be a preregistered comparative experiment, not another theoretical expansion.

## What the research changed

### 1. “Confidence” is not one variable

The central conceptual correction is to type uncertainty by what it is uncertainty *about*.

| Object | Proper question | Candidate representation | Improper shortcut |
|---|---|---|---|
| State uncertainty | Which state will occur? | Probabilities, intervals, model sets | One global confidence score |
| Consequence uncertainty | What happens under option × state? | Outcome distributions or explicit bounds | Multiply central impact by confidence |
| Value uncertainty | How are outcomes valued and traded off? | Weight ranges, preference models, vetoes | Pretend weights are empirical facts |
| Model uncertainty | Is the causal or scenario model adequate? | Competing structured models and misspecification challenges | More parameter jitter inside one model |
| Evidence quality | Does this source support this input? | Provenance, directness, calibration record, defeaters | Treat source quality as consequence magnitude |
| Decision risk | What losses matter, especially in the tail? | Expected loss, regret, CVaR, constraints, stakeholder shortfall | One “robustness” scalar |
| Process legitimacy | Who can challenge or appeal? | Governance record and affected-party review | A fairness score |

This separation is consistent with several mature lines of work. SMAA-2 explores uncertain criterion values and weight spaces and reports rank acceptability rather than shrinking signed outcomes toward zero ([Lahdelma & Salminen, 2001](https://doi.org/10.1287/opre.49.3.444.11220)). Hill's formal model separates probability judgment, confidence ranking, stakes, and cautiousness ([Hill, 2013](https://doi.org/10.1016/j.geb.2013.09.009)). Nau represents indeterminate probability judgments explicitly rather than pretending they are precise ([Nau, 1989](https://people.duke.edu/~rnau/decision_analysis_with_indeterminate_probabilities.pdf)).

These sources do not prove that BDA is correct. They establish that typed alternatives exist and that SES 0.1's transformation is not forced by decision theory.

### 2. A decision claim and an assurance claim are different arguments

Safety engineering supplies a particularly useful architecture. Hawkins and colleagues separate the primary safety argument from a confidence argument about the adequacy of its inferences, context, and evidence. They explicitly represent “assurance deficits”—gaps that might conceal counterevidence ([Hawkins et al., 2011](https://www-users.york.ac.uk/~rdh2/papers/HawkinsSSS11.pdf)). Goodenough and colleagues use eliminative induction: identify reasons for doubt, then show which have been eliminated and which remain ([CMU SEI, 2012](https://sei.cmu.edu/library/toward-a-theory-of-assurance-case-confidence/)).

The lesson for SES is structural:

- **Decision-performance case:** Given the declared representation, how do the options perform?
- **Epistemic-assurance case:** Why should the representation, evidence, and inferences be adequate for this use?

Combining the two causes evidence quality to silently alter consequence magnitude. Separating them allows a consequence to remain severe while the system says, “we have weak support for its probability or magnitude, and this unresolved uncertainty blocks scaling.”

The transfer must remain cautious. Graydon and Holloway found that most proposed numerical confidence-propagation schemes produced implausible results in counterexamples and had little empirical validation ([Safety Science, 2017](https://doi.org/10.1016/j.ssci.2016.09.014)). A 2025 practitioner study reports limited real-world use of quantitative confidence methods and concerns about lost information, trustworthiness, explanation, and input burden ([Information and Software Technology, 2025](https://doi.org/10.1016/j.infsof.2025.107767)). Assurance activities can also create “probative blindness”: activity that reassures without genuinely testing the claim ([Rae & Alexander, 2017](https://doi.org/10.1016/j.ssci.2016.10.005)).

Therefore BDA must not compute “82% confidence in the whole case.” It should expose support and deficits, then test whether doing so improves decisions.

### 3. Robustness is always relative to a declared challenge set

Robust Decision Making already evaluates strategies over many plausible futures and looks for clusters in which they fail ([Lempert et al., 2006](https://doi.org/10.1287/mnsc.1050.0472)). Research on scenario selection shows that the selected scenario distribution can materially alter robustness values and, in some settings, rankings ([McPhail et al., 2020](https://doi.org/10.1029/2019WR026515)). Formal decision theory likewise distinguishes ambiguity within a model set from the possibility that all featured models are approximations or misspecified ([Cerreia-Vioglio et al., 2022](https://arxiv.org/abs/2008.01071)).

This sharpens SES-GEM-011. The problem is not simply that several models can agree and be wrong. It is that a robustness label often hides its quantifier:

> “This option survives **all challenges in set C**,” not “this option survives all important challenges.”

BDA should render the quantifier visible. A valid output says “conditionally preferred over BDA challenge set v0.2” and lists the generators, boundaries, and unresolved omissions. It never says “robust, full stop.”

### 4. The output should be a policy path, not merely a rank

Dynamic Adaptive Policy Pathways recommends a strategic direction, near-term action, and a monitoring framework with signposts for when adaptation is needed ([Haasnoot et al., 2013](https://doi.org/10.1016/j.gloenvcha.2012.12.006)). Value-of-information analysis asks whether a study's expected decision improvement exceeds its cost before the data are observed ([Jackson et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7612319/)).

SES already gestures toward a learning contract. BDA should make it computationally central. “Defer” is not a safe default unless the system prices the harm of delay. “Pilot” is not automatically reversible unless exposure, lock-in, spillovers, and stopping latency are represented. The actual candidate actions are sequences:

- act now;
- learn first;
- run a bounded pilot;
- run the pilot with a specified monitor and stop rule;
- adopt now but preserve an exit option;
- or decline because no acceptable path exists.

### 5. Recursive improvement needs protection from itself

This is the most important new program-level deduction.

SES has already inspected the results of Experiments 001–003A and is now changing its design. Re-running variants on the same generators no longer provides independent confirmation; the benchmark has entered the development loop. Adaptive-data-analysis research shows that repeatedly inspecting and responding to held-out results can overfit the holdout itself ([Dwork et al., 2015](https://doi.org/10.1126/science.aaa9375)). Machine-learning leaderboard research treats the same adaptive evaluation problem explicitly ([Blum & Hardt, 2015](https://arxiv.org/abs/1502.04585)).

The SES improvement program therefore needs two loops:

```text
open development loop
    failures → redesign → public tests → ablation → debugging
                         |
                         | only frozen candidate releases cross
                         v
protected confirmation loop
    unseen cases/seeds → fixed analysis → release full result, including failure
                         |
                         v
prospective field loop
    pre-decision record → action/pilot → outcome → prequential scoring → update
```

The confirmation evaluator must reveal only the information necessary for a release decision until the candidate is frozen. Once the detailed failures are disclosed, those cases become development data and must be retired or supplemented. For real cases, SES should score forecasts and consequences in the sequence they were issued, before outcomes, following the prequential principle ([Dawid, 1984](https://people.csail.mit.edu/jrennie/trg/papers/dawid-prequential-84.pdf)).

This is not full statistical protection for a qualitative research program. It is a governance control against self-congratulating recursion.

## Proposed architecture: Action Protocol 0.2

### Layer A — inquiry and authority contract

Record the decision owner, affected parties, scope, horizon, baseline, legal/ethical constraints, reversibility, and what the tool is and is not authorized to recommend. The output is decision support, not authorization.

### Layer B — typed uncertainty model

Replace every `impact × confidence` entry with:

- a central consequence estimate, if one is justified;
- an interval, quantiles, samples, or an admissible set;
- the elicitation or estimation method;
- source provenance and dependence group;
- a separate evidence-quality record;
- a separate unresolved-defeater record.

Confidence may determine which uncertainty model is defensible—for example, wider bounds or explicit abstention—but it must not mechanically attenuate a negative sign.

### Layer C — value and constraint model

Represent stakeholder-specific outcomes before aggregation. Explore plausible value weights as a set or distribution. Report criteria whose overlap could double-count an effect. Add non-compensable constraints or veto conditions for harms that cannot simply be offset by benefits elsewhere.

This is necessary because additive multi-attribute models are justified only under relevant independence assumptions ([Keeney, 1971](https://doi.org/10.1287/opre.19.4.875)), and systematic reviews of MCDA applications find inconsistent methods, overlapping criteria, and double-counting risks ([Wahlster et al., 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4495941/)). Equity weights remain contestable moral inputs, not discovered facts.

### Layer D — structural challenge model

Create a declared challenge set from multiple generators:

1. provenance failure: remove or corrupt a source family;
2. parameter challenge: vary probabilities, outcomes, and values within declared bounds;
3. causal challenge: alter an edge, mechanism, or interaction in the model;
4. hazard challenge: enumerate unsafe control actions and causal scenarios using an STPA-like procedure;
5. stakeholder challenge: introduce a burden concentrated on an affected subgroup;
6. temporal challenge: delay, lock-in, threshold crossing, and path dependence;
7. adversarial challenge: incentives to game measures, evidence, triggers, or implementation;
8. open-world prompt: name unrepresented mechanisms and record why each was included, bounded, or left unresolved.

No generator proves completeness. The output includes a `coverage_deficit` ledger instead of a completeness score.

### Layer E — performance vector

For every action path, report at least:

- expected welfare or utility under each declared model;
- rank-acceptability across uncertain values and consequences;
- maximum and distribution of regret;
- lower-tail loss, such as CVaR/expected shortfall where meaningful;
- worst-group and group-specific shortfall;
- probability and severity of constraint violation;
- cost of deferral or monitoring;
- expected value and cost of additional information;
- reversibility and recovery time;
- sensitivity to scenario-set construction; and
- evidence-failure trajectory.

CVaR is a useful optimization statistic for tail loss ([Rockafellar & Uryasev, 2000](https://doi.org/10.21314/JOR.2000.038)); it is not a replacement for distributional analysis or rights constraints.

### Layer F — bounded assurance case

The case contains:

- **claim:** the option or path is acceptable for a named context and horizon;
- **support:** the performance vector and evidence;
- **scope:** the exact model/value/challenge set;
- **defeaters:** rebutting evidence, undercutting evidence, invalid inferences, and missing contexts;
- **residual deficits:** unresolved items and their decision relevance;
- **status:** exploratory, pilot-eligible, conditionally preferred, or scale-review-ready;
- **prohibitions:** explicit conditions under which the label cannot be issued.

The status is categorical and rule-based, not a disguised probability of truth.

### Layer G — adaptive learning contract

Specify what will be measured, by whom, when, and at what cost. Include signposts, action triggers, stopping triggers, appeal, a review date, and the precommitted update rule. Compare the expected value of learning with delay and implementation costs.

### Layer H — audit and anti-overfitting contract

Record whether the case belongs to development, protected confirmation, or prospective field evaluation. Hash preregistrations and configurations. Track every analysis deviation. Retire exposed confirmation cases. Never silently tune a method on a failed “test” and call the rerun confirmatory.

## Reform versus overhaul

### What should survive

- evidence-provenance and dependence-group concepts;
- explicit alternative worldviews;
- bounded language and truth-gem discipline;
- challenge and contested-shell concepts;
- reversible-pilot and correction loop;
- deterministic, inspectable reference code;
- preservation of negative and null results.

### What should be replaced

- signed confidence multiplication;
- a single “robust candidate” gate that hides multiple tradeoffs;
- robustness language without an explicit quantifier over the challenge set;
- binary stakeholder-harm thresholds that may never activate;
- the assumption that more Monte Carlo perturbations repair structural omission;
- validation that repeatedly reuses visible benchmark families as independent evidence.

### Why not a full overhaul now

The literature strongly supports the *separations* SES is trying to make: provenance versus repetition, probabilities versus values, performance versus assurance, and decisions versus learning. Experiment 003A diagnosed a local architectural defect and an underpowered distributional metric; it did not show that provenance, adversarial challenge, or bounded updating are useless.

### What would trigger a full overhaul

A full overhaul should follow if BDA fails any of these tests after reasonable implementation:

1. It cannot outperform a transparent simple baseline on protected confirmation cases.
2. Any improvement disappears when deferral, analyst time, and false alarms are priced.
3. Its structural challenge does not find hidden hazards better than ordinary independent review.
4. Its explanations increase automation bias or suppress legitimate disagreement.
5. Different analysts cannot reproduce the same case status from the same packet.
6. Affected participants find that the process obscures rather than exposes value judgments and appeal paths.

## The next experiment

The detailed design is recorded in [`experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md`](../../../experiments/003b-bounded-decision-assurance/DESIGN_DRAFT.md). The essential test is comparative and adversarial.

### Core question

Does BDA reduce harmful false assurance under signed consequence uncertainty, shared structural omission, and stakeholder conflict—without purchasing the result through excessive deferral or privileged access to the true generator?

### Required baselines

1. raw point expected utility;
2. Action Protocol 0.1 confidence shrinkage;
3. minimax regret over the declared model set;
4. SMAA-like stochastic rank acceptability;
5. RDM-like scenario stress testing;
6. evidence-failure trajectory auditing inspired by the new CFC preprint; and
7. BDA plus component ablations.

A September 2026 preprint independently proposes recomputable evidence-failure trajectories for tabular prediction and calls them audit certificates rather than formal robustness certificates ([Cenacchi et al., 2026](https://arxiv.org/abs/2609.00366)). It is only days old and unreviewed at this cutoff, so its reported performance is provisional. It nevertheless becomes an important novelty boundary and a strong conceptual baseline: SES cannot claim that evidence-removal trajectories are new.

### Outcome family

No single outcome decides the study. The preregistration must include true expected welfare, regret, CVaR, worst-group shortfall, constraint violations, harmful-certification rate, deferral cost, structural-hazard recall and false-positive rate, calibration of consequence intervals, and net value of information.

### Decisive falsifier

BDA fails as a general improvement if it does not beat the strongest simple baseline on protected cases at matched deferral or intervention cost. Beating the known-defective 0.1 rule is not enough.

## What could be genuinely novel

The research sharply narrows the novelty claim.

### Low novelty

- weighted averaging of expert or model positions;
- robustness across scenarios;
- imprecise probabilities or uncertain weights;
- confidence arguments and defeater lists;
- evidence-removal stress tests;
- reversible pilots and monitoring triggers individually.

### Moderate, testable novelty candidates

1. **False-assurance rate as a primary decision-system metric:** how often a system grants a favorable bounded status when the selected path is materially worse under hidden but generator-valid structure.
2. **Typed uncertainty contract:** one machine-readable packet that prevents consequence, evidence, value, model, and process uncertainty from being numerically collapsed.
3. **Scenario-set sensitivity plus coverage-deficit reporting:** the robustness result and the uncertainty about the challenge set appear together.
4. **Decision-plus-assurance-plus-learning integration:** the same audit object links conditional performance to unresolved defeaters, a reversible action path, and precommitted triggers.
5. **Dual-loop epistemic improvement:** SES treats its own benchmark adaptivity as a first-class threat and protects confirmation from its design loop.

### High-impact claim, if eventually demonstrated

> An auditable, typed, bounded-assurance workflow can reduce harmful false certainty and improve real decision learning across domains at acceptable cognitive and institutional cost.

Nothing in the current evidence establishes that claim. It is the program's proper north star because it is consequential, measurable, and falsifiable.

## Practical value

The most plausible near-term value is not solving civilization-scale disputes. It is helping a team avoid recognizable failure modes in low-risk but real decisions:

- treating weak evidence of harm as evidence of small harm;
- declaring robustness over a narrow scenario set;
- double-counting overlapping benefits;
- hiding who bears the downside;
- defaulting to delay without pricing delay;
- piloting without a usable stop trigger;
- and declaring methodological improvement after tuning on the same tests.

The first real pilot should be a reversible organizational decision with weeks-to-months feedback, meaningful but non-coercive consequences, an existing comparison process, and affected people who can challenge the model. Examples include information-format choice, voluntary outreach scheduling, or research-resource allocation. It should not begin in diagnosis, criminal justice, military targeting, benefits eligibility, or other rights-affecting domains.

Human factors are part of the intervention. A systematic review found evidence that decision support can induce commission and omission errors, including users abandoning correct judgments for bad automated advice ([Goddard et al., 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/)). BDA should therefore present information and contestable rationale before a recommendation where possible, capture pre-advice judgments, and measure both appropriate acceptance and appropriate rejection.

## Research program from here

### Phase 1 — freeze the architecture, not the conclusions

- Convert this proposal into schema 0.2 and a minimal reference implementation.
- Keep uncertainty types explicit; do not invent default distributions from confidence labels.
- Build scenario-generation modules as separable challengers.
- Run unit tests for sign coherence, monotonicity, dominance, and constraint handling.

### Phase 2 — public development benchmark

- Finalize and freeze Experiment 003B before executing confirmatory hypotheses.
- Use a public development generator to debug implementation and tune no more than declared hyperparameters.
- Report ablations so any benefit can be attributed to a layer rather than the whole package.

### Phase 3 — protected synthetic confirmation

- Commission an independently specified generator family or sealed seeds and structural mutations.
- Freeze BDA before evaluating it.
- Reveal the full confirmation results once, retain failures, and retire the cases into the development suite.

### Phase 4 — shadow evaluation on historical decisions

- Reconstruct decisions using only information available at each historical cutoff.
- Blind consequence adjudication where possible.
- Compare BDA with documented actual practice and simpler baselines.
- Treat archival selection and hindsight leakage as central threats.

### Phase 5 — prospective low-risk field pilot

- Record the baseline decision process before introducing SES.
- Randomize or stagger use where feasible.
- Measure decision quality, process cost, user understanding, contestability, subgroup outcomes, trigger performance, and correction speed.
- Publish negative and null results.

## Frontier search plan

The next search pass should no longer be broad. It should be organized around experiment-threatening unknowns:

1. **Calibration mapping:** What elicitation methods reliably convert expert ranges or quantiles into calibrated consequence distributions? Search for prospective scoring, not only elicitation preference.
2. **Scenario-generator validation:** How can hazard- or scenario-discovery recall be measured when the universe of hazards is unknown? Look for seeded-defect studies, inter-team overlap, and accident backtesting.
3. **Assurance-case efficacy:** Do assurance or defeater methods improve detection and decisions enough to justify their cost? Prioritize controlled or historical comparisons.
4. **Matched-deferral comparison:** How should selective decision methods be compared at equal abstention, delay, or review budgets?
5. **Non-compensable harm:** Compare veto/outranking methods, explicit constraints, distributional welfare, and rights-based review without pretending they are interchangeable.
6. **Adaptive trigger failure:** Find evidence on noisy signposts, trigger delay, policy lock-in, and monitoring gaming.
7. **Evaluator protection:** Translate adaptive holdout ideas into mixed quantitative/qualitative research governance without claiming unavailable formal guarantees.
8. **Human-system performance:** Test whether a bounded assurance display improves calibrated reliance or merely adds complexity and authority cues.

Detailed query construction and stopping rules are in [`SEARCH_PLAN.md`](SEARCH_PLAN.md). Future searches should explicitly include negative-result terms and should compare BDA to named methods, not to vague “traditional decision making.”

## Bottom line

The research does not justify announcing a new universal theory of truth. It does justify a sharper and more consequential research program.

The core “truth gem” is:

> **Uncertainty should constrain claims and actions according to what is uncertain; it should not be used as a universal solvent that washes magnitude, evidence quality, model coverage, values, and legitimacy into one number.**

The core engineering principle is:

> **A robust-looking decision is only as defensible as its declared challenge set, unresolved deficits, and ability to learn before irreversible harm.**

The core recursive-improvement principle is:

> **Once a system learns from an evaluation, that evaluation is training data; independent confirmation must move elsewhere.**

If SES can operationalize those three principles more cheaply, transparently, and effectively than existing methods, then it could become academically and practically significant. The next experiment is designed to let reality say no.
