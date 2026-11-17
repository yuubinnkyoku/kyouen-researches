// band-wide memoized extraction measurement driver for the cost-73k band
// (2026-11-17, n11 class2-lane long-term lane).
//
// MEASUREMENT ONLY (no certificate publication): re-extracts the published
// cost-73k WIN7-D10 band (22 roots, manifest
// class2-lane-cost73k-win7-certificates-20261117.json, per-bit fresh-process
// baseline extraction_nodes total 155,946,109) in ONE process, sequentially
// per bit in ascending manifest bit order, with the extractor's
// process-global memo (position-keyed win/loss table) and fbt (triple-keyed
// forbidden table) carried ACROSS bits. The extractor import below is
// retargeted by the orchestrator at a patched variant of the repo-verbatim
// engine (MS line substitution + clearRows()/memoStats() export block; the
// patch adds no search behavior - see measure_band_memo_extraction_73k_20261117.py).
//
// Differences from the published 73j driver (measure_band_memo_extraction_73j.ts):
//   - per-root row-set SNAPSHOT + clearRows() after every bit, so every root's
//     own certificate is reconstructed and can be byte-compared against the
//     published certificate (split files concatenated), not just the union;
//   - memo occupancy (occupied slots) recorded after every bit via memoStats().
//
// Controls (all must pass for a valid measurement):
//   - every per-bit extractBatch must return ok=true, fatal=null, fbt_drops=0
//   - external byte-identity check of all 22 snapshots vs published certs
//
// Run: node --experimental-strip-types measure_band_memo_extraction_73k.ts \
//        <plan.json> <out.summary.json> <certOutDir>
import { extractBatch, clearRows, memoStats } from './class4_child1_cert_extractor_exact_memo18.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);

const planPath = process.argv[2];
const summaryPath = process.argv[3];
const certOutDir = process.argv[4];

const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const child = plan.child;
const bits = plan.bits;

const perBit: any[] = [];
let totalNodes = 0;
const t0 = Date.now();

for (const b of bits) {
  const tb = Date.now();
  const res: any = extractBatch(child, b.bit, {}, b.moves);
  const ms = Date.now() - tb;
  if (!Array.isArray(res.rows) || res.fatal || res.fbt_drops !== 0) {
    process.stderr.write(`INVALID bit ${b.bit}: fatal=${res.fatal} fbt_drops=${res.fbt_drops}` + NL);
    fs.writeFileSync(summaryPath, JSON.stringify({ status: 'INVALID', bit: b.bit, fatal: res.fatal, fbt_drops: res.fbt_drops, per_bit: perBit }, null, 1));
    process.exit(1);
  }
  const sorted = Array.from(new Set(res.rows)).sort();
  const body = sorted.join(NL) + NL;
  const doc = 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS' + NL +
    'root ' + b.root + NL + body;
  fs.writeFileSync(certOutDir + '/' + b.file, doc);
  const occ = memoStats();
  totalNodes += res.sum;
  perBit.push({
    bit: b.bit,
    root: b.root,
    moves: b.moves.length,
    nodes_this_run: res.sum,
    published_fresh_process_nodes: b.published_nodes,
    node_delta: res.sum - b.published_nodes,
    node_ratio: +(res.sum / b.published_nodes).toFixed(6),
    per_move_ok: Object.entries(res.perMove).every(([k, v]: any) => v.ok && !v.capped),
    rows: sorted.length,
    published_rows: b.published_rows,
    memo_occupied_after: occ.occupied,
    memo_slots: occ.slots,
    ms
  });
  process.stderr.write(`bit ${b.bit} nodes ${res.sum} (published ${b.published_nodes}, ratio ${(res.sum / b.published_nodes).toFixed(3)}) rows ${sorted.length} occ ${occ.occupied} [${ms}ms]` + NL);
  clearRows();
}

const summary = {
  schema: 'n11-class2-lane-band-memo-extraction-measurement-73k-20261117-v1',
  date: '2026-11-17',
  band: 'cost73k',
  child_hex: child,
  bits_extracted: perBit.length,
  total_nodes_single_process_with_band_memo: totalNodes,
  total_nodes_published_fresh_process_baseline: bits.reduce((s: number, b: any) => s + b.published_nodes, 0),
  overall_node_ratio: +(totalNodes / bits.reduce((s: number, b: any) => s + b.published_nodes, 0)).toFixed(6),
  all_bits_ok: perBit.every(p => p.per_move_ok),
  fbt_drops: 0,
  wall_ms: Date.now() - t0,
  per_bit: perBit
};
fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 1));
process.stderr.write(`DONE total ${totalNodes} ratio ${summary.overall_node_ratio}` + NL);
