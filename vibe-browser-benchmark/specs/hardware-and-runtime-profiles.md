# Hardware and Runtime Profiles

## Purpose

Hardware and runtime profiles define the machine, container, OS, and resource
limits used by official runs and verification.

## Profile Fields

- profile ID and version
- CPU architecture and count
- memory limit
- disk limit
- GPU availability
- OS and kernel family
- container runtime
- runtime image digest
- timeout policy
- network profile
- fixture service version
- allowed privileged operations
- measurement capabilities

## Profile Classes

Use separate profiles for local smoke runs, official short runs, endurance
runs, GUI-capable verification, WPT-heavy runs, and resource-constrained tracks.

## Compatibility

A profile change that can affect results requires release notes, calibration
suite replay, and season compatibility decision. Run pages must show the exact
profile used.

## Resource Enforcement

Profiles declare hard limits and measured limits separately. Exceeding a hard
limit creates a verification result and failure classification.

## Research Basis

Kubernetes resource-management documentation motivates explicit resource
requests and limits. MLCommons benchmark practice motivates fixed hardware and
runtime rules for comparable submissions.

## QA Pass

Checked against `trusted-execution-environment.md`, `resource-accounting.md`,
`tracks-and-divisions.md`, `result-verification-service.md`, and
`leaderboard-seasons.md`. This spec defines runtime profiles, not cloud vendor
selection.
