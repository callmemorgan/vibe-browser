# Negative Results and Failed Runs

## Purpose

Negative results and failed runs define how unsuccessful attempts can be
published usefully without polluting official ranks or shaming participants.

## Publishable Failure Types

- invalid submission
- verifier failure
- agent loop or early stop
- timeout
- model refusal
- non-runnable artifact
- missing evidence
- dependency failure
- benchmark or infrastructure failure
- security hold summary

## Public Requirements

Published failures show official state, failure class, affected milestone,
evidence links, infrastructure separation, privacy/redaction status, and whether
the run is eligible for retry or appeal.

## Analysis Use

Failed runs feed failure-mode reports, benchmark meta-evaluation, harness
comparisons, and qualitative analysis. They do not count as ranked results.

## Tone

Failure pages and posts use neutral language. They should explain what failed
and what was learned without mocking participants or exposing private logs.

## Research Basis

Failure-mode reporting and SRE postmortem practice motivate blameless learning
from negative outcomes. NIST AI RMF motivates transparent communication of
limitations and measurement failures.

## QA Pass

Checked against `failure-classification.md`, `failure-mode-report.md`,
`test-run-result-sharing.md`, `incident-response.md`, and
`public-run-result-page.md`. This spec defines failed-run publication, not
private triage workflow.
