# Data Quality Checks

## Purpose

Data quality checks detect corrupt, inconsistent, missing, or impossible
leaderboard data before it appears in public pages, reports, or exports.

## Check Categories

- required field presence
- schema validation
- duplicate run IDs
- impossible timestamps or clock skew
- invalid state transitions
- score/category mismatch
- missing evidence links
- broken artifact references
- inconsistent model or harness identity
- invalid comparison group
- corrupted archives or checksum mismatch
- private artifact referenced from public export

## Check Outputs

Each check emits ID, severity, affected record, field path, expected condition,
observed value summary, evidence link, owner, and recommended action.

## Gates

Blocking quality failures prevent certification, public export generation, and
report publication. Warnings may publish only when the public page shows the
known limitation.

## Operations

Quality checks run at ingestion, certification, export generation, report
generation, and scheduled archival audits.

## Research Basis

Frictionless validation practice motivates schema-backed checks for data
packages. JSON Schema motivates machine-readable validation errors tied to
specific object paths.

## QA Pass

Checked against `ingestion-pipeline.md`, `schema-versioning-and-migrations.md`,
`public-data-export.md`, `official-result-certification.md`, and
`admin-operations.md`. This spec defines data checks, not evaluator scoring.
