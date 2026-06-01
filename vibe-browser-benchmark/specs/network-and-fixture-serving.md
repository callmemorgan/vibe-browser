# Network and Fixture Serving

## Purpose

Network and fixture serving define the official network environment for runs,
public checks, and verification.

## Network Modes

- `offline`: no outbound network except local fixture service.
- `fixture-only`: access to benchmark fixture hosts and dependency mirror.
- `limited-online`: approved package registries or provider endpoints.
- `open-network`: experimental and non-comparable unless a division allows it.

## Fixture Service

Fixture records include hostnames, ports, TLS behavior, DNS behavior, response
checksums, expected failure modes, hidden variants, and fixture registry
version.

## Controls

Outbound access uses allowlists, DNS controls, blocked private ranges,
metadata-endpoint blocking, request logging, and per-run network summaries.

## Comparability

Network mode is part of the comparison profile. A run with broader network
access cannot silently rank beside fixture-only runs.

## Research Basis

OWASP SSRF prevention guidance motivates allowlists and protection for private
network ranges. Web Platform Tests practice motivates controlled test servers
and named test hosts.

## QA Pass

Checked against `fixture-registry.md`, `public-milestone-checker.md`,
`trusted-execution-environment.md`, `comparison-eligibility-rules.md`, and
`security-and-redaction.md`. This spec defines network policy, not individual
fixture content.
