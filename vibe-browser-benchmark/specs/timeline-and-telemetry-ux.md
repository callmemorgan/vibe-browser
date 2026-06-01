# Timeline and Telemetry UX

## Purpose

The timeline view explains what happened during a run: agent starts, tool calls,
file changes, verification attempts, restarts, errors, interventions, and score
decisions.

## Timeline Events

Events include:

- run queued, preflight started, agent started, agent stopped
- tool call started/finished/error
- file changed, artifact exported, verification started/finished
- public checker result, hidden checker result summary
- evaluator assignment, evaluator score submitted, adjudication completed
- redaction block, certification gate passed/failed, publication
- restart, timeout, cancellation, provider outage, infrastructure incident

## Event Fields

Each event includes `event_id`, `run_id`, timestamp, actor, event type, severity,
duration if applicable, parent event, evidence IDs, visibility, and redaction
state. Tool events include tool name and safe argument summaries. Provider events
include model identity and request metadata only when safe.

## Views

The default view is compact and grouped by turn or phase. Filters support
errors, tool calls, verification, artifacts, evaluator actions, and
interventions. The detail drawer shows evidence links and raw logs only when
the viewer has permission.

## Privacy Boundary

The timeline must not expose private reasoning or hidden-test details. It can
show "assistant writing," "tool call," and summarized outputs, but raw transcript
publication follows the reasoning trace/transcript policy.

## Research Basis

OpenTelemetry semantic conventions provide common naming for traces, metrics,
logs, profiles, and resources, and motivate consistent event/attribute names.
OWASP logging guidance motivates sanitization, timestamp handling, and testing
logging failure modes.

## QA Pass

Checked against `evidence-model.md`, `cost-and-efficiency-metrics.md`,
`failure-classification.md`, `security-and-redaction.md`, and
`run-detail-ux.md`. This spec owns timeline UX, not telemetry storage internals.
