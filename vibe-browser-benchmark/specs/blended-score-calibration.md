# Blended Score Calibration

## Purpose

Calibration decides whether the blended score formula rewards the intended
behavior. It prevents the benchmark from accidentally overvaluing shallow late
milestone touches or undervaluing robust foundations.

## Inputs

Calibration uses:

- fixed calibration submissions for each milestone
- intentionally flawed submissions
- historical official runs
- baseline agents and human/reference runs
- evaluator score distributions
- sensitivity analysis over milestone curves
- public-check vs evaluator-score gaps

## Procedure

1. Score calibration submissions with the current rubric.
2. Compute blended scores under candidate curves: linear, quadratic, cubic, and
   any proposed custom curve.
3. Review rank changes against qualitative expectations.
4. Test sensitivity to evaluator disagreement and single-milestone score shifts.
5. Confirm that late milestones matter more without erasing early correctness.
6. Publish a calibration memo before changing official formula behavior.

## Change Rules

Formula changes are season-level changes. Patch releases may fix arithmetic
bugs if reanalysis is published. New weighting curves, repository-quality
multipliers, or uncertainty displays require either a new season or explicit
retroactive reanalysis.

## Guardrails

Do not tune the formula to make a favorite model or harness win. Do not hide
large rank instability behind a single number. If several runs are too close to
distinguish, use uncertainty labels instead of overprecise ranking.

## Research Basis

HELM motivates multi-metric evaluation and tradeoff visibility. MLCommons
motivates fair and useful measurement. Statistical validity and calibration
practices should keep score changes transparent across seasons.

## QA Pass

Checked against `blended-score.md`, `scoring-and-ranking.md`,
`comparison-eligibility-rules.md`, and future statistical validity/calibration
suite specs. This spec governs formula tuning, not per-run scoring.
