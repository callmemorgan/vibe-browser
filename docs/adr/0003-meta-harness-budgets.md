# ADR 0003: Meta-Harness Budgets

Status: accepted

Date: 2026-05-31

## Context

The benchmark needs a way to keep models working beyond a single prompt. Browser
implementation is a long task, and model quality depends on planning,
implementation, verification, recovery, and continuation behavior.

Without a shared meta-harness policy, runs could differ by hidden human nudges,
unbounded time, provider-specific token budgets, or inconsistent stopping rules.

## Decision

Use explicit meta-harness profiles that combine wall-clock, token, turn,
tool-call, cost, idle, and failure limits. The default comparable profile is
`standard-v0`: 24 hours, 200 turns, 8M total model tokens when measurable, and 6
consecutive idle turns.

The meta-harness must record configured limits and observed usage in the run
manifest. The earliest exhausted limit stops the run. Human intervention that
adds substantive guidance creates a different benchmark condition and must be
recorded. Administrative intervention that only keeps the configured harness
running is allowed in comparable runs when recorded.

Add boundary profiles for very large token regimes: `deep-v0` at 1B tokens and
`frontier-v0` at 10B tokens. These are not replacements for `standard-v0`; they
are separate long-horizon conditions for measuring behavior near and beyond a
Chromium-scale corpus budget.

## Consequences

- Long-running model behavior is measured without making runs unlimited.
- Runs can be grouped by profile before comparison.
- Provider differences in token accounting are handled by recording both limits
  and observed usage.
- Idle and repeated-failure limits keep runs from burning budget without
  progress.
- Human assistance is separated into administrative and guided intervention.
- Billion-token profiles can be compared within their own class without
  distorting standard 24-hour results.
- Future harnesses can tune profiles based on observed data without changing old
  run records.

## Alternatives Considered

- Wall-clock only: rejected because slow tools and provider latency would distort
  comparisons.
- Token budget only: rejected because local build and test time is central to the
  task and not captured by tokens.
- Single-turn submissions: rejected because the benchmark is meant to evaluate
  agentic implementation, recovery, and verification.
- Unlimited continuation: rejected because it makes runs expensive and hard to
  compare.
