#!/usr/bin/env python3
"""SQLite datastore for the Vibe Browser Benchmark prototype."""

from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
from collections.abc import Iterator
from typing import Any

from benchmark_lib import BENCHMARK_ROOT, score_result, validate_result


DB_SCHEMA_VERSION = "benchmark-sqlite-v0.1"
DEFAULT_DB_PATH = BENCHMARK_ROOT / "benchmark.db"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def transaction(db_path: Path) -> Iterator[sqlite3.Connection]:
    connection = connect(db_path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    with transaction(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_meta (
              key TEXT PRIMARY KEY,
              value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS runs (
              run_id TEXT PRIMARY KEY,
              batch_id TEXT NOT NULL,
              model_provider TEXT NOT NULL,
              model TEXT NOT NULL,
              agent_tool TEXT NOT NULL,
              harness TEXT NOT NULL,
              profile TEXT NOT NULL,
              target TEXT NOT NULL,
              target_mode TEXT NOT NULL,
              started_at TEXT,
              finished_at TEXT,
              stop_reason TEXT NOT NULL,
              final_score REAL NOT NULL,
              public_check_score REAL NOT NULL,
              evaluator_score REAL NOT NULL,
              confidence REAL NOT NULL,
              uncertainty REAL NOT NULL,
              highest_confirmed_milestone TEXT,
              failure_class TEXT,
              rankable INTEGER NOT NULL,
              visibility TEXT NOT NULL,
              result_json TEXT NOT NULL,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_runs_leaderboard
              ON runs(rankable, final_score DESC, run_id);
            CREATE INDEX IF NOT EXISTS idx_runs_filters
              ON runs(model_provider, model, harness, highest_confirmed_milestone);

            CREATE TABLE IF NOT EXISTS attempts (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              attempt_id TEXT NOT NULL,
              turn INTEGER,
              exit_code INTEGER,
              restart_of TEXT,
              restart_reason TEXT,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, attempt_id)
            );

            CREATE TABLE IF NOT EXISTS turns (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              turn INTEGER NOT NULL,
              verification TEXT,
              material_progress INTEGER NOT NULL,
              tokens INTEGER,
              tool_calls INTEGER,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, turn)
            );

            CREATE TABLE IF NOT EXISTS artifacts (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              artifact_id TEXT NOT NULL,
              kind TEXT,
              path TEXT,
              visibility TEXT,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, artifact_id)
            );

            CREATE TABLE IF NOT EXISTS verification_results (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              result_id TEXT NOT NULL,
              scope TEXT,
              status TEXT,
              failure_class TEXT,
              visibility TEXT,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, result_id)
            );

            CREATE TABLE IF NOT EXISTS milestone_scores (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              milestone TEXT NOT NULL,
              evaluator_score REAL NOT NULL,
              public_check_score REAL NOT NULL,
              claimed_score REAL NOT NULL,
              points REAL NOT NULL,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, milestone)
            );

            CREATE TABLE IF NOT EXISTS interventions (
              run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
              intervention_id TEXT NOT NULL,
              turn INTEGER,
              type TEXT,
              visibility TEXT,
              payload_json TEXT NOT NULL,
              PRIMARY KEY (run_id, intervention_id)
            );
            """
        )
        connection.execute(
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES (?, ?)",
            ("schema_version", DB_SCHEMA_VERSION),
        )


def json_blob(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def upsert_result(db_path: Path, result: dict[str, Any]) -> dict[str, Any]:
    scored = score_result(result)
    errors = validate_result(scored)
    if errors:
        raise ValueError("; ".join(errors))

    init_db(db_path)
    run = scored["run"]
    scores = scored["scores"]
    with transaction(db_path) as connection:
        connection.execute("DELETE FROM attempts WHERE run_id = ?", (run["run_id"],))
        connection.execute("DELETE FROM turns WHERE run_id = ?", (run["run_id"],))
        connection.execute("DELETE FROM artifacts WHERE run_id = ?", (run["run_id"],))
        connection.execute(
            "DELETE FROM verification_results WHERE run_id = ?", (run["run_id"],)
        )
        connection.execute("DELETE FROM milestone_scores WHERE run_id = ?", (run["run_id"],))
        connection.execute("DELETE FROM interventions WHERE run_id = ?", (run["run_id"],))
        connection.execute(
            """
            INSERT OR REPLACE INTO runs (
              run_id, batch_id, model_provider, model, agent_tool, harness,
              profile, target, target_mode, started_at, finished_at, stop_reason,
              final_score, public_check_score, evaluator_score, confidence,
              uncertainty, highest_confirmed_milestone, failure_class, rankable,
              visibility, result_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                run["run_id"],
                run["batch_id"],
                run["model_provider"],
                run["model"],
                run["agent_tool"],
                run["harness"],
                run["profile"],
                run["target"],
                run["target_mode"],
                run.get("started_at"),
                run.get("finished_at"),
                run["stop_reason"],
                float(scores["final_score"]),
                float(scores["public_check_score"]),
                float(scores["evaluator_score"]),
                float(scores["confidence"]),
                float(scores["uncertainty"]),
                scores.get("highest_confirmed_milestone"),
                scores.get("failure_class"),
                1 if scores.get("rankable") else 0,
                scores.get("visibility", "public"),
                json.dumps(scored, indent=2, sort_keys=True),
            ),
        )
        for item in scored.get("attempts", []):
            connection.execute(
                """
                INSERT INTO attempts(run_id, attempt_id, turn, exit_code, restart_of, restart_reason, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    item.get("attempt_id"),
                    as_int(item.get("turn")),
                    as_int(item.get("exit_code")),
                    item.get("restart_of"),
                    item.get("restart_reason"),
                    json_blob(item),
                ),
            )
        for item in scored.get("turns", []):
            connection.execute(
                """
                INSERT INTO turns(run_id, turn, verification, material_progress, tokens, tool_calls, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    as_int(item.get("turn")) or 0,
                    item.get("verification"),
                    1 if item.get("material_progress") else 0,
                    as_int(item.get("tokens")),
                    as_int(item.get("tool_calls")),
                    json_blob(item),
                ),
            )
        for item in scored.get("artifacts", []):
            connection.execute(
                """
                INSERT INTO artifacts(run_id, artifact_id, kind, path, visibility, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    item.get("artifact_id"),
                    item.get("kind"),
                    item.get("path"),
                    item.get("visibility"),
                    json_blob(item),
                ),
            )
        for item in scored.get("verification_results", []):
            connection.execute(
                """
                INSERT INTO verification_results(run_id, result_id, scope, status, failure_class, visibility, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    item.get("result_id"),
                    item.get("scope"),
                    item.get("status"),
                    item.get("failure_class"),
                    item.get("visibility"),
                    json_blob(item),
                ),
            )
        for item in scores.get("milestones", []):
            connection.execute(
                """
                INSERT INTO milestone_scores(run_id, milestone, evaluator_score, public_check_score, claimed_score, points, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    item.get("milestone"),
                    float(item.get("evaluator_score", 0)),
                    float(item.get("public_check_score", 0)),
                    float(item.get("claimed_score", 0)),
                    float(item.get("points", 0)),
                    json_blob(item),
                ),
            )
        for index, item in enumerate(scored.get("interventions", []), start=1):
            intervention_id = item.get("intervention_id") or f"{run['run_id']}-intervention-{index:04d}"
            connection.execute(
                """
                INSERT INTO interventions(run_id, intervention_id, turn, type, visibility, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    intervention_id,
                    as_int(item.get("turn")),
                    item.get("type"),
                    item.get("visibility"),
                    json_blob(item),
                ),
            )
    return scored


def load_result(db_path: Path, run_id: str) -> dict[str, Any] | None:
    init_db(db_path)
    with transaction(db_path) as connection:
        row = connection.execute(
            "SELECT result_json FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if row is None:
        return None
    return score_result(json.loads(row["result_json"]))


def list_results(db_path: Path, filters: dict[str, str] | None = None) -> list[dict[str, Any]]:
    init_db(db_path)
    filters = filters or {}
    where: list[str] = []
    params: list[Any] = []
    for field, column in (
        ("provider", "model_provider"),
        ("model", "model"),
        ("harness", "harness"),
        ("milestone", "highest_confirmed_milestone"),
    ):
        value = filters.get(field)
        if value:
            where.append(f"{column} = ?")
            params.append(value)
    if filters.get("rankable") in {"1", "true", "yes"}:
        where.append("rankable = 1")
    elif filters.get("rankable") in {"0", "false", "no"}:
        where.append("rankable = 0")
    query = """
        SELECT run_id, batch_id, model_provider, model, agent_tool, harness,
               profile, target, target_mode, started_at, finished_at, stop_reason,
               final_score, public_check_score, evaluator_score, confidence,
               uncertainty, highest_confirmed_milestone, failure_class, rankable,
               visibility
        FROM runs
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY rankable DESC, final_score DESC, run_id ASC"
    with transaction(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
    return [
        {
            **dict(row),
            "rankable": bool(row["rankable"]),
        }
        for row in rows
    ]


def export_results(db_path: Path) -> list[dict[str, Any]]:
    init_db(db_path)
    with transaction(db_path) as connection:
        rows = connection.execute(
            "SELECT result_json FROM runs ORDER BY run_id ASC"
        ).fetchall()
    return [score_result(json.loads(row["result_json"])) for row in rows]


def compare_results(db_path: Path, left: str, right: str) -> dict[str, Any] | None:
    left_result = load_result(db_path, left)
    right_result = load_result(db_path, right)
    if left_result is None or right_result is None:
        return None
    return {
        "left": left_result,
        "right": right_result,
        "metrics": [
            "final_score",
            "public_check_score",
            "confidence",
            "uncertainty",
            "failure_class",
            "highest_confirmed_milestone",
        ],
    }
