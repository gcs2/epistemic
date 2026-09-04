# Intake 001 — Shared omission and false consensus

**Received:** 2026-09-04  
**Input type:** two Google AI Mode syntheses supplied by the project owner  
**Primary SES target:** SES-GEM-011  
**Secondary target:** broader novelty of dependence-aware, open-world robustness  
**Does not directly address:** SES-GEM-012's signed-confidence mechanism

## Raw-input record

The full pasted text remains in the Codex attachment store and is not treated as a citable source.

| Input | SHA-256 |
|---|---|
| “Agreement among multiple models or experts…” | `60549B9E41882415D508D10FCCAE1DB5D983EFEA67C07B732D367C5303DBF964` |
| “To precisely map this problem space…” | `561B2B09C7196384B20D6DF842554FB9BA4F6FF298B7D5F9127578B7443D9840` |

## Bottom line

SES-GEM-011 is **not novel as a standalone idea**. Multiple mature literatures already show that redundancy helps only under suitable diversity or independence, common causes defeat redundant safety systems, explicit representations encourage omission neglect, and a decision-maker's awareness can expand beyond a previously represented state space.

What may remain distinctive is the operational synthesis:

1. map evidentiary ancestry before aggregating model opinions;
2. distinguish within-model parameter sensitivity from structural scenario coverage;
3. measure **false certification**, not merely prediction error;
4. require an explicit omitted-state challenge before a decision receives a robustness label; and
5. connect the label to a reversible pilot and subsequent model correction.

That is a candidate systems contribution. It has not yet been shown superior to established Decision Making under Deep Uncertainty (DMDU), exploratory modeling, structured analytic techniques, or ordinary risk governance.

## Corrected claim map

| Intake claim | Assessment | Correction or transfer boundary |
|---|---|---|
| Ensemble error equals average member error minus ambiguity. | Supported within its mathematical setting. | Krogh–Vedelsby concerns weighted ensembles for continuous-valued prediction under squared error. It is not an unconditional theorem about expert panels or arbitrary DSS outputs. |
| Shared blind spots force ensemble ambiguity to zero. | Overstated. | Identical predictions imply zero ambiguity. A shared omitted cause can coexist with substantial disagreement on represented variables. |
| Common-cause failure limits gains from redundant components. | Supported analogy. | Reliability models provide a powerful structural analogy, but model-output error is not automatically a component failure rate. A translation model is required. |
| Reverse Bayesianism addresses discovery of previously unmodeled states. | Supported, with bibliographic correction. | The 2013 paper is in the *American Economic Review*, not *Econometrica*, and is titled “A Choice-Based Theory of Growing Awareness.” It does not by itself mandate a catch-all parameter for every DSS. |
| Algorithmic monoculture can reduce social welfare. | Supported within the paper's ranking-market model. | Kleinberg–Raghavan study shared algorithmic rankings across decision makers. Transfer to same-base LLM critics is plausible but not established by that paper. |
| Pruned fault trees cause probability omission even with an “other” category. | Strongly supported. | This is one of the closest behavioral predecessors to SES's omitted-state concern. The paper concerns judged failure probabilities under alternative problem representations. |
| Condorcet-style ensemble improvement is “fundamentally incompatible with reality.” | Incorrectly framed. | It is a conditional mathematical result. Violating its assumptions limits applicability; it does not make the theorem contradictory to reality. |
| Probabilities summing to one over a state space is false in an open world. | Incorrectly framed. | Probability normalization remains coherent relative to a specified event space. The problem is whether the representation is adequate, not whether probability axioms are false. |
| Dempster–Shafer belief functions are the required remedy. | Unsupported prescription. | They are one possible formalism. Imprecise probabilities, model sets, adaptive pathways, scenario discovery, interval consequences, and explicit abstention are alternatives. Comparative evidence is needed. |
| Majority voting should penalize feature-attribution correlation. | Plausible design hypothesis. | Output-error dependence, data ancestry, model family, feature reliance, and causal assumptions are different objects. Feature attribution alone may be unstable or incomplete. |

## Verified antecedents

### Ensemble diversity

Krogh and Vedelsby's ambiguity decomposition formalizes why disagreement among regression ensemble members can reduce squared error. The original paper itself states that no information is gained from a million identical networks. This strongly precedes the generic “agreement is not independent evidence” idea, but does not address omitted states or decision certification directly.

Primary record: [Neural Network Ensembles, Cross Validation, and Active Learning](https://papers.nips.cc/paper_files/paper/1994/hash/b8c37e33defde51cf91e1e03e51657da-Abstract.html).

### Common-cause failure

Nuclear reliability practice explicitly models failures that defeat redundancy or diversity, including beta-factor approaches. This is a mature engineering antecedent for dependence-aware ensembles. The specific claim that redundancy improves “if and only if beta equals zero” is too absolute; exact behavior depends on architecture and reliability model.

Institutional record: [U.S. NRC, NUREG-2225](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr2225/index).

### Growing awareness

Karni and Vierø axiomatize belief revision as awareness expands and previously unavailable acts or states enter the decision space. This is a direct theoretical neighbor of open-world scenario discovery, although it is not an engineering procedure for generating missing hypotheses.

Primary record: [“Reverse Bayesianism”: A Choice-Based Theory of Growing Awareness](https://www.aeaweb.org/articles?id=10.1257%2Faer.103.7.2790).

### Algorithmic monoculture

Kleinberg and Raghavan show conditions in which multiple decision makers' adoption of a common, individually more accurate ranking algorithm reduces collective welfare. Their conclusion is explicitly conditional: monoculture does not always harm outcomes.

Primary record: [Algorithmic Monoculture and Social Welfare](https://pmc.ncbi.nlm.nih.gov/articles/PMC8179131/).

### Fault-tree omission

Fischhoff, Slovic, and Lichtenstein found that pruning branches changed judged failure probabilities and that an “all other problems” branch did not fully compensate for omitted possibilities. This offers direct behavioral support for the idea that a detailed visible scenario list can create unjustified completeness.

Primary text: [Fault Trees: Sensitivity of Estimated Failure Probabilities to Problem Representation](https://gwern.net/doc/statistics/prediction/1978-fischhoff.pdf).

### Deep uncertainty

DMDU already treats situations in which probabilities or causal relationships are unknown or disputed and uses scenarios, exploratory models, adaptive pathways, and robustness criteria. SES should compare itself against this family rather than imply that parameter sensitivity versus structural uncertainty is a new distinction.

Institutional synthesis: [RAND, Decisionmaking Under Deep Uncertainty](https://www.rand.org/content/dam/rand/pubs/research_reports/RR2700/RR2735/RAND_RR2735.pdf).

## Novelty classification for SES-GEM-011

- **Mechanism novelty:** low. Shared dependence and representation failure are well established.
- **Cross-disciplinary synthesis novelty:** moderate candidate. The combination is coherent, but many DMDU and risk-analysis programs are already interdisciplinary.
- **Metric novelty:** moderate candidate. “Certified non-oracle” or false-certification rate under common scenario omission may be a useful evaluation target; a formal literature search is still required.
- **Workflow novelty:** moderate candidate. Joining provenance mapping, model-space challenge, robustness labeling, reversible action, and correction may be distinctive as one auditable protocol.
- **Empirical novelty:** low so far. Experiment 003A is synthetic and demonstrates a mechanism deliberately placed in its generator.

## Consequences for project language

Prefer:

> Experiment 003A operationalizes a cross-disciplinary common-mode insight: agreement is conditional on shared representation. Its possible contribution is a measurable false-certification test and an auditable decision-learning workflow.

Avoid:

> SES discovered that model consensus can be wrong.

## Next verification tasks

1. Search the formal DMDU and robust-optimization literature for the phrases “false robustness,” “scenario set adequacy,” “scenario discovery,” and “model-set misspecification.”
2. Find empirical measurements of correlated LLM errors using primary benchmark papers; do not retain the pasted “over 60%” number without a verified population, task set, metric, and paper.
3. Compare SES false certification with selective classification, robustness certificates, distribution shift, and conformal risk-control failure under model misspecification.
4. Treat SES-GEM-012 separately. Neither pasted result establishes prior art—or novelty—for multiplying signed impacts by confidence.
5. Add DMDU and fault-tree baselines to Experiment 003B rather than comparing only SES-internal rules.
