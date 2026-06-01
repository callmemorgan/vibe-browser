# Score Uncertainty Display

## Purpose

Score uncertainty display defines how the UI presents repeated-run variance,
evaluator disagreement, flaky checks, and too-close-to-call situations.

## Uncertainty Sources

- repeated run variance
- evaluator disagreement
- hidden-check instability
- provider drift
- flaky verification
- small sample size
- model alias mutability
- incomplete resource accounting

## Display Elements

Use confidence intervals, sample counts, evaluator confidence, unstable-run
badges, too-close-to-call labels, and explanatory tooltips. Avoid false
precision in rank deltas and decimal-heavy scores.

## Ranking Behavior

Rank tables may use deterministic ordering, but close-call groups must be
visually marked and explained. Public claims should use uncertainty-aware
language.

## Data Requirements

Every displayed uncertainty value links to its calculation method, sample set,
and data export.

## Research Basis

NIST uncertainty guidance motivates intervals and confidence statements rather
than unsupported precision. HELM motivates multi-metric reporting and
transparent limitations.

## QA Pass

Checked against `statistical-validity.md`, `public-leaderboard-page.md`,
`chart-library.md`, `model-comparison-report.md`, and
`public-claims-review.md`. This spec defines display rules, not the statistical
estimator.
