# Qualitative Run Analysis

## Purpose

Qualitative analysis captures behaviors that numeric scores flatten: planning,
debugging, testing judgment, honesty about limitations, architecture choices,
and recovery from failure. It supports interpretation without changing the
official score by itself.

## Analysis Dimensions

- task understanding and milestone targeting
- repository exploration and use of local evidence
- implementation strategy and architecture fit
- test selection, test creation, and verification discipline
- response to failing commands or tool errors
- handling of time limits and continuation turns
- artifact hygiene and documentation quality
- self-assessment accuracy
- security, privacy, and hidden-test awareness
- maintainability of produced code

## Source Material

Analysts use public-safe timelines, diffs, verification output, evaluator notes,
run summaries, and artifacts that have passed redaction. Private logs may
inform internal review but should not be quoted publicly.

## Public Summary Template

Each summary includes strengths, weaknesses, notable decision points,
representative evidence links, and a caveat about scope. It should avoid
mocking failures or speculating about model internals beyond observed behavior.

## Scoring Relationship

Qualitative tags may explain evaluator decisions and feed research reports.
They do not directly add leaderboard points unless a future rubric explicitly
defines that metric inside a new season.

## Research Basis

HELM motivates multi-dimensional evaluation beyond a single aggregate score.
Model Cards motivate structured behavioral discussion, limitations, and
intended-use context for model-related claims.

## QA Pass

Checked against `evaluator-workflow.md`, `failure-classification.md`,
`public-run-result-page.md`, `blog-post-template.md`, and
`score-interpretation-guide.md`. This spec defines narrative analysis, not
private evaluator adjudication.
