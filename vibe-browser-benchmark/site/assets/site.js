function escapeHtml(value) {
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
