# Failure Classification

## Purpose

Failure classification gives evaluators, maintainers, and public readers a
shared vocabulary for why a run did not reach a milestone or could not become
official. The classification should make failures analyzable without shaming
participants or hiding infrastructure problems.

## Failure Object

Each failure record includes:

- `failure_id`
- `run_id`
- `scope`: agent, harness, provider, verification, artifact, evaluator,
  infrastructure, security, or benchmark
- `class`: canonical failure class
- `severity`: info, warning, blocking, invalidating, or security-hold
- `first_seen_at`
- `evidence_ids`
- `verification_result_ids`
- `public_summary`
- `private_notes`
- `owner`: participant, maintainer, evaluator, provider, or unknown
- `recoverability`: rerun, reimport, re-evaluate, reclassify, or not recoverable

## Canonical Classes

- `agent-gave-up`
- `agent-looped`
- `timeout`
- `early-stop`
- `invalid-submission`
- `missing-artifact`
- `verification-failure`
- `harness-crash`
- `provider-outage`
- `dependency-outage`
- `tool-permission-failure`
- `dirty-baseline`
- `security-redaction-block`
- `hidden-test-leak`
- `evaluator-disagreement`
- `benchmark-bug-suspected`
- `non-deterministic-result`
- `resource-exhaustion`
- `unsafe-artifact`

## Public Display

Public pages should show the class, severity, affected milestone, and a concise
summary. Private notes may include sensitive logs, hidden-test details, or
maintainer investigation notes and must remain behind access control.

## Analytics

Failure classes feed batch reports, model comparison reports, harness comparison
reports, and public trust dashboards. Counts should be grouped by scope and
season so infrastructure failures do not get mistaken for model capability
failures.

## Research Basis

OWASP logging guidance motivates recording event type, reason, severity,
confidence, and response while avoiding sensitive data in public logs.
OpenTelemetry semantic conventions motivate stable naming for events and
attributes so data can be correlated across tools.

## QA Pass

Checked against `verification-result-schema.md`, `run-state-taxonomy.md`,
`security-and-redaction.md`, `official-result-certification.md`, and future
negative-result reporting. This spec classifies failures; it does not decide
rank or score.
