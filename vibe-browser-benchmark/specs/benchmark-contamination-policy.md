# Benchmark Contamination Policy

## Purpose

The contamination policy explains how the benchmark handles models, prompts, or
agents that may have seen benchmark docs, prior submissions, fixtures, or hidden
tests during training or evaluation.

## Contamination Classes

- `unknown`: no disclosure or insufficient evidence.
- `public-docs`: benchmark docs or public results likely seen.
- `public-submissions`: prior public artifacts likely seen.
- `prompt-aware`: exact prompt or harness wrapper likely seen.
- `fixture-aware`: public fixtures likely seen.
- `hidden-leak`: hidden tests or private artifacts exposed.

## Disclosure Fields

Run metadata records known training cutoff, provider disclosure, model release
date, participant disclosure, benchmark material exposure, and maintainer
confidence level.

## Ranking Effects

Public-docs exposure does not automatically disqualify a run. Hidden-test leaks
or private artifact exposure require security hold and may invalidate affected
results. High contamination risk can create separate comparison groups.

## Mitigations

Use seasons, fixture rotation, hidden variants, calibration checks, and
contamination labels. Avoid claiming clean generalization when contamination is
unknown or plausible.

## Research Basis

HELM motivates transparent reporting of evaluation conditions and limitations.
Benchmark-overfitting research motivates contamination labels, private
holdouts, and refreshed evaluation material.

## QA Pass

Checked against `model-and-tool-identity.md`, `hidden-test-policy.md`,
`comparison-eligibility-rules.md`, `score-interpretation-guide.md`, and
`ethics-and-disclosure.md`. This spec defines contamination handling, not model
training audits.
