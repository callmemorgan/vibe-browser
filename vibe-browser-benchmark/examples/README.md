# Example Benchmark Results

This directory contains the prototype seed dataset used by the scorer, analyzer,
SQLite datastore, and leaderboard.

## Layout

- `runs/`: canonical `vibe-browser-result-v0.1` JSON records.
- `analysis/`: generated markdown summaries from `scripts/benchmark_analyze.py`.
- `artifacts/`: public-safe evidence files linked by result JSON and run pages.

## Included Cases

- `example-success-short`: successful focused M1 run.
- `example-partial`: partial progress into M2.
- `example-failed`: verification failure and non-rankable result.
- `example-restarted`: agent restart/intervention case.
- `example-messy`: intentionally weak metadata and error handling case.
- `pi20260601044042`: normalized dogfood result from a real Pi/Ollama
  `glm-5.1:cloud` Docker benchmark artifact.

Regenerate examples with:

```bash
python3 scripts/benchmark_examples.py \
  --db vibe-browser-benchmark/benchmark.db \
  --reset-db
```

The SQLite database is generated locally and ignored by Git. The checked-in JSON
files remain the portable seed data and review format.
