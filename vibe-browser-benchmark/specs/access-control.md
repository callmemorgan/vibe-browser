# Access Control

## Purpose

Access control determines who can view, evaluate, mutate, publish, download, or
administer benchmark records and artifacts.

## Roles

- `public`: anonymous reader of published pages and public exports.
- `submitter`: owner of submitted private/provisional runs.
- `evaluator`: can inspect assigned review artifacts and submit score sheets.
- `maintainer`: can manage runs, seasons, fixtures, aliases, and publication.
- `security-reviewer`: can inspect quarantine and redaction-sensitive artifacts.
- `admin`: can manage users, roles, and infrastructure settings.

## Resource Classes

Access decisions apply to seasons, runs, result cards, artifacts, evidence,
transcripts, hidden-test outputs, evaluator notes, redaction reports,
certification gates, admin actions, and API exports.

## Policy Rules

Default deny. Grant the least privilege required for the role and resource.
Perform authorization checks server-side for every API request and artifact
download. Do not rely on hidden UI controls. Treat static artifacts as protected
resources when they are private, embargoed, redacted, or quarantined.

## Auditing

Log authorization failures, artifact downloads, evaluator access, admin actions,
role changes, and security-quarantine access. Logs must avoid leaking secrets or
hidden-test content.

## Research Basis

OWASP Authorization guidance recommends least privilege, deny by default,
server-side checks, safe failure handling, and authorization logging. It also
warns against relying on client-side access control.

## QA Pass

Checked against `security-and-redaction.md`, `artifact-retention-policy.md`,
`api-contract.md`, `evaluator-workflow.md`, and
`official-result-certification.md`. This spec defines permissions, not identity
provider implementation.
