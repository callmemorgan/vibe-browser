#!/usr/bin/env python3
"""Build or serve the local Vibe Browser Benchmark leaderboard UI."""

from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import shutil
from urllib.parse import parse_qs, unquote, urlparse

from benchmark_db import (
    DEFAULT_DB_PATH,
    compare_results,
    export_results,
    init_db,
    list_results,
    load_result,
)
from benchmark_lib import (
    BENCHMARK_ROOT,
    ROOT,
    SITE_DIR,
    default_example_paths,
    html_escape,
    load_results,
    score_result,
)


PUBLIC_FILE_ROOTS = (
    BENCHMARK_ROOT / "examples" / "artifacts",
    BENCHMARK_ROOT / "examples" / "analysis",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build a portable static site.")
    build.add_argument(
        "results",
        nargs="*",
        type=Path,
        help="Canonical result JSON files or directories. Defaults to example runs.",
    )
    build.add_argument(
        "--db",
        type=Path,
        help="Build from this SQLite database instead of result JSON files.",
    )
    build.add_argument(
        "--site-dir",
        type=Path,
        default=SITE_DIR,
        help="Output directory for generated HTML, CSS, JS, and JSON.",
    )

    serve = subparsers.add_parser("serve", help="Serve the SQLite-backed UI and API.")
    serve.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="SQLite database to read and write.",
    )
    serve.add_argument("--host", default="127.0.0.1", help="Bind host.")
    serve.add_argument("--port", type=int, default=8765, help="Bind port.")
    return parser


def run_page_name(run_id: str) -> str:
    return f"runs/{run_id}.html"


def render_layout(title: str, body: str, *, depth: int = 0, live: bool = False) -> str:
    prefix = "../" * depth
    live_config = "\n  <script>window.BENCHMARK_LIVE_API = true;</script>" if live else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_escape(title)}</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%23126d6a'/%3E%3Cpath d='M3 4h10v2H3zm0 3h7v2H3zm0 3h5v2H3z' fill='%23f8f5ec'/%3E%3C/svg%3E">
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
  <header class="topbar">
    <a class="wordmark" href="{prefix}index.html">Vibe Browser Benchmark</a>
    <nav>
      <a href="{prefix}index.html">Leaderboard</a>
      <a href="{prefix}compare.html">Compare</a>
      <a href="{prefix}results.json">Data</a>
    </nav>
  </header>
  {body}{live_config}
  <script src="{prefix}assets/results.js"></script>
  <script src="{prefix}assets/site.js"></script>
</body>
</html>
"""


def render_index_shell(*, live: bool = False) -> str:
    body = """<main class="shell">
  <section class="hero">
    <p class="eyebrow">Local prototype</p>
    <h1>Evidence-first browser agent leaderboard</h1>
    <p class="lede">A reproducible view over benchmark runs stored in SQLite, with canonical JSON import and export for review.</p>
  </section>
  <section class="controls" aria-label="Leaderboard filters">
    <label>Provider <select id="providerFilter"><option value="">All</option></select></label>
    <label>Harness <select id="harnessFilter"><option value="">All</option></select></label>
    <label>Milestone <select id="milestoneFilter"><option value="">All</option></select></label>
    <label>Model <input id="modelFilter" type="search" placeholder="filter model"></label>
  </section>
  <section class="table-wrap">
    <table id="leaderboard">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Run</th>
          <th>Model</th>
          <th>Agent</th>
          <th>Profile</th>
          <th>Milestone</th>
          <th>Score</th>
          <th>Conf / Unc</th>
          <th>Failure</th>
        </tr>
      </thead>
      <tbody><tr><td colspan="9" class="empty">Loading runs...</td></tr></tbody>
    </table>
  </section>
</main>"""
    return render_layout("Vibe Browser Benchmark Leaderboard", body, live=live)


def render_compare_shell(*, live: bool = False) -> str:
    body = """<main class="shell">
  <section class="hero compact">
    <p class="eyebrow">Comparison</p>
    <h1>Run-to-run score inspection</h1>
    <p class="lede">Pick two runs to compare milestone scores, confidence, failure class, and run metadata.</p>
  </section>
  <section class="controls" aria-label="Comparison controls">
    <label>Run A <select id="compareA"></select></label>
    <label>Run B <select id="compareB"></select></label>
  </section>
  <section id="comparison" class="comparison"></section>
</main>"""
    return render_layout("Compare Runs - Vibe Browser Benchmark", body, live=live)


def render_run_shell(run_id: str, *, live: bool = False) -> str:
    body = f"""<main class="shell detail" id="runDetail" data-run-id="{html_escape(run_id)}">
  <a class="backlink" href="../index.html">Back to leaderboard</a>
  <section class="hero compact">
    <p class="eyebrow" id="runEyebrow">Run detail</p>
    <h1>{html_escape(run_id)}</h1>
    <p class="lede" id="runSummary">Loading run evidence...</p>
  </section>
  <section class="score-grid" id="scoreGrid"></section>
  <section class="explain">
    <h2>Score Explanation</h2>
    <p>The scorer uses the quadratic milestone curve from <code>blended-score.md</code>, then applies the repository quality multiplier from rubric categories. Confidence is based on verification evidence, rubric presence, artifact links, and comparison eligibility.</p>
  </section>
  <section class="table-wrap">
    <h2>Milestones</h2>
    <table>
      <thead><tr><th>Milestone</th><th>Evaluator</th><th>Public</th><th>Points</th><th>Notes</th></tr></thead>
      <tbody id="milestoneRows"><tr><td colspan="5" class="empty">Loading milestones...</td></tr></tbody>
    </table>
  </section>
  <section class="table-wrap">
    <h2>Verification</h2>
    <table>
      <thead><tr><th>Result</th><th>Scope</th><th>Status</th><th>Failure</th></tr></thead>
      <tbody id="verificationRows"><tr><td colspan="4" class="empty">Loading verification...</td></tr></tbody>
    </table>
  </section>
  <section class="table-wrap">
    <h2>Artifacts</h2>
    <table>
      <thead><tr><th>Artifact</th><th>Kind</th><th>Visibility</th><th>Path</th></tr></thead>
      <tbody id="artifactRows"><tr><td colspan="4" class="empty">Loading artifacts...</td></tr></tbody>
    </table>
  </section>
</main>"""
    return render_layout(f"{run_id} - Vibe Browser Benchmark", body, depth=1, live=live)


def css() -> str:
    return """@font-face { font-family: ui-serif-local; src: local("Iowan Old Style"); }
:root {
  --ink: #20221f;
  --muted: #62675d;
  --paper: #f8f5ec;
  --panel: #fffdf6;
  --line: #d8d0be;
  --accent: #126d6a;
  --accent-2: #9a3b2f;
  --gold: #c28b18;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font: 15px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
.topbar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background: rgba(248, 245, 236, 0.94);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(8px);
}
.wordmark {
  color: var(--ink);
  font: 700 18px/1 ui-serif-local, Georgia, serif;
  text-decoration: none;
}
nav { display: flex; gap: 16px; }
nav a, .backlink { color: var(--accent); text-decoration: none; }
.shell { width: min(1180px, calc(100vw - 32px)); margin: 0 auto; padding: 32px 0 56px; }
.hero {
  border-bottom: 2px solid var(--ink);
  padding: 26px 0 28px;
  margin-bottom: 24px;
}
.hero.compact { padding-bottom: 18px; }
.eyebrow { margin: 0 0 10px; color: var(--accent-2); text-transform: uppercase; letter-spacing: 0; font-weight: 700; }
h1 { max-width: 900px; margin: 0; font: 800 48px/1.02 ui-serif-local, Georgia, serif; }
h2 { margin: 28px 0 12px; font: 800 22px/1.1 ui-serif-local, Georgia, serif; }
.lede { max-width: 760px; margin: 14px 0 0; color: var(--muted); font-size: 17px; }
.controls {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 22px 0;
}
label { display: grid; gap: 6px; color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 700; }
select, input {
  width: 100%;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  min-height: 40px;
  padding: 8px 10px;
  font: inherit;
}
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--line);
  background: var(--panel);
}
.table-wrap h2 { padding: 0 16px; }
table { width: 100%; border-collapse: collapse; min-width: 820px; }
th {
  text-align: left;
  padding: 11px 12px;
  color: var(--muted);
  background: #eee7d6;
  border-bottom: 1px solid var(--line);
  font-size: 12px;
  text-transform: uppercase;
}
td { padding: 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
td span { display: block; color: var(--muted); margin-top: 3px; font-size: 12px; }
.rank { color: var(--accent-2); font-weight: 800; }
.score { color: var(--accent); font-weight: 900; font-size: 17px; }
tr[hidden] { display: none; }
.empty { color: var(--muted); }
.score-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 22px 0;
}
.score-grid div, .explain, .comparison {
  background: var(--panel);
  border: 1px solid var(--line);
  padding: 16px;
}
.score-grid span { display: block; color: var(--muted); text-transform: uppercase; font-size: 12px; font-weight: 700; }
.score-grid strong { display: block; margin-top: 8px; font: 800 30px/1 ui-serif-local, Georgia, serif; color: var(--accent); }
code { background: #eee7d6; padding: 2px 4px; }
@media (max-width: 760px) {
  .topbar { align-items: flex-start; gap: 10px; flex-direction: column; }
  .controls, .score-grid { grid-template-columns: 1fr; }
  h1 { font-size: 34px; }
}
"""


def js() -> str:
    return r"""function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[char]));
}
function formatNumber(value) {
  return typeof value === 'number' ? value.toFixed(2) : escapeHtml(value ?? 'none');
}
function embeddedResults() {
  return window.BENCHMARK_RESULTS || [];
}
function summaryFromResult(result) {
  return {
    run_id: result.run.run_id,
    batch_id: result.run.batch_id,
    model_provider: result.run.model_provider,
    model: result.run.model,
    agent_tool: result.run.agent_tool,
    harness: result.run.harness,
    profile: result.run.profile,
    target: result.run.target,
    stop_reason: result.run.stop_reason,
    final_score: result.scores.final_score,
    public_check_score: result.scores.public_check_score,
    evaluator_score: result.scores.evaluator_score,
    confidence: result.scores.confidence,
    uncertainty: result.scores.uncertainty,
    highest_confirmed_milestone: result.scores.highest_confirmed_milestone,
    failure_class: result.scores.failure_class,
    rankable: Boolean(result.scores.rankable),
  };
}
async function fetchJson(path) {
  if (!window.BENCHMARK_LIVE_API) return null;
  try {
    const response = await fetch(path, { headers: { Accept: 'application/json' } });
    if (!response.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}
async function getRunSummaries() {
  const payload = await fetchJson('/api/runs');
  if (payload && Array.isArray(payload.runs)) return payload.runs;
  return embeddedResults().map(summaryFromResult);
}
async function getFullRun(runId) {
  const payload = await fetchJson(`/api/runs/${encodeURIComponent(runId)}`);
  if (payload && payload.run) return payload;
  return embeddedResults().find((result) => result.run.run_id === runId) || null;
}
function addOptions(select, values, label) {
  if (!select) return;
  select.innerHTML = `<option value="">${escapeHtml(label)}</option>` + values.map((value) => (
    `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`
  )).join('');
}
function populateFilters(rows) {
  addOptions(document.querySelector('#providerFilter'), [...new Set(rows.map((row) => row.model_provider))].sort(), 'All');
  addOptions(document.querySelector('#harnessFilter'), [...new Set(rows.map((row) => row.harness))].sort(), 'All');
  addOptions(document.querySelector('#milestoneFilter'), [...new Set(rows.map((row) => row.highest_confirmed_milestone || 'none'))].sort(), 'All');
}
function renderLeaderboard(rows) {
  const body = document.querySelector('#leaderboard tbody');
  if (!body) return;
  if (!rows.length) {
    body.innerHTML = '<tr><td colspan="9" class="empty">No benchmark runs found.</td></tr>';
    return;
  }
  const ranked = [...rows].sort((a, b) => {
    if (Boolean(a.rankable) !== Boolean(b.rankable)) return a.rankable ? -1 : 1;
    return Number(b.final_score || 0) - Number(a.final_score || 0) || String(a.run_id).localeCompare(String(b.run_id));
  });
  body.innerHTML = ranked.map((row, index) => {
    const rankLabel = row.rankable ? String(index + 1) : 'unranked';
    const milestone = row.highest_confirmed_milestone || 'none';
    return `<tr data-provider="${escapeHtml(row.model_provider)}" data-model="${escapeHtml(row.model)}" data-harness="${escapeHtml(row.harness)}" data-milestone="${escapeHtml(milestone)}">
      <td class="rank">${escapeHtml(rankLabel)}</td>
      <td><a href="runs/${encodeURIComponent(row.run_id)}.html">${escapeHtml(row.run_id)}</a></td>
      <td><strong>${escapeHtml(row.model)}</strong><span>${escapeHtml(row.model_provider)}</span></td>
      <td>${escapeHtml(row.agent_tool)}<span>${escapeHtml(row.harness)}</span></td>
      <td>${escapeHtml(row.profile)}<span>${escapeHtml(row.target)}</span></td>
      <td>${escapeHtml(milestone)}</td>
      <td class="score">${formatNumber(Number(row.final_score || 0))}</td>
      <td>${formatNumber(Number(row.confidence || 0))} / ${formatNumber(Number(row.uncertainty || 0))}</td>
      <td>${escapeHtml(row.failure_class || 'none')}</td>
    </tr>`;
  }).join('');
}
function applyFilters() {
  const provider = document.querySelector('#providerFilter')?.value || '';
  const harness = document.querySelector('#harnessFilter')?.value || '';
  const milestone = document.querySelector('#milestoneFilter')?.value || '';
  const model = (document.querySelector('#modelFilter')?.value || '').toLowerCase();
  document.querySelectorAll('#leaderboard tbody tr').forEach((row) => {
    const visible =
      (!provider || row.dataset.provider === provider) &&
      (!harness || row.dataset.harness === harness) &&
      (!milestone || row.dataset.milestone === milestone) &&
      (!model || (row.dataset.model || '').toLowerCase().includes(model));
    row.hidden = !visible;
  });
}
function artifactUrl(path) {
  if (!path) return '#';
  if (/^https?:\/\//i.test(path)) return path;
  if (window.BENCHMARK_LIVE_API) return `/files/${String(path).split('/').map(encodeURIComponent).join('/')}`;
  const stripped = String(path).replace(/^vibe-browser-benchmark\//, '');
  const prefix = location.pathname.includes('/runs/') ? '../../' : '../';
  return prefix + stripped;
}
function rowsOrEmpty(items, columns, renderRow) {
  if (!items.length) return `<tr><td colspan="${columns}" class="empty">No records.</td></tr>`;
  return items.map(renderRow).join('');
}
function renderRunDetail(result) {
  if (!result) return;
  const run = result.run;
  const scores = result.scores;
  const eyebrow = document.querySelector('#runEyebrow');
  const summary = document.querySelector('#runSummary');
  if (eyebrow) eyebrow.textContent = `${run.model_provider} / ${run.model}`;
  if (summary) summary.innerHTML = `Target ${escapeHtml(String(run.target).toUpperCase())}, profile ${escapeHtml(run.profile)}, stopped because <code>${escapeHtml(run.stop_reason)}</code>.`;
  document.querySelector('#scoreGrid').innerHTML = [
    ['Final', formatNumber(scores.final_score)],
    ['Public Check', formatNumber(scores.public_check_score)],
    ['Confidence', formatNumber(scores.confidence)],
    ['Milestone', escapeHtml(scores.highest_confirmed_milestone || 'none')],
  ].map(([label, value]) => `<div><span>${label}</span><strong>${value}</strong></div>`).join('');
  document.querySelector('#milestoneRows').innerHTML = rowsOrEmpty(scores.milestones || [], 5, (item) => (
    `<tr><td>${escapeHtml(String(item.milestone).toUpperCase())}</td><td>${formatNumber(item.evaluator_score)}</td><td>${formatNumber(item.public_check_score)}</td><td>${formatNumber(item.points)}</td><td>${escapeHtml(item.notes || '')}</td></tr>`
  ));
  document.querySelector('#verificationRows').innerHTML = rowsOrEmpty(result.verification_results || [], 4, (item) => (
    `<tr><td>${escapeHtml(item.result_id)}</td><td>${escapeHtml(item.scope)}</td><td>${escapeHtml(item.status)}</td><td>${escapeHtml(item.failure_class || 'none')}</td></tr>`
  ));
  document.querySelector('#artifactRows').innerHTML = rowsOrEmpty(result.artifacts || [], 4, (item) => {
    const path = item.path || '';
    return `<tr><td>${escapeHtml(item.artifact_id)}</td><td>${escapeHtml(item.kind)}</td><td>${escapeHtml(item.visibility)}</td><td><a href="${escapeHtml(artifactUrl(path))}">${escapeHtml(path)}</a></td></tr>`;
  });
}
function populateCompareSelects(rows) {
  const options = rows.map((row) => `<option value="${escapeHtml(row.run_id)}">${escapeHtml(row.run_id)}</option>`).join('');
  const a = document.querySelector('#compareA');
  const b = document.querySelector('#compareB');
  if (!a || !b) return;
  a.innerHTML = options;
  b.innerHTML = options;
  if (b.options.length > 1) b.selectedIndex = 1;
}
async function renderComparison() {
  const target = document.querySelector('#comparison');
  const selectA = document.querySelector('#compareA');
  const selectB = document.querySelector('#compareB');
  if (!target || !selectA || !selectB || !selectA.value || !selectB.value) return;
  if (selectA.value === selectB.value && selectB.options.length > 1) selectB.selectedIndex = 1;
  const [a, b] = await Promise.all([getFullRun(selectA.value), getFullRun(selectB.value)]);
  if (!a || !b) {
    target.innerHTML = '<p class="empty">Unable to load comparison data.</p>';
    return;
  }
  const rows = ['final_score', 'public_check_score', 'confidence', 'uncertainty', 'failure_class', 'highest_confirmed_milestone'].map((key) => (
    `<tr><th>${escapeHtml(key)}</th><td>${formatNumber(a.scores[key])}</td><td>${formatNumber(b.scores[key])}</td></tr>`
  )).join('');
  const milestoneRows = (a.scores.milestones || []).map((left, index) => {
    const right = (b.scores.milestones || [])[index] || {};
    return `<tr><th>${escapeHtml(String(left.milestone).toUpperCase())}</th><td>${formatNumber(left.evaluator_score)}</td><td>${formatNumber(right.evaluator_score)}</td></tr>`;
  }).join('');
  target.innerHTML = `<div class="table-wrap"><table>
    <thead><tr><th>Metric</th><th>${escapeHtml(a.run.run_id)}</th><th>${escapeHtml(b.run.run_id)}</th></tr></thead>
    <tbody>${rows}${milestoneRows}</tbody>
  </table></div>`;
}
async function init() {
  if (document.querySelector('#leaderboard')) {
    const rows = await getRunSummaries();
    populateFilters(rows);
    renderLeaderboard(rows);
    document.querySelectorAll('#providerFilter, #harnessFilter, #milestoneFilter, #modelFilter').forEach((control) => {
      control.addEventListener('input', applyFilters);
    });
  }
  const detail = document.querySelector('#runDetail');
  if (detail) {
    const result = await getFullRun(detail.dataset.runId);
    renderRunDetail(result);
  }
  if (document.querySelector('#comparison')) {
    const rows = await getRunSummaries();
    populateCompareSelects(rows);
    await renderComparison();
    document.querySelectorAll('#compareA, #compareB').forEach((control) => {
      control.addEventListener('input', renderComparison);
    });
  }
}
init();
"""


def build_site(results: list[dict], site_dir: Path) -> None:
    if site_dir.exists():
        shutil.rmtree(site_dir)
    (site_dir / "assets").mkdir(parents=True)
    (site_dir / "runs").mkdir(parents=True)
    scored = [score_result(result) for result in results]
    (site_dir / "index.html").write_text(render_index_shell(), encoding="utf-8")
    (site_dir / "compare.html").write_text(render_compare_shell(), encoding="utf-8")
    (site_dir / "assets" / "site.css").write_text(css(), encoding="utf-8")
    (site_dir / "assets" / "site.js").write_text(js(), encoding="utf-8")
    (site_dir / "assets" / "results.js").write_text(
        "window.BENCHMARK_RESULTS = "
        + json.dumps(scored, indent=2, sort_keys=True)
        + ";\n",
        encoding="utf-8",
    )
    (site_dir / "results.json").write_text(
        json.dumps(scored, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for result in scored:
        run_id = result["run"]["run_id"]
        (site_dir / run_page_name(run_id)).write_text(
            render_run_shell(run_id),
            encoding="utf-8",
        )


def json_response(handler: BaseHTTPRequestHandler, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def text_response(
    handler: BaseHTTPRequestHandler,
    body: str,
    *,
    content_type: str = "text/html; charset=utf-8",
    status: HTTPStatus = HTTPStatus.OK,
) -> None:
    encoded = body.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def send_public_file(handler: BaseHTTPRequestHandler, relative_path: str) -> None:
    candidate = ROOT / unquote(relative_path)
    if candidate.is_dir() or not candidate.exists():
        handler.send_error(HTTPStatus.NOT_FOUND, "file not found")
        return
    if not any(is_relative_to(candidate, root) for root in PUBLIC_FILE_ROOTS):
        handler.send_error(HTTPStatus.FORBIDDEN, "file is not public")
        return
    content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
    body = candidate.read_bytes()
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(db_path: Path) -> type[BaseHTTPRequestHandler]:
    class BenchmarkHandler(BaseHTTPRequestHandler):
        server_version = "VibeBenchmark/0.1"

        def log_message(self, format: str, *args: object) -> None:
            return

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path in {"/", "/index.html"}:
                text_response(self, render_index_shell(live=True))
                return
            if path == "/compare.html":
                text_response(self, render_compare_shell(live=True))
                return
            if path.startswith("/runs/") and path.endswith(".html"):
                run_id = unquote(Path(path).stem)
                if load_result(db_path, run_id) is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "run not found")
                    return
                text_response(self, render_run_shell(run_id, live=True))
                return
            if path == "/assets/site.css":
                text_response(self, css(), content_type="text/css; charset=utf-8")
                return
            if path == "/assets/site.js":
                text_response(self, js(), content_type="text/javascript; charset=utf-8")
                return
            if path == "/assets/results.js":
                text_response(
                    self,
                    "window.BENCHMARK_RESULTS = [];\n",
                    content_type="text/javascript; charset=utf-8",
                )
                return
            if path == "/api/runs":
                filters = {key: values[0] for key, values in query.items() if values and values[0]}
                json_response(self, {"runs": list_results(db_path, filters)})
                return
            if path.startswith("/api/runs/"):
                run_id = unquote(path.removeprefix("/api/runs/"))
                result = load_result(db_path, run_id)
                if result is None:
                    json_response(self, {"error": "run not found"}, HTTPStatus.NOT_FOUND)
                    return
                json_response(self, result)
                return
            if path == "/api/compare":
                left = query.get("left", [""])[0]
                right = query.get("right", [""])[0]
                comparison = compare_results(db_path, left, right) if left and right else None
                if comparison is None:
                    json_response(self, {"error": "comparison inputs not found"}, HTTPStatus.NOT_FOUND)
                    return
                json_response(self, comparison)
                return
            if path in {"/results.json", "/api/export/results.json"}:
                json_response(self, export_results(db_path))
                return
            if path.startswith("/files/"):
                send_public_file(self, path.removeprefix("/files/"))
                return
            self.send_error(HTTPStatus.NOT_FOUND, "not found")

    return BenchmarkHandler


def serve_site(db_path: Path, host: str, port: int) -> None:
    init_db(db_path)
    server = ThreadingHTTPServer((host, port), make_handler(db_path))
    print(f"Serving SQLite benchmark UI at http://{host}:{port}/")
    print(f"Database: {db_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "build":
        if args.db:
            results = export_results(args.db)
        else:
            paths = args.results or default_example_paths()
            results = load_results(paths)
        build_site(results, args.site_dir)
        print(f"Built {args.site_dir} from {len(results)} run(s)")
        return 0
    if args.command == "serve":
        serve_site(args.db, args.host, args.port)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
