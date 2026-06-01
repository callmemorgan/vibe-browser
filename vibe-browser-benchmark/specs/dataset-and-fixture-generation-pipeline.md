# Dataset and Fixture Generation Pipeline

## Purpose

Dataset and fixture generation pipeline defines how public and hidden fixtures
are created, reviewed, minimized, versioned, and reproduced.

## Fixture Sources

- synthetic pages
- reduced real-world cases
- standards-derived examples
- security scenarios
- accessibility examples
- network failure cases
- rendering goldens
- parser and decoder corpora

## Pipeline Steps

1. Propose capability and oracle.
2. Create fixture and metadata.
3. Review license and privacy.
4. Minimize and normalize input.
5. Generate expected output or oracle.
6. Run calibration submissions.
7. Assign public or hidden visibility.
8. Version and publish or seal.

## Required Metadata

Fixtures record source, license, author, generation command, seed, checksum,
oracle, milestone mapping, visibility, and retirement criteria.

## Reproducibility

Generated fixtures use deterministic seeds and versioned scripts whenever
possible. Non-deterministic generation requires stored outputs and explanation.

## Research Basis

WPT practice motivates metadata, review, and expected behavior for web tests.
FAIR principles motivate reusable metadata and provenance for generated data.

## QA Pass

Checked against `fixture-registry.md`, `task-authoring-and-review.md`,
`ground-truth-oracle-policy.md`, `hidden-test-policy.md`, and
`legal-and-licensing.md`. This spec defines fixture pipeline, not specific
fixtures.
