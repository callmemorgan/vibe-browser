# Product Brief

## Purpose

The leaderboard helps maintainers, model builders, and benchmark participants
compare how far agents get when building a browser from the Vibe Browser task
packet. It supports both targeted milestone runs and open-ended "get as far as
you can" runs.

## Primary Users

- Benchmark maintainers reviewing run quality and harness health.
- Model/tool teams comparing agent performance under fixed conditions.
- Evaluators scoring submissions against the rubric.
- Participants inspecting why a run did or did not qualify.

## Core Questions

- Which agent got furthest under the same benchmark condition?
- Which runs are comparison eligible?
- What evidence supports a milestone or score claim?
- Did a model fail because of capability, tooling, budget, or benchmark setup?
- How reproducible is a submitted result?

## Non-Goals

- Do not provide hidden evaluator feedback to active agents.
- Do not mix guided and administrative-only runs in one ranked table.
- Do not collapse all quality into one unexplained score.
- Do not require full browser compatibility before showing useful progress.

## Success Criteria

- A reviewer can identify the top comparable run in under 30 seconds.
- A reviewer can open any score and see evidence in one click.
- Open-ended runs show progress beyond the last fully confirmed milestone.
- Runs with incompatible conditions are visually separated or excluded by
  default.
