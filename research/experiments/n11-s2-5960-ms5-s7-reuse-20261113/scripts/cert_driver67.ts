// blind certificate extraction driver for class2-lane cost-67 WIN7 roots (2026-11-14)
// imports extractBatch from the repo-verbatim extractor_exact; empty kill table (pref=null).
import { extractBatch } from './scripts/class4_child1_cert_extractor_exact.ts';
import fs from 'fs';
const NL = String.fromCharCode(10);
const child = process.argv[2];
const bit = Number(process.argv[3]);
const outPath = process.argv[4];
// enumerate root legal moves via legal_candidates.py output given on stdin
let input = '';
process.stdin.on('data', c => input += c);
process.stdin.on('end', () => {
  const moves = input.trim().split('\n').pop().trim().split(',').filter(s => s !== '').map(Number);
  const t0 = Date.now();
  const res = extractBatch(child, bit, {}, moves);
  const summary = { child, bit, moves: moves.length, perMove: res.perMove, sum: res.sum,
    nRows: res.nRows, fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0 };
  process.stderr.write(JSON.stringify(summary) + NL);
  if (res.rows && !res.fatal) {
    const lines = ['n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS',
      'root ' + (BigInt('0x' + child) | (1n << BigInt(bit))).toString(16).padStart(32, '0')];
    fs.writeFileSync(outPath, lines.join(NL) + NL + res.rows.join(NL) + NL);
    process.stderr.write('written ' + outPath + NL);
  }
});
