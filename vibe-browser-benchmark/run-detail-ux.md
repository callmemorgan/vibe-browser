# Run Detail UX

## Purpose

The run detail page explains one result. It should answer what happened, what was
built, what passed, what failed, and why the run is or is not comparable.

## Header

Show:

- Run ID
- Model and provider
- Agent tool and harness
- Profile and target
- Benchmark commit and input digest
- Prompt set and checksum
- Human intervention policy
- Comparison eligibility and reason
- Stop reason

## Summary Cards

Cards should be compact and evidence-backed:

- Highest evaluator-confirmed milestone
- Highest public-check milestone
- Highest claimed milestone
- Rubric score
- Verification status
- Wall-clock, turns, tokens, tool calls, cost

## Tabs

### Evidence

List rubric categories with score, notes, and links to artifacts:

- Runnable artifact
- Browser capability
- Standards traceability
- Test quality
- Architecture quality
- Security posture
- Privacy posture
- Scope honesty

### Milestones

Show `M0` through `M9` as a vertical progression. Each milestone has:

- Status: not started, partial, candidate, confirmed, failed
- Acceptance criteria with pass/fail/unknown state
- Evidence links
- Missing evidence

### Artifacts

Show generated files:

- `submission/`
- `benchmark-run.md`
- `summary.json`
- `turn-metrics.json`
- `version-info.json`
- verification logs
- participant diff
- archived untracked files

### Timeline

Show per-turn progress:

- Turn number
- Elapsed time
- Agent exit code
- Verification result
- Token count
- Material paths changed
- Failure or idle count

### Environment

Show Docker image, image ID, OS, Python/Node/npm/Git/PI versions, provider
endpoint, and dependency notes.

## Safety Rules

- Never render raw secrets from logs or environment.
- Flag guided intervention prominently.
- Mark hidden evaluator notes separately from public agent-visible checks.
