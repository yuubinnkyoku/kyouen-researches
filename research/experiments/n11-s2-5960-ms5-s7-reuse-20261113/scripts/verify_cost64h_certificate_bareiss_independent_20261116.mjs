#!/usr/bin/env node
// Third independent verifier for cost-64h WIN7 strategy certificates.
// Exact arithmetic is a direct 4x4 BigInt Bareiss determinant, independent of
// the repository's 3x3-cofactor BigInt verifier and Number-Bareiss TypeScript verifier.
// Run from repository root:
//   node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64h_certificate_bareiss_independent_20261116.mjs CERT [EXPECTED_ROOT] [EXPECTED_MOBILITY]

import fs from "node:fs";
import { resolve } from "node:path";

const certPath = process.argv[2];
if (!certPath) {
  process.stderr.write("usage: node verify_cost64h_certificate_bareiss_independent_20261116.mjs CERT [EXPECTED_ROOT] [EXPECTED_MOBILITY]\n");
  process.exit(2);
}
const expectedRoot = process.argv[3] ?? null;
const expectedMobility = process.argv[4] === undefined ? null : Number(process.argv[4]);
const text = fs.readFileSync(resolve(certPath), "utf8");
const lines = text.split(/\r?\n/).filter(line => line.length > 0);
if (lines.length < 3) throw new Error("certificate is too short");
if (lines[0] !== "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS") {
  throw new Error("unexpected certificate header");
}
const rootFields = lines[1].trim().split(/\s+/);
if (rootFields.length !== 2 || rootFields[0] !== "root" || !/^[0-9a-f]{32}$/.test(rootFields[1])) {
  throw new Error("invalid root line");
}
const rootHex = rootFields[1];
if (expectedRoot !== null && rootHex !== expectedRoot) throw new Error("root differs from expected root");

const strategy = new Map();
let rowsSorted = true;
let previousHex = "";
for (const line of lines.slice(2)) {
  const match = line.trim().match(/^([0-9a-f]{32})\s+(\d+)$/);
  if (!match) throw new Error("invalid strategy row: " + line);
  const hex = match[1];
  const move = Number(match[2]);
  if (strategy.has(hex) || move < 0 || move >= 121) throw new Error("duplicate or invalid strategy row");
  if (previousHex && hex <= previousHex) rowsSorted = false;
  previousHex = hex;
  strategy.set(hex, move);
}
if (!rowsSorted || strategy.size !== lines.length - 2) throw new Error("strategy rows are not strictly sorted and unique");

const FULL = (1n << 121n) - 1n;
const forbiddenCache = new Map();
const legalCache = new Map();

function pointsOf(mask) {
  const points = [];
  for (let bit = 0; bit < 121; bit++) {
    if (((mask >> BigInt(bit)) & 1n) === 1n) points.push(bit);
  }
  return points;
}

// Direct 4x4 Bareiss elimination over BigInt; no floating point and no 3x3 cofactor expansion.
function determinant4(a, b, c, d) {
  const matrix = [a, b, c, d].map(bit => {
    const x = BigInt(bit % 11);
    const y = BigInt(Math.floor(bit / 11));
    return [x * x + y * y, x, y, 1n];
  });
  let sign = 1n;
  let divisor = 1n;
  for (let k = 0; k < 3; k++) {
    if (matrix[k][k] === 0n) {
      let swapped = false;
      for (let row = k + 1; row < 4; row++) {
        if (matrix[row][k] !== 0n) {
          [matrix[k], matrix[row]] = [matrix[row], matrix[k]];
          sign = -sign;
          swapped = true;
          break;
        }
      }
      if (!swapped) return 0n;
    }
    const pivot = matrix[k][k];
    for (let i = k + 1; i < 4; i++) {
      for (let j = k + 1; j < 4; j++) {
        const numerator = matrix[i][j] * pivot - matrix[i][k] * matrix[k][j];
        if (numerator % divisor !== 0n) throw new Error("non-integral Bareiss division");
        matrix[i][j] = numerator / divisor;
      }
      matrix[i][k] = 0n;
    }
    divisor = pivot;
  }
  return sign * matrix[3][3];
}

function forbiddenByTriple(a, b, c) {
  const key = a * 14641 + b * 121 + c;
  const cached = forbiddenCache.get(key);
  if (cached !== undefined) return cached;
  let mask = 0n;
  for (let d = 0; d < 121; d++) {
    if (d !== a && d !== b && d !== c && determinant4(a, b, c, d) === 0n) {
      mask |= 1n << BigInt(d);
    }
  }
  if (forbiddenCache.size >= 25000) forbiddenCache.clear();
  forbiddenCache.set(key, mask);
  return mask;
}

function legalMask(points) {
  const key = points.map(bit => bit.toString(16).padStart(2, "0")).join("");
  const cached = legalCache.get(key);
  if (cached !== undefined) return cached;
  let banned = 0n;
  for (const bit of points) banned |= 1n << BigInt(bit);
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      for (let k = j + 1; k < points.length; k++) {
        banned |= forbiddenByTriple(points[i], points[j], points[k]);
      }
    }
  }
  const result = FULL & ~banned;
  legalCache.set(key, result);
  return result;
}

function bitsOf(mask) {
  const bits = [];
  for (let bit = 0; bit < 121; bit++) {
    if (((mask >> BigInt(bit)) & 1n) === 1n) bits.push(bit);
  }
  return bits;
}

const root = BigInt("0x" + rootHex);
const rootPoints = pointsOf(root);
if (rootPoints.length !== 7) throw new Error("root does not contain seven stones");
for (let a = 0; a < 7; a++) {
  for (let b = a + 1; b < 7; b++) {
    for (let c = b + 1; c < 7; c++) {
      for (let d = c + 1; d < 7; d++) {
        if (determinant4(rootPoints[a], rootPoints[b], rootPoints[c], rootPoints[d]) === 0n) {
          throw new Error("root is not safe");
        }
      }
    }
  }
}

const rootMoves = bitsOf(legalMask(rootPoints));
if (rootMoves.length === 0) throw new Error("root has no opponent replies");
if (expectedMobility !== null && rootMoves.length !== expectedMobility) {
  throw new Error("root mobility mismatch: " + rootMoves.length + " != " + expectedMobility);
}

const consumed = new Set();
let visitedStates = 0;
let winnerStates = 0;
let loserStates = 0;
let loserReplyEdges = 0;
let terminalCount = 0;
let minTerminal = 99;
let maxTerminal = 0;

for (const rootMove of rootMoves) {
  const stack = [[root | (1n << BigInt(rootMove)), 0]];
  const seen = new Set();
  while (stack.length > 0) {
    const [board, depth] = stack.pop();
    const hex = board.toString(16).padStart(32, "0");
    if (seen.has(hex)) continue;
    seen.add(hex);
    visitedStates++;

    const points = pointsOf(board);
    const options = legalMask(points);
    if (options === 0n) {
      if (depth % 2 !== 1) throw new Error("winner is stuck at " + hex);
      if (strategy.has(hex)) throw new Error("terminal state has a strategy row: " + hex);
      terminalCount++;
      minTerminal = Math.min(minTerminal, points.length);
      maxTerminal = Math.max(maxTerminal, points.length);
      continue;
    }

    if (depth % 2 === 0) {
      winnerStates++;
      const move = strategy.get(hex);
      if (move === undefined) throw new Error("missing winner strategy row: " + hex);
      if (((options >> BigInt(move)) & 1n) === 0n) throw new Error("illegal winner move at " + hex);
      consumed.add(hex);
      stack.push([board | (1n << BigInt(move)), depth + 1]);
    } else {
      loserStates++;
      if (strategy.has(hex)) throw new Error("strategy row supplied on loser turn: " + hex);
      let replies = options;
      while (replies !== 0n) {
        const bit = replies & -replies;
        replies -= bit;
        loserReplyEdges++;
        stack.push([board | bit, depth + 1]);
      }
    }
  }
}

const missingRows = [...strategy.keys()].filter(hex => !consumed.has(hex));
const extraRows = [...consumed].filter(hex => !strategy.has(hex));
if (missingRows.length || extraRows.length) {
  throw new Error("strategy/consumed union mismatch: missing=" + missingRows.length + " extra=" + extraRows.length);
}
if (minTerminal < 13 || maxTerminal > 17) throw new Error("terminal range outside 13..17");

const result = {
  verdict: "WIN7 certificate independently verified",
  method: "direct BigInt 4x4 Bareiss determinant; complete all-reply traversal; no repository verifier import",
  root_hex: rootHex,
  root_stones: rootPoints.length,
  root_safe: true,
  root_mobility: rootMoves.length,
  strategy_rows: strategy.size,
  rows_sorted_unique: true,
  subroots_passed: rootMoves.length,
  consumed_winner_rows: consumed.size,
  union_missing: missingRows.length,
  union_extra: extraRows.length,
  visited_states_across_subroots: visitedStates,
  winner_states: winnerStates,
  loser_states: loserStates,
  loser_reply_edges: loserReplyEdges,
  terminal_count: terminalCount,
  terminal_range: [minTerminal, maxTerminal],
  forbidden_triple_cache_entries: forbiddenCache.size,
  legal_state_cache_entries: legalCache.size
};
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
