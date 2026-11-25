// band-wide memoized extraction measurement driver (2026-11-17, long-term lane)
//
// MEASUREMENT ONLY (no certificate publication): re-extracts the published
// cost-73j WIN7-D10 band (16 roots, manifest class2-lane-cost73j-win7-certificates-20261117.json,
// per-bit fresh-process baseline extraction_nodes total 166,238,087) in ONE process,
// sequentially per bit in manifest order, with the extractor's process-global memo
// (MS=1<<18 position-keyed win/loss table) and fbt (FBS=1<<20 triple-keyed forbidden
// table) carried ACROSS bits. The repo-verbatim extractor is imported UNMODIFIED;
// the driver adds no search behavior, it only records per-bit node counts.
//
// Controls (all must pass for a valid measurement):
//   - every per-bit extractBatch must return ok=true, fatal=null, fbt_drops=0
//   - the accumulated row Map after the last bit must equal the union of the 16
//     published certificate row sets (547,910 rows), compared externally against
//     published_union_73j.txt
//
// Run: node --experimental-strip-types measure_band_memo_extraction_73j.ts plan73j.json out.summary.json rows.union.txt
import { extractBatch } from './class4_child1_cert_extractor_exact.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);

const planPath = process.argv[2];
const summaryPath = process.argv[3];
const rowsPath = process.argv[4];

const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const child = plan.child;
const bits = plan.bits;

const perBit = [];
let totalNodes = 0;
let prevRows = 0;
let lastRows: string[] = [];
let lastN = 0;
const t0 = Date.now();

for (const b of bits) {
  const tb = Date.now();
  const res = extractBatch(child, b.bit, {}, b.moves);
  const ms = Date.now() - tb;
  if (!Array.isArray(res.rows) || res.fatal || res.fbt_drops !== 0) {
    process.stderr.write(`INVALID bit ${b.bit}: fatal=${res.fatal} fbt_drops=${res.fbt_drops}` + NL);
    process.exitCode = 1;
    // still write partial summary for the record
    fs.writeFileSync(summaryPath, JSON.stringify({ status: 'INVALID', bit: b.bit, fatal: res.fatal, fbt_drops: res.fbt_drops, perBit }, null, 1));
    process.exit(1);
  }
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
    rows_before: prevRows,
    rows_after: res.nRows,
    rows_new_this_bit: res.nRows - prevRows,
    published_rows: b.published_rows,
    ms
  });
  prevRows = res.nRows;
  lastRows = res.rows;
  lastN = res.nRows;
  process.stderr.write(`bit ${b.bit} nodes ${res.sum} (published ${b.published_nodes}, ratio ${(res.sum / b.published_nodes).toFixed(3)}) rows now ${res.nRows} [${ms}ms]` + NL);
}

const summary = {
  schema: 'n11-class2-lane-band-memo-extraction-measurement-73j-20261117-v1',
  date: '2026-11-17',
  band: 'cost73j',
  child_hex: child,
  bits_extracted: perBit.length,
  total_nodes_single_process_with_band_memo: totalNodes,
  total_nodes_published_fresh_process_baseline: bits.reduce((s: number, b: any) => s + b.published_nodes, 0),
  overall_node_ratio: +(totalNodes / bits.reduce((s: number, b: any) => s + b.published_nodes, 0)).toFixed(6),
  union_rows_map_size: lastN,
  published_union_rows_expected: 547910,
  all_bits_ok: perBit.every(p => p.per_move_ok),
  fbt_drops: 0,
  wall_ms: Date.now() - t0,
  per_bit: perBit
};
fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 1));
fs.writeFileSync(rowsPath, lastRows.sort().join(NL) + NL);
process.stderr.write(`DONE total ${totalNodes} ratio ${summary.overall_node_ratio} union ${lastN}` + NL);
