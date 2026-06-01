# Archival and Preservation

## Purpose

Archival and preservation define how benchmark seasons, artifacts, data exports,
runtime metadata, and citations remain usable after infrastructure and
dependencies change.

## Archived Materials

- benchmark source commit
- season benchmark card
- public data export
- result cards
- verification records
- artifact manifests and public-safe artifacts
- runtime image digests
- dependency mirror manifests
- reports and notebooks
- release notes
- citation metadata

## Preservation Controls

Use immutable snapshots, checksums, replicated storage, documented formats,
periodic fixity checks, preservation logs, and tombstone pages for unavailable
items.

## Rerun Support

Archived seasons include enough instructions for a future reader to attempt a
best-effort rerun, including known unavailable dependencies or provider drift.

## Retention

Retention rules distinguish raw private artifacts, public exports, signed
records, and citable reports. Public citable objects are preserved longest.

## Research Basis

Library of Congress digital preservation guidance motivates long-term access,
format awareness, and fixity practices. DataCite tombstone guidance motivates
clear landing pages when citable content is unavailable.

## QA Pass

Checked against `artifact-retention-policy.md`, `public-data-export.md`,
`reproducibility-contract.md`, `citation-and-doi-policy.md`, and
`benchmark-sunset-or-succession-plan.md`. This spec defines preservation
policy, not storage vendor selection.
