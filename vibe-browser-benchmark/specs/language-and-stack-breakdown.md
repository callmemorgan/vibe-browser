# Language and Stack Breakdown

## Purpose

Language and stack breakdown analyzes which implementation choices appear in
submissions and how those choices correlate with progress, failures, cost, and
maintainability.

## Captured Dimensions

- primary programming language
- UI toolkit
- parser and URL libraries
- networking and TLS libraries
- JavaScript runtime or interpreter
- rendering backend
- storage layer
- test framework
- dependency count and restricted dependency flags
- package manager and lockfile status

## Analysis Views

Reports show stack distribution by season, milestone reach by stack, failure
classes by stack, dependency-policy outcomes, artifact size, verification time,
and notable qualitative patterns.

## Claim Boundaries

Stack analysis is observational. It must not imply that a language or toolkit
caused better results without controlling for model, harness, track, and sample
size.

## Public Display

Run pages show compact stack metadata. Aggregate stack charts use only
redaction-approved dependency data and include sample counts.

## Research Basis

OpenTelemetry resource conventions motivate consistent environment and
technology attributes. Statistical validity guidance motivates cautious
interpretation of observational subgroup comparisons.

## QA Pass

Checked against `allowed-dependency-policy.md`, `public-data-export.md`,
`model-comparison-report.md`, `failure-mode-report.md`, and
`statistical-validity.md`. This spec defines analysis categories, not allowed
dependency decisions.
