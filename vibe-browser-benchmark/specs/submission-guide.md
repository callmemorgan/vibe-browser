# Submission Guide

## Purpose

The submission guide helps a participant run the benchmark, understand whether
their result can be official, and prepare artifacts for review.

## Required Sections

- benchmark overview and intended audience
- official vs local/unofficial runs
- prerequisites: Docker, supported host OS, provider credentials, disk budget,
  network policy, and supported harnesses
- quickstart command for local dry run
- official submission workflow
- artifact checklist
- eligibility checklist
- redaction and privacy expectations
- common failures and troubleshooting
- support and appeal channels

## Workflow

1. Choose season, track, target/run mode, provider, model, and harness.
2. Run local dry check.
3. Run official or submission-producing benchmark command.
4. Review generated snapshot locally.
5. Upload snapshot or submit run ID.
6. Wait for ingestion, public check, evaluator review, and certification.
7. Inspect result page and appeal or correct metadata if needed.

## Eligibility Checklist

The guide must ask participants to confirm clean baseline, exact model/provider,
no hidden-test access, no human guidance outside allowed policy, allowed
dependencies, complete artifacts, and acceptance of artifact publication terms.

## Research Basis

MLPerf's submission guide motivates explicit prerequisites, setup, run,
validation, result structuring, checker, tarball, upload, troubleshooting, and
support sections.

## QA Pass

Checked against `submission-snapshot-format.md`, `ingestion-pipeline.md`,
`official-result-certification.md`, `comparison-eligibility-rules.md`, and
`test-run-result-sharing.md`. This spec defines participant docs, not runner
implementation.
