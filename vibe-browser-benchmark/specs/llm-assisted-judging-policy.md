# LLM-Assisted Judging Policy

## Purpose

LLM-assisted judging policy defines if and how model judges may help evaluators
summarize evidence, prefill rubrics, or detect inconsistencies.

## Allowed Uses

- summarize public-safe timelines
- extract evidence links
- prefill rubric drafts
- flag missing artifacts
- compare evaluator notes for inconsistency
- draft failure-mode summaries for human review

## Disallowed Uses

LLM judges must not assign final official scores, view hidden-test details
without authorization, override human adjudication, or create public claims
without review.

## Disclosure

Records include judge model, prompt version, input scope, output, human
reviewer, accepted fields, rejected fields, and known limitations.

## Controls

Use sampling audits, hallucination checks, evidence-link validation, and human
override. Judge outputs are advisory unless a future season explicitly defines
a test-grounded automated scoring role.

## Research Basis

NIST AI RMF motivates human oversight, measurement transparency, and risk
management for AI-assisted evaluation. HELM motivates transparent release of
prompts and evaluation conditions where safe.

## QA Pass

Checked against `evaluator-workflow.md`, `evaluator-calibration.md`,
`qualitative-run-analysis.md`, `ethics-and-disclosure.md`, and
`manual-audit-sampling.md`. This spec defines assistant use, not a judge model
choice.
