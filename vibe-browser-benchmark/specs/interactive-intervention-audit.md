# Interactive Intervention Audit

## Purpose

Interactive intervention audit records every human approval, restart, prompt,
or guidance event that can affect a run. It makes guided and unguided results
distinguishable.

## Audited Events

- permission approval or rejection
- sandbox escalation
- manual restart
- wall-clock extension
- prompt injection by operator
- substantive debugging hint
- artifact repair
- environment repair
- dependency installation approval
- verifier rerun request
- hidden-test or private feedback exposure

## Event Fields

Each event records timestamp, actor, run ID, turn, event type, visible content,
agent-visible effect, reason, affected eligibility field, and related evidence
ID. Private actor identifiers are redacted in public exports.

## Eligibility Effects

Benign approvals may keep a run comparable if allowed by profile. Substantive
guidance, hidden feedback, or manual code edits move the run to guided,
non-comparable, or rejected status according to comparison rules.

## Public Display

Run pages summarize intervention count and eligibility effect. Detailed audit
events are shown only when redaction-safe.

## Research Basis

GitHub deployment review controls motivate explicit human approvals and
reviewer restrictions. OpenTelemetry event conventions motivate structured
event names and attributes for audit timelines.

## QA Pass

Checked against `comparison-eligibility-rules.md`, `multi-agent-and-team-runs.md`,
`open-ended-run-semantics.md`, `timeline-and-telemetry-ux.md`, and
`test-run-result-sharing.md`. This spec defines intervention logging, not
operator UI controls.
