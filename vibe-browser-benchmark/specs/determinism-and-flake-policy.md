# Determinism and Flake Policy

## Purpose

Determinism and flake policy defines how the benchmark handles nondeterministic
submissions, flaky harness checks, unstable visual diffs, and provider or
network variability.

## Flake Sources

- time, randomness, locale, or filesystem ordering
- network timing and fixture availability
- mutable model provider output
- GUI rendering and screenshot variance
- test isolation failures
- dependency download instability
- resource exhaustion
- race conditions in submitted code

## Rerun Rules

Each check declares allowed rerun count, pass threshold, timeout, and whether a
rerun can change official status. Reruns must be recorded as separate evidence,
not collapsed into a single pass.

## Labels

Use `stable`, `known-flaky`, `environment-flaky`, `submission-flaky`,
`provider-variable`, `quarantined-check`, and `nondeterministic-artifact`.
Unstable labels must appear on public result pages and exports when relevant.

## Quarantine

Quarantined benchmark checks do not block certification until reinstated, but
their removal requires release notes and calibration-suite review.

## Research Basis

pytest flaky-test guidance motivates careful reruns and warnings against
permanent quarantine. Web Platform Tests expectation metadata motivates
recording known intermittent outcomes explicitly.

## QA Pass

Checked against `verification-result-schema.md`, `statistical-validity.md`,
`screenshots-and-golden-artifacts.md`, `provider-drift-tracking.md`, and
`official-result-certification.md`. This spec defines instability policy, not
individual test expectations.
