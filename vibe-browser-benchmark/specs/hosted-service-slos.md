# Hosted Service SLOs

## Purpose

Hosted service SLOs define reliability targets for public and official
benchmark infrastructure.

## SLO Areas

- public site availability
- leaderboard API availability
- artifact download availability
- submission intake availability
- official run scheduling latency
- verification turnaround
- evaluator queue latency
- data export freshness
- incident communication time

## Exclusions

SLOs may exclude participant provider outages, scheduled maintenance, force
majeure events, third-party registry outages, and self-hosted mirrors. Excluded
events still receive operational notes when they affect public interpretation.

## Reporting

Publish monthly or season-level SLO summaries with target, actual value,
measurement window, exclusions, and incident links.

## Error Budgets

If a service repeatedly misses SLO, maintainers prioritize reliability work
over new features affecting that service.

## Research Basis

Google SRE SLO guidance motivates explicit service objectives, user-visible
measurement, and error-budget tradeoffs. OpenTelemetry motivates reliable
measurement from shared telemetry.

## QA Pass

Checked against `official-runner-observability.md`,
`public-trust-dashboard.md`, `queueing-and-run-scheduling.md`,
`incident-response.md`, and `external-integrations.md`. This spec defines
targets and reporting, not current commitments.
