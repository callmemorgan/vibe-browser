# Contributing

Vibe Browser is a benchmark corpus plus documentation for evaluating LLM agents
on building a web browser from scratch. Contributions should make the benchmark
clearer, more reproducible, and easier to evaluate without accidentally changing
the task inputs.

## Contribution Defaults

- Keep changes narrow and reviewable.
- Separate vendored spec updates from benchmark docs or harness changes.
- Do not hand-edit files under `specs/`.
- Update docs when changing architecture guidance, standards scope, security
  expectations, privacy expectations, or scoring rules.
- Prefer explicit status labels over vague claims.
- Preserve benchmark comparability unless the PR explicitly changes benchmark
  scope.

## Before Changing Benchmark Guidance

For changes that affect the participant task or evaluator rubric:

1. Identify the affected milestone in [Roadmap](roadmap.md).
2. Identify the affected tier in [Standards Strategy](standards-strategy.md).
3. Read the relevant architecture, security, privacy, and testing sections.
4. Decide whether an ADR is needed for a durable technical choice.
5. Define how the change affects scoring, artifacts, and comparability.

## Before Adding Harness or Example Code

Benchmark harnesses, fixtures, and example implementations should:

- Be clearly marked as benchmark infrastructure or examples.
- Avoid giving one model run hidden implementation help unless that is the
  intended experimental condition.
- Include reproducible commands.
- Keep generated outputs separate from authored rubric or corpus changes.

## Pull Request Expectations

PR descriptions should include:

- Summary of the change.
- Context or root cause when relevant.
- Links to updated docs, ADRs, or specs when the change affects benchmark scope
  or scoring.

Do not include a required "Test plan" section unless benchmark policy changes.
Tests and verification can still be described naturally in the PR body or commit
message when helpful.

## Review Expectations

Reviewers should check:

- Does the change match the documented roadmap and standards tier?
- Does it create a new security, privacy, or scoring decision?
- Are trust boundaries preserved?
- Are benchmark acceptance checks appropriate for the risk?
- Are docs updated when guidance, scope, or scoring changed?
- Are vendored specs untouched unless the PR is explicitly about corpus updates?
- Does the change preserve comparability for existing benchmark runs?

## Documentation Style

- Use Markdown.
- Keep docs honest about benchmark status and submission expectations.
- Prefer local spec links such as `../specs/url.html` where practical.
- Use the shared status vocabulary from `README.md`.
- Avoid claiming compatibility without tests.
- Avoid framing this repository as the submitted browser implementation.

## ADRs

Use an Architecture Decision Record for choices that future contributors should
not rediscover from scratch, such as:

- Benchmark corpus structure.
- Scoring rubric changes.
- Required participant artifacts.
- Harness architecture.
- Telemetry policy for benchmark runs.
- Major standards scope changes.
- Compatibility-impacting corpus refreshes.

ADRs live in `docs/adr/` and should be numbered sequentially.
