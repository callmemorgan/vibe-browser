# Failure Mode Report

## Purpose

Failure mode reports summarize recurring ways runs fail across a season,
study, model cohort, or harness cohort. They turn negative results into public
learning without confusing infrastructure issues with agent capability.

## Required Inputs

- failure classification records
- run states and exit reasons
- verification results
- harness and provider incidents
- evaluator notes and disagreements
- redacted timeline excerpts
- cost and time metrics around failure points

## Required Sections

1. **Scope**: season, track, cohort, date range, and inclusion rules.
2. **Summary counts**: failures by scope, class, severity, and recoverability.
3. **Milestone impact**: which milestones were blocked or invalidated.
4. **Representative patterns**: evidence-backed examples with redacted links.
5. **Infrastructure separation**: provider, harness, fixture, and benchmark
   bugs split from participant output quality.
6. **Mitigations**: harness hardening, docs changes, scorer calibration, or
   participant guidance.
7. **Open questions**: unresolved investigation items and confidence levels.

## Publication Rules

Do not publish hidden-test inputs, raw private logs, secrets, or humiliating
snippets. Public excerpts should be short, contextual, and tied to a concrete
failure class.

## Research Basis

OWASP logging guidance motivates severity, reason, event context, and data
minimization. Leaderboard-operations research motivates transparent handling of
benchmark and infrastructure failures.

## QA Pass

Checked against `failure-classification.md`, `security-and-redaction.md`,
`timeline-and-telemetry-ux.md`, `harness-comparison-report.md`, and
`model-comparison-report.md`. This spec defines failure reporting, not live
incident response.
