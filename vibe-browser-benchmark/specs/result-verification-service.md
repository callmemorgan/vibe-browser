# Result Verification Service

## Purpose

The result verification service replays submitted artifacts in a controlled
environment and emits signed verification records. It gives maintainers a
repeatable path from submitted snapshot to certification evidence.

## Service Responsibilities

- accept an immutable submission snapshot
- create a clean workspace from the benchmark commit
- apply submitted files without private host state
- enforce resource, wall-clock, filesystem, and network policy
- serve deterministic public fixtures
- run configured build, smoke, public-check, GUI, WPT, and fuzz commands
- capture logs, metrics, exit codes, and artifacts
- generate verification results and failure classifications
- sign or attest the verification record

## Isolation

Verification runs in an approved container or equivalent isolated runtime.
Outbound network access is denied by default except for declared fixtures and
approved dependency mirrors. Host credentials and maintainer files are never
mounted.

## Caching

Dependency caches are allowed only when keyed by dependency lockfiles and
runtime profile. Cache hits must be recorded so reproducibility analysis can
distinguish cached and uncached verification.

## Output Record

The service writes `verification-record.json` with snapshot checksum, benchmark
commit, runtime image digest, command list, result IDs, log references,
resource usage, verifier version, timestamp, and signature metadata.

## Research Basis

SLSA provenance concepts motivate recording source, build, environment, and
attestation facts. Sigstore-style signing motivates verifiable records for
public artifact integrity.

## QA Pass

Checked against `verification-result-schema.md`, `trusted-execution-environment`
backlog scope, `official-result-certification.md`, `security-and-redaction.md`,
and `public-milestone-checker.md`. This spec defines replay service behavior,
not the full production deployment architecture.
