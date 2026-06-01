# Submission Identity and Organizations

## Purpose

Submission identity and organizations define who owns a run, how vendors and
independent researchers are represented, and how aliases are reconciled.

## Identity Types

- individual researcher
- organization
- vendor
- maintainer
- sponsor
- anonymous public dry-run submitter
- independent replication group

## Required Fields

Submission identity records include display name, verified status, contact,
organization URL, submitter role, conflict labels, result ownership, linked
model/provider identities, and public profile preference.

## Alias Handling

Maintainers can merge or split organization aliases through admin operations.
Alias changes preserve old display names in audit history and update affected
run pages with a correction note when public interpretation changes.

## Ownership Transfer

Result ownership transfer requires confirmation from current and target owner
where possible, maintainer approval, and public note for official results.

## Research Basis

MLCommons submission practice motivates explicit submitter and organization
metadata. DataCite contributor metadata practice motivates clear contributor
roles for citable artifacts and datasets.

## QA Pass

Checked against `external-submission-review.md`, `model-and-tool-identity.md`,
`economic-model.md`, `ethics-and-disclosure.md`, and `access-control.md`. This
spec defines submitter identity, not user-login implementation.
