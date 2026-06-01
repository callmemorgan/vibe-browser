# Score Interpretation Guide

## Purpose

The score interpretation guide helps readers understand what a score means, what
it does not mean, and how to compare runs without overclaiming.

## Explain The Three Scores

- `claimed_score`: agent self-report; useful for studying self-assessment, not
  ranking.
- `public_check_score`: deterministic public checker score; useful for previews
  and debugging.
- `evaluator_score`: official score used for ranking after review and
  certification.

## Explain Milestone Depth

A higher blended score usually means deeper browser progress, but readers should
inspect the milestone ladder. A robust M4 result can be more useful than a
fragile run that touches M5 superficially.

## Explain Comparability

Only compare ranked runs within the same season, track, profile, target/run
mode, prompt set, tool surface, model identity class, and intervention policy.
Non-comparable runs can still be interesting evidence.

## Explain Uncertainty

The guide should describe evaluator disagreement, repeated-run variance,
provider drift, flaky checks, and too-close-to-call labels. Avoid false
precision when scores differ by less than the uncertainty band.

## Examples

Include examples of official-ranked, public-check candidate, non-comparable
guided run, failed but useful run, and archived stale-season result.

## Research Basis

HELM motivates showing tradeoffs beyond a single accuracy number. Leaderboard
operations research motivates clearer documentation and mitigation of
leaderboard smells that reduce transparency.

## QA Pass

Checked against `blended-score.md`, `blended-score-calibration.md`,
`comparison-eligibility-rules.md`, `public-leaderboard-page.md`, and
`public-run-result-page.md`. This spec defines reader education, not score
calculation.
