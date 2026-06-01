# Endurance Run Protocol

## Purpose

Endurance run protocol defines long-running benchmark modes such as 24-hour
frontier runs. These runs measure persistence and recovery separately from
short smoke or targeted milestone tests.

## Protocol Fields

- duration limit
- checkpoint cadence
- restart policy
- cost cap
- provider outage handling
- artifact export cadence
- evaluator sampling plan
- required progress summaries
- allowed human interventions
- finalization criteria

## Checkpoints

Endurance runs produce periodic checkpoint manifests with changed files,
metrics, public-check status, failure classes, and artifact references.
Checkpoints must be inspectable even if the final run fails.

## Comparison Rules

Endurance runs rank only in endurance divisions. They must not be compared
directly against 10-minute smoke runs or targeted milestone runs.

## Failure Handling

Timeouts, provider outages, repeated no-op exits, and resource exhaustion
receive explicit labels. Partial progress may be published as non-ranked
evidence.

## Research Basis

SRE workload and incident practices motivate checkpointing, outage labels, and
clear recovery rules for long-running systems. Resource accounting practice
motivates explicit cost and time budgets.

## QA Pass

Checked against `open-ended-run-semantics.md`, `agent-stop-and-restart-policy.md`,
`resource-accounting.md`, `tracks-and-divisions.md`, and
`artifact-retention-policy.md`. This spec defines endurance mode, not short-run
defaults.
