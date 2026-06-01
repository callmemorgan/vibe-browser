# Tracks and Divisions

## Purpose

Tracks and divisions define which runs are comparable. They let the benchmark
support different constraints without collapsing every result into one table.

## Core Tracks

- cloud model
- local model
- open-weights
- cost-capped
- time-capped
- single-agent
- multi-agent
- guided
- unguided
- targeted milestone
- open-ended frontier
- endurance

## Division Fields

Each division defines benchmark season, allowed models, allowed harnesses,
runtime profile, intervention policy, dependency policy, time budget, cost
budget, ranking metric, and required evidence.

## Ranking Rules

Runs rank only inside their division and comparison group. Public pages can show
cross-track context, but must not present cross-track ordering as one official
rank.

## Lifecycle

New divisions require governance review, release notes, baseline runs, and
methodology updates. Retired divisions remain visible for historical results.

## Research Basis

MLCommons submission divisions motivate separating comparable, constrained
submissions from more experimental ones. Leaderboard season practice motivates
immutable rule sets for each ranked group.

## QA Pass

Checked against `comparison-eligibility-rules.md`, `leaderboard-seasons.md`,
`multi-agent-and-team-runs.md`, `open-ended-run-semantics.md`, and
`public-leaderboard-page.md`. This spec defines divisions, not the scoring
formula.
