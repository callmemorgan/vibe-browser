# Longitudinal Trends Page

## Purpose

The longitudinal trends page shows how benchmark results evolve across seasons,
models, harnesses, and methodology revisions. It helps readers see progress
without mixing incompatible results into one rank table.

## Required Views

- best official score by season and track
- milestone frontier over time
- median and percentile score by cohort
- cost-to-score and time-to-milestone trends
- failure-class distribution by season
- harness and provider coverage over time
- scoring or methodology change annotations
- model-family participation timeline

## Comparability Rules

Every chart declares whether it shows within-season comparable data or
cross-season contextual data. Cross-season charts must mark benchmark-card
changes, formula revisions, fixture changes, and prompt changes.

## Interaction Requirements

Users can filter by track, season, model family, harness, official state, and
run mode. Tooltips show sample count, eligibility state, uncertainty, and links
to underlying reports or exports.

## Interpretation Guidance

The page should explain that trend lines can reflect benchmark changes,
provider changes, harness improvements, participant learning, or model
capability. It should avoid implying a single cause without analysis.

## Research Basis

HELM motivates transparent, multi-metric reporting over time. FAIR and
data-package practices motivate reusable public data behind charts.

## QA Pass

Checked against `leaderboard-seasons.md`, `public-leaderboard-page.md`,
`score-interpretation-guide.md`, `model-comparison-report.md`, and
`public-data-export.md`. This spec defines trends display, not rank
certification.
