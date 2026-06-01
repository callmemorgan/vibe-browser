# Security and Redaction

## Purpose

Security and redaction protect secrets, hidden tests, private metadata, and host
systems while preserving enough evidence for useful public benchmark analysis.

## Sensitive Data Classes

Redaction must detect and classify:

- API keys, access tokens, passwords, cookies, private keys, and certificates
- provider account IDs, billing IDs, and request IDs where sensitive
- local usernames, home directories, hostnames, and private network endpoints
- hidden test names, hidden fixture paths, exact hidden assertions, and hidden
  expected outputs
- private evaluator notes and embargoed scores
- unsafe scripts, binaries, symlinks, device files, and oversized artifacts

## Redaction Pipeline

1. Scan raw snapshot files before public preview.
2. Apply deterministic masking for known secret patterns.
3. Replace hidden-test details with category-level summaries.
4. Mark non-redactable unsafe artifacts as private or quarantine.
5. Generate `redaction-report.json` with findings, decisions, and reviewer.
6. Block certification until required redaction gates pass.

## Publication Rules

Public pages may show redacted snippets, summaries, file names, hashes, and
evidence IDs. They must not expose raw hidden-test feedback, secrets, unsafe
downloadables, or private provider metadata.

## Log Safety

The ingestion and runner systems must sanitize log output, prevent log
injection, use access controls for stored logs, and test behavior when logging
fails or storage fills.

## Research Basis

OWASP Logging guidance identifies data that should not be recorded directly and
requires sanitization, access controls, and log-system verification. The NIST
Privacy Framework motivates managing privacy risk in data processing systems.

## QA Pass

Checked against `artifact-retention-policy.md`, `evidence-model.md`,
`submission-snapshot-format.md`, `official-result-certification.md`, and hidden
test backlog entries. This spec defines policy and gates, not scanner regexes.
