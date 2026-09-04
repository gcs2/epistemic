# ADR-0001: Versioned Research Repository and Canonical Documents

**Status:** Accepted  
**Date:** 2026-09-04

## Context

SES combines code, evolving protocols, literature research, generated examples, preregistered experiments, and bounded findings. Without explicit ownership rules, repeated model handoffs can create competing summaries, silently revise experimental history, and confuse design proposals with evidence.

## Decision

Use Git commits as the exhaustive technical history, `CHANGELOG.md` as the curated release history, versioned schemas and engines for breaking semantics, and architecture decision records for durable choices. Assign each project-level question one canonical document as specified in `MAINTAINING.md`.

Published or frozen artifacts are append-only in meaning. Corrections use deviation records and new manifests; they are not silently rewritten.

## Consequences

- Maintenance requires several synchronized files at a release boundary.
- A reader can identify current truth without reconstructing Git history.
- Legacy code remains until its experiments can be reproduced elsewhere.
- Duplicate summaries should be deleted or converted into links to the canonical record.

## Reversal condition

Replace this structure only if a documented repository tool enforces equivalent provenance, canonical ownership, and experiment immutability with lower maintenance cost.
