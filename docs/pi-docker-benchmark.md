# PI Docker Benchmark

This document describes the disposable Docker path for a short PI/Ollama Vibe
Browser benchmark run.

## Purpose

Use this flow to validate the benchmark harness with PI as the agent harness,
Ollama as the provider, and `glm-5.1:cloud` as the model. The default target is a
10-minute `m1` smoke run. The container is the trust boundary: PI runs as root
inside Docker, while host credentials and home directories are not mounted.

## Build

Build the benchmark image from committed repository contents:

```bash
python3 scripts/pi_docker_benchmark.py build-image
```

The wrapper builds from `git archive HEAD`, not the live working tree. This keeps
untracked files and local edits out of the Docker context. The image pins the
Node base image by digest and installs the pinned PI package version recorded in
the Dockerfile. It also includes `python3-tk` and `xvfb` so GUI smoke checks can
run without a physical display.

The Docker wrapper refuses to start from a dirty host worktree by default. Commit
or stash local changes first so the copied image represents a clean benchmark
baseline. For deliberate experiments, pass `--allow-dirty-baseline` and treat
the result as non-comparable.

## Run

Start the 10-minute smoke run:

```bash
python3 scripts/pi_docker_benchmark.py run \
  --target m1 \
  --wall-clock-limit 10m \
  --provider ollama \
  --model glm-5.1:cloud
```

The wrapper initializes `scripts/codex_meta_harness.py` with:

- `--agent-kind pi`
- `--model-provider ollama`
- `--model glm-5.1:cloud`
- `--container-execution docker-admin-v0`
- `--wall-clock-limit 10m`
- `--turn-limit 100` unless you pass an explicit turn limit
- `--stream-agent-events`

The high default turn cap makes the wall-clock limit the primary limiter for the
10-minute smoke run. Pass `--turn-limit N` to make turn count binding again.

The run is attached, so compact agent progress appears in your terminal. The
wrapper also prints a watch command before the agent starts:

```bash
docker logs -f vibe-browser-pi-<run-id>
```

Use that from another terminal if you want Docker-native log following. Logs show
turn starts, tool calls, assistant start/finish events, stderr, and turn exit
status. Raw PI JSON remains in the copied run artifacts, not in the live log.
Pass `--no-stream-agent-events` to disable compact agent progress.

Artifacts are copied out after the container exits to
`.vibe-bench/docker-artifacts/<run-id>/`, including:

- `run/`: raw harness state, prompts, logs, verification logs, and checkpoints.
- `submission/`: copied participant-touched files for quick review.
- `summary.json`: run metadata, Docker image ID, versions, files, and metrics.
- `turn-metrics.json`: compact per-turn elapsed time, token, exit, and
  verification data.
- `version-info.json`: Python, Node, npm, Git, PI, kernel, and provider env
  details.
- `participant.diff`, `participant-git-status.txt`, and
  `participant-untracked-files.tar`.

Legacy aliases (`git-status.txt`, `worktree.diff`, and `untracked-files.tar`)
are also written for older analysis scripts.

After cleanup, the wrapper prints a final summary with the run ID, artifact
directory, exit code, stop reason, latest verification result, observed turns,
token count, and comparison eligibility.

## Verification

The meta-harness always runs `scripts/vibe_bench.py validate` when present and
then runs any build, test, and smoke-test commands recorded in
`benchmark-run.md`. For generated browser artifacts, it also auto-detects and
runs:

```bash
python3 -m unittest discover -s browser/tests -v
python3 -m browser.src.shell --headless https://example.com
```

If a generated `browser/src/shell.py` appears to use tkinter and `xvfb-run` is
available, verification also runs a minimal Tk display smoke check under Xvfb.

These fallback checks make the verification result cover the submitted browser
package even when the participant manifest has not yet listed test commands.

## Agent Restart Model

The PI process is not expected to stay alive for the full benchmark. The
meta-harness runs PI one turn at a time with the same session identity:

```bash
pi --session-id <run-id> --session-dir .vibe-bench/runs/<run-id>/pi/sessions
```

If PI exits, the harness records stdout, stderr, exit code, elapsed time, and
verification result, then starts a new PI process for the next turn. Nonzero
agent exits increment `failure_count`; the run continues until `failure_limit`
is reached, then stops as `blocked-infrastructure`. Clean exits continue through
the normal success, wall-clock, turn, token, idle, and verification stop rules.

This is turn-level restart. If the Docker container or outer wrapper is killed
before artifact export, rerunning `run` starts a fresh container run; container
resume is a separate workflow.

## Environment Policy

Only explicit environment variables are passed to Docker. By default, the wrapper
passes `OLLAMA_HOST` and `OLLAMA_API_KEY` when present. Add more with repeated
`--pass-env NAME` or explicit `--env NAME=value`.

PI does not ship Ollama as a built-in provider. The meta-harness writes a
run-local `models.json` for provider `ollama`, using `OLLAMA_HOST` when set and
falling back to `http://host.docker.internal:11434/v1` in Docker.

The wrapper does not mount the host repository, host home directory, or Docker
socket. PI state is kept under the run directory inside the copied repository:

- `PI_CODING_AGENT_DIR=.vibe-bench/runs/<run-id>/pi/agent`
- `PI_CODING_AGENT_SESSION_DIR=.vibe-bench/runs/<run-id>/pi/sessions`

## Dry Run

Print the Docker commands without executing them:

```bash
python3 scripts/pi_docker_benchmark.py run --print-only --skip-build
```
