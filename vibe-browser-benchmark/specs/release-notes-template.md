# Release Notes Template

## Purpose

Release notes explain what changed in a benchmark season, harness release,
scoring revision, data export, or public-site deployment. They give readers a
compact changelog without replacing the methodology page or benchmark card.

## Required Structure

1. **Version heading**: benchmark, harness, or site version plus release date.
2. **Status**: draft, released, corrected, withdrawn, or superseded.
3. **Affected scope**: seasons, tracks, prompts, harnesses, fixtures, scoring,
   exports, or UI surfaces.
4. **Added**: new capabilities, specs, views, metrics, or data fields.
5. **Changed**: behavior, scoring, eligibility, copy, charts, or schemas.
6. **Fixed**: incorrect public output, broken checks, import issues, or
   documentation errors.
7. **Security and privacy**: redaction, access-control, or artifact-handling
   changes.
8. **Compatibility**: migration notes for clients, scripts, notebooks, and
   exported schemas.
9. **Reanalysis**: whether historical results are unchanged, annotated, or
   queued for recomputation.
10. **Links**: benchmark card, methodology diff, API schema, issue, and
   certification record.

## Version Rules

Use semantic versions for harness and API releases. Use season identifiers for
leaderboard comparability windows. A scoring formula change that can alter
rankings requires a benchmark-card update and a visible reanalysis note.

## Public Display

The public changelog page should group notes by season and by component. Run
detail pages should link to the release note active when the run was certified.

## Research Basis

Keep a Changelog motivates consistent Added, Changed, Deprecated, Removed,
Fixed, and Security sections. Semantic Versioning motivates explicit
compatibility signaling for machine-facing releases.

## QA Pass

Checked against `benchmark-card.md`, `leaderboard-seasons.md`,
`api-contract.md`, `official-result-certification.md`, and
`blog-post-template.md`. This spec defines release communication, not the
governance vote process.
