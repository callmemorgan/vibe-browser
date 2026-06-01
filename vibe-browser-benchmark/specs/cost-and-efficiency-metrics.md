# Cost and Efficiency Metrics

## Purpose

Cost and efficiency metrics explain how much work a result required. They are
secondary metrics and must not override the primary quality ranking.

## Required Metrics

- `wall_clock_seconds`: elapsed time from first agent start to final stop.
- `agent_elapsed_seconds`: cumulative active agent time when available.
- `turn_count`: agent turns or continuation cycles.
- `tool_call_count`: total tool calls and counts by tool type.
- `input_tokens`, `output_tokens`, and `total_tokens` when provider or harness
  data is available.
- `estimated_cost_usd`: transparent formula and provider price snapshot.
- `verification_seconds`: public and hidden checker runtime.
- `artifact_bytes`: retained snapshot size by class.
- `cpu_seconds`, `max_memory_bytes`, `disk_bytes`, and network bytes when the
  runner can measure them.

## Derived Metrics

- score per dollar
- score per thousand tokens
- milestone value per minute
- public-check pass rate per turn
- verification cost by milestone
- cost-to-frontier milestone

Derived metrics must include missing-data flags and should be hidden from rank
tables unless enough runs in the comparison group have comparable measurements.

## Token and Price Caveats

Provider-reported tokens may differ from harness-estimated tokens. Cloud model
pricing changes over time. If exact cost cannot be reconstructed, publish the
price snapshot, formula, and confidence level rather than inventing precision.

## Display Rules

Efficiency leaderboards are opt-in views. Main leaderboards may show compact
cost/time columns, but rank remains based on evaluator score within an eligible
comparison group.

## Research Basis

OpenTelemetry semantic conventions motivate consistent metric names and units
for traces, metrics, logs, and resource attributes. HELM motivates reporting
efficiency alongside capability so tradeoffs stay visible.

## QA Pass

Checked against `blended-score.md`, `model-and-tool-identity.md`,
`comparison-eligibility-rules.md`, current `turn-metrics.json` harness output,
and the future resource accounting spec. This spec defines benchmark-level
metrics, not provider billing integration.
