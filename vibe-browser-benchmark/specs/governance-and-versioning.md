# Governance and Versioning

## Purpose

Governance and versioning define how Vibe Browser Benchmark changes without
quietly invalidating results. The process should be light enough for a small
project and explicit enough for public trust.

## Roles

- **Maintainers** propose and approve benchmark changes.
- **Evaluators** advise on scoring, evidence, and calibration effects.
- **Security reviewers** approve publication-sensitive changes.
- **Participants** can file proposals, corrections, appeals, and replication
  reports.
- **Public readers** can inspect accepted decisions and release notes.

## Change Classes

- `patch`: docs, UI copy, non-ranking bug fixes.
- `minor`: new views, metrics, exports, or optional checks.
- `major`: scoring formula changes, milestone revisions, prompt changes,
  hidden-test policy changes, or eligibility changes that affect ranking.

## Proposal Flow

Every material change records problem, proposal, affected specs, compatibility
impact, season impact, migration plan, reviewer decision, and release-note link.
Major changes require a new season or explicit benchmark-card compatibility
statement.

## Version Rules

Harness and API releases use semantic versions. Seasons use immutable names.
Docs may change continuously, but public methodology snapshots used for a
season must remain addressable.

## Research Basis

W3C process norms motivate visible review, consensus-seeking, objections, and
appeal paths for standards-like work. Semantic Versioning motivates explicit
compatibility levels for machine-facing components.

## QA Pass

Checked against `benchmark-card.md`, `leaderboard-seasons.md`,
`release-notes-template.md`, `appeals-and-corrections` backlog scope, and
`official-result-certification.md`. This spec defines benchmark governance, not
staffing or funding.
