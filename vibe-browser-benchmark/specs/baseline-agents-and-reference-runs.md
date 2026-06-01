# Baseline Agents and Reference Runs

## Purpose

Baseline agents and reference runs anchor benchmark difficulty. They show what
simple, scripted, manual, and canonical agent approaches achieve under each
season profile.

## Baseline Types

- no-op shell baseline
- scripted fixture-only baseline
- minimal hand-written milestone baseline
- simple local model baseline
- official harness baseline
- previous-season best rerun
- human reference run where available
- intentionally flawed anti-gaming baseline

## Required Fields

Each baseline records purpose, owner, source, season, track, runtime profile,
model or non-model identity, allowed tools, expected score, expected failure
classes, artifact checksum, and rerun cadence.

## Usage

Baselines run before season launch, after scoring changes, after verifier
changes, and before major public claims. Baseline regressions require
maintainer review before new official results are published.

## Display

Leaderboards may include baselines in a separate section or filter. Baselines
should never be confused with competitive participant submissions.

## Research Basis

MLCommons benchmark practice motivates reference systems and comparable
baselines. ACM artifact review practice motivates preserving inspectable
artifacts for evaluated claims.

## QA Pass

Checked against `calibration-suite.md`, `benchmark-difficulty-tuning.md`,
`leaderboard-seasons.md`, `statistical-validity.md`, and
`public-leaderboard-page.md`. This spec defines baseline runs, not scoring
weights.
