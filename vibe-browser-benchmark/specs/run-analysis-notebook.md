# Run Analysis Notebook

## Purpose

Run analysis notebooks give maintainers and external researchers an executable
way to inspect benchmark data, reproduce charts, and explore hypotheses without
changing official leaderboard records.

## Notebook Set

- `season-overview.ipynb`: load a season export, summarize rank, score, cost,
  and milestone distribution.
- `single-run-deep-dive.ipynb`: inspect one run timeline, artifacts, failures,
  and evaluator notes.
- `model-comparison.ipynb`: compare model cohorts inside one eligible group.
- `harness-comparison.ipynb`: compare agent harnesses while holding model and
  profile fixed.
- `failure-analysis.ipynb`: group failure classes by scope, severity, and
  recoverability.
- `export-validation.ipynb`: verify checksums, schema versions, and required
  fields in a public export.

## Notebook Requirements

Each notebook declares input export version, expected schema, dependency lock,
random seed, and output directory. It must run from a clean checkout using only
public data unless explicitly marked maintainer-only.

## Output Rules

Generated charts include title, season, track, filters, sample count, and data
source. Notebooks may produce exploratory findings, but official claims require
a technical report or reviewed blog post.

## Publication

Public notebooks should be scrubbed of private artifact paths, hidden-test
details, credentials, and maintainer-only notes before publication.

## Research Basis

Jupyter Notebook documentation motivates literate, executable analysis.
Frictionless Data Package and FAIR principles motivate explicit schemas,
portable data, and reproducible reuse.

## QA Pass

Checked against `public-data-export.md`, `technical-report-generator.md`,
`security-and-redaction.md`, `cost-and-efficiency-metrics.md`, and
`failure-classification.md`. This spec covers analysis workbooks, not official
rank calculation.
