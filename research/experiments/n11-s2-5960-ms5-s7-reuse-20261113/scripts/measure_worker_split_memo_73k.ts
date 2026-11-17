// worker-split memo dump/seed measurement driver for the cost-73k band
// (2026-11-17, n11 class2-lane long-term lane).
//
// MEASUREMENT ONLY (no certificate publication, no verdict changes).
//
// Runs a SUBSET of the published cost-73k WIN7-D10 band (manifest
// class2-lane-cost73k-win7-certificates-20261117.json) in ONE process,
// sequentially per bit in ascending manifest bit order, with the
// repo-verbatim extractor's process-global memo carried ACROSS bits
// (same execution model as the published band-wide measurement
// measure_band_memo_extraction_73k.ts), then DUMPS the full memo table
// (KYOENWM1: one record per occupied slot) so worker tables can be merged
// offline. Optionally SEEDS the memo from a merged table (KYOENWM2) before
// the run (seedMemo); the seed loader inserts records in file order via the
// engine's own memoEntry(), preserving verbatim probe semantics.
//
// Controls (checked externally by the orchestrator):
//   - every per-bit extractBatch must return ok=true, fatal=null, fbt_drops=0
//   - external byte-identity check of all snapshots vs published certs
//   - record-identity check of the final dump vs the seeded table
//
// Run: node --experimental-strip-types measure_worker_split_memo_73k.ts \
//        <plan.json> <out.summary.json> <certOutDir> <dumpPath> [seedPath]
import { extractBatch, clearRows, memoStats, dumpMemo, seedMemo } from './__VARIANT__';
import fs from 'fs';
const NL = String.fromCharCode(10);

const planPath = process.argv[2];
const summaryPath = process.argv[3];
const certOutDir = process.argv[4];
const dumpPath = process.argv[5];
const seedPath = process.argv[6] || '';

const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const child = plan.child;
const bits = plan.bits;

const seedStats = seedPath ? seedMemo(seedPath) : null;
process.stderr.write('seeded ' + (seedStats ? JSON.stringify(seedStats) : 'none') + NL);

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
    per_move_ok: Object.entries(res.perMove).every(([k, v]: any) => v.ok && !v.capped),
    rows: sorted.length,
    published_rows: b.published_rows,
    memo_occupied_after: occ.occupied,
    memo_slots: occ.slots,
    ms
  });
  process.stderr.write(`bit ${b.bit} nodes ${res.sum} rows ${sorted.length} occ ${occ.occupied} [${ms}ms]` + NL);
  clearRows();
}

const occFinal = memoStats();
const header = 'KYOENWM1 slots=' + occFinal.slots + ' child=' + child +
  ' seed=' + (seedPath ? 'merged_KYOENWM2' : 'none') +
  ' bits=' + bits.map((b: any) => b.bit).join(',');
dumpMemo(dumpPath, header);

const summary = {
  schema: 'n11-class2-lane-worker-split-memo-measurement-73k-20261117-v1',
  date: '2026-11-17',
  band: 'cost73k',
  child_hex: child,
  worker_tag: plan.tag,
  bits_extracted: perBit.length,
  seed: seedStats,
  total_nodes: totalNodes,
  final_memo_occupied: occFinal.occupied,
  memo_slots: occFinal.slots,
  dump_path: dumpPath,
  all_bits_ok: perBit.every(p => p.per_move_ok),
  fbt_drops: 0,
  wall_ms: Date.now() - t0,
  per_bit: perBit
};
fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 1));
process.stderr.write(`DONE total ${totalNodes} occ ${occFinal.occupied}` + NL);
