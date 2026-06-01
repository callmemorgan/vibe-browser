#!/usr/bin/env python3
"""Shared helpers for the Vibe Browser Benchmark prototype.

The module is intentionally standard-library-only so local benchmark rendering
does not depend on package installation.
"""

from __future__ import annotations

import copy
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_ROOT = ROOT / "vibe-browser-benchmark"
EXAMPLES_DIR = BENCHMARK_ROOT / "examples" / "runs"
ANALYSIS_DIR = BENCHMARK_ROOT / "examples" / "analysis"
SITE_DIR = BENCHMARK_ROOT / "site"
SCHEMA_VERSION = "vibe-browser-result-v0.1"

MILESTONES = [f"m{index}" for index in range(10)]
MILESTONE_VALUES = {milestone: (index + 1) ** 2 for index, milestone in enumerate(MILESTONES)}
DIMENSION_WEIGHTS = {
    "capability": 0.40,
    "verification": 0.25,
    "traceability": 0.15,
    "integration": 0.10,
    "honesty": 0.10,
}

PASSING_VERIFICATION = {"passed", "pass"}
FAILING_VERIFICATION = {"failed", "fail", "error", "timeout"}


class BenchmarkError(ValueError):
    """Raised when benchmark data cannot be normalized or validated."""


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_path(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def safe_id(value: Any) -> str:
    text = str(value or "unknown").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "unknown"


def compact_text(value: Any, limit: int = 240) -> str:
    text = str(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        return f"{text[: limit - 1]}..."
    return text


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def status_to_score(status: str | None) -> float:
    normalized = safe_id(status)
    if normalized in {"confirmed", "complete", "completed", "passed", "pass", "passes-focused-tests"}:
        return 1.0
    if normalized in {"public-check-passed", "tested", "focused-tests"}:
        return 0.75
    if normalized in {"partial", "implemented", "in-progress"}:
        return 0.50
    if normalized in {"design", "design-only", "placeholder"}:
        return 0.25
    return 0.0


def score_to_status(score: float) -> str:
    if score >= 1.0:
        return "confirmed"
    if score >= 0.75:
        return "passes-focused-tests"
    if score >= 0.50:
        return "partial"
    if score >= 0.25:
        return "design-only"
    return "not-started"


def normalize_dimensions(
    dimensions: dict[str, Any] | None,
    fallback_score: float,
) -> dict[str, float]:
    if not dimensions:
        return {name: fallback_score for name in DIMENSION_WEIGHTS}
    normalized: dict[str, float] = {}
    for name in DIMENSION_WEIGHTS:
        value = dimensions.get(name, fallback_score)
        normalized[name] = clamp_float(value)
    return normalized


def weighted_dimension_score(dimensions: dict[str, Any]) -> float:
    return sum(clamp_float(dimensions.get(name, 0)) * weight for name, weight in DIMENSION_WEIGHTS.items())


def clamp_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, number))


def parse_markdown_milestones(text: str) -> dict[str, dict[str, str]]:
    """Extract milestone status rows from benchmark-run.md-style tables."""

    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        milestone = cells[0].strip("*` ").lower()
        if not re.fullmatch(r"m\d+", milestone):
            continue
        status = cells[1].strip("` ")
        notes = cells[2].strip()
        rows[milestone] = {"status": status, "notes": notes}
    return rows


def parse_turn_number(path: Path) -> int | None:
    match = re.search(r"turn-(\d+)", path.name)
    return int(match.group(1)) if match else None


def verification_status_from_log(path: Path) -> tuple[str, int | None]:
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    exit_match = re.search(r"exit=(\d+)", text)
    exit_code = int(exit_match.group(1)) if exit_match else None
    if exit_code == 0:
        return "pass", exit_code
    if exit_code is not None:
        return "fail", exit_code
    lowered = text.lower()
    if "ok" in lowered or "passed" in lowered:
        return "pass", None
    if "failed" in lowered or "error" in lowered:
        return "fail", None
    return "skipped", None


def verification_result_from_log(run_id: str, path: Path, artifact_root: Path) -> dict[str, Any]:
    turn = parse_turn_number(path)
    status, exit_code = verification_status_from_log(path)
    rel_path = repo_relative(path)
    return {
        "result_id": f"{run_id}-verification-{turn or safe_id(path.stem)}",
        "run_id": run_id,
        "checker_name": "meta-harness-verification",
        "checker_version": "0.1.0",
        "scope": "public milestone",
        "status": status,
        "started_at": None,
        "duration_ms": None,
        "command": "recorded in verification log",
        "exit_code": exit_code,
        "stdout_artifact": rel_path,
        "stderr_artifact": None,
        "environment_profile": "docker-admin-v0" if "docker-artifacts" in str(artifact_root) else "local",
        "inputs_hash": sha256_path(path),
        "failure_class": None if status == "pass" else "verification-failed",
        "evidence_ids": [f"artifact-{safe_id(path.stem)}"],
        "visibility": "public",
    }


def collect_tool_calls(run_id: str, artifact_root: Path) -> list[dict[str, Any]]:
    calls: dict[tuple[int, str], int] = {}
    for path in sorted((artifact_root / "run" / "pi").glob("turn-*.jsonl")):
        turn = parse_turn_number(path) or 0
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = _tool_name_from_event(event)
            if not name:
                continue
            key = (turn, name)
            calls[key] = calls.get(key, 0) + 1
    return [
        {
            "tool_call_id": f"{run_id}-turn-{turn:04d}-{safe_id(name)}",
            "turn": turn,
            "name": name,
            "count": count,
            "visibility": "public",
        }
        for (turn, name), count in sorted(calls.items())
    ]


def _tool_name_from_event(event: dict[str, Any]) -> str | None:
    message = event.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") in {"toolCall", "tool_use"}:
                    return str(item.get("name") or item.get("tool") or "")
    assistant_event = event.get("assistantMessageEvent")
    if isinstance(assistant_event, dict) and assistant_event.get("type") == "toolcall_start":
        content_index = assistant_event.get("contentIndex")
        if isinstance(content_index, int):
            return _tool_name_from_event({"message": message})
    return None


def artifact_entry(
    artifact_id: str,
    kind: str,
    path: Path | str,
    *,
    visibility: str = "public",
    description: str = "",
) -> dict[str, Any]:
    path_obj = Path(path)
    display_path = repo_relative(path_obj) if path_obj.exists() else str(path)
    digest = sha256_path(path_obj) if path_obj.exists() else None
    return {
        "artifact_id": artifact_id,
        "kind": kind,
        "path": display_path,
        "sha256": digest,
        "visibility": visibility,
        "description": description,
    }


def build_milestones_from_manifest(
    run_id: str,
    manifest_path: Path | None,
    target: str,
    latest_verification: str | None,
) -> list[dict[str, Any]]:
    parsed: dict[str, dict[str, str]] = {}
    if manifest_path and manifest_path.exists():
        parsed = parse_markdown_milestones(manifest_path.read_text(encoding="utf-8", errors="replace"))

    assessments: list[dict[str, Any]] = []
    target_index = int(target[1:]) if re.fullmatch(r"m\d+", target or "") else 0
    for index, milestone in enumerate(MILESTONES):
        row = parsed.get(milestone)
        if row:
            score = status_to_score(row.get("status"))
            notes = row.get("notes", "")
        elif index < target_index:
            score = 1.0
            notes = "Implicit prerequisite for target milestone."
        elif index == target_index and latest_verification in PASSING_VERIFICATION:
            score = 0.75
            notes = "Target milestone has passing public verification but no parsed status row."
        else:
            score = 0.0
            notes = "No evidence in parsed manifest."
        dimensions = normalize_dimensions(None, score)
        assessments.append(
            {
                "run_id": run_id,
                "milestone": milestone,
                "claimed_status": score_to_status(score),
                "public_check_status": "pass" if score >= 0.75 else "not-run",
                "evaluator_status": "provisional",
                "score": score,
                "dimensions": dimensions,
                "missing_evidence": [] if score else ["implementation evidence"],
                "evidence_ids": ["benchmark-run"] if row else [],
                "notes": notes,
            }
        )
    return assessments


def normalize_turns_from_artifact(run_id: str, artifact_root: Path) -> list[dict[str, Any]]:
    summary_path = artifact_root / "turn-metrics.json"
    if summary_path.exists():
        raw_turns = json.loads(summary_path.read_text(encoding="utf-8"))
        return [_normalize_turn_metric(run_id, raw) for raw in raw_turns]

    turns: list[dict[str, Any]] = []
    checkpoints = artifact_root / "run" / "checkpoints"
    for path in sorted(checkpoints.glob("checkpoint-*.json")):
        raw = read_json(path)
        turns.append(_normalize_turn_metric(run_id, raw))
    return turns


def _normalize_turn_metric(run_id: str, raw: dict[str, Any]) -> dict[str, Any]:
    turn = raw.get("turn") or raw.get("observed_turns") or parse_turn_number(Path(str(raw.get("latest_agent_log", "")))) or 0
    return {
        "run_id": run_id,
        "turn": int(turn),
        "elapsed_seconds": raw.get("elapsed_seconds"),
        "agent_elapsed_seconds": raw.get("agent_elapsed_seconds") or raw.get("latest_agent_elapsed_seconds"),
        "agent_exit_code": raw.get("agent_exit_code") or raw.get("latest_agent_exit_code"),
        "verification": raw.get("verification") or raw.get("latest_verification"),
        "verification_log": raw.get("verification_log") or raw.get("latest_verification_log"),
        "tokens": raw.get("tokens") or raw.get("observed_token_usage"),
        "tool_calls": raw.get("tool_calls") or raw.get("observed_tool_calls"),
        "material_progress": bool(raw.get("material_progress", raw.get("latest_material_progress", False))),
        "material_paths": raw.get("material_paths") or raw.get("latest_material_paths") or [],
        "idle_count": raw.get("idle_count", 0),
        "failure_count": raw.get("failure_count", 0),
    }


def ingest_artifact_dir(artifact_root: Path) -> dict[str, Any]:
    artifact_root = artifact_root.resolve()
    state = read_json(artifact_root / "run" / "state.json")
    config = read_json(artifact_root / "run" / "config.json")
    run_id = str(state.get("run_id") or config.get("run_id") or artifact_root.name)
    target = safe_id(config.get("target") or "m0")
    manifest_path = artifact_root / "benchmark-run.md"
    turns = normalize_turns_from_artifact(run_id, artifact_root)
    verification_logs = sorted((artifact_root / "run" / "verification").glob("turn-*.txt"))
    verification_results = [
        verification_result_from_log(run_id, path, artifact_root) for path in verification_logs
    ]
    artifacts = [
        artifact_entry("benchmark-run", "manifest", manifest_path, description="Participant benchmark manifest."),
        artifact_entry("worktree-diff", "diff", artifact_root / "worktree.diff", description="Tracked code diff."),
        artifact_entry("git-status", "git-status", artifact_root / "git-status.txt", description="Participant git status."),
    ]
    for path in verification_logs:
        artifacts.append(
            artifact_entry(
                f"artifact-{safe_id(path.stem)}",
                "verification-log",
                path,
                description=f"Verification log for turn {parse_turn_number(path) or '?'}",
            )
        )

    latest_verification = str(state.get("latest_verification") or "not-run")
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_kind": "benchmark_run_result",
        "created_at": utc_now(),
        "run": {
            "run_id": run_id,
            "batch_id": f"{config.get('profile', 'unknown')}-dogfood",
            "model_provider": config.get("model_provider", "unknown"),
            "model": config.get("model", "unknown"),
            "model_snapshot": config.get("model_snapshot", "unknown"),
            "agent_tool": config.get("tool_name") or config.get("agent_kind", "unknown"),
            "tool_version": config.get("tool_version", "unknown"),
            "harness": config.get("harness", "codex-meta-harness"),
            "harness_version": config.get("harness_version", "unknown"),
            "profile": config.get("profile", "unknown"),
            "target": target,
            "target_mode": "fixed-milestone",
            "started_at": config.get("created_at") or state.get("created_at"),
            "finished_at": state.get("updated_at"),
            "stop_reason": state.get("stop_reason", "unknown"),
            "comparison_eligible": str(state.get("comparison_eligible", "no")).lower() == "yes",
            "comparison_reason": "administrative-only intervention policy and captured Docker artifact",
            "wall_clock_limit": config.get("budgets", {}).get("wall_clock_limit"),
            "observed_elapsed_seconds": max([turn.get("elapsed_seconds") or 0 for turn in turns] or [None]),
            "turn_limit": config.get("budgets", {}).get("turn_limit"),
            "observed_turns": state.get("observed_turns"),
            "token_limit": config.get("budgets", {}).get("token_limit"),
            "observed_tokens": state.get("observed_token_usage"),
            "tool_call_limit": config.get("budgets", {}).get("tool_call_limit"),
            "observed_tool_calls": state.get("observed_tool_calls"),
            "cost_limit": config.get("budgets", {}).get("cost_limit"),
            "observed_cost": state.get("observed_cost"),
            "visibility": "public",
        },
        "submission": {
            "run_id": run_id,
            "artifact_root": repo_relative(artifact_root),
            "submission_path": repo_relative(artifact_root / "submission"),
            "manifest_path": repo_relative(manifest_path),
            "summary_path": repo_relative(artifact_root / "summary.json"),
            "diff_path": repo_relative(artifact_root / "worktree.diff"),
            "verification_logs": [repo_relative(path) for path in verification_logs],
            "version_info_path": repo_relative(artifact_root / "version-info.json"),
        },
        "attempts": [
            {
                "attempt_id": f"{run_id}-attempt-{turn.get('turn', 0):04d}",
                "turn": turn.get("turn"),
                "started_at": None,
                "finished_at": None,
                "exit_code": turn.get("agent_exit_code"),
                "restart_of": None if turn.get("turn") == 1 else f"{run_id}-attempt-{int(turn.get('turn', 0)) - 1:04d}",
                "restart_reason": "scheduled-continuation" if turn.get("turn") != 1 else "initial",
            }
            for turn in turns
        ],
        "turns": turns,
        "tool_calls": collect_tool_calls(run_id, artifact_root),
        "artifacts": artifacts,
        "interventions": [],
        "verification_results": verification_results,
        "milestone_assessments": build_milestones_from_manifest(
            run_id,
            manifest_path if manifest_path.exists() else None,
            target,
            latest_verification,
        ),
        "rubric_scores": default_rubric_scores(run_id, latest_verification, state.get("stop_reason")),
    }
    return score_result(record)


def default_rubric_scores(run_id: str, latest_verification: str, stop_reason: Any) -> list[dict[str, Any]]:
    verification_passed = latest_verification in PASSING_VERIFICATION
    exhausted = "budget" in str(stop_reason or "")
    return [
        {
            "run_id": run_id,
            "category": "capability",
            "weight": 0.40,
            "score": 0.80 if verification_passed else 0.35,
            "max_score": 1.0,
            "evidence_links": ["benchmark-run"],
            "notes": "Derived from target milestone status and captured verification.",
        },
        {
            "run_id": run_id,
            "category": "verification",
            "weight": 0.25,
            "score": 0.80 if verification_passed else 0.20,
            "max_score": 1.0,
            "evidence_links": ["verification-results"],
            "notes": "Derived from latest public verification result.",
        },
        {
            "run_id": run_id,
            "category": "traceability",
            "weight": 0.15,
            "score": 0.70,
            "max_score": 1.0,
            "evidence_links": ["benchmark-run"],
            "notes": "Provisional scorer estimate from manifest and documentation artifacts.",
        },
        {
            "run_id": run_id,
            "category": "integration",
            "weight": 0.10,
            "score": 0.70 if not exhausted else 0.60,
            "max_score": 1.0,
            "evidence_links": ["worktree-diff"],
            "notes": "Provisional scorer estimate.",
        },
        {
            "run_id": run_id,
            "category": "honesty",
            "weight": 0.10,
            "score": 0.85,
            "max_score": 1.0,
            "evidence_links": ["benchmark-run"],
            "notes": "Known limitations are explicitly recorded.",
        },
    ]


def score_result(record: dict[str, Any]) -> dict[str, Any]:
    scored = copy.deepcopy(record)
    assessments = scored.get("milestone_assessments") or []
    by_milestone = {item.get("milestone"): item for item in assessments if isinstance(item, dict)}
    milestone_scores: list[dict[str, Any]] = []

    for milestone in MILESTONES:
        assessment = by_milestone.get(milestone, {})
        raw_score = assessment.get("score")
        fallback = status_to_score(assessment.get("evaluator_status") or assessment.get("public_check_status"))
        evaluator_score = clamp_float(raw_score if raw_score is not None else fallback)
        public_score = max(
            status_to_score(assessment.get("public_check_status")),
            evaluator_score if assessment.get("public_check_status") == "pass" else 0,
        )
        claimed_score = max(status_to_score(assessment.get("claimed_status")), evaluator_score)
        dimensions = normalize_dimensions(assessment.get("dimensions"), evaluator_score)
        weighted = weighted_dimension_score(dimensions)
        if raw_score is None:
            evaluator_score = weighted
        value = MILESTONE_VALUES[milestone]
        milestone_scores.append(
            {
                "milestone": milestone,
                "value": value,
                "claimed_score": round(claimed_score, 4),
                "public_check_score": round(public_score, 4),
                "evaluator_score": round(evaluator_score, 4),
                "dimension_score": round(weighted, 4),
                "points": round(value * evaluator_score, 4),
                "dimensions": dimensions,
                "notes": assessment.get("notes", ""),
                "evidence_ids": assessment.get("evidence_ids", []),
            }
        )

    repository_rubric_score = weighted_repository_score(scored.get("rubric_scores") or [])
    denominator = sum(MILESTONE_VALUES.values())
    evaluator_base = 100.0 * sum(item["points"] for item in milestone_scores) / denominator
    public_base = 100.0 * sum(item["value"] * item["public_check_score"] for item in milestone_scores) / denominator
    claimed_base = 100.0 * sum(item["value"] * item["claimed_score"] for item in milestone_scores) / denominator
    quality_multiplier = 0.70 + 0.30 * repository_rubric_score
    final_score = evaluator_base * quality_multiplier
    confidence = confidence_score(scored, milestone_scores)
    scored["scores"] = {
        "score_version": "scorer-v0.1",
        "curve": "quadratic",
        "milestones": milestone_scores,
        "repository_rubric_score": round(repository_rubric_score, 4),
        "quality_multiplier": round(quality_multiplier, 4),
        "claimed_score": round(claimed_base * quality_multiplier, 2),
        "public_check_score": round(public_base * quality_multiplier, 2),
        "evaluator_score": round(evaluator_base, 2),
        "final_score": round(final_score, 2),
        "confidence": round(confidence, 2),
        "uncertainty": round(1.0 - confidence, 2),
        "highest_claimed_milestone": highest_milestone(milestone_scores, "claimed_score"),
        "highest_public_check_milestone": highest_milestone(milestone_scores, "public_check_score"),
        "highest_confirmed_milestone": highest_milestone(milestone_scores, "evaluator_score"),
        "failure_class": classify_failure(scored),
        "rankable": bool(scored.get("run", {}).get("comparison_eligible")) and final_score > 0,
        "visibility": scored.get("run", {}).get("visibility", "public"),
    }
    return scored


def weighted_repository_score(rubric_scores: list[dict[str, Any]]) -> float:
    if not rubric_scores:
        return 0.70
    total_weight = 0.0
    total = 0.0
    for item in rubric_scores:
        weight = float(item.get("weight", 0) or 0)
        max_score = float(item.get("max_score", 1.0) or 1.0)
        score = float(item.get("score", 0) or 0)
        total_weight += weight
        total += weight * clamp_float(score / max_score)
    if total_weight <= 0:
        return 0.70
    return clamp_float(total / total_weight)


def highest_milestone(milestones: list[dict[str, Any]], key: str) -> str | None:
    reached = [item["milestone"] for item in milestones if item.get(key, 0) >= 0.75]
    return reached[-1] if reached else None


def confidence_score(record: dict[str, Any], milestones: list[dict[str, Any]]) -> float:
    verification_results = record.get("verification_results") or []
    passing = sum(1 for item in verification_results if item.get("status") == "pass")
    total = len(verification_results)
    verification_factor = 0.35 if total == 0 else 0.55 + min(0.25, passing / max(total, 1) * 0.25)
    evidence_factor = 0.10 if any(item.get("evidence_ids") for item in milestones) else 0.0
    rubric_factor = 0.10 if record.get("rubric_scores") else 0.0
    eligibility_factor = 0.10 if record.get("run", {}).get("comparison_eligible") else 0.0
    return clamp_float(verification_factor + evidence_factor + rubric_factor + eligibility_factor)


def classify_failure(record: dict[str, Any]) -> str | None:
    statuses = {safe_id(item.get("status")) for item in record.get("verification_results", [])}
    stop_reason = safe_id(record.get("run", {}).get("stop_reason"))
    if statuses & FAILING_VERIFICATION:
        return "verification-failed"
    if "budget-exhausted" in stop_reason:
        return "budget-exhausted"
    if "invalid" in stop_reason:
        return "invalid-run"
    return None


def validate_result(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for key in (
        "run",
        "submission",
        "attempts",
        "turns",
        "tool_calls",
        "artifacts",
        "interventions",
        "verification_results",
        "milestone_assessments",
        "rubric_scores",
    ):
        if key not in record:
            errors.append(f"missing top-level field: {key}")
    run = record.get("run") if isinstance(record.get("run"), dict) else {}
    for key in (
        "run_id",
        "batch_id",
        "model_provider",
        "model",
        "agent_tool",
        "harness",
        "profile",
        "target",
        "started_at",
        "stop_reason",
        "comparison_eligible",
    ):
        if key not in run:
            errors.append(f"missing run field: {key}")
    milestones = record.get("milestone_assessments")
    if not isinstance(milestones, list) or not milestones:
        errors.append("milestone_assessments must be a non-empty list")
    else:
        seen = {item.get("milestone") for item in milestones if isinstance(item, dict)}
        for milestone in MILESTONES:
            if milestone not in seen:
                errors.append(f"missing milestone assessment: {milestone}")
    for result in record.get("verification_results", []):
        if result.get("status") not in {
            "pass",
            "fail",
            "error",
            "timeout",
            "skipped",
            "flaky",
            "expected-fail",
            "blocked",
        }:
            errors.append(f"invalid verification status: {result.get('status')}")
    return errors


def load_results(paths: list[Path]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for path in paths:
        if path.is_dir() and (path / "run" / "state.json").exists():
            results.append(score_result(ingest_artifact_dir(path)))
        elif path.is_dir():
            for child in sorted(path.glob("*.json")):
                results.append(score_result(read_json(child)))
        else:
            results.append(score_result(read_json(path)))
    return results


def default_example_paths() -> list[Path]:
    return sorted(EXAMPLES_DIR.glob("*.json"))


def html_escape(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))
