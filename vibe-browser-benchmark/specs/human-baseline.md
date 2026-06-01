# Human Baseline

## Purpose

The human baseline defines how a calibrated person or team can attempt the
benchmark for context. It should help interpret difficulty without turning the
benchmark into an employment test.

## Baseline Profiles

- individual engineer, short timebox
- individual engineer, full-day timebox
- small team, documented collaboration
- expert reference implementation attempt
- evaluator walkthrough of milestone feasibility

## Required Disclosures

Human baseline records include participant skill summary, time budget, allowed
references, tool access, collaboration rules, breaks, hardware profile,
starting commit, produced artifacts, and evaluator relationship.

## Scoring

Human baselines use the same milestone evidence requirements where feasible,
but appear in a separate public section. They do not rank against agent runs
unless a track explicitly defines human comparison.

## Ethics

Do not publish identifiable performance details without consent. Avoid framing
human scores as hiring signals or as proof that a model is generally better
than people.

## Research Basis

NIST AI RMF human-factors framing motivates care around human-AI evaluation and
interpretation. SWE-bench Verified discussions motivate human review for task
feasibility while recognizing that human baselines need careful context.

## QA Pass

Checked against `baseline-agents-and-reference-runs.md`,
`milestone-evidence-requirements.md`, `ethics-and-disclosure.md`,
`statistical-validity.md`, and `privacy-review.md`. This spec defines human
context runs, not hiring assessment.
