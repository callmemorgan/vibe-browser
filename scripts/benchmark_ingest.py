#!/usr/bin/env python3
"""Normalize raw harness artifacts into canonical benchmark result JSON."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from benchmark_db import upsert_result
from benchmark_lib import BenchmarkError, ingest_artifact_dir, score_result, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "artifact_dir",
        type=Path,
        help="Raw artifact directory, for example .vibe-bench/docker-artifacts/<run-id>",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write normalized JSON to this path. Defaults to stdout.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Upsert the normalized result into this SQLite database.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = score_result(ingest_artifact_dir(args.artifact_dir))
    except (BenchmarkError, FileNotFoundError, ValueError) as exc:
        print(f"benchmark_ingest: {exc}", file=sys.stderr)
        return 2

    if args.output:
        write_json(args.output, result)
        print(f"Wrote {args.output}")
    if args.db:
        stored = upsert_result(args.db, result)
        print(f"Upserted {stored['run']['run_id']} into {args.db}")
    if not args.output and not args.db:
        import json

        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
