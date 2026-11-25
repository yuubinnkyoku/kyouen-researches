// Independent BigInt audit for the cost-56a WIN7 strategy certificate.
// Node >= 22; no solver/verifier imports, no floating-point geometry.
// Run from any directory:
//   node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost56a_bigint_certificate.mjs
import fs from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT_HEX = '00000000020000803202020000000000';
const HEADER = 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS';
const N = 121;
const FULL = (1n << 121n) - 1n;

function requireThat(condition, message) {
  if (!condition) throw new Error(message);
}
function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 ? process.argv[i + 1] : fallback;
}
function det3(m) {
  return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
       - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
       + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
}
// Laplace expansion over BigInt: deliberately different from the repository
// verifier's Number/Bareiss implementation.
function det4Big(points) {
  const a = points.map(p => {
    const x = BigInt(p % 11), y = BigInt(Math.floor(p / 11));
    return [x * x + y * y, x, y, 1n];
  });
  let determinant = 0n;
  for (let j = 0; j < 4; j++) {
    const minor = [];
    for (let i = 1; i < 4; i++) {
      const row = [];
      for (let k = 0; k < 4; k++) if (k !== j) row.push(a[i][k]);
      minor.push(row);
    }
    determinant += (j % 2 === 0 ? 1n : -1n) * a[0][j] * det3(minor);
  }
  return determinant;
}
function pointsOf(mask) {
  const points = [];
  for (let i = 0; i < N; i++) if ((mask >> BigInt(i)) & 1n) points.push(i);
  return points;
}
function popcount(mask) {
  let count = 0;
  while (mask) { mask &= mask - 1n; count++; }
  return count;
}
const tripleCache = new Map();
let determinantEvaluations = 0;
function forbiddenByTriple(a, b, c) {
  // pointsOf() supplies strictly increasing a,b,c.
  const key = a * 14641 + b * 121 + c;
  const cached = tripleCache.get(key);
  if (cached !== undefined) return cached;
  let mask = 0n;
  for (let d = 0; d < N; d++) {
    if (d === a || d === b || d === c) continue;
    determinantEvaluations++;
    if (det4Big([a, b, c, d]) === 0n) mask |= 1n << BigInt(d);
  }
  tripleCache.set(key, mask);
  return mask;
}
function legalOfPoints(points) {
  let banned = 0n;
  for (const p of points) banned |= 1n << BigInt(p);
  for (let i = 0; i < points.length; i++)
    for (let j = i + 1; j < points.length; j++)
      for (let k = j + 1; k < points.length; k++)
        banned |= forbiddenByTriple(points[i], points[j], points[k]);
  return FULL & ~banned;
}
function transform(mask, kind) {
  let out = 0n;
  for (let i = 0; i < N; i++) {
    if (((mask >> BigInt(i)) & 1n) === 0n) continue;
    const x = i % 11, y = Math.floor(i / 11);
    let tx, ty;
    switch (kind) {
      case 0: tx = x; ty = y; break;
      case 1: tx = 10 - y; ty = x; break;
      case 2: tx = 10 - x; ty = 10 - y; break;
      case 3: tx = y; ty = 10 - x; break;
      case 4: tx = 10 - x; ty = y; break;
      case 5: tx = 10 - y; ty = 10 - x; break;
      case 6: tx = x; ty = 10 - y; break;
      case 7: tx = y; ty = x; break;
      default: throw new Error('bad D4 transform');
    }
    out |= 1n << BigInt(ty * 11 + tx);
  }
  return out;
}
function canonicalHex(mask) {
  let best = null;
  for (let k = 0; k < 8; k++) {
    const candidate = transform(mask, k);
    if (best === null || candidate < best) best = candidate;
  }
  return best.toString(16).padStart(32, '0');
}
function verifySubRoot(strategy, subRootHex) {
  const start = BigInt('0x' + subRootHex);
  const points = pointsOf(start);
  requireThat(points.length === 8, 'sub-root must have 8 stones');
  const seen = new Set();
  const consumed = [];
  const stack = [[start, 0]];
  let terminals = 0, opponentEdges = 0, terminalMin = 121, terminalMax = 0;
  while (stack.length) {
    const [board, depth] = stack.pop();
    const hex = board.toString(16).padStart(32, '0');
    if (seen.has(hex)) continue;
    seen.add(hex);
    const boardPoints = pointsOf(board);
    const options = legalOfPoints(boardPoints);
    if (options === 0n) {
      requireThat(depth % 2 === 1, 'winner has no legal move at ' + hex);
      requireThat(!strategy.has(hex), 'terminal has a strategy row at ' + hex);
      terminals++;
      terminalMin = Math.min(terminalMin, boardPoints.length);
      terminalMax = Math.max(terminalMax, boardPoints.length);
      continue;
    }
    if (depth % 2 === 0) {
      const move = strategy.get(hex);
      requireThat(move !== undefined, 'missing winner move at ' + hex);
      requireThat(((options >> BigInt(move)) & 1n) !== 0n, 'illegal winner move at ' + hex);
      consumed.push(hex);
      stack.push([board | (1n << BigInt(move)), depth + 1]);
    } else {
      requireThat(!strategy.has(hex), 'strategy row on opponent turn at ' + hex);
      let remaining = options;
      while (remaining) {
        const bit = remaining & -remaining;
        remaining -= bit;
        opponentEdges++;
        stack.push([board | bit, depth + 1]);
      }
    }
  }
  return {
    seen: seen.size,
    consumed,
    terminals,
    opponentEdges,
    terminalRange: [terminalMin, terminalMax]
  };
}

const defaultCert = fileURLToPath(new URL(
  '../output/class2-lane-cost56a-certificates/bit89-root-' + ROOT_HEX + '.cert',
  import.meta.url
));
const defaultManifestDir = fileURLToPath(new URL(
  '../../n11-s2-5960-milestone5-20261112/output/',
  import.meta.url
));
const certPath = arg('cert', defaultCert);
const rootHex = arg('root', ROOT_HEX).toLowerCase();
const manifestDir = arg('manifest-dir', defaultManifestDir);
const rawBytes = fs.readFileSync(certPath);
const raw = rawBytes.toString('utf8');
const lines = raw.split(/\r?\n/).filter(line => line.trim() !== '');
requireThat(lines[0] === HEADER, 'wrong certificate header');
requireThat(lines[1] === 'root ' + rootHex, 'wrong certificate root');

const strategy = new Map();
let previous = '';
for (const line of lines.slice(2)) {
  const parts = line.split(' ');
  requireThat(parts.length === 2, 'malformed strategy row');
  const [hex, moveText] = parts;
  requireThat(hex.length === 32 && /^[0-9a-f]{32}$/.test(hex), 'bad board encoding');
  requireThat(hex > previous, 'unsorted or duplicate strategy row');
  requireThat(/^\d+$/.test(moveText), 'bad move encoding');
  const board = BigInt('0x' + hex), move = Number(moveText);
  requireThat(board <= FULL && move >= 0 && move < N, 'out-of-range strategy row');
  strategy.set(hex, move);
  previous = hex;
}

const root = BigInt('0x' + rootHex);
const rootPoints = pointsOf(root);
requireThat(rootPoints.length === 7, 'root must have 7 stones');
for (let i = 0; i < 7; i++)
  for (let j = i + 1; j < 7; j++)
    for (let k = j + 1; k < 7; k++)
      for (let q = k + 1; q < 7; q++)
        requireThat(det4Big([rootPoints[i], rootPoints[j], rootPoints[k], rootPoints[q]]) !== 0n,
          'unsafe root: four cocircular/collinear points');
const rootMoves = legalOfPoints(rootPoints);
const rootMobility = popcount(rootMoves);

let totalSeenAcrossSubroots = 0, consumedVisits = 0;
let totalTerminals = 0, totalOpponentEdges = 0;
let terminalMin = 121, terminalMax = 0;
const consumedUnion = new Set();
const subrootStats = [];
let remainingMoves = rootMoves;
while (remainingMoves) {
  const bit = remainingMoves & -remainingMoves;
  remainingMoves -= bit;
  const move = bit.toString(2).length - 1;
  const subRootHex = (root | bit).toString(16).padStart(32, '0');
  const stats = verifySubRoot(strategy, subRootHex);
  totalSeenAcrossSubroots += stats.seen;
  consumedVisits += stats.consumed.length;
  totalTerminals += stats.terminals;
  totalOpponentEdges += stats.opponentEdges;
  terminalMin = Math.min(terminalMin, stats.terminalRange[0]);
  terminalMax = Math.max(terminalMax, stats.terminalRange[1]);
  for (const key of stats.consumed) consumedUnion.add(key);
  subrootStats.push({
    move,
    seen: stats.seen,
    consumed: stats.consumed.length,
    terminals: stats.terminals,
    opponentEdges: stats.opponentEdges,
    terminalRange: stats.terminalRange
  });
}

const missing = [...strategy.keys()].filter(key => !consumedUnion.has(key));
const extra = [...consumedUnion].filter(key => !strategy.has(key));
requireThat(missing.length === 0 && extra.length === 0,
  'strategy-row union mismatch: missing=' + missing.length + ' extra=' + extra.length);

// Recompute the seven one-stone deletions under D4 and match the six-stone worklist.
const manifestRows = new Map();
let manifestLineCount = 0;
for (let part = 1; part <= 6; part++) {
  const file = manifestDir + '/ms5_s6_manifest_part' + part + '.csv';
  const text = fs.readFileSync(file, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const [hex, costText, classesText] = line.split(',');
    if (!/^[0-9a-f]{32}$/.test(hex)) continue; // skips optional header
    requireThat(!manifestRows.has(hex), 'duplicate S6 worklist row ' + hex);
    manifestRows.set(hex, { cost: Number(costText), classes: Number(classesText) });
    manifestLineCount++;
  }
}
const parentLifts = [];
for (const removed of rootPoints) {
  const parent = root ^ (1n << BigInt(removed));
  const parentHex = canonicalHex(parent);
  parentLifts.push({
    winningMove: removed,
    parentHex,
    worklist: manifestRows.get(parentHex) ?? null
  });
}
const worklistHits = parentLifts.filter(row => row.worklist !== null);

const result = {
  schema: 'n11-cost56a-win7-independent-bigint-audit-v1',
  status: 'PASS',
  certificate: {
    path: certPath,
    sha256: createHash('sha256').update(rawBytes).digest('hex'),
    bytes: rawBytes.length,
    nonemptyLines: lines.length,
    strategyRows: strategy.size
  },
  root: { hex: rootHex, stones: rootPoints.length, safe: true, legalLoserMoves: rootMob },
  verification: {
    subrootsPassed: subrootStats.length,
    totalSeenAcrossSubroots,
    consumedWinnerStateVisits: consumedVisits,
    uniqueConsumedWinnerStates: consumedUnion.size,
    terminals: totalTerminals,
    opponentEdges,
    terminalStoneRange: [terminalMin, terminalMax],
    rowUnionMissing: missing.length,
    rowUnionExtra: extra.length,
    geometry: 'BigInt 3x3-minor expansion of det([x^2+y^2,x,y,1]); no floating point',
    distinctTriplesCached: tripleCache.size,
    exactDeterminantEvaluations: determinantEvaluations
  },
  s6ParentLifts: {
    manifestRows: manifestLineCount,
    uniqueManifestRows: manifestRows.size,
    totalD4Parents: parentLifts.length,
    worklistHits,
    allParentLifts: parentLifts
  },
  subrootStats
};
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
