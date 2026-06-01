# Reanalysis Policy

## Purpose

Reanalysis policy defines when existing results are recomputed, re-scored,
re-exported, or relabeled after publication.

## Reanalysis Triggers

- scoring bug
- evaluator correction
- formula change
- schema migration
- provider metadata correction
- contamination discovery
- hidden-test leak
- dependency policy change
- verifier bug
- artifact redaction update
- accepted appeal

## Reanalysis Types

- `metadata-only`: labels or metadata change without score change.
- `score-recompute`: existing evidence is rescored.
- `verification-replay`: submitted artifact is rerun.
- `export-regeneration`: public export is regenerated.
- `season-repair`: affected season receives correction summary.

## Public Rules

Reanalysis never silently mutates old public claims. Result pages, reports,
exports, and citations link original and revised records with rank impact.

## Limits

Historical results are not routinely recomputed under new benchmark difficulty
unless the season explicitly defines a retrospective analysis.

## Research Basis

DataCite versioning guidance motivates linking new and previous versions of
citable datasets. ACM publication integrity practice motivates preserving the
scholarly record while issuing corrections.

## QA Pass

Checked against `appeals-and-corrections.md`, `citation-and-doi-policy.md`,
`leaderboard-seasons.md`, `public-data-export.md`, and
`benchmark-difficulty-tuning.md`. This spec defines reanalysis triggers, not
the scorer implementation.
