# Prompt Injection and Malicious Content Fixtures

## Purpose

Prompt injection and malicious content fixtures define how the benchmark tests
browser-agent robustness against hostile pages, scripts, and instructions.

## Fixture Types

- prompt-injection web pages
- deceptive user-visible instructions
- malicious HTML or JavaScript
- exfiltration attempts
- unsafe downloads
- cross-origin traps
- fake benchmark guidance
- credential or hidden-test bait

## Safety Rules

Malicious fixtures run only in isolated profiles. They must not contact real
external targets, execute outside the sandbox, or expose maintainers to unsafe
downloads during review.

## Scoring Use

Fixtures can be public, hidden, or security-only. Public methodology describes
threat categories without revealing hidden fixture payloads.

## Evidence

Evidence includes fixture ID, threat category, expected safe behavior, observed
behavior, redacted logs, and artifact safety decision.

## Research Basis

OWASP LLM Top 10 identifies prompt injection as a major risk for LLM
applications. OWASP file and container safety guidance motivates safe handling
of malicious artifacts.

## QA Pass

Checked against `hidden-test-policy.md`, `network-and-fixture-serving.md`,
`security-review-for-published-artifacts.md`, `sandbox-escape-and-host-safety.md`,
and `fixture-registry.md`. This spec defines hostile fixture policy, not exact
payloads.
