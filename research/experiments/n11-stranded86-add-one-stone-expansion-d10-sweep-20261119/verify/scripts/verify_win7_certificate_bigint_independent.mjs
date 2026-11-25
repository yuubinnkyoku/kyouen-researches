#!/usr/bin/env node
// Independent exact verifier for n11-terminal-strategy-v1 WIN7 certificates.
// Uses BigInt 3x3 cofactor expansion; no solver, verdict cache, or repo verifier import.
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const certPath = process.argv[2];
if (!certPath) {
  process.stderr.write("usage: node verify_win7_certificate_bigint_independent.mjs CERT [EXPECTED_MOBILITY]\n");
  process.exit(2);
}
const expectedMobility = process.argv[3] === undefined ? null : Number(process.argv[3]);
const text = readFileSync(resolve(certPath), "utf8");
const lines = text.split(/\r?\n/).filter(Boolean);
if (lines.length < 3) throw new Error("certificate is too short");

const header = lines[0].trim();
if (header !== "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS") {
  throw new Error("unexpected certificate header: " + header);
}
const rootFields = lines[1].trim().split(/\s+/);
if (rootFields.length !== 2 || rootFields[0] !== "root" || !/^[0-9a-f]{32}$/.test(rootFields[1])) {
  throw new Error("invalid root line");
}
const rootHex = rootFields[1];

const strategy = new Map();
let rowsSorted = true;
let previousHex = "";
for (const line of lines.slice(2)) {
  const match = line.trim().match(/^([0-9a-f]{32})\s+(\d+)$/);
  if (!match) throw new Error("invalid strategy row: " + line);
  const hex = match[1];
  const move = Number(match[2]);
  if (move < 0 || move >= 121) throw new Error("move outside board: " + line);
  if (strategy.has(hex)) throw new Error("duplicate strategy row: " + hex);
  if (previousHex && hex < previousHex) rowsSorted = false;
  previousHex = hex;
  strategy.set(hex, move);
}

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

function det3(m) {
  const [[a,b,c],[d,e,f],[g,h,i]] = m;
  return a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g);
}

// If rows a,b,c are lifted to [x²+y²,x,y,1], expansion along row d
// gives these four exact integer coefficients.
function coefficientsForTriple(a, b, c) {
  const rows = [a,b,c].map(bit => {
    const x = BigInt(bit % 11);
    const y = BigInt(Math.floor(bit / 11));
    return [x*x + y*y, x, y, 1n];
  });
  return Array.from({length: 4}, (_, column) => {
    const minor = rows.map(row => row.filter((_, j) => j !== column));
    const determinant = det3(minor);
    return column % 2 === 0 ? -determinant : determinant;
  });
}

function forbiddenByTriple(a, b, c) {
  const key = a * 14641 + b * 121 + c;
  const cached = forbiddenCache.get(key);
  if (cached !== undefined) return cached;
  const coeff = coefficientsForTriple(a, b, c);
  let mask = 0n;
  for (let d = 0; d < 121; d++) {
    if (d === a || d === b || d === c) continue;
    const x = BigInt(d % 11);
    const y = BigInt(Math.floor(d / 11));
    if (coeff[0] * (x*x + y*y) + coeff[1] * x + coeff[2] * y + coeff[3] === 0n) {
      mask |= 1n << BigInt(d);
    }
  }
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

function determinant4(a, b, c, d) {
  const coeff = coefficientsForTriple(a, b, c);
  const x = BigInt(d % 11);
  const y = BigInt(Math.floor(d / 11));
  return coeff[0] * (x*x + y*y) + coeff[1] * x + coeff[2] * y + coeff[3];
}

function isSafe(points) {
  for (let a = 0; a < points.length; a++) {
    for (let b = a + 1; b < points.length; b++) {
      for (let c = b + 1; c < points.length; c++) {
        for (let d = c + 1; d < points.length; d++) {
          if (determinant4(points[a], points[b], points[c], points[d]) === 0n) return false;
        }
      }
    }
  }
  return true;
}

const root = BigInt("0x" + rootHex);
const rootPoints = pointsOf(root);
if (rootPoints.length !== 7) throw new Error("root does not contain seven stones");
if (!isSafe(rootPoints)) throw new Error("root is not safe");
const rootMoves = bitsOf(legalMask(rootPoints));
if (expectedMobility !== null && rootMoves.length !== expectedMobility) {
  throw new Error("root mobility mismatch: " + rootMoves.length + " != " + expectedMobility);
}
if (rootMoves.length === 0) throw new Error("WIN7 root has no opponent replies");

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
  while (stack.length) {
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
      if (((options >> BigInt(move)) & 1n) === 0n) throw new Error("illegal strategy move at " + hex);
      consumed.add(hex);
      stack.push([board | (1n << BigInt(move)), depth + 1]);
    } else {
      loserStates++;
      const replies = bitsOf(options);
      loserReplyEdges += replies.length;
      for (const move of replies) stack.push([board | (1n << BigInt(move)), depth + 1]);
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
  method: "BigInt 3x3 cofactor expansion of the exact lifted determinant [x²+y²,x,y,1]; no floating point",
  root_hex: rootHex,
  root_stones: rootPoints.length,
  root_safe: true,
  root_mobility: rootMoves.length,
  strategy_rows: strategy.size,
  rows_sorted_unique: rowsSorted && strategy.size === lines.length - 2,
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
