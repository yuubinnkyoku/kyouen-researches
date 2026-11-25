// Receipt fold for the fifth and sixth residual WIN7-D10 roots
// (00000000000000805202080001000000 and 00000000040000801202000080100000,
// K1036 witness lane certificates, plain .n11 text published on main).
// Chains on the published fourth receipt fold (K1038) exactly as the fourth
// fold chained on the first/second/third receipt folds. All gates are recomputed
// from the pinned inputs. Before any receipt is written, the full published
// verdict universe (head1476 + cost78c/79c/73j transfers + global fold +
// cost78c/79c receipts + 48-root sweep + first/second/third/fourth receipt
// folds) is re-derived and crosschecked against the K1038 post-fourth-receipt
// cover re-solve so a WIN/LOSS conflict for the fifth/sixth roots is detected
// instead of silently folded. Both certificates are re-verified live in this
// environment with both pinned independent verifiers (BigInt 3x3 cofactor and
// 4x4 Bareiss) and the state-flow totals are compared to the K1036 published
// values (per-root verification JSON, bareiss union audits, and summary).
// Usage: node fold_fifth_sixth_win7_receipts_20261119.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const EXP_DIR = path.resolve(SCRIPT_DIR, '..');
const OUT = path.join(EXP_DIR, 'output');
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const gitBlobSha = b => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
function need(ok, m) { if (!ok) throw new Error(m); }
const SPECS = [
  {
    name: 'fifth', root: '00000000000000805202080001000000', child: '00000000000000005202080001000000', added_bit: 71,
    mobility: 54, rows: 55857, total_nodes: 5121073, fbt_drops: 0,
    cert_sha256: '69589e76e5d2e5f22e6992929f38d9fd67f07ce1bd9fe9e3f971d32bdd635a49', cert_bytes: 2017673,
    pub: {
      subroots_passed: 54, consumed_winner_rows: 55857, visited_states_across_subroots: 127080,
      winner_states: 82983, loser_states: 27927, loser_reply_edges: 124176, terminal_count: 16170
    },
    pubBareiss: { certificate_rows: 55857, consumed_records: 82983, consumed_unique: 55857, missing: 0, extra: 0 },
    pins: {
      cert: 'cert5', verif: 'verif5', audit: 'audit5'
    }
  },
  {
    name: 'sixth', root: '00000000040000801202000080100000', child: '00000000000000801202000080100000', added_bit: 90,
    mobility: 55, rows: 30984, total_nodes: 931581, fbt_drops: 0,
    cert_sha256: '5289f152e88072d716f22d42414222162facb7486d07fd024b61fdc50ddef885', cert_bytes: 1117575,
    pub: {
      subroots_passed: 55, consumed_winner_rows: 30984, visited_states_across_subroots: 66292,
      winner_states: 42537, loser_states: 12850, loser_reply_edges: 59089, terminal_count: 10905
    },
    pubBareiss: { certificate_rows: 30984, consumed_records: 42537, consumed_unique: 30984, missing: 0, extra: 0 },
    pins: {
      cert: 'cert6', verif: 'verif6', audit: 'audit6'
    }
  }
];
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
  fold4: ['research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-root-receipt-fold-20261119.json', '38715413d6dd23b97717c92d73d8b4a0af807cda'],
  refold4: ['research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/refuted-excluded-cover-refold-after-fourth-receipt-20261119.json', '791e6be736d7802497df6c1e3a4df81d5ec2d8fe'],
  summary56: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/fifth-sixth-witness-win7-certificates-summary-20261119.json', '9e71ab4e6e7d8e16fb1ca89e9e0c0b08a53190b9'],
  legal56: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/witness-win-roots-legal-move-lists-20261119.json', 'b5b8fb2dec81fc7e648f4d8d10ebb7989af15c36'],
  cert5: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-20261119.n11', 'b072170a0557ee15622c9f8dd94ec0fa81c65e18'],
  verif5: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-independent-verification-20261119.json', '433e59f172b4ccdc2a6246b90a4732243af58f3b'],
  audit5: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000000000805202080001000000-bareiss-union-audit-20261119.json', '3e5bcc808a6f0fd0295a7c79927e0dec450ee29f'],
  cert6: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-20261119.n11', '02ea43b389327ea68c54249017a236d2a93360a0'],
  verif6: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-independent-verification-20261119.json', 'f9819aa373a968bd86d2683ffcb40bf3de547363'],
  audit6: ['research/experiments/n11-head1410-fifth-sixth-witness-win7-certificates-20261119/output/win7-root-00000000040000801202000080100000-bareiss-union-audit-20261119.json', '564e8201cc5f02634637a8463846b0741004474e'],
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
// --- frontier reconstruction (base .. first fold .. second/third fold .. fourth fold) ---
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
const zlib = await import('node:zlib');
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
// --- fourth fold chain (K1038, published at d3a6e69f) ---
const fold4 = js('fold4');
need(fold4.status === 'fold-complete' && fold4.schema === 'n11-five-parent-fourth-win7-receipt-fold-20261119-v1', 'fourth fold schema');
const fold4Rows = fold4.new_receipt_coverage.rows.map(x => x.row_hex);
need(fold4Rows.length === 3 && new Set(fold4Rows).size === 3, 'fourth fold closed rows');
const open3 = new Map([...open2].filter(([h]) => !fold4Rows.includes(h)));
need(open3.size === 6226 && [...open3.values()].reduce((s, x) => s + x.cost, 0) === 492970, 'fourth-fold frontier');
const fa4 = fold4.frontier_after;
need(fa4.unique_remaining_s6 === 6226 && fa4.sum_remaining_cost === 492970 && fa4.solved_s6_in_manifest === 1622 && fa4.parent_row_incidence === 11855 && fa4.remaining_s5_orbits === 173, 'fourth-fold frontier crosscheck');
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
// --- extend with the fourth fold's WIN receipt and its two probed REFUTED companions ---
const FOURTH_ROOT = fold4.receipts[0].root;
need(FOURTH_ROOT === '00000000000000801202060001000000', 'fourth root hex inside fold4 record');
knownWin.add(canon(BigInt('0x' + FOURTH_ROOT)));
for (const r of fold4.witness_plan_after.refuted_probed_roots) knownRefuted.add(r);
need(knownRefuted.size === 284 && knownWin.size === 160, 'post-K1035 published verdict universe: ' + knownRefuted.size + '/' + knownWin.size);
// --- crosscheck against the K1038 post-fourth-receipt cover re-solve ---
const refold4 = js('refold4');
need(refold4.status === 'partial-candidate-cover-with-stranded-rows' && refold4.all_pass === true, 'refold4 schema/pass');
need(refold4.verdict_pool.known_refuted_roots === 284 && refold4.verdict_pool.known_win_roots === 160, 'verdict universe crosscheck vs refold4');
need(refold4.target.parents === 5 && refold4.target.rows === 112, 'refold4 target framework');
const refold4Residual = 112 - 23;
need(refold4Residual === 89, 'refold4 residual arithmetic');
for (const s of SPECS) {
  need(!knownRefuted.has(s.root), 'WIN/LOSS conflict: ' + s.name + ' root already REFUTED in published verdict sources');
  need(!knownWin.has(s.root), s.name + ' root already folded as WIN before this fold');
}
// --- K1036 witness lane records gates ---
const summary56 = js('summary56');
need(summary56.schema === 'n11-fifth-sixth-witness-win7-certificates-20261119-v1', 'summary56 schema');
need(summary56.source_main === 'cc8be6d6dc1df9ef87dd10aae4b9103035e82754', 'summary56 source head');
const legal56 = js('legal56');
const cr = js('coverResolve');
need(cr.schema === 'n11-five-parent-refuted-excluded-cover-resolve-20261119-v1' && cr.all_pass === true, 'cover resolve schema/pass');
for (const s of SPECS) {
  const rec = summary56.roots.find(x => x.name === s.name);
  need(rec && rec.root === s.root, 'summary56 root record ' + s.name);
  need(rec.child === s.child && rec.added_bit === s.added_bit, 'summary56 child/bit ' + s.name);
  need(rec.legal_next_moves === s.mobility && rec.completed_moves === s.mobility, 'summary56 moves ' + s.name);
  need(rec.strategy_rows === s.rows && rec.total_nodes === s.total_nodes && rec.fbt_drops === s.fbt_drops, 'summary56 extraction totals ' + s.name);
  need(JSON.stringify(rec.terminal_stone_range) === JSON.stringify([13, 17]), 'summary56 terminal range ' + s.name);
  need(rec.certificate_sha256 === s.cert_sha256 && rec.certificate_bytes === s.cert_bytes, 'summary56 certificate fingerprint ' + s.name);
  need(canon(BigInt('0x' + s.child) | (1n << BigInt(s.added_bit))) === s.root, 'child|bit != root (' + s.name + ')');
  const L = legal56[s.root];
  need(L && L.expected_count === s.mobility && L.legal.length === s.mobility, 'legal move list ' + s.name);
  const rc = cr.root_checks.find(x => x.root === s.root);
  need(rc && rc.stones === 7 && rc.d4_canonical === true && rc.unsafe_quadruples === 0, 'cover-resolve root check ' + s.name);
  const pl = cr.witness.find(x => x.root === s.root);
  need(pl, s.name + ' root missing from the 28-root witness plan');
  s.legalBits = L.legal;
  s.planRows = [...pl.rows].sort();
}
// --- live independent re-verification of both certificates in this environment ---
function liveVerify(s) {
  const certBytes = read(s.pins.cert);
  need(certBytes.length === s.cert_bytes && sha256(certBytes) === s.cert_sha256, 'certificate bytes/sha256 ' + s.name);
  const certPathLive = path.join(OUT, s.name + '-win7-certificate-live-20261119.n11');
  fs.writeFileSync(certPathLive, certBytes);
  const bigintLive = spawnSync('node', [path.join(ROOT, P.bigintVerifier[0]), certPathLive, String(s.mobility)], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  need(bigintLive.status === 0, 'bigint verifier rerun failed (' + s.name + '): ' + bigintLive.stderr);
  const bi = JSON.parse(bigintLive.stdout.trim());
  need(bi.verdict === 'WIN7 certificate independently verified' && bi.root_safe === true && bi.root_hex === s.root, 'bigint rerun verdict ' + s.name);
  need(bi.root_mobility === s.mobility && bi.strategy_rows === s.rows && bi.rows_sorted_unique === true, 'bigint rerun mobility/rows ' + s.name);
  for (const [k, v] of Object.entries(s.pub)) need(bi[k] === v, 'bigint rerun disagrees on ' + k + ' (' + s.name + '): ' + bi[k]);
  need(JSON.stringify(bi.terminal_range) === JSON.stringify([13, 17]), 'bigint rerun terminal range ' + s.name);
  const pubVerif = js(s.pins.verif);
  need(pubVerif.verdict === 'WIN7 certificate independently verified' && pubVerif.root_hex === s.root && pubVerif.root_safe === true, 'published per-root verification record ' + s.name);
  for (const [k, v] of Object.entries(s.pub)) need(pubVerif[k] === v, 'published bigint record disagrees on ' + k + ' (' + s.name + ')');
  need(pubVerif.strategy_rows === s.rows && pubVerif.subroots_passed === s.mobility && pubVerif.consumed_winner_rows === s.rows && pubVerif.union_missing === 0 && pubVerif.union_extra === 0, 'published bigint record totals ' + s.name);
  const pubSummary = summary56.verification[s.name];
  need(pubSummary.root_safe === true && pubSummary.root_mobility === s.mobility && pubSummary.bigint_subroots_passed === s.pub.subroots_passed && pubSummary.visited_states_across_subroots === s.pub.visited_states_across_subroots && pubSummary.terminal_count === s.pub.terminal_count && pubSummary.loser_reply_edges === s.pub.loser_reply_edges && pubSummary.bigint_union_missing === 0 && pubSummary.bigint_union_extra === 0, 'summary56 verification crosscheck ' + s.name);
  const bareissRootRun = spawnSync('node', ['--experimental-strip-types', path.join(ROOT, P.bareissVerifier[0]), '--cert', certPathLive, '--root', s.root, '--root-check'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  need(bareissRootRun.status === 0, 'bareiss root-check rerun failed (' + s.name + '): ' + bareissRootRun.stderr);
  const bareissRootCheck = JSON.parse(bareissRootRun.stdout.trim().split(/\r?\n/)[0]);
  need(bareissRootCheck.stones === 7 && bareissRootCheck.loserMobility === s.mobility, 'bareiss root check rerun ' + s.name);
  const consumedPathLive = path.join(OUT, s.name + '-win7-bareiss-consumed-live-20261119.txt');
  fs.rmSync(consumedPathLive, { force: true });
  const bareissSubsRun = spawnSync('node', ['--experimental-strip-types', path.join(ROOT, P.bareissVerifier[0]), '--cert', certPathLive, '--root', s.root, '--subroots', s.legalBits.join(','), '--consumed-out', consumedPathLive], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  need(bareissSubsRun.status === 0, 'bareiss subroots rerun failed (' + s.name + '): ' + bareissSubsRun.stderr);
  const subsOut = JSON.parse(bareissSubsRun.stdout.trim().split(/\r?\n/).pop());
  const stats = Object.values(subsOut.stats);
  const bt = { seen: stats.reduce((sx, x) => sx + x.seen, 0), terminals: stats.reduce((sx, x) => sx + x.terminals, 0), opponentEdges: stats.reduce((sx, x) => sx + x.opponentEdges, 0), terminal_min: Math.min(...stats.map(x => x.range[0])), terminal_max: Math.max(...stats.map(x => x.range[1])) };
  const consumed = fs.readFileSync(consumedPathLive, 'utf8').trim().split(/\r?\n/);
  const consumedUnique = new Set(consumed);
  const certRows = certBytes.toString('utf8').trim().split(/\r?\n/).slice(2).map(l => l.split(' ')[0]);
  const certRowSet = new Set(certRows);
  let unionMissing = 0, unionExtra = 0;
  for (const h of certRowSet) if (!consumedUnique.has(h)) unionMissing++;
  for (const h of consumedUnique) if (!certRowSet.has(h)) unionExtra++;
  need(subsOut.rows === s.rows && stats.length === s.mobility, 'bareiss rerun rows/subroots ' + s.name);
  need(bt.seen === s.pub.visited_states_across_subroots && bt.terminals === s.pub.terminal_count && bt.opponentEdges === s.pub.loser_reply_edges && bt.terminal_min === 13 && bt.terminal_max === 17, 'bareiss rerun state flow ' + s.name);
  need(consumed.length === s.pub.winner_states && consumedUnique.size === s.rows && unionMissing === 0 && unionExtra === 0, 'bareiss rerun consumed union ' + s.name);
  need(bi.visited_states_across_subroots === bt.seen && bi.terminal_count === bt.terminals && bi.loser_reply_edges === bt.opponentEdges, 'cross-method state-flow disagreement (' + s.name + ')');
  const pubAudit = js(s.pins.audit);
  need(pubAudit.certificate_rows === s.pubBareiss.certificate_rows && pubAudit.consumed_records === s.pubBareiss.consumed_records && pubAudit.consumed_unique === s.pubBareiss.consumed_unique && pubAudit.missing === 0 && pubAudit.extra === 0 && pubAudit.exact_union === true, 'published bareiss union audit ' + s.name);
  need(pubAudit.consumed_records === consumed.length && pubAudit.consumed_unique === consumedUnique.size, 'published bareiss audit vs live rerun ' + s.name);
  fs.writeFileSync(path.join(OUT, s.name + '-win7-independent-verification-rerun-20261119.json'), JSON.stringify({
    schema: 'n11-' + s.name + '-win7-independent-verification-rerun-20261119-v1', date: '2026-11-19',
    root: s.root, certificate_sha256: s.cert_sha256, certificate_bytes: certBytes.length,
    engines: { bigint: { path: P.bigintVerifier[0], git_blob_sha1: P.bigintVerifier[1] }, bareiss: { path: P.bareissVerifier[0], git_blob_sha1: P.bareissVerifier[1] } },
    bigint_rerun: bi, bareiss_rerun: { root_check: bareissRootCheck, subroots: stats.length, rows: subsOut.rows, state_flow: bt, consumed_records: consumed.length, consumed_unique: consumedUnique.size, union_missing: unionMissing, union_extra: unionExtra },
    cross_method_state_flow_equal: true, published_values_reproduced: true
  }, null, 2) + '\n');
  fs.rmSync(certPathLive); fs.rmSync(consumedPathLive, { force: true });
  return { bi, bt, consumedRecords: consumed.length, consumedUnique: consumedUnique.size, unionMissing, unionExtra, certRows: certRows.length };
}
const live5 = liveVerify(SPECS[0]);
const live6 = liveVerify(SPECS[1]);
// --- receipt construction over the open frontier ---
const parents = new Map(census.open_s5_census.map(p => [p.hex, p]));
const targetResidual = new Set(cover.receipts.residual_row_hex);
need(targetResidual.size === 97, 'residual target rows');
function buildReceipt(s, chest, live) {
  const rootRows = rootRowSet(s.root, chest);
  need(rootRows.size >= 1, s.name + ' root closes no open frontier row');
  for (const h of rootRows) need(chest.has(h), 'receipt row was already closed or absent: ' + h);
  const targetRows = [...rootRows].filter(h => targetResidual.has(h)).sort();
  need(JSON.stringify(targetRows) === JSON.stringify(s.planRows), 'independent root-to-target-row join mismatch (' + s.name + ')');
  const closedCost = [...rootRows].reduce((sxx, h) => sxx + chest.get(h).cost, 0);
  const before = new Map([...parents.keys()].map(p => [p, 0]));
  for (const h of chest.keys()) for (const p of rowParents(h, parents)) before.set(p, before.get(p) + 1);
  const after = new Map(before);
  for (const h of rootRows) for (const p of rowParents(h, parents)) after.set(p, after.get(p) - 1);
  const affectedSet = new Set([...rootRows].flatMap(h => rowParents(h, parents)));
  const parentDeltas = [...affectedSet].sort().map(p => ({ parent_hex: p, classes: parents.get(p).classes, rows_before: before.get(p), rows_closed: before.get(p) - after.get(p), rows_after: after.get(p) }));
  return { rootRows, targetRows, closedCost, parentDeltas, affectedSet, receipt: {
    root: s.root, added_bit: s.added_bit, child_hex: s.child, covered_s6_rows: [...rootRows].sort(),
    covered_five_parent_target_rows: targetRows, legal_next_moves: s.mobility,
    total_nodes: s.total_nodes, unique_strategy_rows: s.rows, fbt_drops: s.fbt_drops,
    closed_edge_cost: closedCost, parent_deltas: parentDeltas, affected_parents: affectedSet.size,
    certificate_path: P[s.pins.cert][0], certificate_git_blob_sha1: P[s.pins.cert][1],
    certificate_sha256: s.cert_sha256, certificate_bytes: s.cert_bytes,
    certificate_strategy_rows: live.certRows,
    independent_verification: {
      published: { per_root_record: P[s.pins.verif][0], per_root_git_blob_sha1: P[s.pins.verif][1], bareiss_union_audit_git_blob_sha1: P[s.pins.audit][1], summary_git_blob_sha1: P.summary56[1] },
      rerun_in_this_environment: { bigint_subroots_passed: live.bi.subroots_passed, bigint_union_missing: live.bi.union_missing, bigint_union_extra: live.bi.union_extra, bareiss_subroots: s.mobility, bareiss_state_flow: live.bt, bareiss_consumed_unique: live.consumedUnique, bareiss_union_missing: live.unionMissing, bareiss_union_extra: live.unionExtra, cross_method_state_flow_equal: true, published_values_reproduced: true }
    }
  } };
}
const r5 = buildReceipt(SPECS[0], open3, live5);
const open4 = new Map([...open3].filter(([h]) => !r5.rootRows.has(h)));
const r6 = buildReceipt(SPECS[1], open4, live6);
const open5 = new Map([...open4].filter(([h]) => !r6.rootRows.has(h)));
// --- frontier after each receipt ---
function frontierAfter(chest, solvedBefore, solvedDelta) {
  const remainingParentsCount = new Set([...chest.keys()].flatMap(h => rowParents(h, parents))).size;
  let parentIncidence = 0;
  {
    const inc = new Map([...parents.keys()].map(p => [p, 0]));
    for (const h of chest.keys()) for (const p of rowParents(h, parents)) inc.set(p, inc.get(p) + 1);
    parentIncidence = [...inc.values()].reduce((x, n) => x + n, 0);
  }
  const neededRows = { s6_needed_by_open_classes: 0, cost_needed_by_open_classes: 0 };
  for (const [h, x] of chest) if (demand(h, parents, parents).c1 === 0) { neededRows.s6_needed_by_open_classes++; neededRows.cost_needed_by_open_classes += x.cost; }
  return {
    solved_s6_in_manifest: solvedBefore + solvedDelta,
    remaining_s5_orbits: remainingParentsCount,
    unique_remaining_s6: chest.size,
    sum_remaining_cost: [...chest.values()].reduce((x, y) => x + y.cost, 0),
    ...neededRows,
    parent_row_incidence: parentIncidence
  };
}
const frontierAfter5 = frontierAfter(open4, fa4.solved_s6_in_manifest, r5.rootRows.size);
const frontierAfter6 = frontierAfter(open5, frontierAfter5.solved_s6_in_manifest, r6.rootRows.size);
// --- five-parent target accounting (49-cover framework) ---
const firstTarget = firstFold.root.covered_five_parent_target_rows;
const target23 = fold23.receipts.flatMap(r => r.covered_five_parent_target_rows);
const target4 = fold4.receipts[0].covered_five_parent_target_rows;
const closedTargetRows = new Set([...firstTarget, ...target23, ...target4, ...r5.targetRows, ...r6.targetRows]);
need(closedTargetRows.size === 10, 'cumulative closed target rows (2+4+2+1+1): ' + closedTargetRows.size);
const targetAfter5 = new Set([...targetResidual].filter(h => !new Set([...firstTarget, ...target23, ...target4, ...r5.targetRows]).has(h)));
const targetAfter = new Set([...targetResidual].filter(h => !closedTargetRows.has(h)));
need(targetAfter5.size === 88 && targetAfter.size === 87, 'residual target rows after the fifth/sixth receipts');
// --- 28-root witness plan state after these folds (K1033 framework) ---
const refutedPlan = new Set(fold4.witness_plan_after.refuted_probed_roots);
const foldedWins = [firstFold.root.hex, ...fold23.receipts.map(r => r.root), FOURTH_ROOT, SPECS[0].root, SPECS[1].root];
const witnessRemaining = cr.witness.filter(x => !foldedWins.includes(x.root) && !refutedPlan.has(x.root));
need(witnessRemaining.length === 23, 'remaining untested witness plan roots: ' + witnessRemaining.length);
const stillCoverablePlan = new Set(witnessRemaining.flatMap(x => x.rows));
for (const h of stillCoverablePlan) need(targetAfter.has(h), 'remaining plan row not in open target set: ' + h);
const planRowProviders = new Map();
for (const x of witnessRemaining) for (const h of x.rows) planRowProviders.set(h, (planRowProviders.get(h) || 0) + 1);
// --- record ---
const rows5 = [...r5.rootRows].sort().map(h => ({ row_hex: h, cost: open3.get(h).cost, category: open3.get(h).category, demand: demand(h, parents, parents), parents: rowParents(h, parents), receipt: { root: SPECS[0].root, verdict: 'WIN7-D10', certificate_sha256: SPECS[0].cert_sha256 } }));
const rows6 = [...r6.rootRows].sort().map(h => ({ row_hex: h, cost: open4.get(h).cost, category: open4.get(h).category, demand: demand(h, parents, parents), parents: rowParents(h, parents), receipt: { root: SPECS[1].root, verdict: 'WIN7-D10', certificate_sha256: SPECS[1].cert_sha256 } }));
const record = {
  schema: 'n11-five-parent-fifth-sixth-win7-receipt-fold-20261119-v1',
  date: '2026-11-19', status: 'fold-complete',
  source_main_head_before: 'd3a6e69fee8ce7873e21499e0dac999313b97b1e',
  previous_fold: { path: P.fold4[0], git_blob_sha1: P.fold4[1], frontier_after: fa4 },
  source_blob_pins: Object.fromEntries(Object.entries(P).map(([k, v]) => [k, v[1]])),
  receipt_count: 2, receipts: [r5.receipt, r6.receipt],
  new_receipt_coverage: {
    unique_s6_rows: rows5.length + rows6.length,
    closed_edge_cost: r5.closedCost + r6.closedCost,
    rows: [...rows5, ...rows6]
  },
  parent_closure: {
    fully_closed_parent_count: [...new Set([...r5.parentDeltas, ...r6.parentDeltas].filter(p => p.rows_after === 0).map(p => p.parent_hex))].length,
    affected_unique_parents: new Set([...r5.affectedSet, ...r6.affectedSet]).size
  },
  frontier_before: fa4, frontier_after: frontierAfter6,
  five_parent_target_after: {
    framework: '49-cover residual framework (97 rows at the first-fold head)',
    closed_target_rows_total: closedTargetRows.size,
    residual_target_rows: targetAfter.size
  },
  witness_plan_after: {
    framework: 'refuted-excluded 63-candidate 28-root witness plan (K1033)',
    planned_cover_rows: cr.resolve.covered_rows,
    folded_win_roots: foldedWins,
    refuted_probed_roots: [...refutedPlan].sort(),
    untested_roots: witnessRemaining.map(x => x.root),
    untested_root_count: witnessRemaining.length,
    rows_still_coverable_by_untested_plan: stillCoverablePlan.size,
    residual_target_rows_after_fold: targetAfter.size,
    note: 'untested roots are candidate plan entries, not certificates; REFUTED-D10 is not a LOSS proof.'
  },
  verdict_join_summary: {
    known_refuted_roots_pre_fold: knownRefuted.size, known_win_roots_pre_fold: knownWin.size,
    join_limitation: 'explicit pinned sources only (head1476/cost78c/79c/73j transfers, global fold, cost78c/79c receipts, 48-root sweep, first/second/third/fourth receipt folds); crosschecked against the K1038 refold verdict_pool (284/160); not the full 8,964-entry cache join',
    win_loss_conflicts: 0
  },
  controls: {
    base_frontier_recomputed: true, first_fold_frontier_chained: true, second_third_fold_frontier_chained: true, fourth_fold_frontier_chained: true,
    verdict_universe_crosschecked_against_k1038_refold: true,
    receipt_rows_rederived_from_all_8_d4_images: true,
    receipt_target_rows_match_cover_resolve_witness: true,
    all_receipt_rows_were_open_before_their_receipt: true,
    live_bigint_verification_rerun_both: true, live_bareiss_verification_rerun_both: true,
    cross_method_state_flow_agreement_rerun_both: true,
    published_verification_values_reproduced_both: true,
    win_loss_conflict_scan_against_published_verdict_universe: true
  },
  interpretation_guard: [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
    'The receipts close their S6 rows in the frontier but prove nothing about the empty board or any two-stone root.',
    'REFUTED-D10 verdicts referenced by the join are NOT LOSS proofs; they only bound first-player wins within depth 10 from those exact roots.',
    'The 23 untested witness roots are a conditional plan, not certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
};
fs.writeFileSync(path.join(OUT, 'fifth-sixth-win7-root-receipt-fold-20261119.json'), JSON.stringify(record, null, 2) + '\n');
console.log(JSON.stringify({
  status: record.status,
  fifth_closed_rows: [...r5.rootRows].sort(), fifth_target_rows: r5.targetRows,
  sixth_closed_rows: [...r6.rootRows].sort(), sixth_target_rows: r6.targetRows,
  closed_edge_cost: record.new_receipt_coverage.closed_edge_cost,
  frontier_after_5: frontierAfter5, frontier_after_6: frontierAfter6,
  residual_target_rows: targetAfter.size, untested_witness_roots: witnessRemaining.length,
  rows_still_coverable_by_untested_plan: stillCoverablePlan.size
}, null, 2));
