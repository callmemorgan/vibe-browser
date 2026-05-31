# ADR 0002: Run Branch Organization

Status: accepted

Date: 2026-05-31

## Context

The benchmark will produce many submitted browser implementations across models,
tools, harnesses, prompts, and time budgets. These outputs are expected to be
large, divergent, and useful to inspect as diffs from the benchmark baseline.

The repository needs a default organization scheme before runs begin so results
remain comparable and the `main` branch stays focused on benchmark inputs,
documentation, and harness code.

## Decision

Store each benchmark run on its own branch using:

```text
runs/<profile>/<harness>/<tool>/<model>/<timestamp>-<target>-<run-id>
```

Each run branch must include a root `benchmark-run.md` manifest with exact
harness, tool, model, prompt, budget, environment, baseline commit, stable run
ID, and verification metadata.

Run branches are archival by default and are not merged into `main`. Benchmark
fixes discovered during a run should be moved through normal maintenance
branches.

## Consequences

- Run artifacts stay isolated from the benchmark baseline.
- Branch listings make it easy to group runs by profile, harness, tool, and
  model.
- The diff from `main` remains the primary implementation artifact.
- Exact metadata lives in a manifest instead of being squeezed into a branch
  name.
- Long-lived repositories may accumulate many remote branches, so maintainers may
  later add tags, dashboards, or retention rules.

## Alternatives Considered

- Store every run under a `runs/` directory on `main`: rejected because it would
  make the benchmark baseline noisy and hard to review.
- Use tags only: rejected because tags do not provide a natural place for mutable
  run notes, evaluation commits, or review workflows.
- Use pull requests for every run: useful as an optional review layer, but too
  heavy as the only required storage model.
- Use an external database first: deferred because git branches and manifests are
  enough for early benchmark reproducibility.
