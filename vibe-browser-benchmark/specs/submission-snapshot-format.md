# Submission Snapshot Format

## Purpose

The submission snapshot is the portable bundle used to inspect, verify, publish,
and reproduce a benchmark run.

## Required Layout

```text
run-<run_id>/
  manifest.json
  summary.json
  turn-metrics.json
  version-info.json
  participant.diff
  participant-git-status.txt
  participant-untracked-files.zlist
  participant-untracked-files.tar
  submission/
  verification/
  evidence/
  redaction-report.json
```

`submission/` contains the generated project files needed to run the artifact
without benchmark-private logs. `participant.diff` captures tracked changes
against the clean benchmark baseline. The untracked tarball captures generated
files not represented in the diff.

## Manifest Fields

`manifest.json` includes run identity, benchmark commit, target, profile,
provider, model, agent, harness version, Docker image digest, wall clock limit,
tool capability manifest hash, artifact checksums, and export timestamp.

## Replay Contract

The snapshot must include commands for public verification from a clean
environment. If replay depends on unavailable provider state, mark the result as
not fully reproducible and explain which components remain replayable.

## Redaction

Snapshots are private until redaction completes. Public snapshots must remove
secrets, local usernames where feasible, private provider account identifiers,
hidden-test clues, and unsafe executable artifacts that are not needed for
verification.

## Research Basis

SWE-bench Verified motivates containerized evaluation for coding-agent tasks,
SLSA motivates provenance and checksums (`https://slsa.dev/spec/latest/`), and
FAIR principles motivate reusable, well-described digital artifacts.

## QA Pass

Checked against the current Docker harness artifacts (`summary.json`,
`turn-metrics.json`, `version-info.json`, participant diff/status files, and
`submission/` export) plus the evidence and certification specs. This document
matches existing harness direction rather than inventing an incompatible bundle.
