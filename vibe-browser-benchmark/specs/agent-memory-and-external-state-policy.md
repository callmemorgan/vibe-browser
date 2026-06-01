# Agent Memory and External State Policy

## Purpose

Agent memory and external state policy defines which persistent context an
agent may use and how stateful runs are disclosed.

## State Classes

- provider-side memory
- local memory files
- dependency caches
- previous benchmark artifacts
- public web retrieval
- private organization notes
- hidden-test leakage
- learned tool preferences
- self-hosted mirror state

## Disclosure Rules

Run metadata records allowed memory classes, known state sources, cache
identity, retrieval policy, and whether prior benchmark material may have been
visible.

## Eligibility Effects

Hidden-test exposure invalidates affected runs. Public-docs exposure may remain
ranked with contamination labels. Private prior-run memory can create a
separate stateful comparison group.

## Controls

Official runners should start from declared clean state unless a division is
specifically stateful. Caches must be described and checksum-bound where
possible.

## Research Basis

Benchmark contamination research motivates disclosure of prior exposure and
holdout leakage. NIST AI RMF transparency guidance motivates documenting system
context that affects evaluation.

## QA Pass

Checked against `benchmark-contamination-policy.md`,
`reproducibility-contract.md`, `comparison-eligibility-rules.md`,
`provider-drift-tracking.md`, and `hidden-test-policy.md`. This spec defines
state disclosure, not provider memory APIs.
