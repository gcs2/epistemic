# ADR-0003: Executable investigation as a separate finite protocol

Status: accepted for development; efficacy and novelty unvalidated.

The BDA proposal requires observable challenges and adaptive learning. The current
engine records these without executing them. Add investigation-0.1 as an explicit
finite model with budget, test likelihoods, source families, terminal outcome
distributions, stakeholder weights and constraints.

Use established one-step and finite lookahead value-of-information policies as
transparent references. Select between investigation and stopping; record the
prediction, observation, posterior and cost at every step. Preserve BDA 0.2
arithmetic; document its expected-score sensitivity semantics. Exact discrete
outcome tails in the new engine use fractional probability mass at the cutoff.

This scoped model cannot discover absent hypotheses. Tests with absent mechanisms
must retain failure. Full BDA integration, real likelihood estimation, elicited
values, general dependence, and real-world investigations remain later work.

Prefer myopic planning unless development comparisons justify extra computation.
Further planning depth is reversible; exposed evaluations are never confirmation.

