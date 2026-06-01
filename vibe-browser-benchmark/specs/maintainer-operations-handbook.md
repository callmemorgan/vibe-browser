# Maintainer Operations Handbook

## Purpose

The maintainer operations handbook defines recurring work needed to run the
benchmark safely and predictably.

## Handbook Sections

- season launch checklist
- queue review
- snapshot ingestion
- verifier operation
- evaluator assignment
- hidden fixture rotation
- calibration and baseline reruns
- artifact privacy and security review
- report publication
- appeals and corrections
- incidents and recovery
- archival tasks
- trust dashboard review

## Operating Cadence

Define daily, weekly, season-close, and emergency tasks. Each task lists owner
role, command or admin screen, expected output, escalation path, and evidence to
record.

## Safety Principles

Prefer reversible state transitions, dry runs for bulk operations, two-person
approval for public destructive actions, and incident records for emergency
exceptions.

## Handoff

The handbook includes runbooks, contacts, access prerequisites, and recent known
risks so maintainers can rotate without losing context.

## Research Basis

Google SRE practice motivates runbooks, ownership, overload control, and
post-incident learning. NIST incident guidance motivates documented roles,
communications, and evidence preservation.

## QA Pass

Checked against `admin-operations.md`, `queueing-and-run-scheduling.md`,
`incident-response.md`, `public-trust-dashboard.md`, and
`archival-and-preservation.md`. This spec defines handbook structure, not the
contents of every runbook.
