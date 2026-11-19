// Receipt fold for the second and third residual WIN7-D10 roots
// (00000000000000821082000000042000 and 00000000000000821082000000420000).
// Chains on the published first receipt fold (extracted from the pinned evidence
// tarball) exactly as fold_first_win7_root_receipt_20261119.mjs chained on the
// cost78c/79c fold. All gates are recomputed from the pinned inputs; certificate
// SHAs are pinned against the extraction summaries at runtime.
// Usage: node fold_second_third_win7_receipts_20261119.mjs
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const EXP_DIR = path.resolve(SCRIPT_DIR, '..');
const OUT = path.join(EXP_DIR, 'output');
const ROOT = path.resolve(SCRIPT_DIR, '../../../..');
const D = SCRIPT_DIR + path.sep;
const gitBlobSha = b => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob ' + b.length), Buffer.from([0]), b])).digest('hex');
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
function need(ok, m) { if (!ok) throw new Error(m); }
const P = {
  worklist: ['research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv', '2fee1d0718547a62e346d35f5858d7913e37c097'],
  ledger: ['research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json', 'e8785d509e8a11a37c0d03cc450455a14708c34d'],
  census: ['research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json', '9c251da3138c5cb0516e097be5e5d0427dfaf5f0'],
  globalFold: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json', '753a4bf4d0e11bea894111f9fa43bcff5e9ab7dc'],
  previousCostFold: ['research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json', '7e6144cc4bc92c34faa14bed3058cde64fb3880e'],
  firstFoldTarball: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz', 'fa5f26a9dc9bd2fb8222aa8ba0431d7578043019'],
  cover: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json', 'a8eaf00bd6494eda50a68e7d06498bed833a7688'],
  mobility: ['research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json', 'b35d54a0ced182153802247452a593096a0acf81'],
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
// --- tarball extraction of the previous (first) receipt fold ---
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
const ledger = js('ledger'), census = js('census'), gf = js('globalFold'), prev = js('previousCostFold');
const cover = js('cover'), mobility = js('mobility');
// --- frontier reconstruction ---
const csv = read('worklist').toString('utf8').trim().split(/\r?\n/), cols = csv[0].split(',');
const ix = cols.indexOf('s6_canonical_hex'), cx = cols.indexOf('own_candidates_s6_s7_edge_cost'), kx = cols.indexOf('category');
need(ix >= 0 && cx >= 0 && kx >= 0, 'worklist header');
const work = new Map();
for (const line of csv.slice(1)) { const a = line.split(','); work.set(a[ix], {cost: Number(a[cx]), category: a[kx]}); }
const old66 = new Set(ledger.derived.closed_rows_66), oldGlobal = new Set(gf.receipts_by_row.map(x => x.row_hex));
const open0 = new Map([...work].filter(([h]) => !old66.has(h) && !oldGlobal.has(h)));
need(open0.size === 6259 && [...open0.values()].reduce((s, x) => s + x.cost, 0) === 495507, 'global-fold base frontier');
const priorReceiptRows = new Set(prev.new_receipt_coverage.receipts_by_row.map(x => x.row_hex));
const open = new Map([...open0].filter(([h]) => !priorReceiptRows.has(h)));
need(open.size === 6240 && [...open.values()].reduce((s, x) => s + x.cost, 0) === 493965, 'cost78c/79c fold frontier');
const firstClosedRows = firstFold.new_receipt_coverage.rows.map(x => x.row_hex);
need(firstClosedRows.length === 4 && new Set(firstClosedRows).size === 4, 'first fold closed rows');
const open1 = new Map([...open].filter(([h]) => !firstClosedRows.includes(h)));
need(open1.size === 6236 && [...open1.values()].reduce((s, x) => s + x.cost, 0) === 493703, 'first-fold frontier');
const fa = firstFold.frontier_after;
need(fa.unique_remaining_s6 === 6236 && fa.sum_remaining_cost === 493703 && fa.solved_s6_in_manifest === 1612 && fa.parent_row_incidence === 11876, 'first-fold frontier crosscheck');
// --- census/parent machinery (as in the first fold) ---
const parents = new Map(census.open_s5_census.map(p => [p.hex, p]));
const tf = [(x, y) => [x, y], (x, y) => [y, 10 - x], (x, y) => [10 - x, 10 - y], (x, y) => [10 - y, x], (x, y) => [10 - x, y], (x, y) => [x, 10 - y], (x, y) => [y, x], (x, y) => [10 - y, 10 - x]];
function d4(m, t) { let z = 0n; for (let p = 0; p < 121; p++) if ((m >> BigInt(p)) & 1n) { const [x, y] = tf[t](p % 11, Math.floor(p / 11)); z |= 1n << BigInt(11 * y + x); } return z; }
function canon(m) { let b = null; for (let t = 0; t < 8; t++) { const z = d4(m, t); if (b === null || z < b) b = z; } return b.toString(16).padStart(32, '0'); }
function rowParents(h) { const m = BigInt('0x' + h), ps = new Set(); for (let q = 0; q < 121; q++) if ((m >> BigInt(q)) & 1n) { const p = canon(m ^ (1n << BigInt(q))); if (parents.has(p)) ps.add(p); } return [...ps].sort(); }
function demand(h) { const d = {c1: 0, c2: 0, c4: 0}; for (const p of rowParents(h)) { const c = parents.get(p).classes; if (c & 1) d.c1++; if (c & 2) d.c2++; if (c & 4) d.c4++; } return d; }
function rootRowSet(rootHex, openSet) {
  const mask = BigInt('0x' + rootHex), set = new Set();
  for (let t = 0; t < 8; t++) { const sr = d4(mask, t); for (let q = 0; q < 121; q++) if ((sr >> BigInt(q)) & 1n) { const h = canon(sr ^ (1n << BigInt(q))); if (openSet.has(h)) set.add(h); } }
  return set;
}
function needed(set) { let n = 0, c = 0; for (const h of set.keys()) if (demand(h).c1 === 0) { n++; c += set.get(h).cost; } return {s6_needed_by_open_classes: n, cost_needed_by_open_classes: c}; }
// --- receipts ---
const RECEIPT_ROOTS = ['00000000000000821082000000042000', '00000000000000821082000000420000'].sort();
const firstRoot = '00000000000000821082000010800000';
const targetResidual = new Set(cover.receipts.residual_row_hex);
need(targetResidual.size === 97, 'residual target rows');
const probeRecords = fs.readFileSync(path.join(OUT, 'residual-48-root-depth10-probe-records-20261119.jsonl'), 'utf8').trim().split(/\r?\n/).map(JSON.parse);
const sweepBytes = fs.readFileSync(path.join(OUT, 'residual-48-root-depth10-sweep-20261119.json'));
const recordsSha = gitBlobSha(fs.readFileSync(path.join(OUT, 'residual-48-root-depth10-probe-records-20261119.jsonl')));
const sweep = JSON.parse(sweepBytes.toString('utf8'));
need(sweep.status === 'sweep-complete' && sweep.classification.counted_roots === 48, 'sweep gate');
const receipts = [];
let openCur = open1;
for (const root of RECEIPT_ROOTS) {
  const witness = cover.witness.find(x => x.root === root);
  const rootCheck = cover.root_checks.find(x => x.root === root);
  const item = mobility.mobility.priority_order.find(x => x.root === root);
  need(witness && rootCheck && item, 'root missing from pinned 49-root data: ' + root);
  need(rootCheck.stones === 7 && rootCheck.d4_canonical && rootCheck.unsafe_quadruples === 0, 'root geometry precheck: ' + root);
  need(item.cache_status === 'no-child-orbit-in-published-index' && item.cache_matches.length === 0, 'root was not previously cache-unclassified: ' + root);
  const summary = JSON.parse(fs.readFileSync(path.join(OUT, 'resid-win7-root-' + root + '-extraction-summary-20261119.json'), 'utf8'));
  const verification = JSON.parse(fs.readFileSync(path.join(OUT, 'resid-win7-root-' + root + '-independent-verification-20261119.json'), 'utf8'));
  const bareissLines = fs.readFileSync(path.join(OUT, 'resid-win7-root-' + root + '-bareiss-subroots-20261119.jsonl'), 'utf8').trim().split(/\r?\n/).map(JSON.parse);
  const bareissRoot = bareissLines[0], bareiss = bareissLines[1], bareissStats = Object.values(bareiss.stats);
  const bareissUnion = JSON.parse(fs.readFileSync(path.join(OUT, 'resid-win7-root-' + root + '-bareiss-union-audit-20261119.json'), 'utf8'));
  const nMoves = item.legal_next_moves;
  need(summary.root === root && summary.status === 'EXTRACTED_UNVERIFIED' && summary.completed_moves === nMoves && summary.legal_next_moves === nMoves && summary.fbt_drops === 0 && summary.failure === null, 'extraction gate: ' + root);
  need(JSON.stringify(summary.completed_move_list) === JSON.stringify(item.legal_bits), 'legal moves mismatch: ' + root);
  need((summary.added_bit ?? -1) === summary.added_bit, 'added bit integer');
  const witnessRowsSorted = [...witness.rows].sort();
  need(JSON.stringify(summary.covered_rows) === JSON.stringify(witnessRowsSorted), 'declared rows mismatch: ' + root);
  need(verification.verdict === 'WIN7 certificate independently verified' && verification.root_hex === root && verification.root_safe === true && verification.root_mobility === nMoves &&
       verification.subroots_passed === nMoves && verification.union_missing === 0 && verification.union_extra === 0 &&
       verification.strategy_rows === summary.unique_strategy_rows && verification.consumed_winner_rows === summary.unique_strategy_rows, 'independent verifier gate: ' + root);
  need(bareissRoot.stones === 7 && bareissRoot.loserMobility === nMoves && bareiss.rows === summary.unique_strategy_rows && bareissStats.length === nMoves, 'Bareiss verifier root/subroots: ' + root);
  const bareissTotals = {seen: bareissStats.reduce((s, x) => s + x.seen, 0), terminals: bareissStats.reduce((s, x) => s + x.terminals, 0), opponent_edges: bareissStats.reduce((s, x) => s + x.opponentEdges, 0), terminal_min: Math.min(...bareissStats.map(x => x.range[0])), terminal_max: Math.max(...bareissStats.map(x => x.range[1]))};
  need(verification.visited_states_across_subroots === bareissTotals.seen && verification.terminal_count === bareissTotals.terminals && verification.loser_reply_edges === bareissTotals.opponent_edges, 'cross-method state-flow disagreement: ' + root);
  need(bareissTotals.terminal_min === summary.terminal_stone_range[0] && bareissTotals.terminal_max === summary.terminal_stone_range[1] && verification.terminal_range[0] === bareissTotals.terminal_min && verification.terminal_range[1] === bareissTotals.terminal_max, 'terminal range disagreement: ' + root);
  need(bareissUnion.exact_union === true && bareissUnion.missing === 0 && bareissUnion.extra === 0 && bareissUnion.certificate_rows === summary.unique_strategy_rows && bareissUnion.consumed_unique === summary.unique_strategy_rows, 'Bareiss consumed-union audit: ' + root);
  const certBytes = fs.readFileSync(path.join(OUT, 'win7-root-' + root + '-20261119.n11'));
  const certSha = sha256(certBytes);
  need(certSha === summary.certificate_sha256, 'certificate sha256 mismatch: ' + root);
  // probe gate: at least one uncapped WIN ordering, all controls pass
  const probes = probeRecords.filter(r => r.root === root);
  for (const r of probes) need(r.control.control === 'pilot_d6' && r.control.loss === false && r.control.nodes === 3402, 'pilot control: ' + root);
  const winRuns = probes.filter(r => r.result.loss === true && r.result.capped === false);
  need(winRuns.length >= 1, 'no uncapped WIN probe run: ' + root);
  const conflict = probes.some(r => r.result.loss === false && r.result.capped === false);
  need(!conflict, 'ordering conflict on receipt root: ' + root);
  // receipt rows from geometry over the current open set
  const rootRows = rootRowSet(root, openCur);
  for (const h of rootRows) need(openCur.has(h), 'receipt row was already closed or absent: ' + root + ' row ' + h);
  const targetRows = [...rootRows].filter(h => targetResidual.has(h)).sort();
  need(JSON.stringify(targetRows) === JSON.stringify(witnessRowsSorted), 'independent root-to-target-row join mismatch: ' + root);
  const closedCost = [...rootRows].reduce((s, h) => s + openCur.get(h).cost, 0);
  const affected = [...rootRows].flatMap(h => rowParents(h));
  const affectedSet = new Set(affected);
  const before = new Map([...parents.keys()].map(p => [p, 0]));
  for (const h of openCur.keys()) for (const p of rowParents(h)) before.set(p, before.get(p) + 1);
  const after = new Map(before);
  for (const h of rootRows) for (const p of rowParents(h)) after.set(p, after.get(p) - 1);
  const parentDeltas = [...affectedSet].sort().map(p => ({parent_hex: p, classes: parents.get(p).classes, rows_before: before.get(p), rows_closed: before.get(p) - after.get(p), rows_after: after.get(p)}));
  receipts.push({
    root, added_bit: summary.added_bit, child_hex: summary.child, covered_s6_rows: [...rootRows].sort(),
    covered_five_parent_target_rows: targetRows, legal_next_moves: nMoves,
    total_nodes: summary.total_nodes, unique_strategy_rows: summary.unique_strategy_rows,
    closed_edge_cost: closedCost, parent_deltas: parentDeltas,
    affected_parents: affectedSet.size,
    probe_runs: probes.map(r => ({ordering: r.ordering, cap: r.cap, loss: r.result.loss, nodes: r.result.nodes, capped: r.result.capped, ms: r.ms})),
    certificate_path: 'research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/win7-root-' + root + '-20261119.n11',
    certificate_sha256: certSha, certificate_bytes: certBytes.length,
    independent_verification: {
      bigint: {subroots_passed: verification.subroots_passed, union_missing: verification.union_missing, union_extra: verification.union_extra, terminal_range: verification.terminal_range},
      bareiss: {subroots: bareissStats.length, ...bareissTotals, consumed_unique: bareissUnion.consumed_unique}
    }
  });
  for (const h of rootRows) openCur.delete(h);
}
// --- frontier/cover after ---
const frontierBefore = firstFold.frontier_after;
const remainingParentsCount = new Set([...openCur.keys()].flatMap(h => rowParents(h))).size;
let parentIncidence = 0;
{
  const inc = new Map([...parents.keys()].map(p => [p, 0]));
  for (const h of openCur.keys()) for (const p of rowParents(h)) inc.set(p, inc.get(p) + 1);
  parentIncidence = [...inc.values()].reduce((s, n) => s + n, 0);
}
const totalClosedRows = receipts.flatMap(r => r.covered_s6_rows);
need(new Set(totalClosedRows).size === totalClosedRows.length, 'two receipts closed the same row');
const frontierAfter = {
  solved_s6_in_manifest: frontierBefore.solved_s6_in_manifest + totalClosedRows.length,
  remaining_s5_orbits: remainingParentsCount,
  unique_remaining_s6: openCur.size,
  sum_remaining_cost: [...openCur.values()].reduce((s, x) => s + x.cost, 0),
  ...needed(openCur),
  parent_row_incidence: parentIncidence
};
// residual cover accounting
const closedTargetRows = new Set(receipts.flatMap(r => r.covered_five_parent_target_rows));
const firstClosedTarget = firstFold.root.covered_five_parent_target_rows;
for (const r of firstClosedTarget) closedTargetRows.add(r);
const targetAfter = new Set([...targetResidual].filter(h => !closedTargetRows.has(h)));
const remainingWitness = cover.witness.filter(x => x.root !== firstRoot && !RECEIPT_ROOTS.includes(x.root));
need(remainingWitness.length === 46, 'remaining witness');
const count = new Map();
for (const w of remainingWitness) for (const h of w.rows) count.set(h, (count.get(h) || 0) + 1);
for (const h of targetAfter) { need(count.get(h) === 1, 'residual cover duplicate/missing row ' + h); }
for (const h of count.keys()) need(targetAfter.has(h), 'residual cover extraneous row ' + h);
const refutedSet = new Set(sweep.classification.refuted_d10.roots);
const sweptRoots = sweep.classification.refuted_d10.count + sweep.classification.win7_d10.count + sweep.classification.capped.count;
need(sweptRoots === 48, 'sweep counts');
const remainingRefuted = remainingWitness.filter(w => refutedSet.has(w.root));
need(remainingRefuted.length === 46 - 0, 'remaining witness all refuted...'); // informational, see below
const record = {
  schema: 'n11-five-parent-second-third-win7-receipt-fold-20261119-v1',
  date: '2026-11-19',
  status: 'fold-complete',
  source_main_head_before: 'c8e974a26629a8b91662f479e1d84e10cae6ddcd',
  previous_fold: {tarball: P.firstFoldTarball[0], git_blob_sha1: P.firstFoldTarball[1], fold_json_extracted_sha256: sha256(firstFoldBytes), fold_json: firstFold.new_receipt_coverage ? 'first-win7-root-receipt-fold-20261119.json (bundle)' : null},
  source_blob_pins: Object.fromEntries(Object.entries(P).map(([k, v]) => [k, v[1]])),
  receipt_count: receipts.length,
  receipts,
  new_receipt_coverage: {
    unique_s6_rows: totalClosedRows.length,
    total_row_root_pairs: totalClosedRows.length,
    closed_edge_cost: receipts.reduce((s, r) => s + r.closed_edge_cost, 0),
    rows: receipts.flatMap(r => r.covered_s6_rows.sort().map(h => ({row_hex: h, cost: open.get(h).cost, category: open.get(h).category, demand: demand(h), parents: rowParents(h), receipt: {root: r.root, verdict: 'WIN7-D10', certificate_sha256: r.certificate_sha256}})))
  },
  parent_closure: {
    fully_closed_parent_count: receipts.flatMap(r => r.parent_deltas).filter(p => p.rows_after === 0).length,
    affected_unique_parents: new Set(receipts.flatMap(r => r.parent_deltas.map(p => p.parent_hex))).size
  },
  frontier_before: frontierBefore,
  frontier_after: frontierAfter,
  five_parent_residual_cover_after: {
    rows: targetAfter.size, roots: remainingWitness.length,
    pair_roots: remainingWitness.filter(w => w.rows.length === 2).length,
    singleton_roots: remainingWitness.filter(w => w.rows.length === 1).length,
    lower_bound_conditioned_on_candidates: Math.ceil(targetAfter.size / 2),
    witness_size: remainingWitness.length,
    witness_condition: 'candidate-conditioned plan: each remaining witness root is now classified REFUTED-D10 by the parallel 48-root depth-10 sweep, so no remaining witness root can close its rows as a WIN7-D10 receipt; the rows cannot be closed by this witness and require re-solved candidates (see the non-refuted cover re-solve audit) or certificates beyond depth 10.',
    sweep_refuted_among_witness: remainingRefuted.length,
    root_list: remainingWitness.map(x => x.root)
  },
  sweep_reference: {path: 'research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json', git_blob_sha1: gitBlobSha(sweepBytes), probe_records_sha1: recordsSha, win: sweep.classification.win7_d10.count, refuted: sweep.classification.refuted_d10.count, capped: sweep.classification.capped.count},
  controls: {
    base_frontier_recomputed: true, first_fold_frontier_chained: true,
    receipt_rows_rederived_from_all_8_d4_images: true,
    receipt_target_rows_match_published_49_cover: true,
    all_receipt_rows_were_open_before_new_receipts: true,
    both_roots_independently_verified_bigint: true, both_roots_independently_verified_bareiss: true,
    cross_method_state_flow_agreement: true,
    receipt_rows_disjoint: true,
    srand: false, win_loss_conflicts: 0
  },
  interpretation_guard: [
    'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone roots of these receipts.',
    'The two receipts close their S6 rows in the frontier but do not prove a win from the empty board or any two-stone root.',
    'REFUTED-D10 (46 of 48 swept roots) is NOT a LOSS proof; it bounds no first-player win within depth 10 from those exact 7-stone roots.',
    'The remaining 46-root witness is now a fully refuted candidate plan at depth 10; residual target rows need re-solved cover candidates or deeper certificates.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
};
delete record.controls.srand;
fs.writeFileSync(path.join(OUT, 'second-third-win7-root-receipt-fold-20261119.json'), JSON.stringify(record, null, 2) + '\n');
console.log(JSON.stringify({status: record.status, closed_unique_s6_rows: totalClosedRows.length, closed_target_rows: closedTargetRows.size, frontier_after: frontierAfter, remaining_witness: remainingWitness.length, refuted_among_witness: remainingRefuted.length, certificates: receipts.map(r => ({root: r.root, sha256: r.certificate_sha256}))}, null, 2));
