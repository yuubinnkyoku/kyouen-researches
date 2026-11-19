// Sweep audit for the 48 remaining five-parent residual candidate roots (the 49-root
// cover minus the published first WIN7 receipt root). Reads the raw probe records
// JSONL (one line per runner invocation: pilot_d6 control + depth-10 result), pins
// the 49-root cover and mobility JSONs, and emits the combined classification JSON.
//
// Classification rule (depth-limited AND/OR engine, exhaustive when uncapped):
//   WIN7-D10        : loss=true,  uncapped in at least one AND ordering (constructive).
//   REFUTED-D10     : loss=false, uncapped in at least one AND ordering and no ordering
//                     produced an uncapped WIN. Uncapped loss=false is a complete
//                     no-winner-win-within-depth-10 proof for this 7-stone root.
//   CAPPED          : every recorded ordering hit its node cap (no verdict).
// The two orderings must not disagree on a definite verdict (WIN vs uncapped REFUTED):
// that check is an engine-soundness tripwire.
// Usage: node audit_residual_48root_sweep_20261119.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const OUT = path.resolve(SCRIPT_DIR, '../output');
const gitBlobSha = b => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const RECORDS = path.join(OUT, 'residual-48-root-depth10-probe-records-20261119.jsonl');
const FOLD_PATH = path.join(OUT, 'second-third-win7-root-receipt-fold-20261119.json');
function need(ok, m) { if (!ok) throw new Error(m); }
const PIN = {
  cover: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json', 'a8eaf00bd6494eda50a68e7d06498bed833a7688'],
  mobility: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json', 'b35d54a0ced182153802247452a593096a0acf81'],
  prevFoldTarball: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz', 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019'],
  runner: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts', 'c132cc6425eee3feaeef1d697dd74f968cfedb59']
};
function readPinned(k) {
  const [rel, sha] = PIN[k];
  const b = fs.readFileSync(path.join(ROOT, rel));
  need(gitBlobSha(b) === sha, 'input blob mismatch: ' + rel);
  return b;
}
const coverBytes = readPinned('cover');
const mobilityBytes = readPinned('mobility');
const prevFoldBytes = readPinned('prevFoldTarball');
const runnerBytes = readPinned('runner');
const cover = JSON.parse(coverBytes.toString('utf8'));
const mobility = JSON.parse(mobilityBytes.toString('utf8'));
need(cover.status === 'exact-residual-candidate-cover' && cover.all_pass === true, 'cover audit gate');
const firstRoot = '00000000000000821082000010800000';
const sweepRoots = cover.witness.filter(w => w.root !== firstRoot);
need(sweepRoots.length === 48, '48 sweep roots expected from the 49-cover witness');
const sweepSet = new Set(sweepRoots.map(w => w.root));
const priorityOrder = mobility.mobility.priority_order;
const all48 = new Set(priorityOrder.map(x => x.root));
need(all48.size === 49 && all48.has(firstRoot), 'mobility priority order gate');
for (const r of sweepSet) need(all48.has(r), 'sweep root absent from mobility data: ' + r);
const prevFoldBuf = prevFoldBytes; // tarball pinned for provenance only
need(gitBlobSha(runnerBytes) === PIN.runner[1], 'runner pin');
// --- probe records ---
const raw = fs.readFileSync(RECORDS, 'utf8').trim().split(/\r?\n/);
const records = raw.map(l => JSON.parse(l));
function ordName(o) { return o === 1 ? 'andclose1' : 'andclose0'; }
const byRun = new Map();
let controlOk = 0;
for (const rec of records) {
  need(typeof rec.root === 'string' && /^andclose[01]$/.test(rec.ordering) && Number.isInteger(rec.cap) && rec.result && rec.control, 'record shape');
  need(rec.control.control === 'pilot_d6' && rec.control.loss === false && rec.control.nodes === 3402 && rec.control.capped === false, 'pilot control failed: ' + rec.root);
  controlOk++;
  const key = rec.root + '|' + rec.ordering + '|' + rec.cap;
  need(!byRun.has(key), 'duplicate probe record: ' + key);
  byRun.set(key, rec);
  need(sweepSet.has(rec.root) || rec.root === firstRoot, 'record root outside sweep: ' + rec.root);
  need(rec.cap === 950000 || rec.cap === 4000000 || rec.cap === 16000000, 'unexpected cap: ' + rec.cap);
}
const expectedRuns = [];
for (const root of sweepSet) {
  expectedRuns.push(sweepSet.has(root) ? root + '|andclose1|950000' : '', root + '|andclose0|950000');
}
for (const root of sweepSet) {
  need(byRun.has(root + '|andclose1|950000') && byRun.has(root + '|andclose0|950000'), 'missing 950k record for ' + root);
}
// 4M/16M escalation records must only exist for roots capped at 950k in both orderings
const escalation = new Map();
for (const rec of records) {
  if (rec.cap > 950000) {
    const baseCapped = byRun.get(rec.root + '|andclose1|950000').result.capped && byRun.get(rec.root + '|andclose0|950000').result.capped;
    need(baseCapped, 'escalation record for a non-capped root: ' + rec.root);
    escalation.set(rec.root + '|' + rec.ordering + '|' + rec.cap, rec);
  }
}
// --- per-root classification ---
function bestVerdicts(root) {
  const out = [];
  for (const [k, rec] of byRun) if (k.startsWith(root + '|')) out.push(rec);
  return out;
}
const rowsOut = [];
const wins = [], refuted = [], capped = [];
const conflicts = [];
for (const root of sweepSet) {
  const recs = bestVerdicts(root);
  let winUncapped = null, refuteUncapped = null, anyCapHit = false, maxCapTried = 0, allCapped = true;
  for (const rec of recs) {
    maxCapTried = Math.max(maxCapTried, rec.cap);
    if (rec.result.capped) { anyCapHit = true; continue; }
    allCapped = false;
    if (rec.result.loss === true) winUncapped = winUncapped || rec;
    else refuteUncapped = refuteUncapped || rec;
  }
  let klass;
  if (winUncapped) klass = 'WIN7-D10';
  else if (refuteUncapped) klass = 'REFUTED-D10';
  else klass = 'CAPPED-' + maxCapTried;
  if (winUncapped && refuteUncapped) conflicts.push(root);
  if (klass === 'WIN7-D10') wins.push(root);
  else if (klass === 'REFUTED-D10') refuted.push(root);
  else capped.push(root);
  const item = priorityOrder.find(x => x.root === root);
  const witness = cover.witness.find(x => x.root === root);
  rowsOut.push({
    root, priority_index: priorityOrder.indexOf(item), declared_covered_rows: witness.rows,
    legal_next_moves: item.legal_next_moves, d4_orbit: item.root_d4_orbit_size,
    added_bit_rule: 'highest set bit of the root; engine verdict independent of the choice',
    probes: recs.map(rec => ({ordering: rec.ordering, cap: rec.cap, loss: rec.result.loss, nodes: rec.result.nodes, capped: rec.result.capped, terminal_range: rec.result.terminalStoneRange, ms: rec.ms, ms_is_observational: true})),
    classification: klass
  });
}
rowsOut.sort((a, b) => a.priority_index - b.priority_index);
need(conflicts.length === 0, 'ordering verdict conflicts: ' + conflicts.join(','));
need(wins.length + refuted.length + capped.length === 48, 'classification total');
need(new Set(wins).size === wins.length, 'dup win');
const winSet = new Set(wins), refSet = new Set(refuted), capSet = new Set(capped);
// every WIN root must have a probe line record consistent with an extraction published alongside
for (const root of wins) {
  const summaryPath = path.join(OUT, 'resid-win7-root-' + root + '-extraction-summary-20261119.json');
  need(fs.existsSync(summaryPath), 'WIN root missing extraction summary: ' + root);
  const s = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
  need(s.status === 'EXTRACTED_UNVERIFIED' && s.root === root && s.fbt_drops === 0 && s.failure === null && s.completed_moves === s.legal_next_moves, 'extraction gate: ' + root);
}
const sweepPath = path.join(OUT, 'residual-48-root-depth10-sweep-20261119.json');
const recordBytes = fs.readFileSync(RECORDS);
const result = {
  schema: 'n11-residual-48-root-depth10-sweep-20261119-v1',
  date: '2026-11-19',
  status: 'sweep-complete',
  source_main_head: 'c8e974a26629a8b91662f479e1d84e10cae6ddcd',
  input_pins: Object.fromEntries(Object.entries(PIN).map(([k, v]) => [k, {path: v[0], git_blob_sha1: v[1]}])),
  probe_records: {path: 'research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-probe-records-20261119.jsonl', git_blob_sha1: gitBlobSha(recordBytes), records: records.length, pilot_controls_passed: controlOk},
  engine: {file: PIN.runner[0] + ' (class4_child1_runner_v17)', depth: 10, caps: [950000, 4000000, 16000000], andclose_orderings: [1, 0], note: 'v17 probe-exhaustion fallback (no silent fbt drops); fresh engine per candidate'},
  classification_rule: 'WIN7-D10 = uncapped loss=true in >=1 ordering (constructive); REFUTED-D10 = uncapped loss=false in >=1 ordering and no uncapped WIN (complete no-win-within-depth-10 proof at this 7-stone root); CAPPED-<cap> = every ordering hit the cap (no verdict). Numbers/nodes are exact proofs; ms fields are observational timing only.',
  classification: {
    counted_roots: 48,
    win7_d10: {count: wins.length, roots: [...wins].sort()},
    refuted_d10: {count: refuted.length, roots: [...refuted].sort()},
    capped: {count: capped.length, roots: [...capped].sort(), note: 'no depth-10 verdict at the highest cap tried (16,000,000)'},
    ordering_conflicts: []
  },
  rows: rowsOut,
  escalation_runs: [...escalation.values()].map(rec => ({root: rec.root, ordering: rec.ordering, cap: rec.cap, loss: rec.result.loss, nodes: rec.result.nodes, capped: rec.result.capped})),
  checks: [
    {name: 'all 48 sweep roots are the published 49-cover witness minus the first WIN7 receipt root', pass: sweepSet.size === 48},
    {name: 'every record carries a passing pilot_d6 control (loss=false, 3402 nodes)', pass: controlOk === records.length},
    {name: 'every root has both-order 950k runs', pass: true},
    {name: 'escalation runs exist only for 950k-capped roots', pass: true},
    {name: 'no WIN/REFUTED ordering conflict', pass: conflicts.length === 0},
    {name: 'classification totals 48', pass: wins.length + refuted.length + capped.length === 48},
    {name: 'every WIN7-D10 root has a complete 0-drop extraction summary alongside', pass: wins.every(r => fs.existsSync(path.join(OUT, 'resid-win7-root-' + r + '-extraction-summary-20261119.json')))}
  ],
  interpretation_guard: [
    'REFUTED-D10 here is a 7-stone-root-level verdict: no first-player win within depth 10 from that exact root (cap never hit). It is NOT a LOSS proof for any earlier position.',
    'CAPPED-16000000 roots have no verdict at the tried caps and remain eligible candidates.',
    'This sweep does not decide the two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4, or the 11x11 empty board; all remain UNKNOWN.'
  ]
};
need(result.checks.every(x => x.pass), 'audit check failed');
fs.writeFileSync(sweepPath, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({records: records.length, win: wins.length, refuted: refuted.length, capped: capped.length, sweep_json: 'residual-48-root-depth10-sweep-20261119.json'}, null, 2));
