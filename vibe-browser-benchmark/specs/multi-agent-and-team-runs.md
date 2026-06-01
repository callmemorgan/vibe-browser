# Multi-Agent and Team Runs

## Purpose

Multi-agent and team run policy defines when a benchmark run may use multiple
agents, multiple humans, or orchestration layers. It protects single-agent
comparisons from hidden collaboration advantages.

## Run Classes

- `single-agent`: one agent process with normal tools.
- `multi-agent`: multiple agent roles or sub-agents coordinate.
- `human-guided`: humans provide substantive guidance during the run.
- `team-run`: multiple humans operate or direct the system.
- `orchestrated`: external planner, router, or supervisor coordinates agents.

## Required Disclosures

Disclose orchestration topology, agent roles, shared memory, prompts, model
identities, handoff rules, sub-agent logs, human interventions, and which
components can edit files.

## Ranking

Multi-agent and team runs rank separately from single-agent runs unless a
season explicitly defines a mixed track. Comparability rules must include
orchestration profile and intervention policy.

## Artifact Requirements

Artifact snapshots include per-agent timelines, shared-state records, handoff
events, and tool permissions where public-safe.

## Research Basis

NIST AI RMF human-AI configuration guidance motivates documenting roles,
responsibilities, and oversight. Multi-agent evaluation practice motivates
separating orchestration effects from model capability claims.

## QA Pass

Checked against `comparison-eligibility-rules.md`,
`interactive-intervention-audit.md`, `prompt-and-harness-registry.md`,
`timeline-and-telemetry-ux.md`, and `tracks-and-divisions` backlog scope. This
spec defines grouping and disclosure, not orchestration APIs.
