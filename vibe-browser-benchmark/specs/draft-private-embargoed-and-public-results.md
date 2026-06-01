# Draft, Private, Embargoed, and Public Results

## Purpose

This spec defines visibility states before and after publication so private
review, vendor embargoes, dry runs, and public ranking do not blur together.

## Visibility States

- `draft`: imported but incomplete or under maintainer review.
- `private`: visible only to maintainers and authorized submitters.
- `embargoed`: accepted for delayed disclosure with recorded expiration.
- `provisional`: public or limited-public but not final certified status.
- `public-unranked`: public and certified, excluded from rank.
- `public-ranked`: official ranked result.
- `withdrawn`: public record remains but result is no longer active.

## Access Rules

Every state declares who can view metadata, artifacts, evaluator notes, hidden
check summaries, redaction reports, and exports. Embargoed records never affect
public rank before release.

## State Transitions

Transitions require actor, reason, timestamp, affected fields, and audit link.
Moving from private or embargoed to public requires privacy, security,
redaction, and certification gates.

## Public Display

Provisional, unranked, embargo-expired, and withdrawn states must be visible in
headers, embeds, exports, and screenshots.

## Research Basis

ACM artifact review practice motivates separating artifact review state from
validated result publication. DataCite versioning guidance motivates preserving
superseded or withdrawn public records with clear status.

## QA Pass

Checked against `access-control.md`, `test-run-result-sharing.md`,
`official-result-certification.md`, `external-submission-review.md`, and
`citation-and-doi-policy.md`. This spec defines visibility state, not account
authentication.
