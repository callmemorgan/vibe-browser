# Data Model

## Entities

### BenchmarkBatch

A group of runs intended for comparison.

Required fields:

- `batch_id`
- `benchmark_commit`
- `benchmark_input_digest`
- `prompt_set`
- `prompt_checksum`
- `profile`
- `target_mode`
- `human_intervention_policy`
- `created_at`

### Run

One harness execution.

Required fields:

- `run_id`
- `batch_id`
- `model_provider`
- `model`
- `model_snapshot`
- `agent_tool`
- `tool_version`
- `harness`
- `harness_version`
- `profile`
- `target`
- `target_mode`
- `started_at`
- `finished_at`
- `stop_reason`
- `comparison_eligible`
- `comparison_reason`

Budget and usage fields:

- `wall_clock_limit`
- `observed_elapsed_seconds`
- `turn_limit`
- `observed_turns`
- `token_limit`
- `observed_tokens`
- `tool_call_limit`
- `observed_tool_calls`
- `cost_limit`
- `observed_cost`

### Submission

The artifact set produced by a run.

Required fields:

- `run_id`
- `artifact_root`
- `submission_path`
- `manifest_path`
- `summary_path`
- `diff_path`
- `verification_logs`
- `version_info_path`

### MilestoneAssessment

Machine and human assessment for a milestone.

Required fields:

- `run_id`
- `milestone`
- `claimed_status`
- `public_check_status`
- `evaluator_status`
- `criteria`
- `missing_evidence`
- `notes`

### RubricScore

Evaluator score for the testing rubric.

Required fields:

- `run_id`
- `category`
- `weight`
- `score`
- `max_score`
- `evidence_links`
- `notes`

### TurnMetric

Per-turn harness summary.

Required fields:

- `run_id`
- `turn`
- `elapsed_seconds`
- `agent_elapsed_seconds`
- `agent_exit_code`
- `verification`
- `verification_log`
- `tokens`
- `tool_calls`
- `material_progress`
- `material_paths`
- `idle_count`
- `failure_count`

## Derived Fields

- `weighted_score`: sum of rubric category scores adjusted by weights.
- `highest_claimed_milestone`: highest milestone the submission claims.
- `highest_public_check_milestone`: highest milestone passing public checks.
- `highest_confirmed_milestone`: highest milestone confirmed by evaluator.
- `rankable`: true only when comparison-eligible and evaluator score exists.

## Source Files

The ingestion pipeline should prefer:

- `.vibe-bench/docker-artifacts/<run-id>/summary.json`
- `.vibe-bench/docker-artifacts/<run-id>/turn-metrics.json`
- `.vibe-bench/docker-artifacts/<run-id>/benchmark-run.md`
- evaluator score sheets

## Prototype Schema

The runnable prototype uses
[`schema/result.schema.json`](schema/result.schema.json) as the canonical v0.1
JSON shape. `scripts/benchmark_ingest.py` converts current Docker harness
artifacts into that shape, and `scripts/benchmark_score.py` appends the derived
`scores` block.

The schema intentionally includes the fields needed by the leaderboard spine:
run identity, attempts, turns, tool-call summaries, artifact links,
interventions, verification results, milestone assessments, rubric scores, and
derived score fields. It is not yet a complete public API contract.

## SQLite Store

`scripts/benchmark_db.py` is the prototype datastore implementation. It keeps
the full scored JSON record in `runs.result_json` and projects the fields needed
for filtering, ranking, comparison, and artifact inspection into normalized
tables:

- `runs`: leaderboard fields, score summaries, rankability, and visibility.
- `attempts`, `turns`, and `interventions`: agent lifecycle and restart data.
- `artifacts` and `verification_results`: public evidence and checker output.
- `milestone_scores`: derived per-milestone score rows.

The local database defaults to `vibe-browser-benchmark/benchmark.db` and is a
generated artifact, not source. Rebuild it from checked-in JSON examples or raw
harness artifacts, then export canonical JSON through `/results.json` or
`scripts/benchmark_score.py --json --db <path>`.
