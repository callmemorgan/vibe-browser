# Model Comparison Report

## Purpose

Model comparison reports compare model behavior within a fixed benchmark
season and comparability group. They make model differences legible while
preventing overbroad claims from a narrow task.

## Comparison Preconditions

- same benchmark season and track
- same prompt and harness profile unless explicitly framed as an ablation
- compatible time, resource, and intervention limits
- certified or clearly labeled provisional runs
- enough samples to discuss variance
- disclosed provider, model, model version, and pricing snapshot

## Required Metrics

Reports include rank distribution, blended score, highest milestone reached,
public and hidden check outcomes, evaluator confidence, failure classes, wall
clock time, token usage, estimated cost, and artifact completeness.

## Analysis Requirements

Separate central tendency from best run. Show uncertainty, sample count, and
non-comparable exclusions. Discuss qualitative differences such as planning,
tool use, recovery, and test discipline only when supported by evidence.

## Claim Boundaries

Use language such as "on Vibe Browser Benchmark season X under profile Y."
Avoid declaring one model generally better at software engineering or browser
building without supporting studies.

## Research Basis

HELM motivates multi-metric model comparison with transparent prompts,
scenarios, and limitations. MLCommons motivates comparable submissions under
defined rules before ranking systems against each other.

## QA Pass

Checked against `comparison-eligibility-rules.md`,
`model-and-tool-identity.md`, `score-interpretation-guide.md`,
`qualitative-run-analysis.md`, and `cost-and-efficiency-metrics.md`. This spec
defines model reporting, not the leaderboard table itself.
