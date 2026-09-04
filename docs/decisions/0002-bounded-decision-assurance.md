# ADR-0002: Replace Scalar Action Confidence with Bounded Decision Assurance

**Status:** Accepted for implementation; efficacy unvalidated  
**Date:** 2026-09-04

## Context

Action Protocol 0.1 multiplies every signed consequence score by a confidence value. For negative consequences, this moves uncertain harms toward zero. Experiment 003A demonstrated increased catastrophe exposure under a registered condition. Deep research DR-001 found established alternatives for consequence uncertainty, uncertain preferences, model ambiguity, assurance deficits, and adaptive action.

## Decision

Create Action Protocol 0.2 as a separate, versioned Bounded Decision Assurance engine. It will:

- represent consequences as explicit bounds or distributions;
- keep evidence quality outside consequence arithmetic;
- represent uncertain values as ranges;
- declare the exact scenario and challenge set;
- report a vector of performance and stakeholder outcomes;
- keep unresolved defeaters and coverage deficits visible;
- issue only bounded, categorical case statuses;
- include an adaptive learning contract; and
- preserve Action Protocol 0.1 solely for reproduction and migration comparison.

## Consequences

- Existing 0.1 packets do not silently change meaning.
- 0.2 requires more explicit input and may abstain more often.
- The reference implementation can test sign coherence and information parity.
- No 0.2 status constitutes authorization or a universal robustness guarantee.

## Reversal condition

Supersede or remove Bounded Decision Assurance if protected comparative evaluation shows no advantage over a simpler transparent method after deferral, elicitation, review, and stakeholder costs are included.
