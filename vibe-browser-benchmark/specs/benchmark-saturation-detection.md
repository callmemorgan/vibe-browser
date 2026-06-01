# Benchmark Saturation Detection

## Purpose

Benchmark saturation detection identifies when Vibe Browser Benchmark is
becoming too easy, too narrow, or no longer useful for frontier comparisons.

## Saturation Signals

- many top runs reach same highest milestone
- hidden-check pass rates cluster near ceiling
- failure diversity collapses
- score uncertainty dominates rank order
- cost-to-score curves flatten
- qualitative differences become minor
- public fixtures are heavily optimized
- benchmark meta-evaluation shows low sensitivity

## Thresholds

Each season defines watch thresholds and action thresholds. Thresholds use
sample count, season age, model diversity, and evaluator confidence.

## Responses

Responses can include new hidden variants, new milestones, harder divisions,
retired tasks, changed scoring curve, successor-season planning, or sunset
review.

## Public Display

Trust dashboards and methodology pages can show saturation status without
revealing hidden-test details.

## Research Basis

HELM frames benchmarks as living evaluations that may need new scenarios and
metrics. Statistical validity guidance motivates monitoring ceiling effects and
score clustering.

## QA Pass

Checked against `benchmark-meta-evaluation.md`,
`benchmark-difficulty-tuning.md`, `leaderboard-seasons.md`,
`score-uncertainty-display.md`, and
`benchmark-sunset-or-succession-plan.md`. This spec defines saturation signals,
not successor task design.
