// certificate extraction driver for the class2-lane cost-63c / cost-63d WIN7
// roots (2026-11-17 regeneration; modeled on cert_driver71e.ts).
//
// RECONSTRUCTION NOTE: the 2026-11-14 first extraction of these two roots ran
// the extractor CLI (class4_child1_cert_extractor_exact.ts) whose default
// KILL_BIT7 session-6 preference table was active, one process per move for
// cost-63c (per-move node sum 14,524,021 = the recorded extraction_nodes) and
// batched processes for cost-63d. Blind extraction (empty kill table) does NOT
// reproduce those bytes (63c bit46 blind union: 43,473 rows vs 45,337); the
// CLI-default KILL_BIT7 table does, byte-identically on both roots, so the
// table is reproduced verbatim here. The pref only reorders the winner-reply
// probe at the top level; validity is established independently by the
// engine-free verifiers after extraction.
//
// usage: node --experimental-strip-types cert_driver63cd.ts CHILD_HEX BIT MOVE OUT_PREFIX
// writes OUT_PREFIX.rows (raw strategy rows for the single loser first-move)
// and OUT_PREFIX.summary.json; refuses output on fatal or fbt_drops != 0.
import { extractBatch } from './class4_child1_cert_extractor_exact.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);
const child = process.argv[2];
const bit = Number(process.argv[3]);
const move = Number(process.argv[4]);
const outPath = process.argv[5];
const KILL_BIT7 = {0:114,8:21,10:81,15:40,18:40,21:40,28:80,32:81,33:18,34:83,38:70,40:18,44:81,45:28,50:18,54:8,66:18,67:80,70:38,72:88,75:50,76:40,78:70,80:28,81:32,82:50,83:8,84:40,86:72,87:70,88:72,90:8,91:8,92:50,93:8,94:28,102:90,104:40,105:18,106:81,108:18,109:70,110:8,112:82,113:81,114:38,116:8,117:8,118:18,120:28};
const t0 = Date.now();
const res = extractBatch(child, bit, KILL_BIT7, [move]);
const summary = { child, bit, move, pref: KILL_BIT7[move] ?? null, perMove: res.perMove,
  sum: res.sum, nRows: res.nRows, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0 };
fs.writeFileSync(outPath + '.summary.json', JSON.stringify(summary));
process.stderr.write(JSON.stringify({ move, pref: KILL_BIT7[move] ?? null, nRows: res.nRows,
  sum: res.sum, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0 }) + NL);
if (!Array.isArray(res.rows) || res.fatal || res.fbt_drops !== 0) {
  process.stderr.write('refusing certificate rows: rows missing, fatal set, or fbt_drops != 0' + NL);
  process.exit(1);
}
fs.writeFileSync(outPath + '.rows', res.rows.join(NL) + NL);
