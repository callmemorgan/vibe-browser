# Result Card

## Purpose

A result card is the compact public summary for one official or shareable run.
It should be embeddable, citeable, and clear about whether the result is ranked,
provisional, private, failed, or non-comparable.

## Required Fields

- `run_id`: stable run identifier.
- `result_url`: canonical public URL.
- `benchmark_version` and `season`.
- `track` and `run_mode`: targeted milestone, open-ended, smoke, endurance, or
  dry run.
- `model_identity`: provider, model, model version or alias, and snapshot
  confidence.
- `agent_identity`: harness, agent package, tool manifest, and version info.
- `runtime_profile`: hardware, Docker image digest, OS, network mode, and wall
  clock limit.
- `scores`: milestone reached, blended score, rubric score, efficiency metrics,
  and uncertainty labels.
- `eligibility`: ranked, official-unranked, provisional, non-comparable, or
  invalid.
- `artifacts`: submission snapshot, participant diff, logs, summary JSON,
  verification results, and redaction status.
- `replication_status`: not attempted, reproduced by maintainers, reproduced by
  third party, or reproduction failed.
- `limitations`: caveats specific to this run.

## Public States

Official ranked cards may appear in leaderboards. Provisional cards may be
linked but must carry a banner. Failed and negative-result cards should remain
useful by showing failure classification and available artifacts. Private and
embargoed cards must not leak score, rank, or artifact metadata outside allowed
roles.

## Embed Rules

Badges and embeds must include the season, track, score, eligibility, and last
verification date. Embeds older than the current season must display a stale
season marker rather than implying current rank.

## Serialization

Publish cards as JSON with immutable values after certification. Corrections
append a new revision record; they do not rewrite the historical card without an
audit trail.

## Research Basis

The compact disclosure format follows the same transparency goal as model cards
(`https://arxiv.org/abs/1810.03993`) and the artifact/result separation in ACM
artifact badging
(`https://www.acm.org/publications/policies/artifact-review-and-badging-current`).

## QA Pass

Checked against `benchmark-card.md`, `leaderboard-ux.md`, `run-detail-ux.md`,
and `comparison-eligibility-rules.md`. This spec intentionally points to other
artifact schemas instead of redefining their fields.
