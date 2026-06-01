# Agent Stop and Restart Policy

## Purpose

Agent stop and restart policy defines what happens when an agent exits before a
wall-clock limit or endurance run has completed.

## Stop Classes

- `completed`: agent claims work is done.
- `early-stop`: agent stops with remaining time and no completion signal.
- `tool-error-stop`: agent exits after tool or provider error.
- `no-op-stop`: agent exits without meaningful progress.
- `crash`: harness or agent process exits unexpectedly.
- `budget-stop`: cost, token, or time cap reached.

## Restart Rules

Profiles declare maximum restart count, continuation prompt, context handoff,
checkpoint behavior, and no-op detection. Restarts are evidence events and are
visible in run timelines.

## Done Criteria

A stopped agent is considered done only when it emits a final answer, reaches a
configured completion state, or the harness exhausts restart policy.

## Public Labels

Run pages show restart count, stop class, continuation policy, and whether the
restart affected comparability.

## Research Basis

SRE incident and recovery practice motivates distinguishing normal completion
from crash recovery. OpenTelemetry event conventions motivate structured stop
and restart events.

## QA Pass

Checked against `endurance-run-protocol.md`, `run-state-taxonomy.md`,
`timeline-and-telemetry-ux.md`, `comparison-eligibility-rules.md`, and
`interactive-intervention-audit.md`. This spec defines restart semantics, not
provider retry internals.
