# Technical Report Generator

## Purpose

The technical report generator creates repeatable per-season and per-study
reports from certified benchmark data. It reduces hand-edited analysis drift
and lets public numbers be regenerated from exported records.

## Inputs

- certified run records
- result cards and benchmark cards
- milestone scores and evaluator decisions
- cost and efficiency metrics
- failure classifications
- model, harness, prompt, and season registry entries
- public artifact references
- data-export manifest and schema versions

## Generated Outputs

- Markdown report for review
- static HTML report for public publication
- PDF-ready report artifact
- chart image directory with alt text
- machine-readable chart data
- provenance manifest with input checksums, generator version, command, and
  generation timestamp

## Required Sections

Every generated report includes scope, methodology summary, cohort definition,
eligibility filters, ranking tables, milestone distribution, cost analysis,
failure-mode summary, representative qualitative observations, limitations,
corrections, and links to raw exports.

## Determinism

Running the generator twice against the same immutable export should produce
the same tables, chart data, and prose blocks except for build metadata stored
outside the public report body.

## Review Workflow

Generated reports enter `draft` state. Maintainers may edit narrative
interpretation, but numeric tables and charts must be regenerated from data
rather than manually changed.

## Research Basis

FAIR principles motivate reusable and provenance-rich research outputs.
Jupyter and data-package workflows motivate executable, data-backed analysis
rather than hand-copied tables.

## QA Pass

Checked against `public-data-export.md`, `run-analysis-notebook.md`,
`model-comparison-report.md`, `failure-mode-report.md`, and
`official-result-certification.md`. This spec defines report generation, not
the visual chart component library.
