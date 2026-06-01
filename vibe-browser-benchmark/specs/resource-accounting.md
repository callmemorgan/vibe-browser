# Resource Accounting

## Purpose

Resource accounting defines how the benchmark measures time, tokens, cost,
CPU, memory, disk, and network usage. It lets efficiency analysis use consistent
units without turning efficiency into the primary rank.

## Required Measurements

- wall-clock seconds
- active agent seconds
- verification seconds
- turn count
- tool-call count by type
- input, output, and total tokens
- estimated provider cost
- CPU seconds
- peak memory bytes
- disk bytes written
- network bytes and allowed endpoints when measurable
- artifact bytes retained

## Attribution Rules

Infrastructure setup time, provider outages, retries, and verifier reruns are
recorded separately from productive agent time. Failed runs still report
resources used so negative results can be analyzed honestly.

## Missing Data

Missing measurements use explicit null values with reason codes such as
`provider-unreported`, `runner-unsupported`, `redacted`, or
`measurement-failed`. Do not infer precise costs from incomplete token data.

## Public Display

Efficiency metrics are secondary. Public pages may show cost and time, but rank
remains governed by score and eligibility unless a track explicitly defines a
cost-capped ranking.

## Research Basis

OpenTelemetry semantic conventions motivate consistent metric names, units, and
resource attributes. HELM motivates reporting efficiency alongside capability
and limitations.

## QA Pass

Checked against `cost-and-efficiency-metrics.md`,
`trusted-execution-environment.md`, `result-verification-service.md`,
`model-comparison-report.md`, and `statistical-validity.md`. This spec defines
measurement policy, not provider billing integration.
