# Queueing and Run Scheduling

## Purpose

Queueing and run scheduling define how official hosted runs are ordered,
retried, canceled, and protected from monopolization.

## Queue Inputs

- submitter identity
- requested season and division
- artifact or hosted-run request
- provider and model
- runtime profile
- expected duration
- priority class
- embargo request
- baseline or calibration reservation

## Scheduling Rules

Use fair queueing by submitter and division. Reserve capacity for baseline
reruns, verifier maintenance, incident recovery, and evaluator calibration.
Paid priority, if offered, must be disclosed and must not affect scoring gates.

## Retry And Cancellation

Provider outages, verifier crashes, and infrastructure errors can trigger
maintainer-controlled retries. Participant-caused invalid submissions require a
new queue entry unless policy grants a repair window.

## Public Status

Submitters can see queue position class, run state, blockers, and estimated
start window when available. Public viewers see only aggregate queue health.

## Research Basis

Google SRE workload management motivates explicit prioritization and overload
controls. MLCommons submission operations motivate scheduled, rule-bound
submission processing.

## QA Pass

Checked against `run-state-taxonomy.md`, `external-submission-review.md`,
`economic-model.md`, `baseline-agents-and-reference-runs.md`, and
`incident-response.md`. This spec defines scheduling policy, not job-runner
implementation.
