# Model Family Pages

## Purpose

Model family pages collect benchmark evidence for a model family or provider
without implying that every run is comparable.

## Page Contents

- family name and provider
- known model aliases and snapshots
- best official result by season and track
- all runs with status labels
- drift notes
- cost and latency summaries
- common failure classes
- harness coverage
- public reports and blog posts
- provider disclosures

## Grouping Rules

Do not merge model aliases unless the model identity registry says they are the
same family. Mutable aliases require visible drift and snapshot caveats.

## Charts

Charts show season, track, comparison group, sample count, and official state.
Cross-season charts are contextual unless compatibility is explicitly declared.

## Public Claims

Use scoped language such as "best official result for this family in season X."
Avoid broad provider rankings from a family page alone.

## Research Basis

Model Cards motivate organized model identity, evaluation, and limitation
disclosure. HELM motivates multi-metric model reporting with clear scenario and
prompt context.

## QA Pass

Checked against `model-and-tool-identity.md`, `provider-drift-tracking.md`,
`model-comparison-report.md`, `longitudinal-trends-page.md`, and
`public-leaderboard-page.md`. This spec defines family pages, not provider
marketing pages.
