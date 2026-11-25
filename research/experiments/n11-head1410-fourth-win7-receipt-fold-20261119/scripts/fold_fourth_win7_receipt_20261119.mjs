// Receipt fold for the fourth residual WIN7-D10 root
// (00000000000000801202060001000000, K1035 certificate).
// Chains on the published second/third receipt fold exactly as
// fold_second_third_win7_receipts_20261119.mjs chained on the first fold tarball.
// All gates are recomputed from the pinned inputs. Before the receipt is written,
// the full published verdict universe (head1476 + cost78c/79c/73j transfers +
// global fold + cost78c/79c receipts + 48-root sweep + first/second/third receipt
// folds) is re-derived so a WIN/LOSS conflict for the fourth root is detected
// instead of silently folded. The certificate is re-verified live in this
// environment with both pinned independent verifiers (BigInt 3x3 cofactor and
// 4x4 Bareiss) and the state-flow totals are compared to K1035's published ones.
// Usage: node fold_fourth_win7_receipt_20261119.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const EXP_DIR = path.resolve(SCRIPT_DIR, '..');
const OUT = path.join(EXP_DIR, 'output');
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const gitBlobSha = b => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
function need(ok, m) { if (!ok) throw new Error(m); }
const FOURTH_ROOT = '00000000000000801202060001000000';
const CERT_GZ_SHA256 = 'f9bf9b2489f6bf656837579490d4b67956290132741ebae0f3d3ebe472ee7f91';
const CERT_SHA256 = 'f3fcf274ee72d98f4501d104f694d679cd3301e0e161a06a22c191c89ad94bae';
const CERT_BYTES = 1843284;
const P = {
  worklist: ['research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv', '2fee1d0718547a62e346d35f5858d7913e37c097'],
  ledger: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json', 'e8785d509e8a11a37c0d03cc450455a14708c34d'],
  census: ['research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json', '9c251da3138c5cb0516e097be5e5d0427dfaf5f0'],
  globalFold: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json', '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc'],
  previousCostFold: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json', '7e6144cc4bc92c34faa14bed3058cde64fb3880e'],
  firstFoldTarball: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz', 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019'],
  cover: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json', 'a8eaf00bd6494eda50a68e7d06498bed833a7688'],
  head1476: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-cost71e-full-universe-verdict-join-20261118.json', '65d0c7ce0200638a50db5451b11b8cb88ec64b5d'],
  cost78c: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json', '626409d50d0a7bb1b925ebecbff7dbee9adfa398'],
  cost79c: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79c-inflight-20261118.json', '054923a47ea0387b25f734222c499e60c054109b'],
  cost73j: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73j-inflight-20261117.json', '74fc3417391e30cf4cff9c2ffce059dce529ed86'],
  sweep: ['research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json', '37aba599d0b69275225bf231d56cb18feed14090'],
  fold23: ['research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json', '7923a0fe5331d1f7c896748031c4071b68fcc13a'],
  coverResolve: ['research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/five-parent-refuted-excluded-cover-resolve-20261119.json', '600b23d39888ea0e693742da4b2ae9c372a9faf0'],
  witnessProbes: ['research/experiments/n11-head1410-residual-28-root-witness-win7-20261119/output/witness-root-probes-and-certificate-20261119.json', '9cfb5c9c5d8d857b46bd147a68f9795d0a3c59b1'],
  certGz: ['research/experiments/n11-head1410-residual-28-root-witness-win7-20261119/output/win7-root-00000000000000801202060001000000-20261119.n11.gz', 'a9030a517d92dee293afc38d5ca7b623ce08e930'],
  runner: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts', 'c132cc6425eee3feaeef1d697dd74f968cfedb59'],
  extractor: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact_v16.ts', '5518d375fc6b4a7a14c22a1a65586f0c1c5731c0'],
  bigintVerifier: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_win7_certificate_bigint_independent.mjs', '62b5d9413daafb172f6e10249976ee6808f7b454'],
  bareissVerifier: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts', '2960afabdf7c1a7012d223974b65f1423e6890da']
};
function read(k) {
  const [rel, sha] = P[k];
  const b = fs.readFileSync(path.join(ROOT, rel));
  need(gitBlobSha(b) === sha, 'input blob mismatch ' + k);
  return b;
}
function js(k) { return JSON.parse(read(k).toString('utf8')); }
// --- D4 machinery (verbatim convention of the fold chain) ---
const tf = [(x, y) => [x, y], (x, y) => [y, 10 - x], (x, y) => [10 - x, 10 - y], (x, y) => [10 - y, x], (x, y) => [10 - x, y], (x, y) => [x, 10 - y], (x, y) => [y, x], (x, y) => [10 - y, 10 - x]];
function d4(m, t) { let z = 0n; for (let p = 0; p < 121; p++) if ((m >> BigInt(p)) & 1n) { const [x, y] = tf[t](p % 11, Math.floor(p / 11)); z |= 1n << BigInt(11 * y + x); } return z; }
function canon(m) { let b = null; for (let t = 0; t < 8; t++) { const z = d4(m, t); if (b === null || z < b) b = z; } return b.toString(16).padStart(32, '0'); }
function rowParents(h, parents) { const m = BigInt('0x' + h), ps = new Set(); for (let q = 0; q < 121; q++) if ((m >> BigInt(q)) & 1n) { const p = canon(m ^ (1n << BigInt(q))); if (parents.has(p)) ps.add(p); } return [...ps].sort(); }
function demand(h, parents, parentsInfo) { const d = { c1: 0, c2: 0, c4: 0 }; for (const p of rowParents(h, parents)) { const c = parentsInfo.get(p).classes; if (c & 1) d.c1++; if (c & 2) d.c2++; if (c & 4) d.c4++; } return d; }
function rootRowSet(rootHex, openSet) {
  const mask = BigInt('0x' + rootHex), set = new Set();
  for (let t = 0; t < 8; t++) { const sr = d4(mask, t); for (let q = 0; q < 121; q++) if ((sr >> BigInt(q)) & 1n) { const h = canon(sr ^ (1n << BigInt(q))); if (openSet.has(h)) set.add(h); } }
  return set;
}
// --- frontier reconstruction (base .. first fold .. second/third fold) ---
const ledger = js('ledger'), census = js('census'), gf = js('globalFold'), prev = js('previousCostFold');
const cover = js('cover');
const csv = read('worklist').toString('utf8').trim().split(/\r?\n/), cols = csv[0].split(',');
const ix = cols.indexOf('s6_canonical_hex'), cx = cols.indexOf('own_candidates_s6_s7_edge_cost'), kx = cols.indexOf('category');
need(ix >= 0 && cx >= 0 && kx >= 0, 'worklist header');
const work = new Map();
for (const line of csv.slice(1)) { const a = line.split(','); work.set(a[ix], { cost: Number(a[cx]), category: a[kx] }); }
const old66 = new Set(ledger.derived.closed_rows_66), oldGlobal = new Set(gf.receipts_by_row.map(x => x.row_hex));
const open0 = new Map([...work].filter(([h]) => !old66.has(h) && !oldGlobal.has(h)));
need(open0.size === 6259 && [...open0.values()].reduce((s, x) => s + x.cost, 0) === 495507, 'global-fold base frontier');
const priorReceiptRows = new Set(prev.new_receipt_coverage.receipts_by_row.map(x => x.row_hex));
const open = new Map([...open0].filter(([h]) => !priorReceiptRows.has(h)));
need(open.size === 6240 && [...open.values()].reduce((s, x) => s + x.cost, 0) === 493965, 'cost78c/79c fold frontier');
// --- first fold (tarball) ---
function untarEntry(gzBytes, wantedSuffix) {
  const t = zlib.gunzipSync(gzBytes);
  let off = 0;
  while (off + 512 <= t.length) {
    const hdr = t.subarray(off, off + 512);
    if (hdr.every(x => x === 0)) break;
    const name = hdr.subarray(0, 100).toString('utf8').replace(/\0.*$/, '');
    const sizeField = hdr.subarray(124, 136).toString('utf8').replace(/\0.*$/, '').trim();
    let size = 0;
    if (sizeField) size = parseInt(sizeField, 8);
    const data = t.subarray(off + 512, off + 512 + size);
    if (name.endsWith(wantedSuffix)) return data;
    off += 512 + Math.ceil(size / 512) * 512;
  }
  throw new Error('entry not found in tarball: ' + wantedSuffix);
}
const firstFoldBytes = untarEntry(read('firstFoldTarball'), 'output/first-win7-root-receipt-fold-20261119.json');
const firstFold = JSON.parse(firstFoldBytes.toString('utf8'));
need(firstFold.status === 'fold-complete' && firstFold.schema === 'n11-five-parent-first-win7-receipt-fold-20261119-v1', 'first fold schema');
const firstClosedRows = firstFold.new_receipt_coverage.rows.map(x => x.row_hex);
need(firstClosedRows.length === 4 && new Set(firstClosedRows).size === 4, 'first fold closed rows');
const open1 = new Map([...open].filter(([h]) => !firstClosedRows.includes(h)));
need(open1.size === 6236 && [...open1.values()].reduce((s, x) => s + x.cost, 0) === 493703, 'first-fold frontier');
const fa = firstFold.frontier_after;
need(fa.unique_remaining_s6 === 6236 && fa.sum_remaining_cost === 493703 && fa.solved_s6_in_manifest === 1612 && fa.parent_row_incidence === 11876, 'first-fold frontier crosscheck');
// --- second/third fold chain ---
const fold23 = js('fold23');
need(fold23.status === 'fold-complete' && fold23.schema === 'n11-five-parent-second-third-win7-receipt-fold-20261119-v1', 'second/third fold schema');
const fold23Rows = fold23.new_receipt_coverage.rows.map(x => x.row_hex);
need(fold23Rows.length === 7 && new Set(fold23Rows).size === 7, 'second/third fold closed rows');
const open2 = new Map([...open1].filter(([h]) => !fold23Rows.includes(h)));
need(open2.size === 6229 && [...open2.values()].reduce((s, x) => s + x.cost, 0) === 493184, 'second/third-fold frontier');
const fa23 = fold23.frontier_after;
need(fa23.unique_remaining_s6 === 6229 && fa23.sum_remaining_cost === 493184 && fa23.solved_s6_in_manifest === 1619 && fa23.parent_row_incidence === 11859 && fa23.remaining_s5_orbits === 173, 'second/third-fold frontier crosscheck');
// --- full published verdict join (WIN/LOSS conflict detection before fold) ---
const head = js('head1476'), c78 = js('cost78c'), c79 = js('cost79c'), c73 = js('cost73j'), sweep = js('sweep');
const knownRefuted = new Set(), knownWin = new Set();
for (const x of head.candidate_root_universe.matched_roots) {
  if (x.verdict === 'REFUTED-D10') knownRefuted.add(x.d4_canon_root);
  else if (x.verdict === 'WIN7-D10') knownWin.add(x.d4_canon_root);
}
for (const c of [c78, c79]) {
  for (const x of Object.values(c.transfers || {})) {
    if (x.verdict === 'REFUTED-D10') knownRefuted.add(x.root_canon);
    else if (x.verdict === 'WIN7-D10') knownWin.add(x.root_canon);
  }
  for (const bit of c.actual_execution.refuted_d10_bits || []) knownRefuted.add(canon(BigInt('0x' + c.s6_child) | (1n << BigInt(bit))));
  for (const bit of c.actual_execution.win7_d10_bits || []) knownWin.add(canon(BigInt('0x' + c.s6_child) | (1n << BigInt(bit))));
}
for (const x of Object.values(c73.transfers || {})) {
  if (x.verdict === 'REFUTED-D10') knownRefuted.add(x.root_canon);
  else if (x.verdict === 'WIN7-D10') knownWin.add(x.root_canon);
}
const c73Wins = new Set(c73.actual_execution.results.win7_d10_bits);
for (const bit of c73.engine_candidate_bits.open_bits) {
  const root = canon(BigInt('0x' + c73.s6_child) | (1n << BigInt(bit)));
  if (c73Wins.has(bit)) knownWin.add(root); else knownRefuted.add(root);
}
for (const row of gf.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt('0x' + x.root)));
for (const row of prev.new_receipt_coverage.receipts_by_row) for (const x of row.receipts) knownWin.add(canon(BigInt('0x' + x.root)));
for (const x of prev.new_receipt_coverage.marginal_by_root) knownWin.add(canon(BigInt('0x' + x.root)));
need(sweep.status === 'sweep-complete' && sweep.classification.counted_roots === 48 && sweep.classification.ordering_conflicts.length === 0, 'sweep gate');
for (const r of sweep.classification.refuted_d10.roots) knownRefuted.add(r);
for (const r of sweep.classification.win7_d10.roots) knownWin.add(r);
knownWin.add(canon(BigInt('0x' + firstFold.root.hex)));
for (const r of fold23.receipts) knownWin.add(canon(BigInt('0x' + r.root)));
need(knownRefuted.size === 282 && knownWin.size === 159, 'enumerated published verdict totals (pre-K1035): ' + knownRefuted.size + '/' + knownWin.size);
need(!knownRefuted.has(FOURTH_ROOT), 'WIN/LOSS conflict: fourth root already REFUTED in published verdict sources');
need(!knownWin.has(FOURTH_ROOT), 'fourth root already folded as WIN before this fold');
// --- K1035 witness probes and certificate record ---
const wp = js('witnessProbes');
need(wp.schema === 'n11-residual-28-root-witness-probe-certificate-20261119-v1' && wp.status === 'WIN7-D10-certificate-independently-verified', 'witness probes schema/status');
need(wp.source_main_head_before === '4d47f236f69eea2c1b207142a3082cbc61d7f569', 'witness probes source head');
const wr = wp.root;
need(wr.hex === FOURTH_ROOT && wr.stones === 7 && wr.d4_canonical === true && wr.unsafe_quadruples === 0, 'fourth root geometry');
need(canon(BigInt('0x' + wr.child_hex) | (1n << BigInt(wr.added_bit))) === FOURTH_ROOT, 'child|bit != root');
need(wr.legal_next_moves === 53 && wr.legal_bits.length === 53, 'fourth root mobility');
need(wp.pilot_controls.all_pass === true && wp.pilot_controls.runs === 9 && wp.pilot_controls.each_nodes === 3402, 'pilot controls');
const certRuns = wp.probe_runs.filter(r => r.root === FOURTH_ROOT);
need(certRuns.length === 4, 'fourth root probe runs');
for (const r of certRuns) need(r.classification === 'WIN7-D10', 'unexpected classification on fourth root run');
const winRuns = certRuns.filter(r => r.loss === true && r.capped === false);
need(winRuns.length === 2, 'both orderings must reach an uncapped WIN at the 4M cap');
need(new Set(winRuns.map(r => r.ordering)).size === 2, 'uncapped WIN orderings');
need(!certRuns.some(r => r.loss === false && r.capped === false), 'ordering conflict on the fourth root');
const companionRefuted = [...new Set(wp.probe_runs.filter(r => r.root !== FOURTH_ROOT && r.classification === 'REFUTED-D10').map(r => r.root))].sort();
need(companionRefuted.length === 2, 'probed companion roots');
// --- cover resolve witness plan (K1033) context gates ---
const cr = js('coverResolve');
need(cr.schema === 'n11-five-parent-refuted-excluded-cover-resolve-20261119-v1' && cr.all_pass === true, 'cover resolve schema/pass');
const witnessEntry = cr.witness.find(x => x.root === FOURTH_ROOT);
need(witnessEntry, 'fourth root missing from the 28-root witness plan');
const witnessRowsSorted = [...witnessEntry.rows].sort();
const rootCheck = cr.root_checks.find(x => x.root === FOURTH_ROOT);
need(rootCheck && rootCheck.stones === 7 && rootCheck.d4_canonical === true && rootCheck.unsafe_quadruples === 0, 'cover-resolve root check');
need(JSON.stringify(wr.covered_target_rows) === JSON.stringify(witnessRowsSorted), 'declared target rows mismatch vs cover-resolve witness');
for (const r of companionRefuted) need(cr.witness.some(x => x.root === r), 'probed companion not in witness plan: ' + r);
// --- extraction record gates ---
const ex = wp.extraction;
need(ex.engine_blob_sha1 === P.extractor[1], 'extraction engine pin');
need(ex.completed_moves === 53 && Object.keys(ex.per_move).length === 53 && ex.fbt_drops === 0, 'extraction completion');
for (const m of Object.values(ex.per_move)) need(m.ok === true && m.capped === false, 'per-move extraction failure');
need(ex.total_nodes === 5469581 && ex.unique_strategy_rows === 50941 && ex.terminal_stone_range[0] === 13 && ex.terminal_stone_range[1] === 17, 'extraction totals');
// --- certificate bytes and live independent re-verification in this environment ---
const certGzBytes = read('certGz');
need(sha256(certGzBytes) === CERT_GZ_SHA256, 'certificate gzip sha256');
const certBytes = zlib.gunzipSync(certGzBytes);
need(certBytes.length === CERT_BYTES && sha256(certBytes) === CERT_SHA256, 'certificate expanded sha256/bytes');
const certPathLive = path.join(OUT, 'fourth-win7-certificate-live-20261119.n11');
fs.writeFileSync(certPathLive, certBytes);
const bigintLive = spawnSync('node', [path.join(ROOT, P.bigintVerifier[0]), certPathLive, '53'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
need(bigintLive.status === 0, 'bigint verifier rerun failed: ' + bigintLive.stderr);
const bi = JSON.parse(bigintLive.stdout.trim());
need(bi.verdict === 'WIN7 certificate independently verified' && bi.root_safe === true && bi.root_hex === FOURTH_ROOT, 'bigint rerun verdict');
const pubBi = wp.verification.bigint;
const pubKeyOf = k => (k === 'visited_states_across_subroots' ? 'visited_states' : k);
for (const [k, v] of Object.entries({ root_mobility: 53, strategy_rows: 50941, subroots_passed: 53, consumed_winner_rows: 50941, union_missing: 0, union_extra: 0, visited_states_across_subroots: 101663, winner_states: 65610, loser_states: 20001, loser_reply_edges: 91807, terminal_count: 16052 })) {
  need(pubBi[pubKeyOf(k)] === v, 'published bigint record disagrees on ' + k);
  need(bi[k] === v, 'bigint rerun disagrees with published value on ' + k);
}
need(JSON.stringify(pubBi.terminal_range) === JSON.stringify([13, 17]) && JSON.stringify(bi.terminal_range) === JSON.stringify([13, 17]), 'bigint terminal range');
const bareissRootRun = spawnSync('node', ['--experimental-strip-types', path.join(ROOT, P.bareissVerifier[0]), '--cert', certPathLive, '--root', FOURTH_ROOT, '--root-check'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
need(bareissRootRun.status === 0, 'bareiss root-check rerun failed: ' + bareissRootRun.stderr);
const bareissRootCheck = JSON.parse(bareissRootRun.stdout.trim().split(/\r?\n/)[0]);
need(bareissRootCheck.stones === 7 && bareissRootCheck.loserMobility === 53, 'bareiss root check rerun');
const consumedPathLive = path.join(OUT, 'fourth-win7-bareiss-consumed-live-20261119.txt');
fs.rmSync(consumedPathLive, { force: true });
const bitsArg = wr.legal_bits.join(',');
const bareissSubsRun = spawnSync('node', ['--experimental-strip-types', path.join(ROOT, P.bareissVerifier[0]), '--cert', certPathLive, '--root', FOURTH_ROOT, '--subroots', bitsArg, '--consumed-out', consumedPathLive], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
need(bareissSubsRun.status === 0, 'bareiss subroots rerun failed: ' + bareissSubsRun.stderr);
const subsOut = JSON.parse(bareissSubsRun.stdout.trim().split(/\r?\n/).pop());
const stats = Object.values(subsOut.stats);
const bt = { seen: stats.reduce((s, x) => s + x.seen, 0), terminals: stats.reduce((s, x) => s + x.terminals, 0), opponentEdges: stats.reduce((s, x) => s + x.opponentEdges, 0), terminal_min: Math.min(...stats.map(x => x.range[0])), terminal_max: Math.max(...stats.map(x => x.range[1])) };
const consumed = fs.readFileSync(consumedPathLive, 'utf8').trim().split(/\r?\n/);
const consumedUnique = new Set(consumed);
const certRows = certBytes.toString('utf8').trim().split(/\r?\n/).slice(2).map(l => l.split(' ')[0]);
const certRowSet = new Set(certRows);
let unionMissing = 0, unionExtra = 0;
for (const h of certRowSet) if (!consumedUnique.has(h)) unionMissing++;
for (const h of consumedUnique) if (!certRowSet.has(h)) unionExtra++;
need(subsOut.rows === 50941 && stats.length === 53, 'bareiss rerun rows/subroots');
need(bt.seen === 101663 && bt.terminals === 16052 && bt.opponentEdges === 91807 && bt.terminal_min === 13 && bt.terminal_max === 17, 'bareiss rerun state flow');
need(consumed.length === 65610 && consumedUnique.size === 50941 && unionMissing === 0 && unionExtra === 0, 'bareiss rerun consumed union');
need(bi.visited_states_across_subroots === bt.seen && bi.terminal_count === bt.terminals && bi.loser_reply_edges === bt.opponentEdges, 'cross-method state-flow disagreement (rerun)');
const pubBa = wp.verification.bareiss;
need(wp.verification.cross_method_state_flow_equal === true && wp.verification.certificate_union_exact === true, 'published cross-method gates');
need(pubBa.subroots === 53 && pubBa.rows === 50941 && pubBa.consumed_records === 65610 && pubBa.consumed_unique === 50941 && pubBa.seen === 101663 && pubBa.terminals === 16052 && pubBa.opponent_edges === 91807 && pubBa.union_missing === 0 && pubBa.union_extra === 0, 'published bareiss record gate');
fs.writeFileSync(path.join(OUT, 'fourth-win7-independent-verification-rerun-20261119.json'), JSON.stringify({
  schema: 'n11-fourth-win7-independent-verification-rerun-20261119-v1', date: '2026-11-19',
  root: FOURTH_ROOT, certificate_gzip_sha256: CERT_GZ_SHA256, certificate_sha256: CERT_SHA256, certificate_bytes: certBytes.length,
  engines: { bigint: { path: P.bigintVerifier[0], git_blob_sha1: P.bigintVerifier[1] }, bareiss: { path: P.bareissVerifier[0], git_blob_sha1: P.bareissVerifier[1] } },
  bigint_rerun: bi, bareiss_rerun: { root_check: bareissRootCheck, subroots: stats.length, rows: subsOut.rows, state_flow: bt, consumed_records: consumed.length, consumed_unique: consumedUnique.size, union_missing: unionMissing, union_extra: unionExtra },
  cross_method_state_flow_equal: true, published_values_reproduced: true
}, null, 2) + '\n');
fs.rmSync(certPathLive); fs.rmSync(consumedPathLive, { force: true });
// --- receipt construction over the open frontier ---
const parents = new Map(census.open_s5_census.map(p => [p.hex, p]));
const targetResidual = new Set(cover.receipts.residual_row_hex);
need(targetResidual.size === 97, 'residual target rows');
const rootRows = rootRowSet(FOURTH_ROOT, open2);
need(rootRows.size >= 1, 'fourth root closes no open frontier row');
for (const h of rootRows) need(open2.has(h), 'receipt row was already closed or absent: ' + h);
const targetRows = [...rootRows].filter(h => targetResidual.has(h)).sort();
need(JSON.stringify(targetRows) === JSON.stringify(witnessRowsSorted), 'independent root-to-target-row join mismatch');
const closedCost = [...rootRows].reduce((s, h) => s + open2.get(h).cost, 0);
const before = new Map([...parents.keys()].map(p => [p, 0]));
for (const h of open2.keys()) for (const p of rowParents(h, parents)) before.set(p, before.get(p) + 1);
const after = new Map(before);
for (const h of rootRows) for (const p of rowParents(h, parents)) after.set(p, after.get(p) - 1);
const affectedSet = new Set([...rootRows].flatMap(h => rowParents(h, parents)));
const parentDeltas = [...affectedSet].sort().map(p => ({ parent_hex: p, classes: parents.get(p).classes, rows_before: before.get(p), rows_closed: before.get(p) - after.get(p), rows_after: after.get(p) }));
const receipt = {
  root: FOURTH_ROOT, added_bit: wr.added_bit, child_hex: wr.child_hex, covered_s6_rows: [...rootRows].sort(),
  covered_five_parent_target_rows: targetRows, legal_next_moves: 53,
  total_nodes: ex.total_nodes, unique_strategy_rows: ex.unique_strategy_rows,
  closed_edge_cost: closedCost, parent_deltas: parentDeltas, affected_parents: affectedSet.size,
  probe_runs: certRuns.map(r => ({ ordering: r.ordering, cap: r.cap, loss: r.loss, nodes: r.nodes, capped: r.capped, ms: r.ms })),
  certificate_path: P.certGz[0], certificate_git_blob_sha1: P.certGz[1],
  certificate_gzip_sha256: CERT_GZ_SHA256, certificate_sha256: CERT_SHA256, certificate_bytes: certBytes.length,
  certificate_strategy_rows: certRows.length,
  independent_verification: {
    published: { bigint: wp.verification.bigint, bareiss: wp.verification.bareiss },
    rerun_in_this_environment: { bigint_subroots_passed: bi.subroots_passed, bigint_union_missing: bi.union_missing, bigint_union_extra: bi.union_extra, bareiss_subroots: stats.length, bareiss_state_flow: bt, bareiss_consumed_unique: consumedUnique.size, bareiss_union_missing: unionMissing, bareiss_union_extra: unionExtra, cross_method_state_flow_equal: true }
  }
};
const open3 = new Map([...open2].filter(([h]) => !rootRows.has(h)));
// --- frontier after ---
const remainingParentsCount = new Set([...open3.keys()].flatMap(h => rowParents(h, parents))).size;
let parentIncidence = 0;
{
  const inc = new Map([...parents.keys()].map(p => [p, 0]));
  for (const h of open3.keys()) for (const p of rowParents(h, parents)) inc.set(p, inc.get(p) + 1);
  parentIncidence = [...inc.values()].reduce((s, n) => s + n, 0);
}
function needed(openSet) { let n = 0, c = 0; for (const h of openSet.keys()) if (demand(h, parents, parents).c1 === 0) { n++; c += openSet.get(h).cost; } return { s6_needed_by_open_classes: n, cost_needed_by_open_classes: c }; }
const frontierAfter = {
  solved_s6_in_manifest: fa23.solved_s6_in_manifest + rootRows.size,
  remaining_s5_orbits: remainingParentsCount,
  unique_remaining_s6: open3.size,
  sum_remaining_cost: [...open3.values()].reduce((s, x) => s + x.cost, 0),
  ...needed(open3),
  parent_row_incidence: parentIncidence
};
// --- five-parent target accounting (49-cover framework) ---
const firstTarget = firstFold.root.covered_five_parent_target_rows;
const target23 = fold23.receipts.flatMap(r => r.covered_five_parent_target_rows);
const closedTargetRows = new Set([...firstTarget, ...target23, ...targetRows]);
need(closedTargetRows.size === 8, 'cumulative closed target rows (2+4+2)');
const targetAfter = new Set([...targetResidual].filter(h => !closedTargetRows.has(h)));
need(targetAfter.size === 89, 'residual target rows after the fourth receipt');
// --- 28-root witness plan state after this fold ---
const refutedPlan = new Set(companionRefuted);
const witnessRemaining = cr.witness.filter(x => x.root !== FOURTH_ROOT);
need(witnessRemaining.length === 27, 'remaining witness plan roots');
const witnessRemainingWin = witnessRemaining.filter(x => !refutedPlan.has(x.root));
need(witnessRemainingWin.length === 25, 'untested witness plan roots');
const stillCoverablePlan = new Set(witnessRemainingWin.flatMap(x => x.rows));
for (const h of stillCoverablePlan) need(targetAfter.has(h), 'remaining plan row not in open target set: ' + h);
const planRowProviders = new Map();
for (const x of witnessRemainingWin) for (const h of x.rows) planRowProviders.set(h, (planRowProviders.get(h) || 0) + 1);
const refutedOnlyRows = [];
for (const x of witnessRemaining) if (refutedPlan.has(x.root)) for (const h of x.rows) if (!planRowProviders.has(h) && !stillCoverablePlan.has(h)) refutedOnlyRows.push(h);
const record = {
  schema: 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1',
  date: '2026-11-19', status: 'fold-complete',
  source_main_head_before: 'cc8be6d6dc1df9ef87dd10aae4b9103035e82754',
  previous_fold: { path: P.fold23[0], git_blob_sha1: P.fold23[1], frontier_after: fa23 },
  source_blob_pins: Object.fromEntries(Object.entries(P).map(([k, v]) => [k, v[1]])),
  receipt_count: 1, receipts: [receipt],
  new_receipt_coverage: {
    unique_s6_rows: [...rootRows].length,
    closed_edge_cost: closedCost,
    rows: [...rootRows].sort().map(h => ({ row_hex: h, cost: open2.get(h).cost, category: open2.get(h).category, demand: demand(h, parents, parents), parents: rowParents(h, parents), receipt: { root: FOURTH_ROOT, verdict: 'WIN7-D10', certificate_sha256: CERT_SHA256 } }))
  },
  parent_closure: {
    fully_closed_parent_count: parentDeltas.filter(p => p.rows_after === 0).length,
    affected_unique_parents: affectedSet.size
  },
  frontier_before: fa23, frontier_after: frontierAfter,
  five_parent_target_after: {
    framework: '49-cover residual framework (97 rows at the first-fold head)',
    closed_target_rows_total: closedTargetRows.size,
    residual_target_rows: targetAfter.size
  },
  witness_plan_after: {
    framework: 'refuted-excluded 63-candidate 28-root witness plan (K1033)',
    planned_cover_rows: cr.resolve.covered_rows,
    folded_win_roots: [FOURTH_ROOT],
    refuted_probed_roots: companionRefuted,
    refuted_probed_rows_now_needing_alternatives: [...new Set(witnessRemaining.filter(x => refutedPlan.has(x.root)).flatMap(x => x.rows))].sort(),
    untested_roots: witnessRemainingWin.map(x => x.root),
    untested_root_count: witnessRemainingWin.length,
    rows_still_coverable_by_untested_plan: stillCoverablePlan.size,
    residual_target_rows_after_fold: targetAfter.size,
    note: 'untested roots are candidate plan entries, not certificates; REFUTED-D10 is not a LOSS proof; rows of the two refuted roots need alternative candidates (see the post-fold cover re-solve) or deeper evidence.'
  },
  verdict_join_summary: {
    known_refuted_roots_pre_k1035: knownRefuted.size, known_win_roots_pre_k1035: knownWin.size,
    join_limitation: 'explicit pinned sources only (head1476/cost78c/79c/73j transfers, global fold, cost78c/79c receipts, 48-root sweep, first/second/third receipt folds); not the full 8,964-entry cache join',
    win_loss_conflicts: 0
  },
  controls: {
    base_frontier_recomputed: true, first_fold_frontier_chained: true, second_third_fold_frontier_chained: true,
    receipt_rows_rederived_from_all_8_d4_images: true,
    receipt_target_rows_match_cover_resolve_witness: true,
    all_receipt_rows_were_open_before_this_receipt: true,
    live_bigint_verification_rerun: true, live_bareiss_verification_rerun: true,
    cross_method_state_flow_agreement_rerun: true,
    published_verification_values_reproduced: true,
    win_loss_conflict_scan_against_published_verdict_universe: true
  },
  interpretation_guard: [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone root of this receipt.',
    'The receipt closes its S6 rows in the frontier but proves nothing about the empty board or any two-stone root.',
    'The two companion witness roots probed REFUTED-D10 are NOT LOSS proofs; they only bound first-player wins within depth 10 from those exact roots.',
    'The 25 untested witness roots are a conditional plan, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
};
fs.writeFileSync(path.join(OUT, 'fourth-win7-root-receipt-fold-20261119.json'), JSON.stringify(record, null, 2) + '\n');
console.log(JSON.stringify({ status: record.status, closed_unique_s6_rows: rootRows.size, closed_edge_cost: closedCost, closed_target_rows: targetRows, frontier_after: frontierAfter, residual_target_rows: targetAfter.size, untested_witness_roots: witnessRemainingWin.length, rows_still_coverable_by_untested_plan: stillCoverablePlan.size }, null, 2));
