# Trusted Execution Environment

## Purpose

The trusted execution environment defines the runtime used for official
verification and reruns. It makes official results less dependent on a
maintainer laptop or undocumented host state.

## Environment Requirements

- pinned container image digest
- declared CPU, memory, disk, and timeout limits
- isolated filesystem with clean checkout
- no host credentials or private mounts
- default-deny outbound network policy
- deterministic fixture service
- captured stdout, stderr, logs, metrics, and artifacts
- explicit clock, locale, and timezone settings where relevant
- recorded runner version and host class

## Privilege Policy

Official replay should use the least privilege that can run the benchmark. Any
privileged container, admin capability, device mount, or network exception must
be justified in the verification record.

## Environment Identity

Every verification record includes image digest, runner version, benchmark
commit, resource profile, network profile, fixture registry version, and
execution timestamp.

## Drift Control

Runtime images are immutable once used for a season. Updates require release
notes, calibration-suite replay, and a season compatibility decision when
results could change.

## Research Basis

OCI image digest practice motivates immutable runtime identity. SLSA provenance
concepts motivate recording trusted environment facts for verifiable replay.

## QA Pass

Checked against `result-verification-service.md`, `reproducibility-contract.md`,
`official-result-certification.md`, `resource-accounting` backlog scope, and
`security-and-redaction.md`. This spec defines official replay environment,
not local participant setup.
