# Incident Response

## Purpose

Incident response defines what maintainers do when the benchmark's integrity,
privacy, security, or public trust is at risk. It covers both infrastructure
incidents and benchmark-specific failures.

## Incident Classes

- secret or credential leak
- hidden-test leak
- fraudulent or deceptive result
- scoring bug affecting public rank
- verification service compromise
- unsafe artifact publication
- provider outage affecting official runs
- data export corruption
- privacy exposure
- site or API compromise

## Severity Levels

Use `sev1` for active security or hidden-test compromise, `sev2` for incorrect
public results or privacy exposure, `sev3` for limited publication or verifier
issues, and `sev4` for low-impact operational defects.

## Response Flow

1. Declare incident, owner, severity, and affected scope.
2. Contain publication, downloads, verifier jobs, or affected seasons.
3. Preserve evidence and audit logs.
4. Notify affected parties when required.
5. Repair records, rotate fixtures, rerun verification, or reissue exports.
6. Publish public incident note when public trust or citations are affected.
7. Complete post-incident review and preventive actions.

## Public Record

Public incident notes include scope, impact, affected results, correction links,
and current status. They avoid exposing secrets, private logs, or hidden-test
details.

## Research Basis

NIST incident handling guidance motivates preparation, detection, containment,
eradication, recovery, and post-incident activity. Google SRE postmortem
practice motivates blameless review with clear owners and action items.

## QA Pass

Checked against `security-and-redaction.md`, `privacy-review.md`,
`hidden-test-policy.md`, `appeals-and-corrections.md`, and
`official-result-certification.md`. This spec defines response workflow, not
on-call staffing.
