# The engine, customer work, and research

Part of [BIZ-001](README.md). SES is an experimental internal method, not yet a validated commercial decision engine.

## Three separate workstreams

| Workstream | Intended outcome | Evidence that counts |
|---|---|---|
| Customer service | Solve a bounded customer problem | Accepted deliverable, measured outcome, costs, customer feedback |
| Delivery engine | Make repeated work more reliable or economical | Comparable task quality, elapsed time, labor, failures, support burden |
| Scientific SES program | Establish when the method improves inquiry | Appropriately controlled and independently evaluated tests with bounded claims |

A customer may receive value from competent engineering even if SES adds none. A customer's payment does not isolate the method's effect. Record that distinction rather than using business success as scientific validation.

## What exists versus what would need building

Existing code supports evidence synthesis, bounded decision analysis, and a finite investigation loop over supplied hypotheses and likelihoods. See the [implementation audit](../../experiments/003b-bounded-decision-assurance/IMPLEMENTATION_AUDIT.md), [investigation protocol](../INVESTIGATION_PROTOCOL.md), and [findings](../../FINDINGS.md).

It does not establish accurate real-world probability inputs, reliable discovery of omitted explanations, or superiority in field decisions. It is not a production customer portal, CRM, billing system, secure data platform, or autonomous sales/delivery agent.

Initial customer work can use ordinary tools and a human checklist. Use the numerical engine only when its inputs have a defensible interpretation; otherwise document uncertainty qualitatively instead of manufacturing probabilities to fill a schema.

## Improvement loop

1. Observe a real recurring delivery failure or cost with permission.
2. State the proposed mechanism and a falsifiable improvement claim.
3. Compare the simplest remedy with an SES-specific addition.
4. Select a suitable evaluation design and freeze outcomes, costs, and stop criteria before a prospective test.
5. Measure benefit, harm, human effort, tool cost, and support burden—not output fluency alone.
6. Retain null and adverse outcomes. Adopt only justified improvements and record their scope.
7. Validate transfer on fresh cases before claiming a general method improvement.

For the first pilot, baseline and post-change observations can establish local usefulness but generally do not isolate causal contribution. Where feasible, later compare ordinary delivery against an otherwise matched SES-assisted process; account for task differences, learning effects, and unequal resources.

Customer data are not automatically research data. Obtain appropriate permissions and review before research use. Keep protected evaluation cases out of tuning, and do not present exposed customer-development work as independent confirmation.

## Engine backlog admission rule

An engine feature needs a documented repeated bottleneck, a concrete evaluation, or a justified safety/maintenance need. Customer requests enter [the business tracker](TRACKER.md); scientific protocol changes still follow [MAINTAINING.md](../../MAINTAINING.md) and the [research roadmap](../../experiments/PROGRAM_ROADMAP.md).

Initial priorities are records and reliable delivery, not a large autonomous platform. Build intake automation, connectors, reporting, or orchestration only as evidence warrants. Commodity CRM/invoicing tools can be selected later; they need not become custom SES modules.

## Productization gate

Before offering a hosted or reusable product, establish repeat demand, delivery quality, support cost, security requirements, data rights, recovery procedures, model/tool dependencies, and willingness to pay for the product rather than only the founder's service. Assess whether documentation, a template, or a small tool is sufficient.

The desired loop is customer value funding better investigation, with better investigation improving delivery. It remains a hypothesis until both links are measured. More autonomy, more compute, and more complexity are not success measures by themselves.
