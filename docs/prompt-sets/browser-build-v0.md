# Prompt Set: browser-build-v0

`browser-build-v0` is the initial stable prompt set for comparable Vibe Browser
implementation runs. It assumes a run-specific target milestone and uses short,
mechanical continuation prompts so the meta-harness keeps the agent working
without adding new human insight.

## Purpose

Use this prompt set for benchmark runs where the participant should produce a
runnable browser implementation, tests, and design notes according to a configured
roadmap milestone.

## Required Run Variables

The harness or evaluator must record these values in `benchmark-run.md`:

- `TARGET_MILESTONE`: roadmap milestone or objective, such as `m1`, `m3`, `m5`,
  or `open`.
- `META_HARNESS_PROFILE`: profile such as `smoke-v0`, `sprint-v0`, or
  `standard-v0`.
- `HUMAN_INTERVENTION_POLICY`: `none`, `administrative-only`, or `guided`.
- `BASE_BENCHMARK_COMMIT`: baseline commit for the run.
- `BENCHMARK_INPUT_DIGEST`: corpus or benchmark input digest when available.

## Initial Participant Instruction

Use [Participant Task](../participant-task.md) as the participant-visible task.
Fill `{{TARGET_MILESTONE}}` with the configured target for the run before the
participant begins.

The participant should implement cumulative milestones through the configured
target, avoid unrelated later scope, and produce the required artifacts listed in
the task template.

## Continuation Prompt

Continue pursuing the configured target milestone. Prefer implementation, tests,
verification, or concrete blocker diagnosis over additional planning. Do not add
scope beyond the target milestone unless required for verification.

## Verification Prompt

Run the submitted build, test, and smoke-test commands if available. Fix failures
that block the configured target milestone, and update `benchmark-run.md` with
the latest verification result.

## Premature-Stop Prompt

The task is not complete unless the target milestone acceptance criteria are met
or a concrete blocker is recorded. Continue with the next implementation or
verification step.

## Blocked Prompt

Record the blocker, evidence, attempted fixes, and the smallest useful fallback
milestone. Continue with that fallback if possible.

## Non-Guidance Rule

Continuation prompts must remain short and mechanical. They must not leak
evaluator-only tests, hidden requirements, debugging hints, or new prioritization
that is unavailable to other runs in the same comparison group.
