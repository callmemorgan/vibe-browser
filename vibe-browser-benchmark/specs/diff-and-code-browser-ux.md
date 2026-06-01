# Diff and Code Browser UX

## Purpose

The diff and code browser lets reviewers inspect generated submissions quickly
without downloading unsafe artifacts or losing the connection between code,
evidence, and scores.

## Primary Views

- **Changed files**: tree grouped by added, modified, deleted, renamed,
  generated, binary, and oversized.
- **Participant diff**: unified diff with line numbers, hunk navigation, syntax
  highlighting, and whitespace controls.
- **File viewer**: read-only source view for submitted files.
- **Evidence links**: badges showing which tests, milestones, or evaluator notes
  reference each file or hunk.
- **Safety state**: redaction, quarantine, private-only, or downloadable.

## Required Interactions

Reviewers need search by path/content, jump to changed files, copy stable
evidence links, collapse generated files, hide whitespace-only hunks, and compare
two run revisions. Large files should show metadata and require explicit
download permission.

## Safety Rules

The browser is read-only. It must not execute submitted HTML, scripts, binaries,
or symlinks. HTML artifacts render as escaped source unless opened in a
controlled fixture viewer. Private or quarantined files show a reason and
required role instead of a broken link.

## Public UX

Public readers should see enough code to understand the result, but hidden-test
evidence, private logs, and unsafe files must remain inaccessible. If a file was
redacted, show a redaction banner and a link to the redaction report summary.

## Research Basis

Git's diff-format documentation anchors patch and hunk terminology. ACM
artifact badging motivates making artifacts documented and exercisable, while
OWASP authorization guidance motivates server-side access checks for static
resources and downloads.

## QA Pass

Checked against `submission-snapshot-format.md`, `evidence-model.md`,
`security-and-redaction.md`, `artifact-retention-policy.md`, and
`result-card.md`. This spec defines UX behavior, not storage layout.
