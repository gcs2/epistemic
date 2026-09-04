# Experiment 003A Deviations

## D1 — H5 implementation corrected after first output inspection

The first full execution completed on 2026-09-04. The initial code marked H5 supported whenever the robustness gate improved either regret or catastrophe exposure. The frozen preregistration imposed a stricter joint condition: improvement in one measure without worsening the other by more than 10% of the baseline-to-declared gap.

Inspection showed that the gate reduced catastrophe exposure but increased regret. The hypothesis evaluator was corrected to apply the frozen 10% allowance. Under that registered criterion H5 is **not supported**. The entire deterministic benchmark is rerun after the correction, and only corrected artifacts are retained as the result set.

This changes result classification, not the generator, configuration, methods, or metric values. The preregistration and configuration hashes remain unchanged.
