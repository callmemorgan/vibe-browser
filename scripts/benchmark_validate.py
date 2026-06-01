#!/usr/bin/env python3
"""Validate benchmark result data and generated benchmark site files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from benchmark_db import export_results
from benchmark_lib import (
    EXAMPLES_DIR,
    ROOT,
    SITE_DIR,
    default_example_paths,
    load_results,
    score_result,
    validate_result,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "results",
        nargs="*",
        type=Path,
        help="Canonical result JSON files or directories. Defaults to example runs.",
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=SITE_DIR,
        help="Generated static site directory to check.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Validate benchmark results exported from this SQLite database.",
    )
    parser.add_argument(
        "--skip-site",
        action="store_true",
        help="Skip generated static site checks.",
    )
    return parser


def path_exists(path_value: str | None) -> bool:
    if not path_value:
        return True
    path = Path(path_value)
    if path.is_absolute():
        return path.exists()
    return (ROOT / path).exists()


def validate_artifact_links(result: dict) -> list[str]:
    errors: list[str] = []
    run_id = result["run"]["run_id"]
    public_ids = {
        artifact["artifact_id"]
        for artifact in result.get("artifacts", [])
        if artifact.get("visibility") == "public"
    }
    for score in result.get("scores", {}).get("milestones", []):
        for evidence_id in score.get("evidence_ids", []):
            if evidence_id not in public_ids and evidence_id != "verification-results":
                errors.append(f"{run_id}: missing public evidence artifact {evidence_id}")
    for artifact in result.get("artifacts", []):
        if artifact.get("visibility") == "public" and not path_exists(artifact.get("path")):
            errors.append(f"{run_id}: artifact path does not exist: {artifact.get('path')}")
    return errors


def validate_site(site_dir: Path) -> list[str]:
    errors: list[str] = []
    if not site_dir.exists():
        errors.append(f"site directory missing: {site_dir}")
        return errors
    for relative in (
        "index.html",
        "compare.html",
        "assets/site.css",
        "assets/site.js",
        "assets/results.js",
        "results.json",
    ):
        if not (site_dir / relative).exists():
            errors.append(f"site file missing: {site_dir / relative}")
    run_pages = list((site_dir / "runs").glob("*.html")) if (site_dir / "runs").exists() else []
    if not run_pages:
        errors.append(f"no run detail pages found under {site_dir / 'runs'}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = args.results or ([] if args.db else default_example_paths())
    results: list[dict] = []
    if paths:
        results.extend(load_results(paths))
    if args.db:
        results.extend(export_results(args.db))
    if not results:
        source = args.db if args.db else EXAMPLES_DIR
        print(f"benchmark_validate: no result files found under {source}", file=sys.stderr)
        return 2

    errors: list[str] = []
    seen_run_ids: set[str] = set()
    for result in results:
        scored = score_result(result)
        run_id = scored.get("run", {}).get("run_id")
        if run_id in seen_run_ids:
            errors.append(f"duplicate run_id: {run_id}")
        seen_run_ids.add(run_id)
        errors.extend(f"{run_id}: {error}" for error in validate_result(scored))
        errors.extend(validate_artifact_links(scored))

    if not args.skip_site:
        errors.extend(validate_site(args.site_dir))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    site_note = f" and site {args.site_dir}" if not args.skip_site else ""
    print(f"Validated {len(seen_run_ids)} benchmark result(s){site_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
