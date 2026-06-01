# Public Milestone Checker

## Purpose

The public milestone checker is an agent-visible feedback tool. It helps agents
understand deterministic public progress without revealing hidden tests or
turning the benchmark into an interactive grader for official scoring.

## Tool Contract

The checker accepts:

- `run_id`
- `target_milestone`
- `submission_path`
- `benchmark_commit`
- `checker_version`
- optional `changed_paths`

It returns JSON with:

- `status`: pass, fail, error, timeout, skipped, or blocked
- `highest_public_milestone`
- `milestone_results`
- `verification_result_ids`
- `evidence_ids`
- `summary`
- `next_public_hint`
- `hidden_tests_consulted`: always `false`
- `official_score`: always `null`

## Allowed Feedback

Feedback may name public fixtures, failing public assertions, command failures,
missing artifacts, and deterministic smoke-test blockers. It may suggest broad
capability gaps, such as "M2 fetch fixtures fail redirect handling."

Feedback must not reveal hidden test names, hidden inputs, evaluator judgments,
private rubric notes, or exact scoring deltas.

## Checker Scope

Public checks should be stable enough for local iteration and cheap enough to
run repeatedly. They may include unit tests, smoke launch, fixture tests,
schema checks, and public WPT subsets. Hidden checks, human scoring, and
certification gates remain separate.

## Agent Interaction Rules

Public-check use is recorded in the run timeline. It does not count as human
intervention if the same checker is available to all runs in the profile. If a
maintainer provides custom guidance outside the checker, the run must be labeled
guided or non-comparable.

## Research Basis

WPT expectation metadata provides a model for public expected-fail and flaky
status handling. SWE-bench Verified motivates containerized, reliable automated
checks for agentic code submissions.

## QA Pass

Checked against `verification-result-schema.md`, `milestone-evidence-requirements.md`,
`comparison-eligibility-rules.md`, and `official-result-certification.md`. This
spec defines agent-visible feedback, not official evaluator scoring.
