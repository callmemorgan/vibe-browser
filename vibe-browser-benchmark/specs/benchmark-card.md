# Benchmark Card

## Purpose

The benchmark card is the public one-page disclosure for a benchmark version or
season. It should let a reader understand what the benchmark is for, how results
are produced, and which caveats apply before trusting a leaderboard position.

## Required Fields

- `benchmark_name`: `Vibe Browser Benchmark`.
- `benchmark_version`: semantic benchmark version, such as `0.1.0`.
- `season`: immutable season identifier, such as `2026-smoke-v0`.
- `maintainers`: people or organizations responsible for the release.
- `intended_use`: comparing coding-agent progress on this benchmark under
  declared profiles.
- `out_of_scope_use`: hiring, procurement decisions without reanalysis, claims
  about full browser conformance, or claims about model quality independent of
  the agent harness.
- `task_summary`: milestone ladder, run modes, and official profiles.
- `data_sources`: local fixtures, public web specs, generated artifacts,
  evaluator scores, and optional WPT-derived evidence.
- `scoring_summary`: milestone depth, rubric quality, blended score, efficiency
  metrics, and non-comparable labels.
- `hidden_tests`: whether hidden checks exist, what they measure, and what
  feedback they provide.
- `known_limitations`: contamination risk, provider drift, evaluator
  subjectivity, task representativeness, and harness/tool differences.
- `publication_policy`: which artifacts are public, redacted, private, or
  embargoed.
- `citation`: stable URL, checksum, release date, and citation text.

## Layout

The card should render as a public page and as machine-readable JSON. The page
view should prefer short sections, direct links to methodology, and a compact
"can I compare these results?" checklist.

The JSON view should use stable keys so papers and external leaderboards can
record exactly which benchmark definition produced a result.

## Update Rules

Patch-level changes may clarify language or fix broken links. Minor changes may
add optional metadata or docs. Major changes alter score meaning, official
profiles, hidden-check scope, or comparability rules and require a new season.

## Research Basis

The shape borrows from model cards
(`https://arxiv.org/abs/1810.03993`) and datasheets for datasets
(`https://arxiv.org/abs/1803.09010`): state intended use, limitations,
evaluation procedures, provenance, and recommended/non-recommended uses.

## QA Pass

Checked against `benchmark-charter.md`, `scoring-and-ranking.md`, and
`final-gap-analysis.md`. This spec defines benchmark-level disclosure only;
individual runs use `result-card.md`.
