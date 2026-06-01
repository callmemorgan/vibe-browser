# Reproducibility Contract

## Purpose

The reproducibility contract defines the minimum evidence required for another
party to replay, inspect, and understand a benchmark result.

## Required Materials

- submission snapshot with checksums
- benchmark commit and season
- harness version and prompt checksum
- provider, model, and model snapshot metadata
- container image digest or runtime profile
- dependency lockfiles
- run command and verification command
- public fixture versions
- evaluator rubric version
- verification records
- known nondeterminism notes

## Replay Levels

- `artifact-inspectable`: artifacts and metadata can be inspected.
- `public-check-replayable`: public checks replay from snapshot.
- `clean-room-replayable`: official verification service can replay the run.
- `provider-replayable`: provider/model behavior can be approximately rerun.
- `not-replayable`: missing or mutable dependencies block meaningful replay.

## Nondeterminism

Record mutable model aliases, network access, wall-clock dependence, flaky
tests, randomized behavior, and provider incidents. Reproducibility labels must
not hide known nondeterminism.

## Publication

Run pages and data exports show replay level, missing materials, verification
record, and exact commands when public-safe.

## Research Basis

ACM artifact badging motivates separating artifact availability,
functionality, and reproducibility. SLSA provenance concepts motivate recording
source, environment, dependency, and verification facts.

## QA Pass

Checked against `submission-snapshot-format.md`, `result-verification-service.md`,
`public-data-export.md`, `official-result-certification.md`, and
`provider-drift-tracking` backlog scope. This spec defines replay guarantees,
not the provider contract.
