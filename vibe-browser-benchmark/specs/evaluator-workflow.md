# Evaluator Workflow

## Purpose

The evaluator workflow defines how humans review benchmark evidence and convert
automated run artifacts into official milestone and rubric scores.

## Queue States

Evaluator-facing states mirror `run-state-taxonomy.md`:

- `awaiting_evaluation`
- `assigned`
- `in_review`
- `needs_more_evidence`
- `needs_adjudication`
- `ready_for_certification`
- `returned_to_import`
- `rejected`

## Assignment

Official ranked runs require at least two independent evaluators for the first
public season and for any top-result candidate. Maintainers may reduce duplicate
review for routine baseline reruns only after calibration data shows acceptable
agreement.

Evaluators must disclose conflicts with submitters, vendors, model providers,
or benchmark changes they authored.

## Review Steps

1. Confirm the run is import-valid and redaction-safe for evaluator access.
2. Read the result card, run timeline, public checks, participant diff, design
   notes, and submitted tests.
3. Score each claimed milestone using `milestone-rubrics.md` and
   `milestone-evidence-requirements.md`.
4. Attach evidence IDs to every nonzero score and every blocking failure.
5. Classify failure modes and notable qualitative behavior.
6. Record limitations and reviewer confidence.
7. Submit score sheet for agreement check or adjudication.

## Disagreement Handling

If evaluator milestone scores differ by more than 0.20 or disagree on highest
confirmed milestone, the run enters adjudication. The adjudicator writes a short
decision note referencing evidence IDs and updates the final score sheet.

## Output

The workflow produces a versioned evaluator score sheet, qualitative notes,
required correction flags, and a certification recommendation:
`certify-ranked`, `certify-unranked`, `reject`, or `security-hold`.

## Research Basis

ACM artifact badging motivates independent artifact audit and result validation.
HELM motivates exposing multiple dimensions rather than collapsing evaluator
judgment into a single unexplained score.

## QA Pass

Checked against `official-result-certification.md`, `evidence-model.md`,
`run-state-taxonomy.md`, `milestone-rubrics.md`, and the future evaluator
calibration backlog item. This spec owns human review flow, not schema import.
