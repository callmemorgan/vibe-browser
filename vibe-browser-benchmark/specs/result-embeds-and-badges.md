# Result Embeds and Badges

## Purpose

Embeds and badges let projects, posts, and vendor pages reference benchmark
results while preserving scope, season, and verification status.

## Badge Types

- official score badge
- milestone badge
- certification status badge
- replication status badge
- not-ranked/provisional badge
- season-stale badge

## Required Badge Content

Badges must include benchmark name or short code, season, track/profile when
space permits, score or milestone, and status. Hover/title text or linked
destination must disclose full result URL and eligibility.

## Embed Card

Embed cards show model, agent, season, score, confirmed milestone, rank scope,
certification state, caveats, and links to result card JSON and artifacts.
Cards must render in light/dark mode, fit narrow widths, and remain legible in
screenshots.

## Anti-Staleness

Badges resolve dynamically to current metadata for the result revision. If a
season is archived, corrected, or superseded, the badge shows stale/corrected
state rather than preserving an old winning claim.

## Research Basis

Shields.io motivates concise, consistent, legible badges that can be included in
README files and web pages. Public benchmark registries motivate source and
verification labels on shared results.

## QA Pass

Checked against `result-card.md`, `public-run-result-page.md`,
`test-run-result-sharing.md`, `leaderboard-seasons.md`, and public claims review
backlog. This spec defines badge semantics, not final visual design.
