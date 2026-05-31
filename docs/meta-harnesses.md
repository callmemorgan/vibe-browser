# Meta-Harnesses

A meta-harness is the controller that keeps an LLM agent working on a benchmark
run. It creates or resumes the run branch, gives the model the next instruction,
tracks budgets, records outputs, and decides when to stop.

Meta-harness configuration is part of the benchmark condition. Two runs are not
directly comparable if one model gets unlimited continuation and another gets a
single prompt.

## What to Configure

Each meta-harness profile should define:

- `profile`: stable profile slug, such as `smoke-v0`, `sprint-v0`,
  `standard-v0`, `deep-v0`, or `frontier-v0`.
- `harness`: implementation name and version.
- `tool`: agent tool name and version.
- `model`: provider, exact model name, and snapshot or release identifier when
  known.
- `prompt_set`: prompt or prompt-set identifier.
- `prompt_checksum`: checksum of the exact prompt bundle when available.
- `target`: roadmap milestone or open-ended target, such as `m2`, `m5`, or
  `open`.
- `wall_clock_limit`: elapsed time from run start to forced stop.
- `token_limit`: total model input plus output tokens when available.
- `turn_limit`: maximum model turns or continuation cycles.
- `tool_call_limit`: maximum tool calls when the harness can count them.
- `cost_limit`: optional currency budget when provider cost is measurable.
- `idle_limit`: maximum consecutive turns without material progress.
- `failure_limit`: maximum repeated infrastructure failures before stopping.
- `checkpoint_interval`: how often the harness commits or records progress.
- `human_intervention_policy`: which human actions are allowed.
- `stop_conditions`: success, budget exhaustion, blocked state, safety stop, or
  evaluator intervention.

If limits disagree, the earliest stop wins. The manifest should record both the
configured limits and the observed usage.

Token limits are comparable only when the measurement method is recorded. If a
tool cannot measure tokens, set observed token usage to `unknown` and rely on the
wall-clock, turn, and tool-call limits for enforcement.

A turn means one model response to one meta-harness instruction. Tool calls,
command executions, browser actions, and checkpoint commits inside that response
do not increment the turn count unless the model receives a new instruction.

## Profile Format

Harnesses may store profiles in code, configuration, or CI settings, but the
effective profile for a run must be copied into `benchmark-run.md`.

Example profile:

```yaml
profile: standard-v0
harness: manual-controller 0.1.0
tool: codex-cli
model:
  provider: openai
  name: gpt-5.4
  snapshot: null
prompt_set: browser-build-v0
prompt_checksum: null
target: m3
wall_clock_limit: 24h
token_limit: 8000000
turn_limit: 200
tool_call_limit: null
cost_limit: null
idle_limit: 6
failure_limit: 5
checkpoint_interval: 30m
human_intervention_policy: administrative-only
stop_conditions:
  - success
  - budget-exhausted
  - blocked
  - safety-stop
  - evaluator-stop
```

## Recommended Profiles

Use these profiles until real run data suggests better defaults.

| Profile | Purpose | Wall Clock | Turn Limit | Token Limit | Idle Limit |
| --- | --- | ---: | ---: | ---: | ---: |
| `smoke-v0` | Verify harness plumbing and basic agent behavior. | 30 minutes | 8 | 200k | 2 |
| `sprint-v0` | Short iteration run for fast harness and prompt comparisons. | 4 hours | 40 | 1.5M | 3 |
| `standard-v0` | Default comparable benchmark run. | 24 hours | 200 | 8M | 6 |
| `deep-v0` | High-context boundary run near one Chromium-scale corpus pass. | 7 days | 2,000 | 1B | 20 |
| `frontier-v0` | Frontier-scale boundary run for many-pass long-horizon work. | 30 days | 20,000 | 10B | 50 |

The default profile should be `standard-v0`. It gives models enough time to plan,
write code, recover from mistakes, run tests, and continue through several
substantial implementation cycles.

`smoke-v0` should not be used for model quality comparisons except to confirm
that a model and tool can operate in the environment.

`sprint-v0` is useful while developing harnesses and prompts, but it should be
reported separately from `standard-v0` results.

`deep-v0` and `frontier-v0` are boundary profiles. If Chromium is roughly 708M
tokens, then a 1B-token run is in the neighborhood of one Chromium-scale context
budget, while a 10B-token run measures whether a model and harness can sustain
many-pass, long-horizon engineering work. These profiles should not be mixed with
standard runs on a leaderboard.

## Continuation Policy

The meta-harness should keep the model going until a stop condition is reached.
After each turn, it should decide whether the next instruction is:

- Continue the current objective.
- Run verification and fix failures.
- Summarize current state and choose the next milestone task.
- Stop and mark the run complete or blocked.

Continuation prompts should be short and mechanical. They should not add new
human insight, hidden requirements, or debugging hints that are unavailable to
other runs. If a human intervenes with substantive guidance, record it in the
manifest and treat the run as a different condition.

## Human Intervention Policy

Use one of these policies:

- `none`: no human action after the run starts except emergency stop.
- `administrative-only`: humans may approve permissions, restart crashed
  infrastructure, or resume the meta-harness without adding task guidance.
- `guided`: humans may provide substantive debugging, design, or prioritization
  guidance.

Comparable leaderboard runs should use `administrative-only` by default.
Administrative actions must be recorded, but they do not change the benchmark
condition if they only keep the configured harness running. Guided interventions
create a separate condition and should not be mixed with unguided runs.

## Progress and Idle Detection

A turn counts as material progress when it produces at least one of:

- New or changed implementation code.
- New or changed tests.
- Passing verification that previously failed.
- A documented design decision needed for implementation.
- A narrowed blocker with concrete evidence.

A turn is idle when it only repeats plans, reruns the same failing command without
new diagnosis, or produces no durable artifact. Stop after `idle_limit`
consecutive idle turns.

Infrastructure failures should be counted separately from model idleness. Network
outages, sandbox failures, or provider rate limits should pause or retry within
the configured `failure_limit`; repeated failures should stop the run as
`blocked-infrastructure`.

## Checkpointing

The meta-harness should checkpoint often enough that a run can be audited after a
crash.

At each checkpoint, record:

- Run ID.
- Current commit SHA.
- Elapsed time.
- Token, turn, and tool-call usage when available.
- Latest model-visible instruction.
- Commands run since the previous checkpoint.
- Current verification status.
- Current blocker, if any.

Checkpoint commits may be noisy on run branches. That is acceptable because run
branches are archival and are not merged to `main`.

## Stop Conditions

Stop the run when any of these occurs:

- The target milestone acceptance criteria are met and verified.
- Wall-clock, token, turn, tool-call, or cost budget is exhausted.
- The model declares the task complete and verification does not contradict it.
- The model is blocked for the configured idle or failure limit.
- A safety, credential, or external-system boundary requires human approval not
  granted by the benchmark condition.
- The evaluator manually stops the run.

The final manifest entry should state the stop reason, observed usage, final
commit, verification result, and whether the run is eligible for comparison with
other runs.

## Comparison Eligibility

A run is comparison eligible when:

- It starts from the recorded benchmark baseline.
- It uses a documented meta-harness profile without unrecorded budget changes.
- Prompt set, tool permissions, and intervention policy are recorded.
- Stop reason and observed usage are recorded.
- Verification commands and results are recorded.

Mark a run comparison-ineligible when the harness changes mid-run, a human gives
substantive unplanned guidance, accounting data is missing for required limits,
or benchmark inputs change without being recorded.

## Why This Shape

Wall-clock limits alone are not enough because models and tools vary widely in
latency. Token limits alone are not enough because browser-building requires
tool execution, compilation, tests, and waiting for local processes. Turn limits
alone reward huge turns and make provider differences awkward.

The best default is a combined budget: wall-clock plus token plus turn limits,
with idle and failure guards. That makes runs finite, reproducible, and fair
without pretending that every provider exposes identical accounting. Extremely
large token-boundary profiles are useful, but only when clearly separated from
standard comparable runs.
