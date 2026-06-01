# Verification Result Schema

## Purpose

Verification results describe automated checks in a stable, queryable format.
They are evidence, not final scores; evaluators and certification workflows use
them to support or challenge milestone claims.

## Result Object

Each result includes:

- `result_id`
- `run_id`
- `checker_name`
- `checker_version`
- `scope`: build, unit, smoke, GUI, public milestone, hidden milestone, WPT,
  fuzz, security, redaction, or replay
- `status`: pass, fail, error, timeout, skipped, flaky, expected-fail, or blocked
- `started_at` and `duration_ms`
- `command`
- `exit_code`
- `stdout_artifact` and `stderr_artifact`
- `environment_profile`
- `inputs_hash`
- `failure_class`
- `evidence_ids`
- `visibility`

## Aggregation

A milestone public check may aggregate several result objects. Aggregates must
preserve child results and explain whether a single failing child blocks the
milestone or only reduces confidence.

## Flake Handling

Repeated checks append attempts. A flaky result records all observed statuses,
attempt count, timing spread, and final policy decision. WPT-style expected
failure metadata is allowed, but expected failures must not count as newly
passing capability.

## Public vs Hidden Results

Public result objects may include command names and failure summaries. Hidden
result objects must hide exact inputs, assertions, and paths that would train
future agents against hidden checks.

## Research Basis

WPT expectation metadata provides a model for expected failures and intermittent
statuses, and SWE-bench Verified shows why coding-agent evaluation benefits from
reliable containerized replay.

## QA Pass

Checked against `evidence-model.md`, `submission-snapshot-format.md`, WPT
expectation metadata, and current harness auto-verification behavior. The schema
supports existing smoke/unit checks and future WPT/fuzz expansion.
