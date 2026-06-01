# Appeals and Corrections

## Purpose

Appeals and corrections define how participants challenge scores, metadata,
eligibility decisions, or public claims while preserving an auditable public
record.

## Appeal Scope

Participants may appeal evaluator score, comparison eligibility, metadata,
artifact redaction, dependency classification, external submission rejection,
or conflict labels. Hidden-test content is not disclosed during appeal.

## Appeal Packet

An appeal includes run ID, challenged decision, requested change, evidence,
affected specs, submitter identity, and urgency. Maintainers may request
additional public-safe artifacts.

## Workflow

Appeals move through `submitted`, `triage`, `under-review`, `needs-info`,
`accepted`, `rejected`, or `withdrawn`. Accepted appeals create a correction
record and may trigger reanalysis.

## Corrections

Corrections append public history. They do not silently mutate result pages,
exports, reports, or citations. Superseded records link to corrected records
and explain rank impact.

## Research Basis

W3C-style process norms motivate objection handling and appeal paths. DataCite
versioning guidance motivates linking corrected or superseded citable objects.

## QA Pass

Checked against `governance-and-versioning.md`,
`official-result-certification.md`, `citation-and-doi-policy.md`,
`external-submission-review.md`, and `release-notes-template.md`. This spec
defines appeal handling, not legal dispute resolution.
