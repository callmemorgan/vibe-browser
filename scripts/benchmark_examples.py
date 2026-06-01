#!/usr/bin/env python3
"""Generate the checked-in prototype benchmark example dataset."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
from typing import Any

from benchmark_db import upsert_result
from benchmark_lib import (
    ANALYSIS_DIR,
    BENCHMARK_ROOT,
    DIMENSION_WEIGHTS,
    EXAMPLES_DIR,
    MILESTONES,
    ROOT,
    SCHEMA_VERSION,
    ingest_artifact_dir,
    score_result,
    write_json,
)


ARTIFACT_DIR = BENCHMARK_ROOT / "examples" / "artifacts"
FIXED_CREATED_AT = "2026-06-01T12:00:00+00:00"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dogfood-artifact-dir",
        type=Path,
        default=Path(".vibe-bench/docker-artifacts/pi20260601044042"),
        help="Real Pi Docker artifact directory to normalize when available.",
    )
    parser.add_argument(
        "--skip-dogfood",
        action="store_true",
        help="Generate only synthetic examples.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Also upsert generated examples into this SQLite database.",
    )
    parser.add_argument(
        "--reset-db",
        action="store_true",
        help="Remove --db before writing examples, useful for deterministic local demos.",
    )
    return parser


def dimensions(score: float) -> dict[str, float]:
    return {name: score for name in DIMENSION_WEIGHTS}


def milestone_assessments(
    run_id: str,
    scores: dict[str, float],
    *,
    notes: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    notes = notes or {}
    rows: list[dict[str, Any]] = []
    for milestone in MILESTONES:
        score = scores.get(milestone, 0.0)
        rows.append(
            {
                "run_id": run_id,
                "milestone": milestone,
                "claimed_status": "confirmed" if score >= 0.75 else "partial" if score >= 0.5 else "not-started",
                "public_check_status": "pass" if score >= 0.75 else "fail" if score > 0 else "not-run",
                "evaluator_status": "provisional",
                "score": score,
                "dimensions": dimensions(score),
                "missing_evidence": [] if score >= 0.75 else ["stronger verification evidence"],
                "evidence_ids": ["example-summary"],
                "notes": notes.get(milestone, "Synthetic v0 example for UI and scorer validation."),
            }
        )
    return rows


def artifact_summary(run_id: str, text: str) -> dict[str, Any]:
    path = ARTIFACT_DIR / run_id / "summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return {
        "artifact_id": "example-summary",
        "kind": "summary",
        "path": str(path.relative_to(ROOT)),
        "sha256": None,
        "visibility": "public",
        "description": "Synthetic example evidence summary.",
    }


def make_result(
    *,
    run_id: str,
    model_provider: str,
    model: str,
    agent_tool: str,
    target: str,
    stop_reason: str,
    comparison_eligible: bool,
    milestone_scores: dict[str, float],
    verification_status: str,
    failure_class: str | None = None,
    interventions: list[dict[str, Any]] | None = None,
    messy: bool = False,
) -> dict[str, Any]:
    artifact = artifact_summary(
        run_id,
        f"# {run_id}\n\nSynthetic evidence summary for `{model_provider}/{model}`.\n",
    )
    verification_result = {
        "result_id": f"{run_id}-verification-0001",
        "run_id": run_id,
        "checker_name": "prototype-fixture-checker",
        "checker_version": "0.1.0",
        "scope": "public milestone",
        "status": verification_status,
        "started_at": "2026-06-01T12:00:00+00:00",
        "duration_ms": 900,
        "command": "synthetic fixture",
        "exit_code": 0 if verification_status == "pass" else 1,
        "stdout_artifact": artifact["path"],
        "stderr_artifact": None,
        "environment_profile": "synthetic-local",
        "inputs_hash": None,
        "failure_class": failure_class,
        "evidence_ids": ["example-summary"],
        "visibility": "public",
    }
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_kind": "benchmark_run_result",
        "created_at": FIXED_CREATED_AT,
        "run": {
            "run_id": run_id,
            "batch_id": "prototype-examples",
            "model_provider": model_provider,
            "model": model,
            "model_snapshot": "example",
            "agent_tool": agent_tool,
            "tool_version": "example",
            "harness": "codex-meta-harness",
            "harness_version": "0.1.0",
            "profile": "smoke-v0",
            "target": target,
            "target_mode": "fixed-milestone",
            "started_at": "2026-06-01T12:00:00+00:00",
            "finished_at": "2026-06-01T12:03:00+00:00",
            "stop_reason": stop_reason,
            "comparison_eligible": comparison_eligible,
            "comparison_reason": "Synthetic prototype fixture.",
            "wall_clock_limit": "10m",
            "observed_elapsed_seconds": 180,
            "turn_limit": "8",
            "observed_turns": 2 if interventions else 1,
            "token_limit": "200000",
            "observed_tokens": 14000,
            "tool_call_limit": "unknown",
            "observed_tool_calls": 24,
            "cost_limit": "unknown",
            "observed_cost": "unknown",
            "visibility": "public",
        },
        "submission": {
            "run_id": run_id,
            "artifact_root": str((ARTIFACT_DIR / run_id).relative_to(ROOT)),
            "submission_path": str((ARTIFACT_DIR / run_id).relative_to(ROOT)),
            "manifest_path": artifact["path"],
            "summary_path": artifact["path"],
            "diff_path": artifact["path"],
            "verification_logs": [artifact["path"]],
            "version_info_path": artifact["path"],
        },
        "attempts": [
            {
                "attempt_id": f"{run_id}-attempt-0001",
                "turn": 1,
                "started_at": "2026-06-01T12:00:00+00:00",
                "finished_at": "2026-06-01T12:01:20+00:00",
                "exit_code": 0 if verification_status == "pass" else 1,
                "restart_of": None,
                "restart_reason": "initial",
            }
        ],
        "turns": [
            {
                "run_id": run_id,
                "turn": 1,
                "elapsed_seconds": 80,
                "agent_elapsed_seconds": 70,
                "agent_exit_code": 0 if verification_status == "pass" else 1,
                "verification": verification_status,
                "verification_log": artifact["path"],
                "tokens": 14000,
                "tool_calls": 24,
                "material_progress": verification_status == "pass",
                "material_paths": [artifact["path"]],
                "idle_count": 0,
                "failure_count": 0 if verification_status == "pass" else 1,
            }
        ],
        "tool_calls": [
            {
                "tool_call_id": f"{run_id}-turn-0001-write",
                "turn": 1,
                "name": "write",
                "count": 4,
                "visibility": "public",
            },
            {
                "tool_call_id": f"{run_id}-turn-0001-bash",
                "turn": 1,
                "name": "bash",
                "count": 3,
                "visibility": "public",
            },
        ],
        "artifacts": [artifact],
        "interventions": interventions or [],
        "verification_results": [verification_result],
        "milestone_assessments": milestone_assessments(run_id, milestone_scores),
        "rubric_scores": [
            {
                "run_id": run_id,
                "category": "capability",
                "weight": 0.40,
                "score": max(milestone_scores.values()) if milestone_scores else 0,
                "max_score": 1.0,
                "evidence_links": ["example-summary"],
                "notes": "Synthetic capability estimate.",
            },
            {
                "run_id": run_id,
                "category": "verification",
                "weight": 0.25,
                "score": 0.85 if verification_status == "pass" else 0.15,
                "max_score": 1.0,
                "evidence_links": ["example-summary"],
                "notes": "Synthetic verification estimate.",
            },
            {
                "run_id": run_id,
                "category": "traceability",
                "weight": 0.15,
                "score": 0.65 if not messy else 0.25,
                "max_score": 1.0,
                "evidence_links": ["example-summary"],
                "notes": "Synthetic traceability estimate.",
            },
            {
                "run_id": run_id,
                "category": "integration",
                "weight": 0.10,
                "score": 0.60,
                "max_score": 1.0,
                "evidence_links": ["example-summary"],
                "notes": "Synthetic integration estimate.",
            },
            {
                "run_id": run_id,
                "category": "honesty",
                "weight": 0.10,
                "score": 0.70 if not messy else 0.20,
                "max_score": 1.0,
                "evidence_links": ["example-summary"],
                "notes": "Synthetic limitation disclosure estimate.",
            },
        ],
    }
    if interventions:
        record["attempts"].append(
            {
                "attempt_id": f"{run_id}-attempt-0002",
                "turn": 2,
                "started_at": "2026-06-01T12:01:20+00:00",
                "finished_at": "2026-06-01T12:03:00+00:00",
                "exit_code": 0,
                "restart_of": f"{run_id}-attempt-0001",
                "restart_reason": "agent-stopped-before-budget",
            }
        )
        record["turns"].append(
            {
                "run_id": run_id,
                "turn": 2,
                "elapsed_seconds": 180,
                "agent_elapsed_seconds": 95,
                "agent_exit_code": 0,
                "verification": verification_status,
                "verification_log": artifact["path"],
                "tokens": 21000,
                "tool_calls": 31,
                "material_progress": True,
                "material_paths": [artifact["path"]],
                "idle_count": 0,
                "failure_count": 0,
            }
        )
    return score_result(record)


def copy_dogfood_evidence(raw_dir: Path, run_id: str) -> dict[str, Path]:
    output = ARTIFACT_DIR / run_id
    output.mkdir(parents=True, exist_ok=True)
    copied: dict[str, Path] = {}
    for name in ("benchmark-run.md", "worktree.diff", "git-status.txt"):
        source = raw_dir / name
        if source.exists():
            destination = output / name
            shutil.copyfile(source, destination)
            copied[name] = destination
    verification_out = output / "verification"
    verification_out.mkdir(exist_ok=True)
    for source in sorted((raw_dir / "run" / "verification").glob("turn-*.txt")):
        destination = verification_out / source.name
        shutil.copyfile(source, destination)
        copied[f"verification/{source.name}"] = destination
    return copied


def rewrite_dogfood_paths(record: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    run_id = record["run"]["run_id"]
    copied = copy_dogfood_evidence(raw_dir, run_id)
    record["created_at"] = FIXED_CREATED_AT
    root = ARTIFACT_DIR / run_id
    record["submission"]["artifact_root"] = str(root.relative_to(ROOT))
    record["submission"]["submission_path"] = str(root.relative_to(ROOT))
    if "benchmark-run.md" in copied:
        manifest = str(copied["benchmark-run.md"].relative_to(ROOT))
        record["submission"]["manifest_path"] = manifest
        record["submission"]["summary_path"] = manifest
    if "worktree.diff" in copied:
        record["submission"]["diff_path"] = str(copied["worktree.diff"].relative_to(ROOT))
    logs = [path for key, path in copied.items() if key.startswith("verification/")]
    record["submission"]["verification_logs"] = [str(path.relative_to(ROOT)) for path in logs]
    for artifact in record.get("artifacts", []):
        artifact_id = artifact.get("artifact_id")
        if artifact_id == "benchmark-run" and "benchmark-run.md" in copied:
            artifact["path"] = str(copied["benchmark-run.md"].relative_to(ROOT))
        elif artifact_id == "worktree-diff" and "worktree.diff" in copied:
            artifact["path"] = str(copied["worktree.diff"].relative_to(ROOT))
        elif artifact_id == "git-status" and "git-status.txt" in copied:
            artifact["path"] = str(copied["git-status.txt"].relative_to(ROOT))
        elif str(artifact_id).startswith("artifact-turn-"):
            name = str(artifact.get("path", "")).split("/")[-1]
            key = f"verification/{name}"
            if key in copied:
                artifact["path"] = str(copied[key].relative_to(ROOT))
    for result in record.get("verification_results", []):
        stdout = str(result.get("stdout_artifact", ""))
        key = f"verification/{stdout.split('/')[-1]}"
        if key in copied:
            result["stdout_artifact"] = str(copied[key].relative_to(ROOT))
    return score_result(record)


def generate_examples(dogfood_artifact_dir: Path, skip_dogfood: bool) -> list[dict[str, Any]]:
    if EXAMPLES_DIR.exists():
        shutil.rmtree(EXAMPLES_DIR)
    if ARTIFACT_DIR.exists():
        shutil.rmtree(ARTIFACT_DIR)
    if ANALYSIS_DIR.exists():
        shutil.rmtree(ANALYSIS_DIR)
    EXAMPLES_DIR.mkdir(parents=True)
    ARTIFACT_DIR.mkdir(parents=True)

    results = [
        make_result(
            run_id="example-success-short",
            model_provider="openai",
            model="gpt-5.1",
            agent_tool="codex",
            target="m1",
            stop_reason="verification-passed",
            comparison_eligible=True,
            milestone_scores={"m0": 1.0, "m1": 1.0},
            verification_status="pass",
        ),
        make_result(
            run_id="example-partial",
            model_provider="ollama",
            model="glm-5.1:cloud",
            agent_tool="pi",
            target="m2",
            stop_reason="wall-clock-limit",
            comparison_eligible=True,
            milestone_scores={"m0": 1.0, "m1": 0.75, "m2": 0.45},
            verification_status="pass",
        ),
        make_result(
            run_id="example-failed",
            model_provider="local",
            model="broken-baseline",
            agent_tool="reference-script",
            target="m1",
            stop_reason="verification-failed",
            comparison_eligible=False,
            milestone_scores={"m0": 0.75, "m1": 0.20},
            verification_status="fail",
            failure_class="verification-failed",
        ),
        make_result(
            run_id="example-restarted",
            model_provider="ollama",
            model="glm-5.1:cloud",
            agent_tool="pi",
            target="m1",
            stop_reason="verification-passed-after-restart",
            comparison_eligible=True,
            milestone_scores={"m0": 1.0, "m1": 0.85},
            verification_status="pass",
            interventions=[
                {
                    "intervention_id": "example-restarted-admin-0001",
                    "turn": 1,
                    "type": "restart-agent",
                    "reason": "Agent stopped before wall-clock budget while material progress remained possible.",
                    "visibility": "public",
                }
            ],
        ),
        make_result(
            run_id="example-messy",
            model_provider="unknown",
            model="metadata-missing",
            agent_tool="unknown-agent",
            target="m1",
            stop_reason="invalid-metadata",
            comparison_eligible=False,
            milestone_scores={"m0": 0.25, "m1": 0.10},
            verification_status="error",
            failure_class="invalid-run",
            messy=True,
        ),
    ]

    if not skip_dogfood and dogfood_artifact_dir.exists():
        results.append(rewrite_dogfood_paths(ingest_artifact_dir(dogfood_artifact_dir), dogfood_artifact_dir))

    for result in results:
        write_json(EXAMPLES_DIR / f"{result['run']['run_id']}.json", result)
    return results


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    results = generate_examples(args.dogfood_artifact_dir, args.skip_dogfood)
    if args.db:
        if args.reset_db and args.db.exists():
            args.db.unlink()
        for result in results:
            upsert_result(args.db, result)
        print(f"Upserted {len(results)} example benchmark result(s) into {args.db}")
    print(f"Wrote {len(results)} example benchmark result(s) to {EXAMPLES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
