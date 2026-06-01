# Reference Implementation Policy

## Purpose

Reference implementation policy defines whether maintainers provide example
browser code and how those examples avoid contaminating scored submissions.

## Allowed Examples

- minimal harness smoke submission
- intentionally incomplete shell
- public fixture client
- verifier replay example
- calibration artifacts with limited scope
- documentation snippets that explain interfaces

## Restricted Examples

Maintainers should not publish complete solutions for current scored
milestones unless the season is archived or the implementation is explicitly
excluded from scored comparisons.

## Contamination Controls

Reference code is labeled with version, intended use, excluded seasons if
needed, and known overlap with milestone requirements. Runs derived from
reference code must disclose that relationship.

## Evaluator Use

Evaluators may use private reference artifacts for calibration. Private
references must not be exposed in public checker feedback or agent-visible
documentation.

## Research Basis

Benchmark contamination research motivates limiting public solution leakage.
ACM artifact practice motivates keeping reference artifacts inspectable when
they support published claims.

## QA Pass

Checked against `calibration-suite.md`, `benchmark-contamination-policy.md`,
`anti-overfitting-and-anti-gaming.md`, `hidden-test-policy.md`, and
`submission-guide.md`. This spec defines example-code boundaries, not a
specific implementation.
