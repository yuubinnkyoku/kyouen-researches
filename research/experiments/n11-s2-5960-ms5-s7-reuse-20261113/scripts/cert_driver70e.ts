// blind certificate extraction driver for class2-lane cost-70e WIN7 roots (2026-11-15)
// modeled on cert_driver78a.ts: imports extractBatch from the repo-verbatim
// class4_child1_cert_extractor_exact.ts; empty kill table (pref=null) = blind.
// usage: node --experimental-strip-types cert_driver70e.ts CHILD_HEX BIT OUT_PATH MOVES(comma list)
// writes raw rows only (no header/root); merge chunk files with sort -u, then prepend
// the n11-terminal-strategy-v1 header and root lines (cost-74d chunk convention).
import { extractBatch } from './class4_child1_cert_extractor_exact.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);
const child = process.argv[2];
const bit = Number(process.argv[3]);
const outPath = process.argv[4];
const moves = (process.argv[5] || '').split(',').filter(s => s !== '').map(Number);
const t0 = Date.now();
const res = extractBatch(child, bit, {}, moves);
const summary = { child, bit, moves, nMoves: moves.length, perMove: res.perMove, sum: res.sum,
  nRows: res.nRows, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0 };
fs.writeFileSync(outPath + '.summary.json', JSON.stringify(summary));
process.stderr.write(JSON.stringify({moves: moves.length, nRows: res.nRows, sum: res.sum, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now()-t0}) + NL);
if (res.rows && !res.fatal) {
  fs.writeFileSync(outPath, res.rows.join(NL) + NL);
  process.stderr.write('written ' + outPath + NL);
}
