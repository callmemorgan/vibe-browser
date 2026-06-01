# Artifact Retention Policy

## Purpose

Artifact retention defines what the benchmark stores, for how long, with which
access level, and under what conditions artifacts are redacted, quarantined, or
discarded.

## Retention Classes

- `public-permanent`: result cards, certified summaries, public datasets,
  checksums, methodology pages, and published reports.
- `public-season`: redacted submission snapshots, public verification logs,
  participant diffs, screenshots, and public evidence objects.
- `private-review`: raw transcripts, raw provider logs, evaluator drafts,
  unredacted artifacts, and private redaction reports.
- `security-quarantine`: unsafe files, suspected secrets, malware, exfiltration
  attempts, and hidden-test leakage.
- `ephemeral`: intermediate build outputs, temporary containers, caches, and
  failed partial exports that are not needed for audit.

## Default Durations

Public certified records should be retained indefinitely or until a published
sunset plan replaces them. Public-season artifacts should be retained for the
life of the season plus at least five years. Private-review artifacts should be
retained only as long as needed for appeals, audits, and reproducibility, with a
default target of 18 months. Security-quarantine retention is incident-specific.
Ephemeral data should be removed after successful import or within 30 days.

## Access and Deletion

Retention class determines default access, but legal, privacy, security, or
licensing review may further restrict an artifact. Deletion of certified public
records requires a tombstone explaining what was removed and why.

## Storage Requirements

Immutable retained artifacts must have checksums and storage location metadata.
Compressed archives must be reproducible enough that checksum drift indicates a
real content change, not repacking.

## Research Basis

FAIR principles motivate persistent metadata and reuse, while NIST Privacy
Framework guidance motivates privacy-risk management for data processing. OWASP
logging guidance motivates strict access and exclusion of secrets from logs.

## QA Pass

Checked against `submission-snapshot-format.md`, `evidence-model.md`,
`official-result-certification.md`, and `security-and-redaction.md`. This spec
sets retention classes; it does not define scanner implementation.
