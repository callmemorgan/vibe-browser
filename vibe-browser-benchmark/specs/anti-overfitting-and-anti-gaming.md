# Anti-Overfitting and Anti-Gaming

## Purpose

Anti-overfitting and anti-gaming rules protect the benchmark from submissions
that optimize leaderboard mechanics instead of browser behavior.

## Suspicious Patterns

- hardcoded fixture URLs, expected bodies, or exact hidden-like outputs
- fake tests that assert implementation shortcuts
- no-op shell UI that only satisfies smoke checks
- copied full browser engine when policy disallows it
- dependencies that perform the entire milestone without disclosure
- conditional behavior keyed to benchmark paths or environment variables
- fabricated verification logs or result summaries
- benchmark-specific string matching instead of general parsing behavior

## Detection Signals

Use code review, hidden variants, fixture rotation, dependency inspection,
calibration examples, diff analysis, and evaluator notes. A signal starts
review; it is not proof by itself.

## Outcomes

Maintainers may request explanation, mark a run official-unranked, reject the
run, rotate fixtures, open an incident, or update dependency policy. Severe
fraud or hidden-test leakage triggers security hold.

## Public Handling

Public pages should use neutral labels such as `gaming-review`,
`non-general-implementation`, or `policy-rejected` without publishing exploit
details.

## Research Basis

Leaderboard-overfitting research motivates private holdouts and cautious
interpretation of optimized scores. MLCommons submission rules motivate clear
allowed and disallowed implementation boundaries.

## QA Pass

Checked against `fixture-registry.md`, `hidden-test-policy.md`,
`allowed-dependency-policy.md`, `external-submission-review.md`, and
`failure-classification.md`. This spec defines anti-gaming policy, not a static
detector list.
