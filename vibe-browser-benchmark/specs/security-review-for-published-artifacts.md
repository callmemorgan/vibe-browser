# Security Review for Published Artifacts

## Purpose

Security review for published artifacts ensures public downloads, previews, and
evidence links do not expose readers or infrastructure to dangerous submitted
content.

## Review Scope

- executable files and scripts
- archives and nested archives
- symlinks and path traversal
- device files and special files
- oversized binaries
- HTML, SVG, PDF, and media with active content
- dependency lockfiles and install scripts
- suspicious network or credential access
- malware or cryptomining indicators
- hidden-test or secret leakage

## Required Controls

Artifacts are scanned, typed, size-limited, and assigned a publication decision:
`public-preview`, `public-download`, `private`, `quarantined`, or `removed`.
Public previews render content inertly and avoid executing submitted code.

## Download Rules

High-risk but publishable artifacts require warning banners, checksum display,
content type controls, and authorization where appropriate. Quarantined
artifacts are unavailable outside maintainers and security reviewers.

## Incident Linkage

Suspicious or malicious artifacts create security review records and may open
an incident, invalidate a run, or require participant follow-up.

## Research Basis

OWASP file upload guidance motivates validating type, limiting execution,
scanning files, and storing uploads safely. SLSA provenance concepts motivate
artifact integrity and traceability.

## QA Pass

Checked against `artifact-explorer.md`, `security-and-redaction.md`,
`privacy-review.md`, `deceptive-or-unsafe-submission-handling` backlog scope,
and `official-result-certification.md`. This spec defines publication review,
not full malware analysis tooling.
