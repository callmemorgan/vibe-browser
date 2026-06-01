# Deceptive or Unsafe Submission Handling

## Purpose

Deceptive or unsafe submission handling defines how maintainers respond to
submissions that intentionally mislead the benchmark or endanger systems,
readers, or maintainers.

## Unsafe Patterns

- fake browser engine or fabricated artifacts
- benchmark sabotage
- hidden-test exfiltration
- credential theft attempt
- cryptomining or resource abuse
- malware or persistence
- license laundering
- forged verification records
- deceptive dependency use
- prompt-injection payload targeting evaluators

## Response Options

Maintainers may quarantine artifacts, reject the run, suspend hosted access,
open an incident, rotate secrets or fixtures, notify affected parties, and add
public disclosure when public trust is affected.

## Evidence Handling

Unsafe evidence is preserved privately with access controls. Public summaries
describe category and impact without publishing exploit instructions.

## Participant Process

Accidental unsafe behavior can receive a remediation path. Intentional abuse can
lead to rejection, account restrictions, and public policy notes.

## Research Basis

NIST incident handling guidance motivates evidence preservation and severity
response. OWASP file upload and container security guidance motivates
quarantine, scanning, and safe handling of dangerous artifacts.

## QA Pass

Checked against `security-review-for-published-artifacts.md`,
`sandbox-escape-and-host-safety.md`, `incident-response.md`,
`anti-overfitting-and-anti-gaming.md`, and
`submission-abuse-and-rate-limits` backlog scope. This spec defines response
policy, not malware reverse engineering.
