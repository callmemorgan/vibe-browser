# Public Data Export

## Purpose

Public data exports make benchmark results inspectable, reusable, and citable
without exposing private artifacts, secrets, hidden tests, or unsafe submitted
content.

## Export Package

Each export package includes:

- `datapackage.json` with package metadata and resource list
- `runs.jsonl`
- `scores.jsonl`
- `verification-results.jsonl`
- `failure-classifications.jsonl`
- `models.jsonl`
- `harnesses.jsonl`
- `artifacts.jsonl` with public-safe references only
- `events-summary.jsonl`
- `README.md`
- `CHECKSUMS.txt`
- schema files for each resource

## Required Metadata

Package metadata includes export ID, benchmark version, season, track, creation
time, generator version, source commit, license, citation text, contact, schema
version, redaction policy, and compatibility notes.

## Stability

Published exports are immutable. Corrections produce a new export with a
supersedes link and a correction note. Public pages should link to the exact
export used for each chart or report.

## Privacy And Safety

Exports include only redaction-approved data. Hidden-test details, private logs,
credentials, local filesystem paths, and unsafe artifacts are excluded or
replaced by stable public references.

## Research Basis

Frictionless Data Package motivates machine-readable packages with named
resources and schemas. FAIR principles and Zenodo DOI guidance motivate
findable, citable, versioned data releases.

## QA Pass

Checked against `security-and-redaction.md`, `api-contract.md`,
`evidence-model.md`, `technical-report-generator.md`, and
`run-analysis-notebook.md`. This spec defines public exports, not private
artifact storage.
