# Experiment 002A Truth Gems

These findings concern a generated provenance world. They become claims about real knowledge systems only after adjudicated real-corpus testing.

## SES-GEM-006 — Provenance recovery is a precision–recall problem

Finding more true relationships is not enough. The hybrid method recovered 86.7% of true within-family relationships, compared with 40.4% for citation-only recovery, but its precision fell to 61.2% because topical similarity sometimes joined independent families. Its overall Brier loss was therefore 0.08770, compared with 0.07977 for the less complete citation method.

**Boundary:** this ordering follows the registered generator, Jaccard rule, and transformation grid. It is not a universal claim that citations dominate text.

## SES-GEM-007 — False mergers can be worse than false splits

Citation recovery missed many dependencies but never falsely merged independent roots. It still improved Brier loss over treating every document as independent. In contrast, high-contamination text and hybrid recovery merged unrelated families so frequently that hybrid Brier reached 0.1069 in the exploratory high-contamination stratum, worse than the 0.0886 all-independent baseline.

**Boundary:** the relative cost depends on the downstream decision and loss function. This benchmark makes an erroneous merger remove an independent evidence contribution.

## SES-GEM-008 — Combining weak signals can amplify their failure modes

Hybrid graph recovery was guaranteed to have at least as much pairwise recall as either citation or text recovery. That did not guarantee better truth estimation. Connected-component closure allowed a small number of false text edges to merge entire otherwise-correct citation components.

**Boundary:** this is a failure of unconditional edge union and transitive closure, not evidence against all hybrid inference. Probabilistic edges, temporal constraints, and bridge-edge audits may avoid it.

## SES-GEM-009 — Context determines whether hybrid recovery helps

In a post-run, explicitly exploratory stratification, hybrid recovery had perfect precision and Brier 0.0685 under low topical contamination, compared with 0.0866 for all-independent synthesis and 0.0626 for the oracle. Under high contamination, precision fell to 22.5% and hybrid performance reversed.

**Boundary:** this condition was registered but this cross-stratum contrast was not a confirmatory hypothesis. It is a candidate threshold finding requiring preregistered replication.

## SES-GEM-010 — Real-world transfer remains untested

Experiment 002A shows that source-family recovery can help and can backfire. It does not show whether real citations, quotations, metadata, semantic similarity, authorship, time, and institutional context are sufficient to keep false mergers within a useful range.

This ignorance gem defines Experiment 002B: recover adjudicated real source ancestry and measure whether the recovered structure improves downstream synthesis.
