# Official Runner Observability

## Purpose

Official runner observability defines internal telemetry for hosted benchmark
runners, verifiers, fixture services, and artifact exporters.

## Required Signals

- queue depth
- container startup time
- provider latency and error rate
- tool-call failures
- public-check duration
- verification duration
- disk and memory pressure
- network policy denials
- token accounting gaps
- artifact export errors
- redaction scanner failures
- runner crash loops

## Telemetry Requirements

Telemetry uses stable names, units, labels, run IDs, profile IDs, and component
IDs. High-cardinality or sensitive values are controlled and redacted before
public summaries.

## Dashboards

Maintainer dashboards show service health, stuck runs, degraded providers,
artifact backlog, cost anomalies, and incident indicators.

## Public Boundary

Internal observability can feed public trust dashboards, but raw operational
logs remain private unless explicitly redacted.

## Research Basis

OpenTelemetry motivates vendor-neutral traces, metrics, logs, and events.
SRE practice motivates dashboards tied to user-visible reliability and
operational response.

## QA Pass

Checked against `resource-accounting.md`, `hosted-service-slos.md`,
`run-state-taxonomy.md`, `incident-response.md`, and `public-trust-dashboard.md`.
This spec defines runner telemetry, not a dashboard vendor.
