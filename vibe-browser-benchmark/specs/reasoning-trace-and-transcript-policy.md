# Reasoning Trace and Transcript Policy

## Purpose

Reasoning trace and transcript policy defines what agent conversation,
tool-call, and provider metadata is stored, redacted, summarized, or published.

## Transcript Classes

- user prompt
- system or harness prompt
- assistant visible response
- tool call
- tool output
- public timeline event
- provider metadata
- private reasoning if supplied by provider
- evaluator notes
- hidden-check feedback

## Storage Rules

Store tool calls, tool outputs, visible assistant messages, prompts, and
timeline events when allowed by provider and policy. Do not publish private
reasoning or hidden-check details. Sensitive outputs enter redaction review.

## Public Derivatives

Public pages may show summaries, timestamps, tool names, changed files, and
redacted excerpts. They should not imply access to full private reasoning when
only derived timeline data exists.

## Retention

Retention varies by transcript class. Private reasoning and sensitive logs have
shorter retention and stricter access than public result cards.

## Research Basis

OWASP logging guidance motivates sensitive-data minimization and access control.
OpenTelemetry event and log conventions motivate structured public derivatives
without exposing raw private content.

## QA Pass

Checked against `timeline-and-telemetry-ux.md`, `security-and-redaction.md`,
`privacy-review.md`, `artifact-retention-policy.md`, and
`public-run-result-page.md`. This spec defines transcript handling, not model
provider contracts.
