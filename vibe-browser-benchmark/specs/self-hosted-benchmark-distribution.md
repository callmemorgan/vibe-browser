# Self-Hosted Benchmark Distribution

## Purpose

Self-hosted benchmark distribution defines how outside users can run a local
mirror for experimentation, teaching, or private evaluation.

## Distribution Contents

- Docker Compose or equivalent local setup
- sample data
- public fixture server
- public checker
- seed runs
- local-only leaderboard
- documentation
- offline mode instructions
- export and import examples

## Officialness Boundary

Self-hosted results are not official by default. Public docs must explain which
additional artifacts, verification, and evaluator review are required for
official submission.

## Configuration

Local mirrors use public fixtures only unless the operator is part of an
approved hidden-test program. Configuration files must avoid embedding secrets.

## Support

Self-hosting support covers installation, known limitations, and data export.
Maintainers do not guarantee equivalence to official hosted infrastructure.

## Research Basis

MLCommons reproducibility practice motivates runnable benchmark packages and
clear official-submission boundaries. FAIR principles motivate reusable public
data and tooling.

## QA Pass

Checked against `submission-guide.md`, `public-milestone-checker.md`,
`network-and-fixture-serving.md`, `public-data-export.md`, and
`official-result-certification.md`. This spec defines local distribution, not
official hosted operations.
