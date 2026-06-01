# Open-Ended Run Semantics

## Purpose

Open-ended runs ask an agent to get as far as possible through the browser
milestone ladder within a fixed budget. They are different from targeted runs,
where the requested goal is one named milestone.

## Progress Fields

Store three separate progress claims:

- `highest_claimed_milestone`: what the agent says it reached.
- `highest_public_check_milestone`: highest milestone supported by deterministic
  public checks.
- `highest_evaluator_confirmed_milestone`: highest milestone confirmed by
  official review.

Also store `frontier_milestone`, the first milestone where meaningful work
exists but confirmation is incomplete.

## Ranking

Open-ended runs rank only against other open-ended runs with the same season,
profile, wall clock, restart policy, tool capability class, and scoring formula.
They must not be mixed into targeted milestone tables except as exploratory
comparisons with rank suppressed.

## Partial Credit

Partial progress inside the frontier milestone contributes through fractional
rubric scores. A run that reaches M3 with strong tests can outrank a run that
touches M4 superficially, depending on the blended score.

## Agent Stop Behavior

If the agent exits early, the stop/restart policy decides whether to continue.
If continuation is exhausted, the run is scored from existing artifacts and
marked with stop reason, elapsed time, and restart count.

## Public Display

Run detail pages should show a ladder with claimed, public-check, and evaluator
markers. The leaderboard should show evaluator-confirmed progress by default,
with claimed progress only visible in drill-down.

## Research Basis

HELM's multi-metric framing motivates exposing progress, quality, efficiency,
and caveats separately. MLCommons' fair-comparison goals motivate separating
open-ended and targeted profiles.

## QA Pass

Checked against `blended-score.md`, `comparison-eligibility-rules.md`,
`run-state-taxonomy.md`, and final blind-spot restart policy entries. This spec
defines run semantics, not restart mechanics.
