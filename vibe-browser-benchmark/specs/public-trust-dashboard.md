# Public Trust Dashboard

## Purpose

The public trust dashboard shows benchmark health indicators so readers can
judge whether the leaderboard process itself is functioning.

## Dashboard Metrics

- certified result count by season
- provisional and rejected counts
- replication rate
- evaluator backlog
- median evaluation latency
- open appeals
- recent corrections
- recent incidents
- hidden-test rotation age
- calibration-suite status
- baseline rerun status
- data export freshness
- maintainer conflict disclosures

## Display Rules

Metrics use time windows, definitions, and links to source records. Security or
privacy-sensitive details are summarized without exposing private data.

## Health States

Use `healthy`, `watch`, `degraded`, and `paused` for benchmark process health.
State changes require an audit note and public explanation.

## Interpretation

The dashboard explains that process health is not model quality. It measures
whether the benchmark's publication and review machinery is trustworthy.

## Research Basis

NIST AI RMF motivates transparency, monitoring, and accountability for AI
evaluation systems. SRE practice motivates visible service health and incident
context.

## QA Pass

Checked against `benchmark-meta-evaluation.md`, `incident-response.md`,
`appeals-and-corrections.md`, `evaluator-calibration.md`, and
`public-homepage.md`. This spec defines public trust metrics, not internal
observability dashboards.
