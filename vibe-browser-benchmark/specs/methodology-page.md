# Methodology Page

## Purpose

The methodology page explains how Vibe Browser Benchmark measures progress,
how scoring works, what is comparable, and which limitations readers should
consider before interpreting results.

## Required Sections

- benchmark thesis and task definition
- milestone ladder M0-M9
- run modes: targeted, open-ended, smoke, endurance
- official profiles and runtime constraints
- prompt/harness registry and versioning
- public vs hidden checks
- evaluator workflow and evidence requirements
- scoring formula and calibration
- comparison eligibility
- artifact retention and redaction
- reproducibility and certification
- known limitations and threats to validity
- governance, seasons, appeals, corrections, and reanalysis

## Tone

The page should be precise and humble. It should say what the benchmark can
support and what it cannot support. Avoid prose that turns leaderboard position
into broad claims about model intelligence or production browser readiness.

## Diagrams and Tables

Include milestone ladder, run lifecycle, certification gates, score formula,
and comparable-vs-non-comparable examples. Every figure should have a text
equivalent and link to the underlying spec.

## Research Basis

HELM motivates broad, multi-metric evaluation and transparent release of prompts
and outputs where safe. MLCommons motivates fair comparison, reproducibility,
useful measurement, and clear submission rules.

## QA Pass

Checked against `benchmark-charter.md`, `benchmark-card.md`,
`milestone-rubrics.md`, `blended-score.md`,
`comparison-eligibility-rules.md`, and `leaderboard-seasons.md`. This spec
defines public explanation, not formal scoring schemas.
