# Maintaining SES Without Losing the Plot

This is the repository's maintenance contract. It applies to human contributors and coding or research agents.

## The three records

SES uses three complementary histories:

1. **Git commits** record every coherent technical change and why it was made.
2. **`CHANGELOG.md`** records release-level changes that alter behavior, evidence, claims, schemas, or user workflow.
3. **Decision records in `docs/decisions/`** explain durable architectural choices and the conditions for reversing them.

Commits do not replace the changelog: a reader should not need to reconstruct scientific meaning from a diff. The changelog does not replace commits: it is curated, not exhaustive.

## Canonical documents

Each question has one authoritative home:

| Question | Canonical file |
|---|---|
| What is this project? | `README.md` |
| Where does something belong? | `docs/INDEX.md` |
| What is true now? | `STATUS.md` |
| What findings are established? | `FINDINGS.md` |
| How should another model continue? | `HANDOFF.md` |
| What changed by release? | `CHANGELOG.md` |
| Why was an architecture chosen? | `docs/decisions/` |
| What is the scientific boundary? | `FOUNDING.md` and the relevant protocol |

Do not create a second status page, roadmap, findings list, or handoff note. Update the canonical file and link to it.

## Placement rules

- `syntruth/`: versioned reference implementation. Preserve legacy engines needed to reproduce published experiments.
- `schema/`: machine contracts. A breaking semantic change gets a new versioned file; never rewrite an old schema in place.
- `docs/`: stable protocols, architecture, decisions, and navigation—not run outputs.
- `experiments/`: one directory per study. Keep proposals, frozen inputs, deviations, results, and manifests visibly distinct.
- `research/`: source-backed literature work and external intake. Search summaries are not findings.
- `examples/`: illustrative inputs and generated outputs. They are never evidence of efficacy.
- `templates/`: blank operational forms.
- `tests/`: behavioral and invariance tests mirroring implementation modules.
- `work/`: disposable intermediate material. Nothing in it may be cited as a result.

## Change classes

### Documentation-only

Update the affected canonical document, check links, and add a changelog entry only if interpretation or workflow changed.

### Backward-compatible behavior

Add tests, update the implementation and examples, document semantics, and add a changelog entry.

### Protocol or schema change

Create a new versioned schema and implementation path. Add an architecture decision, migration notes, tests for both new behavior and legacy reproducibility, examples, changelog, status, index, and handoff updates.

### New experiment

Begin with `DESIGN_DRAFT.md`. Promotion requires a preregistration, frozen configuration, and integrity hash before execution. Results require a run log, deviation record, machine-readable summary, bounded truth gems, and manifest.

### New finding

A finding enters `FINDINGS.md` only when its evidence artifact exists and its boundary is stated. Literature synthesis changes design beliefs; it does not become an SES empirical finding.

## Required change sequence

1. Read `docs/INDEX.md`, `STATUS.md`, `FINDINGS.md`, and `HANDOFF.md`.
2. Classify the change and identify canonical files.
3. Write or update tests before claiming behavior.
4. Implement the smallest coherent vertical slice.
5. Run validation, unit tests, link checks, and relevant manifest checks.
6. Update documentation and generated examples.
7. Update `CHANGELOG.md`, `STATUS.md`, and `HANDOFF.md` when the project checkpoint changes.
8. Inspect `git diff` and `git status`; exclude disposable, secret, or machine-local files.
9. Commit one coherent change with a message that states the outcome, not the activity.

## Commit convention

Use a short conventional prefix:

- `feat:` new behavior or protocol;
- `fix:` corrected behavior;
- `research:` literature, design, or experimental evidence;
- `docs:` documentation without behavior change;
- `test:` tests only;
- `chore:` repository mechanics.

The commit body should name changed semantics, validation performed, and any unresolved boundary. Never rewrite published experimental history to make the project look cleaner.

## Release checklist

- [ ] Version agrees in `pyproject.toml`, `syntruth/__init__.py`, `STATUS.md`, and the changelog.
- [ ] All examples validate under their declared protocol.
- [ ] Unit tests pass from a clean checkout.
- [ ] Relative documentation links resolve.
- [ ] Frozen experiment inputs and completed result manifests verify.
- [ ] New claims cite their evidence artifact and include a boundary.
- [ ] Legacy protocol behavior required by earlier experiments remains reproducible.
- [ ] No example or synthetic result is described as field validation.
- [ ] `HANDOFF.md` gives the next model an executable continuation path.

## Complexity budget

Every new abstraction must remove a documented failure mode, enable a preregistered test, or reduce maintenance cost. If it does none of these, do not add it. Prefer a typed field and explicit limitation over a clever score whose meaning changes across contexts.
