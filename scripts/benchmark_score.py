#!/usr/bin/env python3
"""Score canonical Vibe Browser Benchmark result JSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from benchmark_db import export_results, upsert_result
from benchmark_lib import default_example_paths, load_results, score_result, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results",
        nargs="*",
        type=Path,
        help="Canonical result JSON files or directories. Defaults to example runs.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print scored result JSON instead of a text table.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Write scored result JSON files to this directory.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Read from this SQLite database; with input files, also upsert them first.",
    )
    return parser


def print_table(results: list[dict]) -> None:
    rows = []
    ranked = sorted(
        results,
        key=lambda result: (
            not result["scores"].get("rankable", False),
            -float(result["scores"].get("final_score", 0)),
            result["run"]["run_id"],
        ),
    )
    for result in ranked:
        run = result["run"]
        scores = result["scores"]
        rows.append(
            [
                run["run_id"],
                f"{run['model_provider']}/{run['model']}",
                run["agent_tool"],
                run["target"],
                scores.get("highest_confirmed_milestone") or "-",
                f"{scores['final_score']:.2f}",
                f"{scores['confidence']:.2f}",
                scores.get("failure_class") or "-",
                "yes" if scores.get("rankable") else "no",
            ]
        )
    headers = ["run_id", "model", "agent", "target", "milestone", "final", "conf", "failure", "rank"]
    widths = [
        max(len(str(row[index])) for row in rows + [headers])
        for index in range(len(headers))
    ]
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.db:
        if args.results:
            loaded = [score_result(result) for result in load_results(args.results)]
            for result in loaded:
                upsert_result(args.db, result)
            results = loaded
        else:
            results = export_results(args.db)
    else:
        paths = args.results or default_example_paths()
        if not paths:
            print("benchmark_score: no result files found", file=sys.stderr)
            return 2
        results = [score_result(result) for result in load_results(paths)]

    if not results:
        source = args.db if args.db else "input paths"
        print(f"benchmark_score: no result files found in {source}", file=sys.stderr)
        return 2

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for result in results:
            write_json(args.output_dir / f"{result['run']['run_id']}.json", result)

    if args.json:
        payload = results[0] if len(results) == 1 else {"results": results}
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_table(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
