# Evidence Model

## Purpose

Evidence objects connect scores to observable artifacts. Every official
milestone decision should be traceable to one or more evidence objects.

## Evidence Object

Each evidence object includes:

- `evidence_id`: stable identifier within the run.
- `run_id`: parent run.
- `type`: command, log, screenshot, golden diff, source file, design note,
  evaluator note, verification result, WPT report, fuzz report, or artifact
  manifest.
- `path_or_url`: storage location.
- `checksum`: hash for immutable artifacts.
- `created_at`: UTC timestamp.
- `visibility`: public, evaluator-only, maintainer-only, hidden-test-private, or
  redacted-public.
- `producer`: runner, agent, verifier, evaluator, maintainer, or third party.
- `summary`: short human-readable description.
- `attached_to`: milestone, rubric criterion, failure class, score component, or
  certification gate.
- `redaction_status`: pending, clean, redacted, blocked, or private.

## Evidence Types

Command evidence stores command, exit code, duration, stdout/stderr artifact
links, and environment profile. Screenshot evidence stores viewport, platform,
render mode, and image diff metadata where applicable. Source evidence links to
submitted files and diff hunks. Evaluator notes store rubric rationale and may
quote only short excerpts from private logs.

## Attachment Rules

A score cell must not link directly to a raw private artifact. It links to an
evidence object, which then resolves to the safest visible representation for
the viewer role.

One evidence object may support multiple criteria, but hidden-test evidence must
not reveal hidden test names, inputs, or exact assertions to participants.

## Research Basis

ACM artifact badging motivates documented, complete, exercisable artifacts, and
FAIR data principles motivate persistent identifiers, metadata, provenance, and
clear access conditions (`https://www.go-fair.org/fair-principles/`).

## QA Pass

Checked against `run-detail-ux.md`, `milestone-rubrics.md`, security/redaction
backlog entries, and artifact explorer requirements. This spec defines evidence
shape; retention and redaction policies are separate specs.
