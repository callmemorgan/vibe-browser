# Public Leaderboard Page

## Purpose

The public leaderboard page ranks official comparable runs while keeping
non-comparable, provisional, failed, and historical runs inspectable without
polluting the official table.

## Default Table

Default to the latest open or locked season, primary track, and official-ranked
runs only. Rank numbers are scoped to the active season, track, target/run mode,
runtime profile, prompt set, and intervention policy.

## Required Columns

- rank
- model and provider
- agent and harness
- track and profile
- target or open-ended mode
- evaluator-confirmed milestone
- evaluator score
- public-check milestone
- cost/time summary
- verification status
- eligibility
- submitted/certified date

## Controls

Controls include season selector, track selector, profile selector, target/run
mode filter, model/provider filter, agent/harness filter, eligibility toggles,
date range, and "show non-comparable." Changing filters must not silently reuse
rank numbers from another comparison group.

## Row Behavior

Rows link to public run pages. Score cells link to evidence. Non-comparable
rows are muted and unranked with visible reason. Pending results show no rank.
Invalid and negative results are visible only when explicitly included.

## Export

Users can export the current view as CSV or JSON with the active filters, season
ID, generated timestamp, and schema version.

## Research Basis

MLCommons motivates fair comparison and reproducible benchmark groupings.
CodeSOTA's public registry pattern motivates source/evidence labels, dated
snapshots, open JSON, and visible correction paths.

## QA Pass

Checked against `leaderboard-ux.md`, `comparison-eligibility-rules.md`,
`result-card.md`, `leaderboard-seasons.md`, and `score-interpretation-guide.md`.
This spec expands the public page contract beyond the starter UX doc.
