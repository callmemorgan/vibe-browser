# Benchmark Charter

## Purpose

Vibe Browser Benchmark measures how far an autonomous coding agent can progress
toward a small, standards-aware browser implementation under a declared time,
tool, model, and environment profile. It is a benchmark of engineering behavior:
planning, implementation, testing, debugging, milestone judgment, and artifact
quality.

## What It Measures

- Functional browser capability across the milestone ladder in
  `milestone-rubrics.md`.
- Quality of implementation evidence: tests, logs, design notes, and runnable
  artifacts.
- Agent operating behavior: tool use, recovery from failures, cost, time, and
  scope control.
- Reproducibility: whether another evaluator can rerun the submitted artifact
  from the published snapshot.

## What It Does Not Measure

- General software engineering ability outside this browser task.
- Human developer productivity.
- Raw model intelligence independent of the agent harness and tool surface.
- Full web browser conformance; WPT coverage is a long-term signal, not the
  complete target.
- Safety of deployed browsers or production readiness.

## Design Principles

Evidence beats claims. A milestone claim is not official until backed by command
output, artifacts, and evaluator-confirmed behavior.

Comparisons require sameness. Runs must not share a ranked table unless their
benchmark commit, prompt profile, target, runtime profile, intervention policy,
and tool capability class are compatible.

Partial progress matters. Open-ended runs should expose the difference between
claimed, public-check, and evaluator-confirmed progress.

Transparency has boundaries. Public artifacts should be rich enough for
reanalysis, but hidden tests, secrets, private evaluator notes, and unsafe files
must stay protected.

## Change Authority

Maintainers may fix docs, schemas, and UI copy within a season. Changes to
scoring, hidden checks, official prompts, runtime profiles, or eligibility rules
require either a new season or a published reanalysis decision.

## Conflict Resolution

When goals conflict, use this order:

1. Protect hidden tests, secrets, and host infrastructure.
2. Preserve scientific comparability.
3. Preserve reproducibility and artifact integrity.
4. Publish useful partial progress.
5. Optimize ranking excitement or marketing value.

## Research Basis

This charter follows public benchmark patterns that emphasize broad measurement,
fair comparison, reproducibility, and transparent artifacts: HELM
(`https://arxiv.org/abs/2211.09110`), MLCommons
(`https://mlcommons.org/benchmarks/`), and ACM artifact badging
(`https://www.acm.org/publications/policies/artifact-review-and-badging-current`).

## QA Pass

This charter was checked against the existing product brief, scoring docs, final
gap analysis, and backlog. It is intentionally higher-level than the rubric and
does not duplicate the certification workflow.
