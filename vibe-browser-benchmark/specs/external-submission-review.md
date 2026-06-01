# External Submission Review

## Purpose

External submission review defines how third-party runs become official results.
It protects the leaderboard from incomplete artifacts, non-reproducible claims,
undisclosed interventions, and vendor-conflict ambiguity.

## Required Submission Packet

- submission snapshot archive
- run summary and result card
- model, provider, harness, prompt, and runtime metadata
- exact command and environment instructions
- artifact checksums
- public-check results
- intervention disclosure
- dependency disclosure
- requested season, track, and ranking status
- submitter contact and conflict-of-interest statement

## Review Flow

1. Intake validates packet shape and redaction eligibility.
2. Maintainer assigns independent reviewer or evaluator.
3. Clean-room verification service replays the artifact where feasible.
4. Eligibility rules decide ranked, official-unranked, provisional, or rejected.
5. Evaluators score milestone evidence.
6. Submitter receives decision and appeal path.
7. Accepted results enter certification and publication.

## Embargoes

Submitters may request a private embargo for coordination, but embargoed results
are not ranked publicly. Embargo duration, participants, and expiration must be
recorded.

## Rejection Reasons

Common reasons include missing artifacts, dirty baseline, unverifiable runtime,
unsafe artifacts, hidden-test leakage, undisclosed intervention, incompatible
profile, or failed clean-room replay.

## Research Basis

MLCommons submission practice motivates explicit artifacts, reproducibility
checks, and defined review rules. ACM artifact review practice motivates
separating artifact availability from validated result claims.

## QA Pass

Checked against `submission-guide.md`, `submission-snapshot-format.md`,
`comparison-eligibility-rules.md`, `evaluator-workflow.md`, and
`official-result-certification.md`. This spec defines third-party intake, not
the public upload UI.
