# Test Run Result Sharing

## Purpose

Test run result sharing lets maintainers and participants share smoke tests,
dry runs, failed harness experiments, and unofficial reruns without making them
look like official leaderboard results.

## Shareable States

- `local-dry-run`: produced outside official infrastructure.
- `smoke-test`: short harness verification or development run.
- `provisional-submission`: uploaded but not evaluated or certified.
- `failed-run`: useful negative evidence or debugging artifact.
- `unofficial-rerun`: replay by a third party or different profile.
- `admin-debug`: internal diagnostic run, private by default.

## Required Banners

Every shared non-official page must show a persistent banner with state, reason
not ranked, retention window, artifact visibility, and whether it can become
official.

## Expiration and Retention

Smoke and debug shares expire by default unless promoted to retained artifacts.
Failed and unofficial reruns may remain public when redacted and useful for
analysis, but never acquire official rank without certification.

## URLs and Embeds

Share URLs are stable while retained. Embeds and badges for non-official results
must include "not ranked" or the exact provisional state.

## Research Basis

MLPerf submission guidance separates unofficial submissions from official
submission processes and uses submission checkers before final upload. CodeSOTA
motivates visible source tiers such as reproduced, paper, or vendor-reported.

## QA Pass

Checked against `public-run-result-page.md`, `official-result-certification.md`,
`artifact-retention-policy.md`, `result-embeds-and-badges.md`, and
`failure-classification.md`. This spec owns sharing state, not final scoring.
