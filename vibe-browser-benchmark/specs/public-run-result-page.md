# Public Run Result Page

## Purpose

The public run result page is the canonical, shareable page for one run. It
should explain what happened, what was built, how it was scored, and whether the
result is official, provisional, failed, or non-comparable.

## Header

Show run ID, result status, season, track, model/provider, agent/harness,
runtime profile, target/run mode, eligibility, certification revision, and
stable citation URL.

## Summary

Summary cards show evaluator score, highest evaluator-confirmed milestone,
highest public-check milestone, highest claimed milestone, cost/time metrics,
verification status, failure class if any, and replication status.

## Evidence Tabs

- **Milestones**: M0-M9 ladder with criteria, status, and evidence links.
- **Artifacts**: redacted snapshot, diff, logs, screenshots, public reports.
- **Timeline**: phase/turn events with filters.
- **Code**: safe diff and file browser.
- **Environment**: model, tool, prompt, Docker, provider, and runtime metadata.
- **Caveats**: limitations, non-comparable reasons, redaction, and hidden-test
  boundary.

## Sharing

Every public run page includes citation text, JSON result-card link, badge link,
and report issue/correction link. Provisional and non-comparable pages must show
a banner that survives screenshots and embeds.

## Research Basis

Model cards motivate compact disclosure of intended use, evaluation, and
limitations. ACM artifact badging motivates linking results to evaluated
artifacts and validation status.

## QA Pass

Checked against `run-detail-ux.md`, `result-card.md`, `evidence-model.md`,
`timeline-and-telemetry-ux.md`, `diff-and-code-browser-ux.md`, and
`test-run-result-sharing.md`. This spec defines public run page behavior, not
private evaluator UI.
