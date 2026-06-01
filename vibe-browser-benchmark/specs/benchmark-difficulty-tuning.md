# Benchmark Difficulty Tuning

## Purpose

Benchmark difficulty tuning defines how maintainers change task difficulty
without destroying comparability or making historical results unreadable.

## Tuning Levers

- milestone criteria
- fixture complexity
- hidden variant coverage
- allowed dependencies
- time and resource profiles
- prompt wording
- scoring weights
- evaluator rubric examples
- required evidence
- WPT and fuzzing scope

## Change Rules

Difficulty changes that can affect ranking require proposal review, calibration
suite replay, baseline reruns, release notes, and either a new season or a
benchmark-card statement explaining compatibility.

## Signals For Change

Consider tuning when too many runs saturate a milestone, no runs make progress,
agents exploit narrow checks, evaluators frequently disagree, or new browser
capabilities become central to the benchmark thesis.

## Historical Results

Old seasons remain visible. Do not rewrite old scores under a harder or easier
task unless a formal reanalysis policy applies.

## Research Basis

MLCommons season and rule-management practice motivates controlled benchmark
updates. Statistical validity practice motivates calibration before interpreting
score-distribution shifts as capability changes.

## QA Pass

Checked against `leaderboard-seasons.md`, `blended-score-calibration.md`,
`calibration-suite.md`, `baseline-agents-and-reference-runs.md`, and
`governance-and-versioning.md`. This spec defines difficulty changes, not the
roadmap priority order.
