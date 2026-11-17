// Fail-closed certificate driver for the cost76c WIN7-D10 extraction.
// Uses the published v16 extractor without changing its search algorithm.
// The raw child|bit root is retained; do not D4-canonicalize the defense list.
import fs from 'node:fs';
import { extractBatch } from './class4_child1_cert_extractor_exact_v16.ts';

const NL = String.fromCharCode(10);
const child = process.argv[2] ?? '';
const bit = Number(process.argv[3]);
const outPath = process.argv[4] ?? '';

function refuse(message: string) {
  process.stderr.write(message + NL);
  process.exitCode = 1;
}

if (!/^[0-9a-f]{32}$/i.test(child) ||
    !Number.isInteger(bit) || bit < 0 || bit >= 121 ||
    outPath.length === 0) {
  process.stderr.write('usage: cert_driver76c.ts <raw-child-hex> <bit> <output-path>' + NL);
  process.exit(2);
}
const childMask = BigInt('0x' + child);
let childStones = 0;
for (let v = childMask; v !== 0n; v &= v - 1n) childStones++;
if (childStones !== 6 || (childMask >> 121n) !== 0n ||
    ((childMask >> BigInt(bit)) & 1n) !== 0n) {
  process.stderr.write('refusing certificate output: child must contain exactly six in-board stones and the selected bit must be empty' + NL);
  process.exit(2);
}

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  const lines = input.trim().split(NL);
  const last = lines[lines.length - 1] ?? '';
  const moves = last.split(',').filter(s => s.length > 0).map(Number);
  if (moves.length === 0 ||
      moves.some(m => !Number.isInteger(m) || m < 0 || m >= 121) ||
      new Set(moves).size !== moves.length) {
    refuse('refusing certificate output: empty, invalid, or duplicate raw-root defense list');
    return;
  }

  const t0 = Date.now();
  // Empty kill table: every listed raw-root defense is extracted independently.
  const res = extractBatch(child, bit, {}, moves);
  const perMoveComplete = moves.every(m => {
    const item = res.perMove?.[m];
    return item !== undefined && item.ok === true && item.capped === false;
  });
  const rowsWellFormed = Array.isArray(res.rows) &&
    res.rows.length > 0 && res.rows.every(row => typeof row === 'string');
  const rowCountMatches = rowsWellFormed && res.nRows === res.rows.length;
  const rowsUnique = rowsWellFormed && new Set(res.rows).size === res.rows.length;
  const complete = rowsWellFormed && rowCountMatches && rowsUnique &&
    !res.fatal && res.fbt_drops === 0 && perMoveComplete;

  const summary = {
    child, bit, moves: moves.length, perMove: res.perMove, sum: res.sum,
    nRows: res.nRows, rowsAvailable: rowsWellFormed,
    rowCountMatches, rowsUnique, perMoveComplete,
    fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0
  };
  process.stderr.write(JSON.stringify(summary) + NL);
  if (!complete) {
    refuse('refusing certificate output: extraction incomplete, fatal, capped, or fbt_drops != 0');
    return;
  }

  const root = (BigInt('0x' + child) | (1n << BigInt(bit)))
    .toString(16).padStart(32, '0');
  const sorted = Array.from(new Set(res.rows)).sort();
  const body = [
    'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS',
    'root ' + root,
    ...sorted
  ].join(NL) + NL;

  // Stage beside the destination and link without overwriting an existing receipt.
  const tmpPath = outPath + '.tmp-' + process.pid;
  try {
    fs.writeFileSync(tmpPath, body, { flag: 'wx' });
    fs.linkSync(tmpPath, outPath);
    fs.unlinkSync(tmpPath);
  } catch (err) {
    try { fs.rmSync(tmpPath, { force: true }); } catch {}
    refuse('refusing certificate output: atomic publication failed: ' + String(err));
    return;
  }
  process.stderr.write('written ' + outPath + NL);
});
