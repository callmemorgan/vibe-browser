# Fixture Registry

## Purpose

The fixture registry defines public and hidden test fixtures used by benchmark
checks. Fixtures must be reproducible, versioned, documented, and resistant to
hardcoding.

## Fixture Record

Each fixture includes:

- `fixture_id`
- display name
- version
- visibility: public, hidden, embargoed, or retired
- owner
- subsystem: URL, fetch, HTML, DOM, CSS, layout, paint, navigation, JS, storage,
  security, accessibility, or WPT
- served URL or local path
- content checksum
- expected behavior summary
- oracle type: assertion, golden, reftest, WPT expectation, evaluator-only, or
  fuzz seed
- linked milestones
- anti-hardcoding notes
- license/provenance
- retirement reason if applicable

## Serving Rules

Fixtures should be served from deterministic local infrastructure when possible.
Network, DNS, TLS, redirects, MIME types, timing, and cache headers must be
declared. Hidden fixtures must not be reachable from participant-visible logs or
public checker feedback.

## Versioning

Fixture changes create new versions. Public fixtures may be patched for
documentation or typo fixes only when checksums and expected behavior remain
unchanged. Behavior changes require a new fixture version and possibly a new
season.

## Review

New fixtures require oracle review, license review, ambiguity review,
contamination risk review, and difficulty estimate before becoming official.

## Research Basis

WPT metadata and wptrunner design motivate fixture manifests, expected results,
run-info properties, and local server control. Datasheets for Datasets motivate
documenting motivation, composition, collection, recommended uses, and
provenance.

## QA Pass

Checked against `public-milestone-checker.md`,
`milestone-evidence-requirements.md`, `leaderboard-seasons.md`,
`security-and-redaction.md`, and future hidden-test/task-authoring specs. This
spec defines registry records, not fixture generation tooling.
