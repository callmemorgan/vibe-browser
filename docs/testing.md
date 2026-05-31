# Testing and Evaluation

Testing is how the Vibe Browser benchmark turns browser-building claims into
engineering facts. A submission is evaluated on what it runs, what it proves, and
how clearly it maps implemented behavior back to the supplied standards corpus.

This document defines the default rubric for benchmark evaluators and the test
expectations participants should design toward. See
[Evaluator Procedure](evaluator-procedure.md) for an operational score sheet and
evidence checklist.

## Required Submission Artifacts

Each evaluated submission should include:

- Source code for the browser or browser-shaped prototype.
- Build and run instructions that work from a clean checkout.
- A root `benchmark-run.md` manifest when the work is on a run branch.
- Meta-harness profile and observed budget usage when a controller is used.
- A smoke-test path evaluators can run manually.
- Automated tests for implemented subsystems.
- Design notes or ADRs citing relevant files under `specs/`.
- A status summary using the shared vocabulary from `README.md`.
- Known limitations, unsupported APIs, and security or privacy shortcuts.

## Evaluation Rubric

Score each category independently. A strong submission does not need full web
compatibility, but it must be honest, runnable, and test-backed.

| Category | Weight | What Good Looks Like |
| --- | ---: | --- |
| Runnable artifact | 15% | Builds locally, launches consistently, and provides clear commands. |
| Browser capability | 20% | Demonstrates meaningful progress through the targeted roadmap milestone. |
| Standards traceability | 15% | Cites local specs for implemented behavior and names documented deviations. |
| Test quality | 15% | Includes focused automated tests, useful fixtures, and reproducible smoke checks. |
| Architecture quality | 10% | Has clear internal boundaries, data flow, and justified technology choices. |
| Security posture | 10% | Treats web content as hostile and preserves trusted browser boundaries. |
| Privacy posture | 5% | Makes storage, identifiers, telemetry, and private-mode behavior explicit. |
| Scope honesty | 10% | Distinguishes implemented, partial, deferred, unsupported, and risky behavior. |

Rubric scores should include notes, not just numbers. Evaluators should call out
excellent partial implementations and should penalize broad compatibility claims
that are not supported by tests.

## Test Layers

- Unit tests: parsers, algorithms, data structures, policy decisions.
- Integration tests: navigation, fetch, document loading, storage, permissions.
- Golden tests: layout and paint output for stable fixtures.
- Web Platform Tests: compatibility source of truth for standards behavior.
- Fuzzing: hostile input for URL, HTML, CSS, image, and network parsers.
- Manual smoke tests: launch, navigate, reload, back/forward, basic rendering.

## Conformance Labels

Use these labels in docs, dashboards, or module status files once code exists:

- `not-started`: no implementation.
- `partial`: implementation exists but coverage is incomplete.
- `passes-focused-tests`: local targeted tests pass.
- `wpt-backed`: mapped Web Platform Tests exist and pass for the claimed subset.
- `shipping-quality`: reviewed, fuzzed where relevant, and stable enough for
  repeated benchmark evaluation.

No subsystem should claim broad compatibility without at least `wpt-backed`
evidence for the claimed behavior.

## Minimum Bar for New Subsystems

Every spec-backed subsystem in a submission should include:

- A short design note or doc reference naming the relevant specs.
- Unit tests for core algorithms.
- Error-handling tests for malformed web input.
- Cross-origin tests if the subsystem touches origins, storage, network, or
  permissions.
- Private-mode tests if the subsystem touches persistent state.
- Fuzz target plan for parsers and decoders.

## Initial Test Priorities

Participants attempting the early milestones should prioritize:

- URL parser fixtures from the URL standard.
- Encoding detection and decode behavior.
- HTML tokenizer/tree-builder fixtures.
- CSS parser error recovery.
- Selector matching and specificity.
- Cascade and inheritance.
- Block layout golden tests.
- Fetch redirect and TLS failure policy.
- Cookie parsing and origin/site behavior.

## Web Platform Tests Strategy

WPT integration is a milestone, not a day-one dependency. Submissions should:

- Start with focused local tests while no engine harness exists.
- Add a WPT runner once URL, DOM, fetch, and rendering entrypoints are stable.
- Map each supported spec subset to WPT directories or test files.
- Track failures as expected only when linked to an issue or milestone.
- Avoid counting un-run tests as compatibility evidence.

## Evaluator Procedure

Use [Evaluator Procedure](evaluator-procedure.md) for the operational score sheet,
evidence requirements, and comparison-eligibility checklist. At a high level, for
each benchmark run:

1. Record model, prompt, tool access, time budget, and repository revision.
2. Record the meta-harness profile from
   [Meta-Harnesses](meta-harnesses.md), including configured limits and human
   intervention policy.
3. Create or verify the run branch using
   [Run Organization](run-organization.md).
4. Record the target roadmap milestone or open-ended objective.
5. Run the submitted build instructions from a clean environment where practical.
6. Run automated tests and capture failures.
7. Perform the documented smoke test.
8. Inspect design notes for spec citations and scope honesty.
9. Score the rubric and cite concrete evidence for each major score.
10. Record stop reason, observed budget usage, and any benchmark-input changes.
11. Record whether the run is comparison eligible and why.

## Documentation Acceptance Checks

For documentation changes:

- `README.md` must link to the main docs.
- New docs must be reachable from `README.md` or a linked doc.
- Status words should use the shared vocabulary.
- Roadmap, standards tiers, and architecture status should not contradict each
  other.
- Spec references should use local `specs/` paths where practical.
- Changes must not silently alter benchmark inputs or scoring expectations.
