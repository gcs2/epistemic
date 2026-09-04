# Research Intake

This directory converts external reconnaissance into auditable SES context. AI-generated search summaries are discovery aids, not evidence.

Each intake packet should contain:

- `ANALYSIS.md` — claim map, corrections, novelty assessment, and next searches;
- `source-ledger.json` — one record per cited source with verification and transfer status;
- hashes and locations for the raw inputs when the original text cannot be stored here; and
- a clear statement of which SES claims the packet does and does not address.

## Evidence labels

- **verified-primary** — the original paper or issuing institution was inspected.
- **verified-metadata** — title, authors, venue, and topic were corroborated, but the full claim was not checked in the primary text.
- **secondary-only** — supported only through a review, summary, or institutional synthesis.
- **unverified** — discovered but not yet checked.
- **overstated** — the intake attributes a stronger conclusion than the checked source supports.
- **incorrect** — bibliographic or substantive statement conflicts with the checked record.

“Transfers to SES” is always a separate judgment from “source is correct.” An equation proven for squared-error regression does not automatically validate a socio-technical decision protocol.

Use [`INTAKE_TEMPLATE.md`](INTAKE_TEMPLATE.md) for subsequent batches. One packet should normally cover one SES claim or one tightly coupled source family rather than one browser tab.

## Deep research

- [`deep/001-bounded-robustness/report-source.md`](deep/001-bounded-robustness/report-source.md) — canonical report recommending Bounded Decision Assurance, a dual-loop improvement program, and Experiment 003B.
- [`deep/001-bounded-robustness/SEARCH_PLAN.md`](deep/001-bounded-robustness/SEARCH_PLAN.md) — search ladder, gap matrix, adversarial-query rule, and stopping criteria.
- [`deep/001-bounded-robustness/SEARCH_LOG.md`](deep/001-bounded-robustness/SEARCH_LOG.md) — eight search waves and saturation assessment.
- [`deep/001-bounded-robustness/claim-source-ledger.json`](deep/001-bounded-robustness/claim-source-ledger.json) — claim-to-source and transfer ledger.

The deep-research report is a design input, not an empirical finding. Its architecture becomes evidence only after comparative evaluation.
