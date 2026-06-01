# Comparison Eligibility Rules

## Purpose

Eligibility rules decide which runs may appear in the same ranked comparison.
They protect the benchmark from false precision when runs differ in ways that
materially affect difficulty.

## Ranked Comparison Requirements

Runs are comparable only when all required fields match or are explicitly marked
compatible:

- benchmark commit and season
- target milestone or open-ended profile
- prompt set checksum
- wall clock and restart policy
- Docker image digest and runtime profile
- network and fixture-serving policy
- provider, model identity, and snapshot confidence class
- agent harness and tool capability class
- intervention policy
- hidden/public checker version
- scoring formula version
- baseline cleanliness and artifact completeness

## Non-Comparable Labels

Use precise labels instead of a single generic failure:

- `different-profile`
- `dirty-baseline`
- `guided-run`
- `unknown-model-snapshot`
- `tool-surface-mismatch`
- `provider-drift-risk`
- `incomplete-artifacts`
- `unofficial-rerun`
- `embargoed`
- `security-hold`
- `scoring-version-mismatch`

## Allowed Grouping

The UI may group non-comparable runs in exploratory tables when labels are
visible and ranking numbers are suppressed. For example, "all GLM 5.1 cloud
runs" can show score distributions without declaring a single official rank.

## Reanalysis

If a scoring bug, metadata correction, or provider drift investigation changes
eligibility, publish a reanalysis record and preserve the old label in history.

## Research Basis

MLCommons emphasizes fair comparison and reproducibility, while HELM motivates
standardized conditions and multi-metric transparency across shared scenarios.

## QA Pass

Checked against `scoring-and-ranking.md`, `blended-score.md`, final gap entries
for tool manifests and external state, and existing Docker benchmark docs. This
spec defines comparison grouping, not score formulas.
