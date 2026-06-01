# Search, Discovery, and Compare UX

## Purpose

Search, discovery, and compare UX helps readers find runs, models, reports,
artifacts, seasons, and explanations without losing comparison context.

## Search Scope

- run IDs
- models and providers
- harnesses
- seasons and tracks
- organizations
- failure classes
- milestones
- reports and posts
- public artifacts
- data exports

## Filters

Support season, track, model, harness, official state, comparison group,
milestone, score range, cost range, failure class, organization, and date.
Filters must preserve shareable URLs.

## Compare View

Side-by-side comparison shows metadata, score breakdown, milestone evidence,
cost, timeline summary, diff summary, failures, caveats, and comparability
state. Non-comparable fields are highlighted before any numeric comparison.

## Discovery Surfaces

Model family pages, tag pages, report pages, and artifact links should all
route back to canonical run pages and data exports.

## Research Basis

OpenSearch-style discovery practice motivates structured search metadata and
shareable queries. WCAG guidance motivates keyboard-accessible filters,
headings, and result navigation.

## QA Pass

Checked against `public-leaderboard-page.md`, `model-family-pages.md`,
`artifact-explorer.md`, `chart-library.md`, and `comparison-eligibility-rules.md`.
This spec defines discovery UX, not search-index infrastructure.
