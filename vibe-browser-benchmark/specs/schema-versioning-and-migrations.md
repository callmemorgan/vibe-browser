# Schema Versioning and Migrations

## Purpose

Schema versioning and migrations keep run records, scores, artifacts, reports,
and exports readable as the benchmark evolves.

## Versioned Schemas

- run summary
- result card
- benchmark card
- score sheet
- milestone evidence
- artifact manifest
- verification result
- failure classification
- public data export
- report manifest

## Version Rules

Every persisted object includes schema name, schema version, benchmark version,
and creation timestamp. Breaking changes require a major schema version and
migration notes. Additive fields require defaults, nullability rules, and export
compatibility notes.

## Migration Requirements

Migrations are deterministic, reviewed, reversible where feasible, and tested
against archived season examples. Migration output records source version,
target version, actor, timestamp, changed fields, and validation result.

## Compatibility

Old seasons remain readable. Public APIs may expose both original and migrated
views when exact historical meaning matters.

## Research Basis

JSON Schema provides a standard vocabulary for structured validation.
Frictionless Data Package practice motivates explicit schemas for reusable
tabular and JSON resources.

## QA Pass

Checked against `api-contract.md`, `public-data-export.md`,
`verification-result-schema.md`, `result-card.md`, and
`governance-and-versioning.md`. This spec defines schema lifecycle, not
database migration tooling.
