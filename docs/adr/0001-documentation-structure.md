# ADR 0001: Documentation Structure

Status: accepted

Date: 2026-05-31

## Context

The repository began as a large local standards corpus under `specs/`, plus a
compressed `specs.zip` copy. The objective is to use that corpus as the input to
a benchmark that asks LLM agents to build a web browser from scratch.

Before benchmark runs are comparable, maintainers and participants need a durable
place for benchmark intent, reference architecture, standards priorities,
security and privacy expectations, roadmap phases, scoring expectations, and spec
corpus maintenance rules.

## Decision

Use Markdown files under `docs/` for benchmark-authored documentation, with
`README.md` as the root entrypoint.

Architecture Decision Records live under `docs/adr/` and are numbered
sequentially.

Vendored standards snapshots remain under `specs/` and are not hand-edited.

## Consequences

- Benchmark documentation is readable and reviewable before any harness exists.
- Benchmark decisions are separated from upstream specs.
- Participants have a stable task packet for understanding expected browser
  deliverables.
- Evaluators have a stable place for rubric and scope decisions.
- Future generated reports or harness docs can be added later without replacing
  the authored benchmark docs.

## Alternatives Considered

- Wiki-only documentation: rejected because it would not travel with code review
  and local development.
- Generated docs only: rejected because no benchmark harness exists yet.
- Embedding benchmark notes in `specs/`: rejected because upstream spec snapshots
  should remain unmodified.
