// blind certificate extraction driver for class2-lane cost-73k WIN7 roots (2026-11-17)
// duplicated from cert_driver73j.ts (71e driver, argv-driven); imports extractBatch
// from the repo-verbatim extractor_exact; empty kill table (pref=null).
import { extractBatch } from './class4_child1_cert_extractor_exact.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);
const child = process.argv[2];
const bit = Number(process.argv[3]);
const outPath = process.argv[4];
// enumerate root legal moves (loser first-move defenses) via legal_candidates.py on stdin
let input = '';
process.stdin.on('data', c => input += c);
process.stdin.on('end', () => {
  const moves = input.trim().split(NL).pop().trim().split(',').filter(s => s !== '').map(Number);
  const t0 = Date.now();
  const res = extractBatch(child, bit, {}, moves);
  const summary = { child, bit, moves: moves.length, perMove: res.perMove, sum: res.sum,
    nRows: res.nRows, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0 };
  process.stderr.write(JSON.stringify(summary) + NL);
  // Never publish a partial certificate: the extractor may return rows even when
  // its bounded forbidden-bit table dropped entries or reported a fatal condition.
  if (!Array.isArray(res.rows) || res.fatal || res.fbt_drops !== 0) {
    process.stderr.write('refusing certificate output: rows missing, fatal set, or fbt_drops != 0' + NL);
    process.exitCode = 1;
    return;
  }
  const lines = ['n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS',
    'root ' + (BigInt('0x' + child) | (1n << BigInt(bit))).toString(16).padStart(32, '0')];
  const sorted = Array.from(new Set(res.rows)).sort();
  fs.writeFileSync(outPath, lines.join(NL) + NL + sorted.join(NL) + NL);
  process.stderr.write('written ' + outPath + NL);
});
