# Sandbox Escape and Host Safety

## Purpose

Sandbox escape and host safety define how official infrastructure runs
untrusted agent-generated code while protecting hosts, credentials, networks,
and maintainers.

## Threats

- container escape
- privileged process abuse
- Docker socket access
- host filesystem overwrite
- credential exfiltration
- private network scanning
- resource exhaustion
- malicious dependency scripts
- unsafe artifacts
- persistence after run completion

## Required Controls

Use isolated runtime profiles, least privilege, no host credentials, no Docker
socket mounts, constrained capabilities, read-only mounts where possible,
network egress policy, resource limits, artifact scanning, and emergency kill
switches.

## Host Hygiene

Runner hosts are patched, disposable where feasible, monitored, and separated
from maintainer personal machines. Secrets needed for provider access are
scoped, rotated, and never mounted into submitted code unless a profile
explicitly requires them.

## Incident Triggers

Suspected escape, persistence, exfiltration, or host compromise triggers
incident response, run quarantine, credential rotation, and affected-season
review.

## Research Basis

NIST container security guidance motivates securing images, registries,
orchestrators, containers, and host OS layers. OWASP Docker security guidance
motivates least privilege, avoiding Docker socket exposure, and host hardening.

## QA Pass

Checked against `trusted-execution-environment.md`,
`security-review-for-published-artifacts.md`, `incident-response.md`,
`network-and-fixture-serving.md`, and `dependency-mirror-and-supply-chain.md`.
This spec defines host safety policy, not a complete hardening checklist.
