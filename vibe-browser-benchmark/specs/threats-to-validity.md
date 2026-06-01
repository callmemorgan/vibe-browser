# Threats to Validity

## Purpose

Threats to validity define the standard limitations section for methodology
pages, reports, papers, and public claims. It keeps the benchmark honest about
what evidence can and cannot prove.

## Required Threat Categories

- model contamination
- provider drift
- harness mismatch
- evaluator subjectivity
- hidden-test brittleness
- fixture representativeness
- task overfitting
- dependency and language bias
- environment drift
- small sample size
- publication bias toward successful runs
- browser-task representativeness

## Evidence Requirements

Each report identifies which threats are material to its claim, what mitigation
exists, what remains unresolved, and whether the threat affects ranking,
generalization, reproducibility, or public interpretation.

## Public Language

Use concrete statements such as "this season compares agents under one Docker
profile" rather than vague caveats. Threats should be visible near headline
charts and result summaries.

## Research Basis

NIST AI RMF motivates validity, transparency, and risk communication for AI
measurement. HELM motivates explicit scenario limitations and cautious
interpretation of benchmark results.

## QA Pass

Checked against `methodology-page.md`, `white-paper-outline.md`,
`statistical-validity.md`, `benchmark-contamination-policy.md`, and
`provider-drift-tracking.md`. This spec defines limitation categories, not a
specific paper's final prose.
