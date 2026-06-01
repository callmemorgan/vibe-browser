# Milestone Evidence Requirements

## Purpose

Milestone evidence requirements define the minimum proof needed before an
evaluator can confirm a milestone. They are stricter than rubric descriptions:
a plausible implementation without evidence should not score as confirmed.

## Common Requirements

Every confirmed milestone needs:

- runnable artifact or focused module
- command evidence with exit code
- submitted tests or public checker output
- source evidence linking implementation to behavior
- documented limitations
- no blocking redaction or security issue

## Milestone Requirements

| Milestone | Required evidence |
| --- | --- |
| M0 | Orientation note, target interpretation, chosen stack, test plan, and risk notes. |
| M1 | Launch command, shell/chrome screenshot or headless smoke output, navigation-state tests, and UI/process model note. |
| M2 | URL parsing tests, HTTP fixture fetch, redirect fixture, TLS/error behavior, MIME/content-type capture, and no-network limitation notes. |
| M3 | HTML tokenizer/tree tests, malformed HTML recovery fixture, title/body extraction, DOM representation evidence, and spec citations. |
| M4 | CSS parse tests, selector/cascade/inheritance fixtures, block/inline layout evidence, viewport/scroll behavior, and layout limitations. |
| M5 | Paint command, golden screenshot or image diff, text/background/border evidence, image handling evidence if claimed, and viewport metadata. |
| M6 | Back/forward/reload/stop tests, same-document vs cross-document note, security chrome state, and transition timeline evidence. |
| M7 | JS runtime launch, DOM mutation test, event/timer evidence if claimed, Web IDL strategy, and unsupported binding disclosure. |
| M8 | Origin storage/cookie tests, clearing/private-mode behavior, permission or policy notes, threat model update, and state-leak checks. |
| M9 | WPT or equivalent report, expected-fail metadata, subsystem ownership map, fuzz/crash evidence where applicable, and conformance labels. |

## Evidence Sufficiency

Evidence may be public-check, hidden-check, evaluator-observed, or artifact
based. At least one public or redacted-public evidence object should support
each confirmed milestone, even when hidden checks contribute.

## Research Basis

ACM artifact badging motivates documented, complete, exercisable evidence.
WPT metadata practices motivate explicit expected-fail and conformance labels
for advanced compatibility milestones.

## QA Pass

Checked against `milestone-rubrics.md`, `verification-result-schema.md`,
`evidence-model.md`, and `public-milestone-checker.md`. This spec defines proof
minimums; the rubric still assigns fractional quality.
