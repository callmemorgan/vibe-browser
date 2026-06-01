# Vibe Browser Benchmark UI Specs

This folder describes a leaderboard UI for comparing Vibe Browser benchmark
runs. The product should make model progress legible without hiding the
engineering evidence behind a single score.

## Spec Index

- [Product Brief](product-brief.md): audience, goals, and non-goals.
- [Leaderboard UX](leaderboard-ux.md): primary screens, filters, states, and
  interactions.
- [Run Detail UX](run-detail-ux.md): evidence view for a single benchmark run.
- [Data Model](data-model.md): canonical entities and fields.
- [Scoring and Ranking](scoring-and-ranking.md): ranking rules and comparison
  guardrails.
- [Milestone Rubrics](milestone-rubrics.md): per-milestone scoring dimensions.
- [Blended Score](blended-score.md): combined progress and quality score.
- [Completed Specs](specs/README.md): standalone specs expanded from backlog
  entries.
- [Spec Status](spec-status.md): progress tracker and next recommended batch.
- [Corpus Map](distilled/corpus-map.md): distilled navigation guide for keeping
  context small as the corpus grows.
- [Spec Backlog](spec-backlog.md): additional benchmark, governance, public
  site, and operations specs still worth writing.
- [Final Gap Analysis](final-gap-analysis.md): last-pass blind spots before the
  benchmark graduates from leaderboard product to public benchmark program.

## Design Principles

- Evidence first: every score links back to commands, logs, artifacts, or
  evaluator notes.
- Comparability is explicit: do not rank runs together when profile, target,
  prompt set, benchmark commit, or intervention policy differ.
- Partial progress matters: open-ended runs should show the highest claimed,
  public-check, and evaluator-confirmed milestone.
- Honest limitations are a feature: blockers and unsupported behavior should be
  visible, not buried.
- Operational UI, not marketing: dense tables, clear filters, stable metrics,
  and fast drill-downs.
