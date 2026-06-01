# Run State Taxonomy

## Purpose

Run states standardize how the harness, ingestion pipeline, evaluator workflow,
and public UI describe lifecycle progress.

## States

- `queued`: run request accepted but not started.
- `preflight`: baseline cleanliness, provider config, Docker image, and profile
  checks are running.
- `running`: agent is active inside the official runtime profile.
- `stopped`: agent exited before the run budget ended and restart policy has not
  resolved the outcome.
- `timed_out`: wall clock or resource limit ended the run.
- `artifact_exported`: submission snapshot and harness outputs were collected.
- `public_checked`: deterministic public checks completed.
- `awaiting_evaluation`: run is ready for human review.
- `in_evaluation`: one or more evaluators are scoring evidence.
- `evaluated`: evaluator score exists but result is not yet certified.
- `certified`: official certification workflow completed.
- `published`: public pages and exports include the result.
- `invalid`: run cannot be scored because required artifacts or rules failed.
- `non_comparable`: run is useful but not eligible for ranked comparison.
- `archived`: retained for history but no longer active in queues.

## Transitions

Only the runner may move `queued` through `artifact_exported`. Public checkers
may move `artifact_exported` to `public_checked` or `invalid`. Evaluators may
move `awaiting_evaluation` through `evaluated`. Maintainers may certify,
publish, invalidate, mark non-comparable, or archive with an audit note.

Restart logic may move `stopped` back to `running`, but each restart must append
an intervention event.

## Terminal States

`published`, `invalid`, and `archived` are terminal for a specific run revision.
Corrections create a new revision or reanalysis record, not silent mutation.

## UI Requirements

The public UI should show friendly labels while preserving raw state in JSON.
Queues and admin screens should expose blockers, owner, updated time, and next
allowed transition.

## Research Basis

The state model reflects MLCommons-style submission discipline
(`https://mlcommons.org/benchmarks/`) and ACM's distinction between artifact
evaluation and result validation.

## QA Pass

Checked against the backlog entries for evaluator workflow, open-ended
semantics, official certification, negative results, and restart policy. The
taxonomy avoids scoring decisions; it only describes lifecycle state.
