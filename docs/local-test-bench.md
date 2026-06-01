# Local Test Bench

This document describes the lightweight plumbing for running the first local-model
Vibe Browser smoke tests. The bench is intentionally small: it can create run
metadata, render prompts, call an OpenAI-compatible local model endpoint, serve
fixtures, and validate benchmark docs. It is not yet a fully autonomous coding
agent.

## What This Bench Proves

The first local run should answer a narrow question: can a small local model read
the benchmark packet, follow a milestone target, and produce useful implementation
instructions or artifacts without drifting into unrelated scope?

Use the bench for:

- `smoke-v0` / M1 harness shakedowns.
- Prompt and manifest validation before a more capable agent run.
- Fixture-server smoke checks for M2 through M5 submissions.
- Capturing local-model transcripts for evaluator review.

Do not use early bench output as a leaderboard-quality comparison until the
runner, environment, and scoring workflow are calibrated.

## Script Overview

`scripts/vibe_bench.py` uses only the Python standard library and provides these
subcommands:

- `init-run`: create a run branch name, root `benchmark-run.md`, rendered initial
  prompt, and local run metadata under `.vibe-bench/runs/`.
- `render-prompt`: render `docs/participant-task.md` with a concrete target
  milestone.
- `run-openai`: call a local OpenAI-compatible `/v1/chat/completions` endpoint
  and save transcripts.
- `serve-fixtures`: serve `fixtures/` over HTTP, including redirect, 404, and
  explicit `text/html` behavior for M2 smoke checks.
- `validate`: check expected docs, fixture files, and local Markdown links.

## Quick Start: Manual M1 Smoke Run

Start from a clean checkout on the benchmark baseline branch.

```bash
python3 scripts/vibe_bench.py validate
python3 scripts/vibe_bench.py init-run \
  --target m1 \
  --profile smoke-v0 \
  --model llama3.2 \
  --create-branch
```

This writes:

- `benchmark-run.md`
- `.vibe-bench/runs/<run-id>/initial-prompt.md`
- `.vibe-bench/runs/<run-id>/metadata.json`

If your local model exposes an OpenAI-compatible endpoint, run one or more
transcript turns:

```bash
python3 scripts/vibe_bench.py run-openai \
  --target m1 \
  --model llama3.2 \
  --endpoint http://localhost:11434/v1 \
  --turns 1
```

The default endpoint is `http://localhost:11434/v1`, which matches Ollama's
OpenAI-compatible API when enabled. Other local runners can be used if they
implement `/v1/chat/completions`.

The runner records model output only. Review the transcript, then apply any
useful implementation steps manually or through the agent tool under test.

## Fixture Server

For M2 and later smoke checks, serve the public fixtures locally:

```bash
python3 scripts/vibe_bench.py serve-fixtures --port 8765
```

Useful URLs include:

- `http://127.0.0.1:8765/m2-network/hello.html`
- `http://127.0.0.1:8765/m2-network/redirect.html`
- `http://127.0.0.1:8765/m2-network/content-type-html.txt`
- `http://127.0.0.1:8765/m2-network/not-found.html`
- `http://127.0.0.1:8765/m3-html-dom/title.html`
- `http://127.0.0.1:8765/m4-style-layout/block-layout.html`
- `http://127.0.0.1:8765/m5-paint/colors-and-borders.html`

The server maps `/m2-network/redirect.html` to a `302` response, serves
`/m2-network/not-found.html` with `404`, and forces
`/m2-network/content-type-html.txt` to `text/html`.

## Suggested Local-Model Pilot Sequence

1. Run `smoke-v0` / M1 with one local model and one transcript turn.
2. Review whether the model stayed within M1 and respected the constraints in
   `docs/participant-task.md`.
3. If useful, apply the model's implementation through the coding tool under
   evaluation, run its build/test/smoke commands, and update `benchmark-run.md`.
4. Repeat with `sprint-v0` / M2 or M3 only after M1 plumbing works.
5. Treat `standard-v0` / M5 as a later serious comparison target.

## Current Limitations

- The script does not execute model-proposed shell commands or edit files on the
  model's behalf.
- The script does not enforce wall-clock, token, or idle limits beyond recording
  profile defaults in `benchmark-run.md`.
- Token counts are recorded as `unknown` unless the model endpoint includes usage
  metadata in its response.
- Transcript logs under `.vibe-bench/` are local run artifacts and are not meant
  for the benchmark baseline unless intentionally reviewed and committed.
