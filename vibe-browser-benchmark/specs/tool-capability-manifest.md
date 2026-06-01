# Tool Capability Manifest

## Purpose

The tool capability manifest describes what an agent can do during a run. Tool
differences are first-class comparison inputs because they can change results as
much as model choice.

## Manifest Fields

- harness name and version
- shell access
- filesystem read/write scope
- Docker access
- network access
- browser or GUI tools
- image or document tools
- admin privileges
- approval prompts
- tool timeout defaults
- tool output truncation policy
- unavailable tools

## Capability Classes

Use stable classes such as `read-only`, `workspace-write`, `full-admin`,
`network-disabled`, `network-limited`, `browser-enabled`, and
`docker-enabled`.

## Comparison Effects

Runs compare only when tool manifests are compatible or when a division
explicitly allows differences. Public pages show tool capability summary near
model and harness identity.

## Verification

The runner records the effective manifest at run start and attaches it to the
submission snapshot.

## Research Basis

MLCommons rule practice motivates explicit system conditions before comparison.
NIST AI RMF transparency guidance motivates documenting AI system capabilities
and constraints.

## QA Pass

Checked against `prompt-and-harness-registry.md`,
`comparison-eligibility-rules.md`, `trusted-execution-environment.md`,
`multi-agent-and-team-runs.md`, and `interactive-intervention-audit.md`. This
spec defines manifest shape, not individual tool implementations.
