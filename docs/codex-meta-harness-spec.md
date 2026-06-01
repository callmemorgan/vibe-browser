# Codex Meta-Harness Spec

Status: initial implementation in `scripts/codex_meta_harness.py`, with PI
Docker smoke-run support in `scripts/pi_docker_benchmark.py`.

This document specifies a concrete controller for running agent CLIs against the
Vibe Browser benchmark. It covers OpenAI Codex CLI long-horizon runs and the
short PI/Ollama Docker smoke path. It builds on
[Meta-Harnesses](meta-harnesses.md), [Run Organization](run-organization.md), and
[Prompt Set: browser-build-v0](prompt-sets/browser-build-v0.md).

## Purpose

The Codex meta-harness keeps Codex working on one benchmark run until a stop
condition is reached. It must make the run reproducible, auditable, resumable,
and comparable without adding hidden human guidance.

The first serious target is:

```yaml
profile: standard-v0
target: m5
harness: codex-meta-harness
tool: codex-cli
wall_clock_limit: 24h
turn_limit: 200
token_limit: 8000000
idle_limit: 6
failure_limit: 5
checkpoint_interval: 30m
human_intervention_policy: administrative-only
```

The first PI/Ollama Docker target is:

```yaml
profile: smoke-v0
target: m1
agent_kind: pi
provider_interface: pi-cli-v0
model_provider: ollama
model: glm-5.1:cloud
wall_clock_limit: 10m
container_execution: docker-admin-v0
```

## Goals

- Start from a recorded benchmark baseline and create one isolated run branch.
- Invoke Codex CLI repeatedly with stable initial, continuation, verification,
  premature-stop, and blocked prompts.
- Capture raw Codex event streams, last messages, prompts, budget counters,
  verification output, and checkpoint metadata.
- Emit compact live progress for container logs without exposing raw JSON or
  model reasoning deltas.
- Resume after controller crashes, Codex exits, terminal disconnects, or machine
  restarts without changing the benchmark condition.
- Commit useful implementation checkpoints while keeping raw local logs out of
  normal benchmark-maintenance branches.
- Stop deterministically on success, budget exhaustion, idle progress,
  infrastructure failure, safety stop, or evaluator stop.

## Non-Goals

- It is not the evaluator or scorer. Final scoring still follows
  [Evaluator Procedure](evaluator-procedure.md).
- It does not run hidden tests during the model-visible work loop.
- It does not rewrite benchmark rules, roadmap milestones, or the standards
  corpus.
- It does not normalize all model providers. This spec covers the Codex CLI
  adapter and leaves other tools to separate adapters.

## Required Inputs

The harness requires:

- `run_id`: stable run identifier.
- `profile`: one of the documented meta-harness profiles.
- `target`: roadmap milestone or objective, usually `m5` for a 24-hour run.
- `base_benchmark_commit`: commit SHA used as the benchmark input baseline.
- `benchmark_input_digest`: digest from `specs.zip` or equivalent corpus
  manifest.
- `prompt_set`: `browser-build-v0`.
- `model`: exact Codex model name and snapshot when known.
- `codex_cli_version`: output of `codex --version`.
- `sandbox_mode`: `read-only`, `workspace-write`, or `danger-full-access`.
- `network_policy`: dependency and remote-network rules for the run.
- `human_intervention_policy`: `none`, `administrative-only`, or `guided`.
- `checkpoint_interval`: default `30m`.

The effective configuration must be copied into root `benchmark-run.md` before
or with the first implementation checkpoint.

## Run Directory Layout

Live harness state is written under the ignored `.vibe-bench/` tree:

```text
.vibe-bench/runs/<run-id>/
|-- config.json
|-- state.json
|-- initial-prompt.md
|-- prompts/
|   |-- turn-0001.md
|   `-- turn-0002.md
|-- codex/
|   |-- turn-0001.jsonl
|   |-- turn-0001.last.md
|   |-- turn-0002.jsonl
|   `-- turn-0002.last.md
|-- verification/
|   |-- turn-0001.txt
|   `-- turn-0002.txt
`-- checkpoints/
    |-- checkpoint-0001.json
    `-- checkpoint-0002.json
```

The run branch contains the implementation, root `benchmark-run.md`, design
notes, tests, and normal source files. Raw `.vibe-bench/` logs stay ignored by
default. If an evaluator wants committed logs, the harness should export a
reviewed, compact archive such as `run-artifacts/<run-id>/summary.jsonl`; it
must not commit Codex auth files, provider secrets, or unbounded raw transcripts
by accident.

## State Machine

The controller stores its state in `.vibe-bench/runs/<run-id>/state.json`.

- `created`: config exists but no Codex turn has started.
- `initializing`: branch, manifest, and initial prompt are being created.
- `running-turn`: one Codex invocation is active.
- `post-turn-audit`: Codex returned and the harness is collecting evidence.
- `verifying`: build, test, smoke, or docs checks are running.
- `checkpointing`: manifest and git checkpoint are being written.
- `resuming`: the controller is reconstructing state after interruption.
- `stopping`: final manifest fields are being written.
- `complete`: success or verified target completion.
- `blocked`: model, infrastructure, safety, or budget stop.
- `invalid`: run cannot be compared because the condition changed or a rule was
  violated.

State writes must be atomic: write a temporary file, then rename it into place.

## Codex CLI Adapter

The adapter invokes Codex non-interactively. The locally observed CLI supports
`codex exec --json`, `--cd`, `--model`, `--sandbox`, `--output-last-message`,
and `codex exec resume`.

Initial turn:

```bash
codex exec \
  --json \
  --cd /path/to/vibe-browser \
  --model <model> \
  --sandbox <sandbox-mode> \
  --output-last-message .vibe-bench/runs/<run-id>/codex/turn-0001.last.md \
  -
```

Resume turn:

```bash
codex exec resume <session-id> \
  --json \
  --model <model> \
  --output-last-message .vibe-bench/runs/<run-id>/codex/turn-0002.last.md \
  -
```

The prompt is supplied on stdin. The controller captures stdout JSONL and stderr
separately. It should parse the Codex session id from the JSON event stream when
available. Resume invocations must run with the repository root as the process
working directory, because `codex exec resume` does not take `--cd`. `--last` is
only allowed in a single-run environment with an isolated `CODEX_HOME`, because
otherwise it can resume the wrong session.

When the launch command is a zsh alias or function, such as
`ollama-codex --model glm-5.1:cloud`, the harness must use
`--codex-command-mode interactive-shell` so the alias is expanded by an
interactive zsh process.

`--dangerously-bypass-approvals-and-sandbox` is disallowed unless the run is
inside a separately documented disposable sandbox and the manifest records that
condition.

## Prompt Contract

The initial prompt is the rendered participant task for `target`, plus only
run-mechanical context:

- Run ID.
- Target milestone.
- Profile and budget limits.
- Human intervention policy.
- Base benchmark commit and benchmark input digest.
- Reminder that `specs/` must not be edited.

Continuation prompts must be short and drawn from
[Prompt Set: browser-build-v0](prompt-sets/browser-build-v0.md). They may include
mechanical state that the model itself produced or the harness observed:

- elapsed time,
- turn count,
- latest git status summary,
- latest verification result,
- current blocker text if already recorded.

They must not include evaluator-only tests, fresh debugging advice, new
priorities, or human interpretation that was not part of the original benchmark
condition.

## Turn Lifecycle

Each turn follows this sequence:

1. Select prompt type: initial, continue, verify, premature-stop, or blocked.
2. Write the exact model-visible prompt to `prompts/turn-NNNN.md`.
3. Invoke Codex through the adapter.
4. Store raw JSONL, stderr, exit code, elapsed time, and last message.
5. Run post-turn audit:
   - `git status --short`,
   - changed file summary,
   - whether source, tests, docs, or manifest changed,
   - whether Codex reported completion or blockage.
6. Run verification when appropriate.
7. Update budget, idle, failure, and stop-condition counters.
8. Write a checkpoint.
9. Either continue, stop, or mark the run invalid.

A turn is one Codex response to one harness instruction. Shell commands and tool
use inside that response do not increment the turn counter.

## Turn-Level Restart Model

Agent CLIs are treated as turn workers, not as immortal processes. The harness
may start a fresh agent subprocess for every turn and use the recorded session
identity to preserve continuity.

For Codex, the first turn uses `codex exec`; later turns use
`codex exec resume <session-id>` once the session id has been parsed from the
JSON event stream. For PI, every turn uses the same run-scoped session id and
session directory:

```bash
pi --session-id <run-id> --session-dir .vibe-bench/runs/<run-id>/pi/sessions
```

When an agent subprocess exits, the harness records stdout, stderr, exit code,
elapsed time, and parsed usage. A clean exit means the turn finished; the next
iteration decides whether to verify, continue, stop, or send a blocked prompt. A
nonzero exit is an infrastructure failure unless post-turn evidence proves a
different stop condition. The harness may start another agent subprocess with
the same prompt and session context until `failure_limit` is reached.

This restart model is separate from controller or container recovery. Restarting
the controller must load existing `.vibe-bench/runs/<run-id>/state.json` and
resume from the latest completed turn; it must not reinitialize the run or erase
session state. Disposable Docker container resume requires explicit artifact
rehydration before it can be considered the same benchmark condition.

## Budget Accounting

The controller enforces the earliest of:

- wall-clock limit,
- turn limit,
- token limit when available,
- tool-call limit when available,
- cost limit when configured,
- idle limit,
- failure limit,
- explicit stop condition.

Wall time is measured with a monotonic clock and recorded as elapsed seconds.
Token, cost, and tool-call counters are parsed from Codex JSON events when
available. If unavailable, observed values must be recorded as `unknown`; the run
can still be comparable on wall-clock and turn limits if the measurement gap is
declared.

## Progress and Idle Detection

A turn counts as material progress when it produces at least one durable result:

- implementation code changed,
- tests changed,
- design notes or ADRs changed,
- verification changed from failing to passing,
- a blocker was narrowed with concrete evidence,
- `benchmark-run.md` was made more complete.

A turn is idle when it only repeats a plan, reruns the same failing command
without new diagnosis, or exits without durable artifacts. After `idle_limit`
consecutive idle turns, the harness sends the blocked prompt once. If that does
not produce progress, the run stops as `blocked-idle`.

## Verification Policy

The harness always supports:

```bash
python3 scripts/vibe_bench.py validate
```

For submitted browser code, it runs the build, test, and smoke-test commands
recorded in `benchmark-run.md` once they exist. For M2 through M5 smoke checks,
it may start the fixture server with:

```bash
python3 scripts/vibe_bench.py serve-fixtures --port <port>
```

The fixture server must be treated as infrastructure. Its port, process id, and
logs are recorded in harness state. Hidden tests are reserved for post-run
evaluation and must not be surfaced to the model during the run.

## Checkpointing

The harness checkpoints after each turn and at least every `checkpoint_interval`
while a long verification command is running.

Each checkpoint records:

- run id,
- state,
- current branch,
- current commit SHA,
- elapsed seconds,
- observed turn count,
- observed token, cost, and tool-call usage when known,
- latest prompt path,
- latest Codex log path,
- latest verification result,
- material progress decision,
- idle and failure counters,
- stop condition if any.

When the worktree has material implementation changes, the harness should commit
a checkpoint on the run branch:

```text
checkpoint(<run-id>): turn <n>
```

Checkpoint commits may include source, tests, docs, and `benchmark-run.md`. They
must not include provider secrets, raw auth state, local machine paths beyond
normal manifest metadata, or accidental corpus rewrites under `specs/`.

## Failure Handling

Infrastructure failures increment `failure_count` and do not count as model idle
turns. Examples include Codex process crashes, malformed JSONL output, fixture
server startup failure, local disk errors, provider outages, and approval
timeouts.

The controller may retry an infrastructure failure with the same prompt if doing
so does not add new guidance. After `failure_limit`, it stops as
`blocked-infrastructure`.

Model failures are evaluated through idle and stop-condition rules. A model that
changes `specs/`, delegates implementation to a prohibited browser engine, or
hard-codes fixtures can make the run `invalid` or comparison-ineligible.

## Human Intervention Log

Administrative actions are allowed only when the profile permits them. Every
action must be recorded with:

- timestamp,
- actor,
- action,
- reason,
- whether model-visible guidance changed.

Examples of administrative actions:

- approve a permission prompt covered by the recorded tool policy,
- restart the controller after a crash,
- restart a fixture server,
- resume a Codex session by recorded session id.

Any substantive debugging, design, prioritization, or implementation guidance
changes the condition to `guided` and makes the run ineligible for comparison
with administrative-only runs.

## Finalization

At stop, the harness updates `benchmark-run.md` with:

- stop reason,
- observed elapsed time,
- observed turns,
- observed token, tool-call, and cost usage when known,
- final commit,
- latest build command,
- latest test command,
- latest smoke-test command,
- latest verification result,
- comparison eligibility and reason.

Then it writes a final checkpoint and exits nonzero only for harness failure. A
normal benchmark stop due to success, budget exhaustion, idle, or model blockage
is a completed harness run, even if the submitted browser scores poorly.

## Minimal CLI Shape

The first implementation should expose:

```bash
python3 scripts/codex_meta_harness.py init \
  --target m5 \
  --profile standard-v0 \
  --model <model> \
  --codex-command "ollama-codex --model glm-5.1:cloud" \
  --codex-command-mode interactive-shell \
  --sandbox workspace-write

python3 scripts/codex_meta_harness.py run --run-id <run-id>

python3 scripts/codex_meta_harness.py resume --run-id <run-id>

python3 scripts/codex_meta_harness.py status --run-id <run-id>

python3 scripts/codex_meta_harness.py finalize --run-id <run-id>
```

The implementation should use only Python standard-library modules until a
dependency decision is recorded.

## Acceptance Criteria

The first usable harness is complete when it can:

- run `smoke-v0` for M1 without manual prompt copying,
- resume a stopped Codex session by recorded session id,
- restart a stopped agent subprocess at the next turn without changing the
  model-visible benchmark condition,
- produce turn logs, prompt files, state, and checkpoints,
- update `benchmark-run.md`,
- enforce wall-clock, turn, idle, and failure limits,
- run `python3 scripts/vibe_bench.py validate`,
- stop cleanly with a recorded reason,
- avoid committing ignored raw logs or secrets by default.

The first serious harness is complete when it can run `standard-v0` for M5 for
24 hours without unrecorded human guidance and leave enough evidence for
[Evaluator Procedure](evaluator-procedure.md).

## Open Decisions

- Whether raw logs should be force-added on archival run branches or exported as
  compact summaries.
- Whether standard runs should allow dependency downloads by default.
- Whether each run should use an isolated `CODEX_HOME`.
- Which Codex JSON events provide stable token, tool-call, cost, and session-id
  fields.
- Whether serious runs should execute in a disposable container or a normal git
  worktree with `workspace-write` sandboxing.
