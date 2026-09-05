# 003B development run log

1. Read the existing architecture, findings and broad design draft.
2. Recorded IMPLEMENTATION_AUDIT.md and DEVELOPMENT_PROTOCOL.md.
3. Added investigation-0.1, six reference policies, explicit outcome risk and tests.
4. Fourteen targeted tests passed, including an analytic rare-tail case, a
   complementary-test example, budgets, family reuse and impossible observations.
5. Froze protocol, config, source modules, CLI and schema in DEVELOPMENT_FROZEN.sha256.
6. Ran 120 cases x five regimes x six policies with budget three.
7. Identical fixed/random/entropy results exposed the full-menu ordering limitation.
8. Recorded D1 and froze BUDGET2_EXTENSION.md plus a new config in BUDGET2_FROZEN.sha256.
9. Ran the budget-two exploratory extension without changing the original engine.
10. Repeated both complete runs into disposable work directories. Episodes, summary,
    sample traces, report and manifest matched byte-for-byte for each run.
11. All 60 tests passed. Portable checks validated JSON, Markdown links, version
    consistency and eight manifests.

All runs are public development, never protected confirmation. No external APIs
or real-world actions were invoked. Actual outcomes are analytically scored
conditional on sampled true states, with paired pre-sampled test observations.
The exposed 003B design remains a broader unexecuted proposal.

## Historical Git artifact repair

Inspection found nine preexisting generated result files whose working-copy bytes
matched their manifests but Git blobs did not: report.md, summary.json and cells.csv
in Experiments 001, 002 and 003A. Git text normalization had changed CRLF to LF.
Added exact-path -text attributes and restaged original manifested bytes.
No numerical result or historical manifest was changed. The new 003B writer
explicitly uses LF and the final export is checked against all manifests.
