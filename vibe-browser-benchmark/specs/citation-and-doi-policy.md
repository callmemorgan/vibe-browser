# Citation and DOI Policy

## Purpose

The citation and DOI policy defines how readers cite benchmark versions,
leaderboard seasons, reports, and public data exports. Citations must identify
the exact artifact used rather than a mutable homepage.

## Citable Objects

- benchmark methodology version
- leaderboard season
- public data export
- technical report
- white paper
- certified run result page
- benchmark card
- prompt and harness registry release

## Citation Fields

Each citable object provides title, authors or maintainers, publication date,
version or season, stable URL, checksum or export ID when applicable, license,
recommended citation text, and supersedes or superseded-by links.

## DOI Rules

Use DOI publication for stable public data exports, major white papers, and
season-level reports that external researchers are expected to cite. Do not mint
a DOI for draft pages, provisional runs, unpublished artifacts, or mutable
leaderboard views.

## Versioning

Citation text must include both human-readable version and immutable identifier.
Corrections produce a new citable revision and link back to the original record
instead of changing citation meaning in place.

## Display

Public pages include "Cite this" controls with plain-text, BibTeX, and JSON
metadata. The control must show whether the cited object is official,
provisional, corrected, withdrawn, or superseded.

## Research Basis

DataCite guidance motivates persistent identifiers, versioned dataset records,
and metadata suitable for citation. FAIR principles motivate findable,
accessible, interoperable, and reusable benchmark data.

## QA Pass

Checked against `public-data-export.md`, `public-run-result-page.md`,
`release-notes-template.md`, `technical-report-generator.md`, and
`official-result-certification.md`. This spec defines citation policy, not
dataset licensing terms.
