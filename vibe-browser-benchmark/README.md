# Vibe Browser Benchmark UI Specs

This folder describes a leaderboard UI for comparing Vibe Browser benchmark
runs. The product should make model progress legible without hiding the
engineering evidence behind a single score.

## Runnable Prototype

The prototype spine turns raw harness artifacts into canonical result JSON,
stores scored runs in SQLite, writes analysis markdown, and serves a local
leaderboard from that database. Generated `.db` files are ignored by Git.

```bash
# Refresh examples and seed a local SQLite database.
python3 scripts/benchmark_examples.py \
  --db vibe-browser-benchmark/benchmark.db \
  --reset-db

# Normalize a raw Docker harness artifact into canonical JSON and SQLite.
python3 scripts/benchmark_ingest.py .vibe-bench/docker-artifacts/pi20260601044042 \
  --output vibe-browser-benchmark/examples/runs/pi20260601044042.json \
  --db vibe-browser-benchmark/benchmark.db

# Score/list database results, or upsert files into the database.
python3 scripts/benchmark_score.py --db vibe-browser-benchmark/benchmark.db
python3 scripts/benchmark_score.py vibe-browser-benchmark/examples/runs \
  --db vibe-browser-benchmark/benchmark.db

# Generate per-run analysis markdown from SQLite.
python3 scripts/benchmark_analyze.py --db vibe-browser-benchmark/benchmark.db

# Serve the live SQLite-backed UI and API.
python3 scripts/benchmark_site.py serve \
  --db vibe-browser-benchmark/benchmark.db \
  --port 8765

# Build and validate the portable static export.
python3 scripts/benchmark_site.py build --db vibe-browser-benchmark/benchmark.db
python3 scripts/benchmark_validate.py --db vibe-browser-benchmark/benchmark.db
```

Open `http://127.0.0.1:8765/` for the live SQLite-backed prototype. The served
site exposes `/api/runs`, `/api/runs/<run-id>`, `/api/compare`, and
`/results.json`. The static build still embeds `assets/results.js`, so filters
and comparison work from a local file without a server.

## Spec Index

- [Product Brief](product-brief.md): audience, goals, and non-goals.
- [Leaderboard UX](leaderboard-ux.md): primary screens, filters, states, and
  interactions.
- [Run Detail UX](run-detail-ux.md): evidence view for a single benchmark run.
- [Data Model](data-model.md): canonical entities and fields.
- [Scoring and Ranking](scoring-and-ranking.md): ranking rules and comparison
  guardrails.
- [Milestone Rubrics](milestone-rubrics.md): per-milestone scoring dimensions.
- [Blended Score](blended-score.md): combined progress and quality score.
- [Completed Specs](specs/README.md): standalone specs expanded from backlog
  entries.
- [Spec Status](spec-status.md): progress tracker and next recommended batch.
- [Corpus Map](distilled/corpus-map.md): distilled navigation guide for keeping
  context small as the corpus grows.
- [Spec Backlog](spec-backlog.md): additional benchmark, governance, public
  site, and operations specs still worth writing.
- [Final Gap Analysis](final-gap-analysis.md): last-pass blind spots before the
  benchmark graduates from leaderboard product to public benchmark program.
- [JSON Schema](schema/result.schema.json): machine-readable v0.1 import/export
  result schema.
- [Example Runs](examples/runs/): canonical sample dataset for scorer and UI
  dogfooding.

## Design Principles

- Evidence first: every score links back to commands, logs, artifacts, or
  evaluator notes.
- Comparability is explicit: do not rank runs together when profile, target,
  prompt set, benchmark commit, or intervention policy differ.
- Partial progress matters: open-ended runs should show the highest claimed,
  public-check, and evaluator-confirmed milestone.
- Honest limitations are a feature: blockers and unsupported behavior should be
  visible, not buried.
- Operational UI, not marketing: dense tables, clear filters, stable metrics,
  and fast drill-downs.

## Prototype Boundaries

- Scores are deterministic v0 estimates, not official evaluator judgments.
- JSON Schema is documented and partially enforced by
  `scripts/benchmark_validate.py`; full JSON Schema validation can be added
  when the project accepts a validator dependency.
- SQLite is the canonical local datastore for the runnable prototype; JSON
  remains the portable import/export format.
- The served site is local-only and intentionally standard-library based.
- Dogfood evidence intentionally copies public-safe manifests, diffs, status,
  and verification logs; raw agent transcripts are not published by the example
  generator.
