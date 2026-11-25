#!/usr/bin/env node
import fs from 'node:fs';

const ROOT = '00000000000000809083000000004000';
const PARENT = '00000000000000809082000000004000';
const MOVE = 48;
const N = 121;
const FULL = (1n << 121n) - 1n;
const BIT = Array.from({ length: N }, (_, i) => 1n << BigInt(i));
const cache = new Map();

function fail(message) {
  throw new Error(message);
}

function det3(a) {
  return a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
       - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
       + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]);
}

// Exact integer geometry, independent of the 4x4 Bareiss implementation:
// a non-collinear triple determines a circle; a collinear triple determines a line.
function forbiddenByTriple(a, b, c) {
  const key = a * 14641 + b * 121 + c;
  const old = cache.get(key);
  if (old !== undefined) return old;

  const ps = [a, b, c].map(p => {
    const x = p % 11;
    const y = Math.floor(p / 11);
    return [x, y, x * x + y * y];
  });
  const [[x1, y1, r1], [x2, y2, r2], [x3, y3, r3]] = ps;
  const D = det3([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]]);
  let mask = 0n;

  if (D === 0) {
    for (let d = 0; d < N; d++) {
      if (d === a || d === b || d === c) continue;
      const x = d % 11;
      const y = Math.floor(d / 11);
      const value = det3([[x1, y1, 1], [x2, y2, 1], [x, y, 1]]);
      if (!Number.isSafeInteger(value)) fail('unsafe line determinant');
      if (value === 0) mask |= BIT[d];
    }
  } else {
    const A = det3([[-r1, y1, 1], [-r2, y2, 1], [-r3, y3, 1]]);
    const B = det3([[x1, -r1, 1], [x2, -r2, 1], [x3, -r3, 1]]);
    const C = det3([[x1, y1, -r1], [x2, y2, -r2], [x3, y3, -r3]]);
    for (const value of [D, A, B, C]) {
      if (!Number.isSafeInteger(value)) fail('unsafe circle coefficient');
    }
    for (let d = 0; d < N; d++) {
      if (d === a || d === b || d === c) continue;
      const x = d % 11;
      const y = Math.floor(d / 11);
      const value = D * (x * x + y * y) + A * x + B * y + C;
      if (!Number.isSafeInteger(value)) fail('unsafe circle evaluation');
      if (value === 0) mask |= BIT[d];
    }
  }

  if (cache.size > 25000) cache.clear();
  cache.set(key, mask);
  return mask;
}

function pointsOf(mask) {
  const points = [];
  for (let i = 0; i < N; i++) {
    if ((mask & BIT[i]) !== 0n) points.push(i);
  }
  return points;
}

function legalOfPoints(points) {
  let banned = 0n;
  for (const p of points) banned |= BIT[p];
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      for (let k = j + 1; k < points.length; k++) {
        banned |= forbiddenByTriple(points[i], points[j], points[k]);
      }
    }
  }
  return FULL & ~banned;
}

function countBits(mask) {
  let count = 0;
  while (mask !== 0n) {
    mask &= mask - 1n;
    count++;
  }
  return count;
}

function isSafe(points) {
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      for (let k = j + 1; k < points.length; k++) {
        const forbidden = forbiddenByTriple(points[i], points[j], points[k]);
        for (const d of points) {
          if (d !== points[i] && d !== points[j] && d !== points[k]
              && (forbidden & BIT[d]) !== 0n) return false;
        }
      }
    }
  }
  return true;
}

function parseCertificate(text) {
  const lines = text.split('\n').filter(line => line.trim() !== '');
  if (lines[0] !== 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS') {
    fail('wrong certificate header');
  }
  if (lines[1] !== 'root ' + ROOT) fail('wrong certificate root');
  if (lines.length !== 66682) fail('wrong nonempty line count: ' + lines.length);

  const strategy = new Map();
  let previous = '';
  for (const line of lines.slice(2)) {
    const parts = line.split(' ');
    if (parts.length !== 2) fail('malformed strategy row');
    const [key, moveText] = parts;
    if (key.length !== 32 || !/^[0-9a-f]+$/.test(key) || key <= previous) {
      fail('unsorted, duplicate, or malformed board key');
    }
    previous = key;
    if (!/^\d+$/.test(moveText) || Number(moveText) >= N) fail('invalid strategy move');
    if (BigInt('0x' + key) > FULL) fail('out-of-board strategy key');
    strategy.set(key, Number(moveText));
  }
  if (strategy.size !== 66680) fail('wrong strategy row count: ' + strategy.size);
  return strategy;
}

function verifySubRoot(strategy, subRoot) {
  if (pointsOf(subRoot).length !== 8) fail('sub-root must have eight stones');
  const seen = new Set();
  const consumed = [];
  const stack = [[subRoot, 0]];
  let terminals = 0;
  let opponentEdges = 0;
  let terminalMin = 999;
  let terminalMax = 0;

  while (stack.length !== 0) {
    const [board, depth] = stack.pop();
    const key = board.toString(16).padStart(32, '0');
    if (seen.has(key)) continue;
    seen.add(key);

    const points = pointsOf(board);
    const options = legalOfPoints(points);
    if (options === 0n) {
      if (depth % 2 !== 1) fail('winner has no move at terminal ' + key);
      if (strategy.has(key)) fail('terminal has a strategy row ' + key);
      terminals++;
      terminalMin = Math.min(terminalMin, points.length);
      terminalMax = Math.max(terminalMax, points.length);
    } else if (depth % 2 === 0) {
      const move = strategy.get(key);
      if (move === undefined) fail('missing winner move at ' + key);
      if ((options & BIT[move]) === 0n) fail('illegal winner move at ' + key);
      consumed.push(key);
      stack.push([board | BIT[move], depth + 1]);
    } else {
      if (strategy.has(key)) fail('strategy row on opponent turn at ' + key);
      let remaining = options;
      while (remaining !== 0n) {
        const move = remaining & -remaining;
        remaining -= move;
        opponentEdges++;
        stack.push([board | move, depth + 1]);
      }
    }
  }

  return {
    seen: seen.size,
    consumed,
    terminals,
    opponentEdges,
    terminalMin,
    terminalMax
  };
}

const [part1Path, part2Path] = process.argv.slice(2);
if (!part1Path || !part2Path) {
  console.error('Usage: node verify_cost73d_win7_certificate_independent.mjs <part1> <part2>');
  process.exit(2);
}

const part1 = fs.readFileSync(part1Path, 'utf8');
const part2 = fs.readFileSync(part2Path, 'utf8');
const certificate = part1 + part2;
const strategy = parseCertificate(certificate);
const parent = BigInt('0x' + PARENT);
const root = BigInt('0x' + ROOT);
if ((parent | BIT[MOVE]) !== root) fail('root is not parent + bit 48');

const parentPoints = pointsOf(parent);
const rootPoints = pointsOf(root);
if (parentPoints.length !== 6 || rootPoints.length !== 7) fail('wrong parent/root stone count');
if (!isSafe(parentPoints) || !isSafe(rootPoints)) fail('unsafe parent or root');

const parentOptions = legalOfPoints(parentPoints);
if (countBits(parentOptions) !== 73) fail('parent legal-move count is not 73');
if ((parentOptions & BIT[MOVE]) === 0n) fail('bit 48 is not legal at the parent');

const rootOptions = legalOfPoints(rootPoints);
const rootMobility = countBits(rootOptions);
if (rootMobility !== 59) fail('root loser mobility is not 59');

const consumedUnion = new Set();
const subrootStats = [];
let totalSeen = 0;
let totalTerminals = 0;
let totalOpponentEdges = 0;
let terminalMin = 999;
let terminalMax = 0;

for (let move = 0; move < N; move++) {
  if ((rootOptions & BIT[move]) === 0n) continue;
  const result = verifySubRoot(strategy, root | BIT[move]);
  for (const key of result.consumed) consumedUnion.add(key);
  totalSeen += result.seen;
  totalTerminals += result.terminals;
  totalOpponentEdges += result.opponentEdges;
  terminalMin = Math.min(terminalMin, result.terminalMin);
  terminalMax = Math.max(terminalMax, result.terminalMax);
  subrootStats.push({
    move,
    seen: result.seen,
    terminals: result.terminals,
    opponentEdges: result.opponentEdges,
    terminalRange: [result.terminalMin, result.terminalMax]
  });
}

const missing = [];
for (const key of strategy.keys()) {
  if (!consumedUnion.has(key)) missing.push(key);
}
const extra = [];
for (const key of consumedUnion) {
  if (!strategy.has(key)) extra.push(key);
}
if (missing.length !== 0 || extra.length !== 0) {
  fail('certificate union mismatch: missing=' + missing.length + ' extra=' + extra.length);
}
if (subrootStats.length !== 59) fail('wrong sub-root count');
if (terminalMin < 13 || terminalMax > 17) fail('terminal stone range outside [13,17]');

console.log(JSON.stringify({
  parent: PARENT,
  parentStones: parentPoints.length,
  parentSafe: true,
  parentLegalMoves: countBits(parentOptions),
  addedMove: MOVE,
  addedMoveLegal: true,
  root: ROOT,
  rootStones: rootPoints.length,
  rootSafe: true,
  rootLoserMobility: rootMobility,
  partBytes: [Buffer.byteLength(part1), Buffer.byteLength(part2)],
  certificateBytes: Buffer.byteLength(certificate),
  nonemptyLines: 66682,
  certificateRows: strategy.size,
  subroots: subrootStats.length,
  allSubrootsPass: true,
  consumedWinnerStates: consumedUnion.size,
  missing: missing.length,
  extra: extra.length,
  totalSeenAcrossSubroots: totalSeen,
  totalTerminals,
  totalOpponentEdges,
  terminalStoneRange: [terminalMin, terminalMax],
  tripleCacheEntries: cache.size,
  perSubrootSummary: {
    minSeen: Math.min(...subrootStats.map(x => x.seen)),
    maxSeen: Math.max(...subrootStats.map(x => x.seen)),
    minTerminals: Math.min(...subrootStats.map(x => x.terminals)),
    maxTerminals: Math.max(...subrootStats.map(x => x.terminals))
  }
}, null, 2));
