# Provenance and Signing

## Purpose

Provenance and signing make official results tamper-evident. Readers should be
able to verify that a public result, artifact bundle, or report corresponds to
the certified run record.

## Signed Objects

- submission snapshot manifest
- verification record
- official result card
- certification revision
- public data export
- technical report input manifest
- runtime image digest list
- evaluator signoff bundle

## Required Provenance Fields

Each signed record includes object type, object digest, benchmark commit,
season, run ID, verifier version, runtime image digest, artifact checksums,
creation time, signer identity, signature method, and supersedes links.

## Verification UX

Public pages expose a compact verification status and a downloadable
verification bundle. Command-line examples should verify digest, signature,
signer identity, and transparency-log inclusion where supported.

## Key And Identity Policy

Signing identities are tied to maintainer or CI roles. Key rotation, revoked
credentials, and compromised signing workflows create incident records and may
force re-signing or result withdrawal.

## Research Basis

SLSA provenance motivates recording source, build, builder, and artifact facts
for downstream verification. Sigstore and Cosign motivate identity-based
signing, timestamps, and transparency-log backed verification.

## QA Pass

Checked against `result-verification-service.md`,
`trusted-execution-environment.md`, `official-result-certification.md`,
`public-data-export.md`, and `incident-response.md`. This spec defines signed
records, not a mandatory signing vendor.
