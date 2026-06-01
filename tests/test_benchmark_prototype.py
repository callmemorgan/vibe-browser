from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
LIB_PATH = ROOT / "scripts" / "benchmark_lib.py"
SITE_PATH = ROOT / "scripts" / "benchmark_site.py"
DB_PATH = ROOT / "scripts" / "benchmark_db.py"

sys.path.insert(0, str(ROOT / "scripts"))

lib_spec = importlib.util.spec_from_file_location("benchmark_lib", LIB_PATH)
assert lib_spec is not None
benchmark_lib = importlib.util.module_from_spec(lib_spec)
assert lib_spec.loader is not None
lib_spec.loader.exec_module(benchmark_lib)

site_spec = importlib.util.spec_from_file_location("benchmark_site", SITE_PATH)
assert site_spec is not None
benchmark_site = importlib.util.module_from_spec(site_spec)
assert site_spec.loader is not None
site_spec.loader.exec_module(benchmark_site)

db_spec = importlib.util.spec_from_file_location("benchmark_db", DB_PATH)
assert db_spec is not None
benchmark_db = importlib.util.module_from_spec(db_spec)
assert db_spec.loader is not None
db_spec.loader.exec_module(benchmark_db)


class BenchmarkPrototypeTests(unittest.TestCase):
    def test_example_results_validate_and_score(self) -> None:
        results = benchmark_lib.load_results([benchmark_lib.EXAMPLES_DIR])
        self.assertGreaterEqual(len(results), 5)
        run_ids = {result["run"]["run_id"] for result in results}
        self.assertIn("example-success-short", run_ids)
        self.assertIn("example-restarted", run_ids)
        self.assertIn("example-messy", run_ids)

        for result in results:
            scored = benchmark_lib.score_result(result)
            self.assertFalse(benchmark_lib.validate_result(scored))
            self.assertIn("final_score", scored["scores"])
            self.assertIn("confidence", scored["scores"])
            self.assertIn("uncertainty", scored["scores"])
            self.assertEqual(len(scored["scores"]["milestones"]), 10)

    def test_scoring_uses_quadratic_milestone_curve(self) -> None:
        result = benchmark_lib.read_json(
            benchmark_lib.EXAMPLES_DIR / "example-success-short.json"
        )
        scored = benchmark_lib.score_result(result)
        by_milestone = {
            item["milestone"]: item for item in scored["scores"]["milestones"]
        }
        self.assertEqual(by_milestone["m0"]["value"], 1)
        self.assertEqual(by_milestone["m1"]["value"], 4)
        self.assertEqual(by_milestone["m9"]["value"], 100)

    def test_site_builder_writes_leaderboard_compare_and_run_pages(self) -> None:
        results = benchmark_lib.load_results([benchmark_lib.EXAMPLES_DIR])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "site"
            benchmark_site.build_site(results, output)
            self.assertTrue((output / "index.html").exists())
            self.assertTrue((output / "compare.html").exists())
            self.assertTrue((output / "assets" / "site.css").exists())
            self.assertTrue((output / "assets" / "site.js").exists())
            self.assertTrue((output / "assets" / "results.js").exists())
            self.assertTrue((output / "runs" / "example-success-short.html").exists())

    def test_sqlite_store_round_trips_and_filters_results(self) -> None:
        results = benchmark_lib.load_results(
            [benchmark_lib.EXAMPLES_DIR / "example-success-short.json"]
        )
        with tempfile.TemporaryDirectory() as temp:
            db_path = Path(temp) / "benchmark.db"
            stored = benchmark_db.upsert_result(db_path, results[0])
            benchmark_db.upsert_result(db_path, stored)

            loaded = benchmark_db.load_result(db_path, "example-success-short")
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["run"]["run_id"], "example-success-short")

            exported = benchmark_db.export_results(db_path)
            self.assertEqual(len(exported), 1)

            rows = benchmark_db.list_results(db_path, {"provider": "openai"})
            self.assertEqual([row["run_id"] for row in rows], ["example-success-short"])

            with benchmark_db.transaction(db_path) as connection:
                attempt_count = connection.execute(
                    "SELECT COUNT(*) FROM attempts WHERE run_id = ?",
                    ("example-success-short",),
                ).fetchone()[0]
            self.assertEqual(attempt_count, len(stored["attempts"]))

    def test_sqlite_compare_returns_full_results(self) -> None:
        results = benchmark_lib.load_results([benchmark_lib.EXAMPLES_DIR])
        with tempfile.TemporaryDirectory() as temp:
            db_path = Path(temp) / "benchmark.db"
            for result in results[:2]:
                benchmark_db.upsert_result(db_path, result)

            comparison = benchmark_db.compare_results(
                db_path,
                results[0]["run"]["run_id"],
                results[1]["run"]["run_id"],
            )
            self.assertIsNotNone(comparison)
            self.assertIn("final_score", comparison["metrics"])
            self.assertEqual(comparison["left"]["run"]["run_id"], results[0]["run"]["run_id"])


if __name__ == "__main__":
    unittest.main()
