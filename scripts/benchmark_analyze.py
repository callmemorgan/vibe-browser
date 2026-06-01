#!/usr/bin/env python3
"""Generate human-readable run analysis markdown."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from benchmark_db import export_results
from benchmark_lib import (
    ANALYSIS_DIR,
    html_escape,
    ingest_artifact_dir,
    load_results,
    read_json,
    score_result,
    validate_result,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Canonical result JSON files or raw artifact directories.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Read benchmark results from this SQLite database.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ANALYSIS_DIR,
        help="Directory for generated markdown analysis files.",
    )
    return parser


def load_input(path: Path) -> dict:
    if path.is_dir():
        return score_result(ingest_artifact_dir(path))
    return score_result(read_json(path))


def expand_inputs(paths: list[Path]) -> list[dict]:
    results: list[dict] = []
    for path in paths:
        if path.is_dir() and (path / "run" / "state.json").exists():
            results.append(score_result(ingest_artifact_dir(path)))
        elif path.is_dir():
            results.extend(load_results([path]))
        else:
            results.append(score_result(read_json(path)))
    return results


def analysis_markdown(result: dict) -> str:
    run = result["run"]
    scores = result["scores"]
    verification = result.get("verification_results", [])
    turns = result.get("turns", [])
    attempts = result.get("attempts", [])
    tool_calls = result.get("tool_calls", [])
    artifacts = result.get("artifacts", [])

    passing = sum(1 for item in verification if item.get("status") == "pass")
    failing = [item for item in verification if item.get("status") in {"fail", "error", "timeout", "blocked"}]
    total_tool_calls = sum(int(item.get("count") or 0) for item in tool_calls)
    elapsed = run.get("observed_elapsed_seconds")
    suspicious: list[str] = []
    if scores.get("failure_class"):
        suspicious.append(f"Failure class recorded: `{scores['failure_class']}`.")
    if run.get("stop_reason") and "budget" in str(run["stop_reason"]):
        suspicious.append("Run stopped on a budget boundary; score reflects achieved artifacts only.")
    if not verification:
        suspicious.append("No verification results were attached.")
    if not artifacts:
        suspicious.append("No artifacts were attached.")
    if not suspicious:
        suspicious.append("No obvious suspicious conditions detected by v0 analysis.")

    lines = [
        f"# Run Analysis: {run['run_id']}",
        "",
        "## Summary",
        "",
        f"- Model: `{run['model_provider']}/{run['model']}`",
        f"- Agent/tool: `{run['agent_tool']}` via `{run['harness']}`",
        f"- Target: `{run['target']}` in `{run['profile']}`",
        f"- Stop reason: `{run['stop_reason']}`",
        f"- Final score: `{scores['final_score']:.2f}` with confidence `{scores['confidence']:.2f}`",
        f"- Highest confirmed milestone: `{scores.get('highest_confirmed_milestone') or 'none'}`",
        "",
        "## What Happened",
        "",
        f"The run produced `{len(turns)}` recorded turns, `{len(attempts)}` agent attempts, "
        f"and `{total_tool_calls}` summarized tool calls. Observed elapsed time was "
        f"`{elapsed if elapsed is not None else 'unknown'}` seconds.",
        "",
        "## Verification",
        "",
        f"- Verification records: `{len(verification)}`",
        f"- Passing records: `{passing}`",
        f"- Failing records: `{len(failing)}`",
        "",
        "## Milestone Scores",
        "",
        "| Milestone | Evaluator | Public | Points | Notes |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for milestone in scores["milestones"]:
        lines.append(
            "| {milestone} | {evaluator:.2f} | {public:.2f} | {points:.2f} | {notes} |".format(
                milestone=milestone["milestone"].upper(),
                evaluator=milestone["evaluator_score"],
                public=milestone["public_check_score"],
                points=milestone["points"],
                notes=str(milestone.get("notes") or "").replace("|", "\\|"),
            )
        )

    lines.extend(
        [
            "",
            "## Suspicious Or Important Conditions",
            "",
        ]
    )
    for item in suspicious:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "| Artifact | Kind | Visibility | Path |",
            "| --- | --- | --- | --- |",
        ]
    )
    for artifact in artifacts:
        lines.append(
            "| {artifact_id} | {kind} | {visibility} | `{path}` |".format(
                artifact_id=artifact.get("artifact_id", ""),
                kind=artifact.get("kind", ""),
                visibility=artifact.get("visibility", ""),
                path=str(artifact.get("path", "")).replace("`", ""),
            )
        )
    lines.append("")
    lines.append("Generated by `scripts/benchmark_analyze.py`.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    if args.db:
        results.extend(export_results(args.db))
    results.extend(expand_inputs(args.inputs))
    if not results:
        print("benchmark_analyze: no inputs or database results found", file=sys.stderr)
        return 2
    failures = 0
    for result in results:
        errors = validate_result(result)
        if errors:
            print(f"benchmark_analyze: {result.get('run', {}).get('run_id', 'unknown')}: {errors[0]}", file=sys.stderr)
            failures += 1
            continue
        run_id = result["run"]["run_id"]
        output = args.output_dir / f"{run_id}.md"
        output.write_text(analysis_markdown(result), encoding="utf-8")
        print(f"Wrote {html_escape(output)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
