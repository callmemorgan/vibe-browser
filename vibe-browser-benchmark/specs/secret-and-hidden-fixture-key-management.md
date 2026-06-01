# Secret and Hidden Fixture Key Management

## Purpose

Secret and hidden fixture key management defines how hidden tests, fixture
secrets, signing keys, and provider credentials are protected and rotated.

## Secret Classes

- hidden fixture archives
- hidden expected outputs
- fixture TLS private keys
- provider credentials
- signing keys
- evaluator-only access tokens
- storage credentials
- incident recovery credentials

## Controls

Secrets use least privilege, access logging, rotation schedule, revocation path,
separate storage from public artifacts, and emergency rotation after suspected
leak.

## Runner Injection

Secrets are injected only into profiles that require them, scoped to a run, and
never persisted in submission artifacts. Logs are scanned for accidental
exposure.

## Leak Response

Leaks trigger incident response, fixture rotation, affected-run review, and
season compatibility decision.

## Research Basis

NIST key-management guidance motivates key lifecycle, cryptoperiod, revocation,
and protection policies. OWASP logging guidance motivates avoiding secret
exposure in logs and artifacts.

## QA Pass

Checked against `hidden-test-policy.md`, `security-and-redaction.md`,
`incident-response.md`, `trusted-execution-environment.md`, and
`provenance-and-signing.md`. This spec defines key-management requirements, not
secret storage tooling.
