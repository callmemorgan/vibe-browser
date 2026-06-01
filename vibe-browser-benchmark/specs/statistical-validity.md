# Statistical Validity

## Purpose

Statistical validity defines when benchmark claims are supported by enough
repeated evidence. It keeps leaderboards from overstating tiny, noisy, or
non-comparable differences.

## Required Fields

Aggregate result views record sample count, run mode, model identity,
harness identity, seed or run identifier, score distribution, missing data,
excluded runs, confidence method, and tie policy.

## Minimum Practices

- Report sample count for every aggregate.
- Separate best-run claims from average-run claims.
- Show uncertainty intervals when comparing repeated runs.
- Label comparisons with too few samples as exploratory.
- Keep infrastructure failures separate from model variance.
- Avoid significance claims across incompatible seasons or profiles.

## Tie And Close-Call Rules

If uncertainty intervals overlap materially or sample count is below the
season threshold, show `too-close-to-call` instead of forcing a headline
winner. Rank tables may still sort deterministically, but the caveat must be
visible.

## Repeated Runs

Official single-run leaderboards can exist, but statistical reports should use
multiple runs per model/harness/profile when making capability claims beyond a
single certified artifact.

## Research Basis

NIST statistical guidance motivates explicit uncertainty, confidence intervals,
sample size, and experimental design. HELM motivates reporting multiple metrics
and limitations rather than reducing evaluation to one unqualified score.

## QA Pass

Checked against `score-interpretation-guide.md`, `model-comparison-report.md`,
`harness-comparison-report.md`, `longitudinal-trends-page.md`, and
`blended-score-calibration.md`. This spec defines claim validity, not the exact
statistical library implementation.
