# Harness Comparison Report

## Purpose

Harness comparison reports evaluate agent wrappers, tool surfaces, restart
behavior, permissions, and artifact capture while holding the model and
benchmark profile as constant as practical.

## Comparison Preconditions

- same model, provider, benchmark season, and target track
- same wall-clock and intervention policy
- disclosed tool set, sandbox profile, restart policy, and prompt wrapper
- comparable artifact retention and telemetry capture
- known infrastructure incidents excluded or labeled

## Required Metrics

Reports include milestone score, verification outcomes, turn count, tool calls,
restart count, context growth, timeout behavior, shell/error recovery, artifact
completeness, redaction pass rate, and cost overhead.

## Qualitative Questions

- Did the harness preserve enough context across continuations?
- Did tool feedback make failures actionable without leaking hidden tests?
- Did permission prompts or sandbox limits block useful progress?
- Did restart handling recover from normal agent stops?
- Did artifact capture support subsequent inspection and certification?

## Publication Rules

Do not rank harnesses without saying which model, provider, and profile were
used. A harness that enables more tools may be more capable and less isolated;
that tradeoff should be visible.

## Research Basis

MLCommons fair-comparison practice motivates holding benchmark conditions
constant before ranking systems. OpenTelemetry motivates comparable event and
resource attributes across runner implementations.

## QA Pass

Checked against `prompt-and-harness-registry.md`,
`comparison-eligibility-rules.md`, `timeline-and-telemetry-ux.md`,
`artifact-retention-policy.md`, and `failure-classification.md`. This spec
defines harness reporting, not harness implementation.
