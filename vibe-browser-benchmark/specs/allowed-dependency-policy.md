# Allowed Dependency Policy

## Purpose

The allowed dependency policy defines which libraries are acceptable in
benchmark submissions and how dependency choices affect comparability.

## Dependency Classes

- `allowed`: general-purpose standard libraries, UI toolkits, test frameworks,
  build tools, and small utilities.
- `disclose`: parsers, HTTP clients, TLS libraries, graphics libraries,
  JavaScript runtimes, layout helpers, and platform bindings.
- `restricted`: browser engines, full rendering engines, automation frameworks,
  or libraries that implement a scored milestone wholesale.
- `disallowed`: malware, credential harvesters, hidden-test tooling, unsafe
  downloaders, or dependencies that bypass benchmark intent.

## Disclosure Requirements

Submissions record dependency name, version, license, source, lockfile, install
method, and which milestone behavior it supports. Missing lockfiles reduce
reproducibility confidence.

## Review Rules

Dependency policy is evaluated by season and track. A dependency may be allowed
for one profile and restricted for another if it changes what the benchmark
measures.

## Security Review

External packages are scanned for known vulnerabilities, unsafe scripts,
unexpected binaries, and license issues before public artifact download.

## Research Basis

OpenSSF dependency and scorecard practices motivate supply-chain transparency
and package risk review. MLCommons division-style rules motivate separating
allowed implementation choices from shortcuts that invalidate comparison.

## QA Pass

Checked against `comparison-eligibility-rules.md`,
`anti-overfitting-and-anti-gaming.md`, `security-and-redaction.md`,
`submission-snapshot-format.md`, and `legal-and-licensing` backlog scope. This
spec defines policy classes, not a final package allowlist.
