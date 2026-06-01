# Ingestion Pipeline

## Purpose

The ingestion pipeline turns raw benchmark run directories into validated,
queryable leaderboard records. It must be deterministic, idempotent, auditable,
and conservative about malformed or unsafe artifacts.

## Inputs

The importer accepts a submission snapshot as defined in
`submission-snapshot-format.md`. Required inputs are `manifest.json`,
`summary.json`, `turn-metrics.json`, `version-info.json`, participant diff/status
files, `submission/`, `verification/`, `evidence/`, and `redaction-report.json`.

External score sheets, evaluator notes, and certification records enter through
separate evaluator/admin paths and must reference the imported `run_id`.

## Pipeline Stages

1. **Discover**: locate snapshots by run directory, upload batch, or object store
   prefix.
2. **Identify**: compute content hashes and check whether this exact snapshot
   was already imported.
3. **Validate shape**: validate JSON files against versioned JSON Schemas and
   confirm required artifact paths exist.
4. **Validate semantics**: check run state, timestamps, target/profile fields,
   version compatibility, artifact checksums, and impossible score values.
5. **Normalize**: map provider/model aliases, tool names, paths, timestamps, and
   result statuses into canonical fields.
6. **Index evidence**: create evidence objects and attach them to milestones,
   verification results, and certification gates.
7. **Classify visibility**: apply redaction status, artifact retention class, and
   access-control tags.
8. **Derive records**: compute preliminary eligibility, run-state transitions,
   public-check summaries, and cost/efficiency metrics.
9. **Quarantine or publish internally**: malformed or unsafe snapshots go to
   quarantine; valid snapshots enter `awaiting_evaluation`.

## Idempotency

Imports are keyed by `run_id`, snapshot hash, and manifest revision. Reimporting
the same snapshot is a no-op. Reimporting the same `run_id` with a different
snapshot creates a new revision and marks the older revision superseded only
after maintainer review.

## Failure Handling

Malformed inputs must not partially update public records. The pipeline writes a
failed ingestion record with error code, failing file, schema path when
available, importer version, and remediation hint. Dangerous artifacts move to
security quarantine before preview.

## Research Basis

JSON Schema provides the validation vocabulary and current 2020-12 meta-schema
for machine-checkable artifacts (`https://json-schema.org/specification`).
FAIR principles motivate rich metadata, persistent identifiers, provenance, and
machine-actionable reuse (`https://www.go-fair.org/fair-principles/`).

## QA Pass

Checked against `submission-snapshot-format.md`, `verification-result-schema.md`,
`evidence-model.md`, `run-state-taxonomy.md`, and
`official-result-certification.md`. This spec owns import mechanics only; it
does not define scoring or publication approval.
