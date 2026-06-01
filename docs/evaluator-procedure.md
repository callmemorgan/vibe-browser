# Evaluator Procedure

This document turns the rubric in [Testing](testing.md) into an operational score
sheet. It is intended for evaluators reviewing a completed run branch.

## Inputs

Evaluators should collect:

- Run branch and final commit.
- Root `benchmark-run.md` manifest.
- Submitted source code and implementation artifacts.
- Build, test, and smoke-test commands.
- Design notes, ADRs, or module docs.
- Harness logs and checkpoint records when available.
- Public fixture results and any evaluator-only test results.

## Required Evidence

For every score, cite at least one of:

- Command output.
- Test result.
- Source file path.
- Design note path.
- Smoke-test observation.
- Harness log entry.
- Manifest field.

Do not award broad compatibility credit for un-run tests, unsupported claims, or
behavior that is only described in plans.

## Score Sheet

Use the weights from [Testing](testing.md). Record a score, evidence, notes, and
follow-up questions for each category.

### Runnable Artifact — 15%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Browser Capability — 20%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Standards Traceability — 15%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Test Quality — 15%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Architecture Quality — 10%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Security Posture — 10%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Privacy Posture — 5%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

### Scope Honesty — 10%

- Score:
- Evidence:
- Notes:
- Follow-up questions:

## Comparison Eligibility

Runs should be compared only when these fields match or are intentionally grouped:

- Base benchmark commit or benchmark input digest.
- Meta-harness profile.
- Harness and prompt set.
- Target milestone or objective.
- Tool access policy.
- Human intervention policy.

Model and tool names are typically the variables being compared, so they do not
need to match unless the comparison is studying something else.

## Findings Classification

Classify review findings separately from the weighted rubric score.

### Automatic Invalidation

Use for findings that make the run invalid for the intended implementation task,
such as undisclosed use of an existing browser engine as the implementation.

### Comparison-Ineligible but Reviewable

Use when the run may still be informative but should not be mixed with comparable
runs, such as guided human intervention in an administrative-only comparison
batch.

### Score Penalty

Use when the run remains comparable but earns less credit, such as weak tests,
missing spec citations, or overstated support.

### Reviewer Warning

Use for issues that deserve attention but do not clearly affect the score or
comparison group, such as minor manifest omissions that are corrected before
final scoring.

## Examples of Comparison-Affecting Findings

- Uses Chromium, WebKit, Gecko, Electron WebView, system WebView, Playwright,
  Puppeteer, Selenium, or equivalent browser-engine delegation as the
  implementation.
- Cannot build from a clean checkout.
- Cannot run any submitted entrypoint.
- Modifies benchmark corpus files under `specs/`.
- Lacks a root `benchmark-run.md` manifest.
- Lacks a target milestone or objective.
- Receives guided human intervention during a supposedly comparable run.
- Changes benchmark inputs during the run.
- Appears to hard-code public fixtures, evaluator fixtures, or hidden tests.
