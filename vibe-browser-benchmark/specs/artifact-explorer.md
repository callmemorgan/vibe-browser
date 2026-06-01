# Artifact Explorer

## Purpose

The artifact explorer lets public readers and evaluators inspect redacted run
artifacts safely. It should make evidence easy to follow without executing or
trusting submitted code.

## Views

- snapshot manifest
- changed-file tree
- source file viewer
- participant diff
- command logs
- screenshots and golden artifacts
- verification records
- result card and benchmark card
- exported data references
- redaction and safety reports

## Evidence Links

Leaderboard cells, milestone rows, evaluator notes, failure classes, and report
charts can deep-link into a specific artifact, line, image, or log excerpt.
Each deep link shows artifact ID, checksum, redaction state, and certification
revision.

## Safety Rules

The explorer renders submitted files as inert text or media previews. It does
not execute scripts, load remote assets from submitted HTML, follow symlinks
outside the artifact root, or allow unsafe downloads without a warning and
authorization gate.

## UX Requirements

Large files show previews with download controls. Redacted sections display the
redaction reason. Missing, private, quarantined, or superseded artifacts show
clear states rather than broken links.

## Research Basis

ACM artifact review practice motivates connecting results to inspectable
artifacts. OWASP logging and file-handling guidance motivates safe rendering,
access control, and data minimization for public artifact browsing.

## QA Pass

Checked against `diff-and-code-browser-ux.md`, `screenshots-and-golden-artifacts.md`,
`artifact-retention-policy.md`, `security-and-redaction.md`, and
`public-run-result-page.md`. This spec defines artifact inspection, not
artifact storage retention.
