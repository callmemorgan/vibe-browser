# Leaderboard UX

## Default View

The first screen is a dense table of comparable runs. Default grouping should be:

- Benchmark commit
- Prompt set
- Profile
- Target mode: targeted milestone or open-ended
- Human intervention policy

The UI should default to the latest comparable batch. Older or incompatible runs
remain searchable but are not mixed into the main ranking.

## Table Columns

Required columns:

- Rank
- Model
- Agent tool
- Provider
- Profile
- Target
- Highest evaluator-confirmed milestone
- Highest public-check milestone
- Rubric score
- Verification status
- Stop reason
- Wall-clock used
- Tokens used
- Comparison eligibility
- Submitted at

Optional expanded columns:

- Harness version
- Prompt checksum
- Benchmark input digest
- Cost
- Tool calls
- Human interventions
- Artifact count

## Filters

Filters should be visible and persistent:

- Target: `m1` through `m9`, `open`
- Profile: `smoke-v0`, `sprint-v0`, `standard-v0`, `deep-v0`, `frontier-v0`
- Eligibility: comparable, non-comparable, guided, invalid
- Model/provider
- Agent tool/harness
- Stop reason
- Verification result
- Date range

## Row States

- Comparable: normal row with rank.
- Non-comparable: muted row, no global rank, reason shown inline.
- Invalid: red status, excluded from ranking.
- Pending evaluation: visible but rank withheld.
- Public-check only: badge shows "candidate", not "confirmed".

## Interactions

- Click a row to open run detail.
- Click a score to open rubric evidence.
- Click a milestone badge to open milestone evidence.
- Toggle "show non-comparable" without changing rank numbers.
- Export current table as CSV or JSON.

## Empty States

- No comparable runs: show which filters prevent comparison.
- No evaluator score yet: show public checks and submitted artifacts.
- Missing artifacts: show which required artifact path is absent.
