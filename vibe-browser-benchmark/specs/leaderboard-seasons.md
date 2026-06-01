# Leaderboard Seasons

## Purpose

Seasons freeze benchmark conditions so official comparisons remain meaningful
even as prompts, fixtures, scoring, tooling, or public pages evolve.

## Season Record

Each season includes:

- `season_id`
- display name
- benchmark version
- benchmark commit
- prompt set checksum
- scoring formula version
- public and hidden checker versions
- runtime profiles
- allowed tracks
- model/tool identity rules
- intervention and restart policy
- fixture registry version
- release date and archive date
- changelog URL

## Lifecycle

`draft` seasons are editable. `open` seasons accept official submissions.
`locked` seasons stop accepting new official runs but may still process appeals
and corrections. `archived` seasons are read-only except for published
correction records.

## Comparison Rules

Official rank is scoped to a season and track. Cross-season pages may show trend
charts and exploratory comparisons, but they must not present a single rank
without explaining formula, fixture, or profile differences.

## Season Changes

Create a new season when changing hidden checks materially, scoring formulas,
official prompts, runtime profiles, allowed dependency policy, or intervention
rules. Minor copy fixes and UI improvements do not require a new season.

## Research Basis

MLCommons benchmark releases and submission windows motivate explicit benchmark
batches, rule sets, and reproducibility expectations. Semantic versioning
motivates separating breaking, additive, and patch-level changes.

## QA Pass

Checked against `benchmark-card.md`, `comparison-eligibility-rules.md`,
`official-result-certification.md`, and `blended-score-calibration.md`. This
spec owns season lifecycle; it does not define public page layout.
