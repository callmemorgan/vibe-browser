# Admin Operations

## Purpose

Admin operations define the maintainer tools needed to keep the benchmark
accurate, safe, and usable without ad hoc database edits.

## Operations

Maintainers need actions to:

- reingest a snapshot
- quarantine or release artifacts
- rerun public checks
- assign or unassign evaluators
- trigger adjudication
- mark runs invalid or non-comparable
- certify, publish, unpublish, or archive result revisions
- merge model aliases
- lock or archive seasons
- rotate fixture versions
- regenerate result cards, exports, and charts
- open correction, appeal, incident, or reanalysis records

## Controls

Every operation requires role authorization, preview of affected records,
explicit reason, idempotency key when applicable, dry-run mode for bulk actions,
and audit log entry. Destructive or public-facing actions require confirmation
and may require two-maintainer approval.

## Safety

Admin tools must prefer reversible state transitions. Direct deletion of public
records is disallowed except through documented takedown flow with tombstones.
Bulk operations must provide progress, cancelation, and rollback notes.

## UX

Admin screens should show queue health, stuck runs, failed imports, security
holds, evaluator backlog, pending appeals, stale aliases, and season readiness
checks. Actions should be close to the affected record but never hidden behind
ambiguous icon-only controls.

## Research Basis

MLCommons benchmark management motivates explicit working-group style rule and
submission operations. OWASP authorization and logging guidance motivates
server-side permission checks and auditability for administrative actions.

## QA Pass

Checked against `access-control.md`, `ingestion-pipeline.md`,
`official-result-certification.md`, `leaderboard-seasons.md`, and incident/
appeals backlog entries. This spec defines operations, not maintainer staffing.
