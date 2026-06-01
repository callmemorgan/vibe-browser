# Submission Abuse and Rate Limits

## Purpose

Submission abuse and rate limits protect hosted infrastructure from spam,
resource exhaustion, duplicate submissions, scraping, and adversarial users.

## Abuse Classes

- duplicate runs
- enormous artifacts
- repeated invalid submissions
- queue flooding
- API scraping
- credential abuse
- malicious packages
- denial of service
- hidden-test probing
- automated account creation

## Controls

Use per-organization quotas, artifact size limits, rate limits, duplicate
detection, manual review gates, abuse labels, temporary suspension, and
maintainer override.

## Fairness

Limits should avoid blocking legitimate research groups. Exceptions require
reason, duration, owner, and audit log entry.

## Public Communication

Document normal limits in the submission guide. Do not disclose thresholds that
would make hidden-test probing easier.

## Research Basis

OWASP API security guidance identifies unrestricted resource consumption and
rate limiting as core API risks. SRE overload practice motivates capacity
protection and prioritization.

## QA Pass

Checked against `queueing-and-run-scheduling.md`, `economic-model.md`,
`deceptive-or-unsafe-submission-handling.md`, `access-control.md`, and
`submission-guide.md`. This spec defines abuse controls, not anti-fraud
identity verification.
