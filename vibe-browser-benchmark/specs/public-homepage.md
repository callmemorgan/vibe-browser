# Public Homepage

## Purpose

The public homepage introduces Vibe Browser Benchmark, routes readers to the
leaderboard and methodology, and makes the benchmark's caveats visible before a
reader sees any rank.

## First View

Show:

- benchmark name
- one-sentence thesis: coding agents build a browser under controlled profiles
- latest official season
- top comparable result with season and track
- links to leaderboard, methodology, submit guide, public data, and artifacts
- prominent caveat that rank only applies within comparable groups

The first viewport should not be a marketing splash detached from the benchmark.
It should lead with actual benchmark state.

## Core Sections

- **What is measured**: milestone ladder, evidence, evaluator-confirmed score,
  cost/time metrics.
- **Latest results**: compact table or chart with official-ranked results only.
- **How comparison works**: profile, prompt, runtime, and intervention
  compatibility.
- **How to run it**: link to submission guide and local dry-run command.
- **Open data and artifacts**: links to exports, result cards, and retention
  policy.
- **Trust and caveats**: contamination, provider drift, hidden tests,
  reanalysis, appeals, and public trust dashboard once available.

## Public Claims

Avoid unsupported "best model" copy. Use scoped phrases like "top official run
in `2026-smoke-v0/open-ended`." If no official result exists, show a clear
pre-launch state instead of placeholder ranks.

## Research Basis

MLCommons motivates fair comparison, reproducibility, commercial/research
utility, and affordability. Leaderboard-operations research warns that weak
documentation and unclear comparison rules reduce transparency and trust.

## QA Pass

Checked against `product-brief.md`, `benchmark-charter.md`,
`benchmark-card.md`, `leaderboard-seasons.md`, and `public-leaderboard-page.md`.
This spec defines public entry content, not visual brand styling.
