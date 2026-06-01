# Benchmark Meta-Evaluation

## Purpose

Benchmark meta-evaluation measures whether Vibe Browser Benchmark itself
remains useful, fair, reproducible, and trusted. It treats the benchmark as a
system that needs evaluation.

## Health Metrics

- correlation with independent engineering tasks
- sensitivity to model and harness improvements
- failure-mode diversity
- evaluator workload and agreement
- reproducibility rate
- appeal and correction rate
- hidden-test rotation health
- benchmark saturation
- contamination risk
- community trust indicators
- public data reuse

## Review Cadence

Run a meta-evaluation at season close and before major methodology changes.
Publish a public summary when findings affect interpretation, governance, or
future season design.

## Inputs

Use certified runs, failed runs, evaluator notes, appeals, replication reports,
incident records, public feedback, and external research comparisons.

## Outcomes

Outcomes can include new specs, retired tracks, revised milestones, calibration
changes, hidden-test rotation, scorer retraining, or benchmark sunset planning.

## Research Basis

NIST AI RMF measurement guidance motivates evaluating whether an AI evaluation
system remains valid for its intended use. Leaderboard-operations research
motivates monitoring transparency, reproducibility, and trust over time.

## QA Pass

Checked against `threats-to-validity.md`, `statistical-validity.md`,
`public-trust-dashboard` backlog scope, `benchmark-difficulty-tuning.md`, and
`governance-and-versioning.md`. This spec defines benchmark self-evaluation,
not a single season report.
