// Fail-closed certificate driver for the cost76c WIN7-D10 extraction.
// Uses the published v16 extractor without changing its search algorithm.
// The raw child|bit root is retained; do not D4-canonicalize the defense list.
// The defense list is independently re-derived here (Bareiss 4x4), then matched exactly.
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

function cellsFromMask(mask: bigint): number[] {
  const cells: number[] = [];
  for (let i = 0; i < 121; i++) {
    if (((mask >> BigInt(i)) & 1n) !== 0n) cells.push(i);
  }
  return cells;
}

function det4Zero(points: number[]): boolean {
  // Exact Bareiss determinant of rows [x^2+y^2, x, y, 1].
  const a = points.map(cell => {
    const x = cell % 11;
    const y = Math.floor(cell / 11);
    return [x * x + y * y, x, y, 1];
  });
  let previous = 1;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0) {
      let pivotRow = -1;
      for (let r = k + 1; r < 4; r++) {
        if (a[r][k] !== 0) { pivotRow = r; break; }
      }
      if (pivotRow < 0) return true;
      [a[k], a[pivotRow]] = [a[pivotRow], a[k]];
    }
    const pivot = a[k][k];
    for (let i = k + 1; i < 4; i++) {
      for (let j = k + 1; j < 4; j++) {
        const numerator = a[i][j] * pivot - a[i][k] * a[k][j];
        if (numerator % previous !== 0) {
          throw new Error('non-exact Bareiss division while deriving legal defenses');
        }
        a[i][j] = numerator / previous;
      }
    }
    previous = pivot;
  }
  return a[3][3] === 0;
}

function legalDefenses(rootMask: bigint): number[] {
  const stones = cellsFromMask(rootMask);
  // Reject a malformed/unsafe seven-stone root before deriving its replies.
  for (let i = 0; i < stones.length; i++)
    for (let j = i + 1; j < stones.length; j++)
      for (let k = j + 1; k < stones.length; k++)
        for (let l = k + 1; l < stones.length; l++)
          if (det4Zero([stones[i], stones[j], stones[k], stones[l]])) {
            throw new Error('selected seven-stone root is not safe');
          }
  const occupied = new Set(stones);
  const out: number[] = [];
  for (let p = 0; p < 121; p++) {
    if (occupied.has(p)) continue;
    let unsafe = false;
    for (let i = 0; i < stones.length && !unsafe; i++)
      for (let j = i + 1; j < stones.length && !unsafe; j++)
        for (let k = j + 1; k < stones.length; k++)
          if (det4Zero([stones[i], stones[j], stones[k], p])) {
            unsafe = true;
            break;
          }
    if (!unsafe) out.push(p);
  }
  return out;
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
const rootMask = childMask | (1n << BigInt(bit));
let expectedMoves: number[];
try {
  expectedMoves = legalDefenses(rootMask);
} catch (err) {
  process.stderr.write('refusing certificate output: independent root/defense derivation failed: ' + String(err) + NL);
  process.exit(2);
}
if (expectedMoves.length === 0) {
  process.stderr.write('refusing certificate output: selected root has no legal defenses' + NL);
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
  const defenseListExact = moves.length === expectedMoves.length &&
    moves.every((m, i) => m === expectedMoves[i]);
  if (!defenseListExact) {
    refuse('refusing certificate output: supplied defenses do not exactly equal the independently derived raw-root legal list (expected ' + expectedMoves.length + ', got ' + moves.length + ')');
    return;
  }

  const t0 = Date.now();
  // Empty kill table: every legal raw-root defense is extracted independently.
  const res = extractBatch(child, bit, {}, moves);
  const perMoveComplete = moves.every(m => {
    const item = res.perMove?.[m];
    return item !== undefined && item.ok === true && item.capped === false;
  });
  const perMoveKeys = Object.keys(res.perMove ?? {}).map(Number).sort((a, b) => a - b);
  const perMoveKeysExact = perMoveKeys.length === expectedMoves.length &&
    perMoveKeys.every((m, i) => m === expectedMoves[i]);
  const rowsWellFormed = Array.isArray(res.rows) && res.rows.length > 0 &&
    res.rows.every(row => {
      if (typeof row !== 'string') return false;
      const match = /^([0-9a-f]{32}) ([0-9]{1,3})$/i.exec(row);
      return match !== null && Number(match[2]) >= 0 && Number(match[2]) < 121;
    });
  const rowCountMatches = rowsWellFormed && res.nRows === res.rows.length;
  const rowKeys = rowsWellFormed ? res.rows.map(row => row.slice(0, 32)) : [];
  const rowsUnique = rowsWellFormed && new Set(rowKeys).size === rowKeys.length;
  const complete = rowsWellFormed && rowCountMatches && rowsUnique &&
    !res.fatal && res.fbt_drops === 0 && perMoveComplete && perMoveKeysExact;

  const summary = {
    child, bit, moves: moves.length, defenseListExact,
    expectedMoves, perMove: res.perMove, sum: res.sum,
    nRows: res.nRows, rowsAvailable: rowsWellFormed,
    rowCountMatches, rowsUnique, perMoveComplete, perMoveKeysExact,
    fbt_drops: res.fbt_drops, fatal: res.fatal, ms: Date.now() - t0
  };
  process.stderr.write(JSON.stringify(summary) + NL);
  if (!complete) {
    refuse('refusing certificate output: extraction incomplete, fatal, capped, malformed, or fbt_drops != 0');
    return;
  }

  const root = rootMask.toString(16).padStart(32, '0');
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
