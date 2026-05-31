# Run Organization

Each benchmark run should happen on its own git branch. The branch name should
encode the meta-harness profile, harness, tool, and model so results stay easy to
find without opening every run artifact.

Branch-per-run is the default because it isolates generated browser code,
preserves the exact diff from the benchmark baseline, and makes it easy to push,
review, archive, or delete one attempt at a time.

## Branch Naming

Use this branch shape:

```text
runs/<profile>/<harness>/<tool>/<model>/<timestamp>-<target>-<run-id>
```

Example:

```text
runs/standard-v0/manual-v0/codex-cli/gpt-5-4/20260531-1542-m3-r001
```

Components:

- `profile`: meta-harness profile slug, such as `smoke-v0`, `sprint-v0`,
  `standard-v0`, or `endurance-v0`.
- `harness`: benchmark harness or protocol slug, such as `manual-v0`,
  `smoke-v0`, or `wpt-v0`.
- `tool`: agent or execution tool slug, such as `codex-cli`, `claude-code`, or
  `cursor-agent`.
- `model`: model slug, such as `gpt-5-4` or `claude-opus-4-1`.
- `timestamp`: UTC start time in `YYYYMMDD-HHMM` format.
- `target`: targeted roadmap milestone or open-ended objective, such as `m1`,
  `m3`, or `open`.
- `run-id`: stable short run identifier, such as `r001` or the first 8
  characters of a generated UUID.

Slugs should be lowercase ASCII and use hyphens for separators. Replace spaces,
slashes, colons, and provider punctuation with hyphens. Keep exact names,
versions, and checksums in the run manifest.

The branch name is an index, not identity. The stable run identity is the
manifest `Run ID`, because branches can be renamed or mirrored.

## Run Manifest

Every run branch should include a `benchmark-run.md` file at the repository root.
The manifest is the source of truth for metadata that does not fit safely in a
branch name.

Record:

- Run ID.
- Base benchmark commit.
- Corpus digest or benchmark input digest when available.
- Branch name.
- Harness name and version.
- Meta-harness profile, configured budgets, and observed usage.
- Tool name and version.
- Model provider, exact model name, and model version or snapshot when known.
- Prompt or prompt-set identifier and checksum when available.
- Target roadmap milestone or objective.
- Time budget, tool access, and environment constraints.
- Stop reason and comparison eligibility after the run completes.
- Build, test, and smoke-test commands.
- Links to evaluation notes or artifacts when added.

The branch name is for navigation. The manifest is for scoring and
reproducibility.

## Manifest Template

Use this shape for the root `benchmark-run.md` file:

```markdown
# Benchmark Run

## Identity

- Run ID:
- Branch:
- Base benchmark commit:
- Benchmark input digest:
- Target:

## Harness

- Harness:
- Harness version:
- Meta-harness profile:
- Tool:
- Tool version:
- Model provider:
- Model:
- Model snapshot:
- Prompt set:
- Prompt checksum:

## Budgets

- Wall-clock limit:
- Token limit:
- Turn limit:
- Tool-call limit:
- Cost limit:
- Idle limit:
- Failure limit:

## Environment

- Operating system:
- Runtime dependencies:
- Network access:
- Tool permissions:
- Human intervention policy:

## Verification

- Build command:
- Test command:
- Smoke-test command:
- Latest verification result:

## Completion

- Stop reason:
- Observed elapsed time:
- Observed token usage:
- Observed turns:
- Observed tool calls:
- Final commit:
- Comparison eligible:
- Notes:
```

## Branch Lifecycle

1. Start from the benchmark baseline branch, usually `main`.
2. Create a stable Run ID and the run branch using the naming scheme above.
3. Commit the run manifest before or with the first generated implementation
   commit.
4. Let the model and harness write implementation artifacts on that branch.
5. Add evaluator notes, scores, and logs as follow-up commits on the same branch
   when practical.
6. Push the branch to the shared GitHub repository for archival.
7. Do not merge run branches back to `main` by default.

If a run reveals a benchmark bug or missing harness feature, fix that through a
normal benchmark-maintenance branch and PR. Do not quietly merge generated
browser code into the benchmark baseline.

## Why This Shape

Branch-per-run is better than committing all run outputs under `main` because
generated browser implementations will be large, noisy, and intentionally
divergent. Keeping them on separate branches prevents the benchmark baseline from
turning into an archive dump.

Branch names alone are not enough. Model names change, tool versions matter,
prompts matter, and branch names have awkward character restrictions. The run
manifest keeps the full metadata stable and reviewable.

Tags can be added later for immutable score snapshots, and draft PRs can be used
when reviewers want GitHub's diff UI for a specific run. Those are optional
layers on top of the branch-per-run structure, not replacements for it.

## Comparison Rules

Runs should be compared only when these fields match or are intentionally grouped:

- Base benchmark commit or benchmark input digest.
- Meta-harness profile.
- Harness and prompt set.
- Target milestone or objective.
- Tool access policy.
- Human intervention policy.

Model and tool names are the thing being compared, so they do not need to match.
Everything else should match unless the comparison explicitly studies that
variable.
