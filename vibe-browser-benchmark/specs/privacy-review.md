# Privacy Review

## Purpose

Privacy review prevents public benchmark artifacts from exposing personal data,
private machine details, provider identifiers, or sensitive operational
metadata.

## Review Scope

- local usernames and home paths
- hostnames and private network names
- provider account, billing, or request identifiers
- API keys, cookies, and tokens
- email addresses or names in logs
- private repository paths
- maintainer or evaluator notes
- screenshots containing private data
- telemetry fields that can identify a person or machine

## Review Flow

Privacy checks run before public preview, certification, data export, DOI
publication, and report publication. Findings are recorded in a privacy review
record with action, reviewer, timestamp, and affected artifacts.

## Redaction Rules

Mask sensitive values deterministically when evidence remains useful. Quarantine
artifacts when masking would mislead readers or leave residual private data.

## Public Guarantees

Public pages should describe privacy review scope and acknowledge that published
artifacts are redacted evidence, not complete raw transcripts.

## Research Basis

The NIST Privacy Framework motivates identifying and managing privacy risk in
data processing. OWASP logging guidance motivates avoiding sensitive data in
logs and controlling access to retained records.

## QA Pass

Checked against `security-and-redaction.md`, `artifact-retention-policy.md`,
`public-data-export.md`, `artifact-explorer.md`, and
`ethics-and-disclosure.md`. This spec defines privacy review, not secret
scanner implementation.
