# Repository Guidelines

## Project Structure & Module Organization

This repository is the Vibe Browser benchmark packet, not a browser
implementation. `README.md` is the entry point. `docs/` contains benchmark
guidance, scoring, architecture, prompt sets, and ADRs. `fixtures/` holds
authored smoke-test pages by milestone. `scripts/` contains standard-library
helpers: `vibe_bench.py`, `codex_meta_harness.py`, and
`pi_docker_benchmark.py`. `tests/` contains `unittest` coverage. `specs/` and
`specs.zip` are vendored inputs; do not hand-edit spec snapshots.

## Build, Test, and Development Commands

- `python3 scripts/vibe_bench.py validate`: checks docs, fixtures, and Markdown
  links.
- `python3 scripts/vibe_bench.py serve-fixtures --port 8765`: serves
  `fixtures/` locally for browser-submission smoke checks.
- `python3 scripts/vibe_bench.py render-prompt --target m1 --include-system`:
  renders the participant prompt for a milestone.
- `python3 scripts/codex_meta_harness.py init --target m5 --model glm-5.1:cloud --codex-command "ollama-codex --model glm-5.1:cloud" --codex-command-mode interactive-shell`:
  initializes a Codex-controlled benchmark run.
- `python3 scripts/pi_docker_benchmark.py run --target m1 --wall-clock-limit 10m --provider ollama --model glm-5.1:cloud`:
  runs the PI/Ollama smoke benchmark in Docker.
- `python3 -m unittest discover -s tests`: runs repository unit tests.

No package manager or application build step is required.

## Coding Style & Naming Conventions

Use Markdown for benchmark guidance. Keep docs concise, link new docs from a
reachable doc, and prefer local links such as
`../specs/url.html` when citing standards. Python code should remain
standard-library-only unless a dependency decision is recorded, use 4-space
indentation, type hints where helpful, and `snake_case` for functions and
variables. Run branch slugs should be lowercase ASCII with hyphens, following
`runs/<profile>/<harness>/<tool>/<model>/<timestamp>-<target>-<run-id>`.

## Testing Guidelines

For documentation or harness changes, run `python3 scripts/vibe_bench.py
validate` before submitting. For fixture or milestone changes, also run
`serve-fixtures` and manually verify representative URLs. New fixtures should
live under the relevant milestone directory and avoid advanced APIs unless the
milestone requires them. Do not claim browser compatibility without tests or
clear status labels such as `partial`, `deferred`, or `blocked`.

## Commit & Pull Request Guidelines

Recent commits use short imperative subjects such as `Add local smoke bench
plumbing`, with occasional scoped docs subjects like `docs: add run organization
and meta-harness documentation`. Keep commits narrow, especially around
`specs/` or `specs.zip`. PRs need a summary and relevant context; link docs,
ADRs, or specs when scope or scoring changes. Do not add a required "Test plan"
section.

## Security & Configuration Tips

Treat remote web content as hostile in all browser-submission guidance.
`.vibe-bench/` is local run output and ignored by git. `run-openai` may read
`OPENAI_BASE_URL` and `OPENAI_API_KEY`; avoid committing endpoints, secrets, or
transcripts unless intentionally reviewed.
