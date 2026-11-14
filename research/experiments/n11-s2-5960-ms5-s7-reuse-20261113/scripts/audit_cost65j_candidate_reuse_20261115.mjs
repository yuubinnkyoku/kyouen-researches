#!/usr/bin/env node
// Independently audit the cost65j S7 candidate set and reuse one published WIN7 certificate.
// Run from the repository root: node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65j_candidate_reuse_20261115.mjs

import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

const OUT = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output";
const CLAIM_PATH = OUT + "/class2-lane-cost65j-inflight-20261115.json";
const CERT_DIR = OUT + "/class2-lane-cost63a-certificates";
const PART1 = CERT_DIR + "/bit97-root-00000002000000809102000800000000.cert.part1of2";
const PART2 = CERT_DIR + "/bit97-root-00000002000000809102000800000000.cert.part2of2";
const EXPECTED_PART_BLOBS = [
  "a33afbaba4c99511872108223b70c1f15e786db1",
  "af1545ee1ebd70ab7f48274732678c15c286fa12",
];
const SOURCE_COMMITS = [
  "ebe98af00406ba6c4a5d1b959578d1d696dc0444",
  "15bad4487c78e21fc59af53ed5f89b5af693368f",
];
const EXPECTED_S5 = "00000000000000809102000000000000";
const EXPECTED_S6 = "00000000000000809102000080000000";
const EXPECTED_SOURCE_ROOT = "00000002000000809102000800000000";
const TARGET_BIT = 79;
const SOURCE_ADDED_BIT = 35;
const TRANSFORM_INDEX = 5;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
function popcount(mask) {
  let n = 0;
  while (mask) { mask &= mask - 1n; n++; }
  return n;
}
function pointsOf(mask) {
  const out = [];
  for (let p = 0; p < 121; p++) if ((mask >> BigInt(p)) & 1n) out.push(p);
  return out;
}
function occupiedMask(points) {
  let mask = 0n;
  for (const p of points) mask |= 1n << BigInt(p);
  return mask;
}
function det3(a,b,c,d,e,f,g,h,i) {
  return a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g);
}
// Exact cofactor expansion of a 4x4 determinant; no floating point.
function det4(m) {
  let total = 0n;
  for (let col = 0; col < 4; col++) {
    const minor = [];
    for (let row = 1; row < 4; row++) {
      const values = [];
      for (let c = 0; c < 4; c++) if (c !== col) values.push(m[row][c]);
      minor.push(values);
    }
    const d = det3(
      minor[0][0],minor[0][1],minor[0][2],
      minor[1][0],minor[1][1],minor[1][2],
      minor[2][0],minor[2][1],minor[2][2],
    );
    total += (col % 2 ? -1n : 1n) * m[0][col] * d;
  }
  return total;
}
const XY = Array.from({ length: 121 }, (_, p) => [BigInt(p % 11), BigInt(Math.floor(p / 11))]);
const tripleCache = new Map();
function forbiddenMask(a,b,c) {
  if (a > b) [a,b] = [b,a];
  if (b > c) [b,c] = [c,b];
  if (a > b) [a,b] = [b,a];
  const key = a * 14641 + b * 121 + c;
  const old = tripleCache.get(key);
  if (old !== undefined) return old;
  const [x1,y1] = XY[a], [x2,y2] = XY[b], [x3,y3] = XY[c];
  const s1 = x1*x1 + y1*y1, s2 = x2*x2 + y2*y2, s3 = x3*x3 + y3*y3;
  const D = det3(x1,y1,1n, x2,y2,1n, x3,y3,1n);
  let mask = 0n;
  if (D === 0n) {
    const dx = x2-x1, dy = y2-y1;
    for (let p = 0; p < 121; p++) {
      if (p === a || p === b || p === c) continue;
      const [x,y] = XY[p];
      if (dx*(y-y1)-dy*(x-x1) === 0n) mask |= 1n << BigInt(p);
    }
  } else {
    const A = det3(-s1,y1,1n, -s2,y2,1n, -s3,y3,1n);
    const B = det3(x1,-s1,1n, x2,-s2,1n, x3,-s3,1n);
    const C = det3(x1,y1,-s1, x2,y2,-s2, x3,y3,-s3);
    for (let p = 0; p < 121; p++) {
      if (p === a || p === b || p === c) continue;
      const [x,y] = XY[p], s = x*x + y*y;
      if (D*s + A*x + B*y + C === 0n) mask |= 1n << BigInt(p);
    }
  }
  tripleCache.set(key,mask);
  return mask;
}
function isSafe(points) {
  const occupied = occupiedMask(points);
  for (let i=0;i<points.length;i++) for (let j=i+1;j<points.length;j++) for (let k=j+1;k<points.length;k++) {
    assert((forbiddenMask(points[i],points[j],points[k]) & occupied) === 0n, "unsafe position");
  }
  return true;
}
const FULL = (1n << 121n) - 1n;
function legalMask(points) {
  let banned = occupiedMask(points);
  for (let i=0;i<points.length;i++) for (let j=i+1;j<points.length;j++) for (let k=j+1;k<points.length;k++) {
    banned |= forbiddenMask(points[i],points[j],points[k]);
  }
  return FULL & ~banned;
}
function exactLegalBits(mask) {
  const stones = pointsOf(mask);
  const rows = stones.map(p => {
    const [x,y] = XY[p];
    return [x*x+y*y,x,y,1n];
  });
  const result = [];
  for (let p=0;p<121;p++) {
    if ((mask >> BigInt(p)) & 1n) continue;
    const [x,y] = XY[p], candidate = [x*x+y*y,x,y,1n];
    let forbidden = false;
    for (let i=0;i<stones.length && !forbidden;i++)
      for (let j=i+1;j<stones.length && !forbidden;j++)
        for (let k=j+1;k<stones.length;k++)
          if (det4([rows[i],rows[j],rows[k],candidate]) === 0n) { forbidden = true; break; }
    if (!forbidden) result.push(p);
  }
  return result;
}
const D4 = [
  (x,y)=>[x,y], (x,y)=>[y,10-x], (x,y)=>[10-x,10-y], (x,y)=>[10-y,x],
  (x,y)=>[10-x,y], (x,y)=>[x,10-y], (x,y)=>[y,x], (x,y)=>[10-y,10-x],
];
function transformPoint(p,t) {
  const [x,y] = XY[p];
  const [u,v] = D4[t](Number(x),Number(y));
  return 11*v+u;
}
function transformMask(mask,t) {
  let out = 0n;
  for (let p=0;p<121;p++) if ((mask >> BigInt(p)) & 1n)
    out |= 1n << BigInt(transformPoint(p,t));
  return out;
}
function canonicalD4(mask) {
  return D4.map((_,t)=>transformMask(mask,t).toString(16).padStart(32,"0")).sort()[0];
}
function gitBlobSha(raw) {
  const header = Buffer.from("blob " + raw.length + "\0","utf8");
  return createHash("sha1").update(Buffer.concat([header,raw])).digest("hex");
}
function verifySubroot(strategy,subroot) {
  const seen = new Set(), consumed = [];
  let terminals = 0, opponentEdges = 0, minTerminal = 99, maxTerminal = 0;
  const stack = [[subroot,0]];
  while (stack.length) {
    const [board,depth] = stack.pop();
    const hex = board.toString(16).padStart(32,"0");
    if (seen.has(hex)) continue;
    seen.add(hex);
    const points = pointsOf(board), options = legalMask(points);
    if (options === 0n) {
      assert(depth % 2 === 1, "terminal on winner-to-move ply: " + hex);
      assert(!strategy.has(hex), "strategy row on terminal: " + hex);
      terminals++;
      minTerminal = Math.min(minTerminal,points.length);
      maxTerminal = Math.max(maxTerminal,points.length);
    } else if (depth % 2 === 0) {
      const move = strategy.get(hex);
      assert(move !== undefined, "missing winner move: " + hex);
      assert((options & (1n << BigInt(move))) !== 0n, "illegal winner move: " + hex);
      consumed.push(hex);
      stack.push([board | (1n << BigInt(move)),depth+1]);
    } else {
      assert(!strategy.has(hex), "strategy row on opponent turn: " + hex);
      let rest = options;
      while (rest) {
        const bit = rest & -rest;
        rest -= bit;
        opponentEdges++;
        stack.push([board | bit,depth+1]);
      }
    }
  }
  return { seen:seen.size, consumed, terminals, opponentEdges, terminalRange:[minTerminal,maxTerminal] };
}

const claim = JSON.parse(fs.readFileSync(CLAIM_PATH,"utf8"));
assert(claim.s5 === EXPECTED_S5 && claim.s6_child === EXPECTED_S6, "cost65j target changed");
assert(claim.legal_candidates_total === 65, "cost65j legal candidate total changed");
const s5 = BigInt("0x" + claim.s5), child = BigInt("0x" + claim.s6_child);
const s5Points = pointsOf(s5), childPoints = pointsOf(child);
assert(s5Points.length === 5 && childPoints.length === 6, "S5/S6 stone count mismatch");
isSafe(s5Points); isSafe(childPoints);
assert((child & s5) === s5 && popcount(child ^ s5) === 1, "S6 is not a one-stone extension of S5");
const s5AddedBit = pointsOf(child ^ s5)[0];
assert((legalMask(s5Points) & (1n << BigInt(s5AddedBit))) !== 0n, "S5-to-S6 extension is illegal");

const legalBits = exactLegalBits(child);
assert(legalBits.length === 65, "independent exact legal count mismatch");
assert(JSON.stringify(legalBits) === JSON.stringify(claim.candidate_bits), "independent legal bits differ from claim");
const candidateRoots = legalBits.map(bit => child | (1n << BigInt(bit)));
const candidateD4 = new Set(candidateRoots.map(canonicalD4));
assert(candidateD4.size === 65, "cost65j candidates are not 65 distinct D4 classes");

const raw1 = fs.readFileSync(PART1), raw2 = fs.readFileSync(PART2);
const partBlobs = [gitBlobSha(raw1),gitBlobSha(raw2)];
assert(JSON.stringify(partBlobs) === JSON.stringify(EXPECTED_PART_BLOBS), "certificate part Git blob SHA mismatch");
const content = Buffer.concat([raw1,raw2]).toString("utf8");
const lines = content.split(/\r?\n/).filter(line=>line.trim().length>0);
assert(lines[0] === "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS", "certificate header mismatch");
assert(lines[1] === "root " + EXPECTED_SOURCE_ROOT, "certificate root mismatch");
const sourceRoot = BigInt("0x" + EXPECTED_SOURCE_ROOT);
const sourcePoints = pointsOf(sourceRoot);
assert(sourcePoints.length === 7, "certificate root is not seven stones");
isSafe(sourcePoints);

const strategy = new Map();
let previous = "";
for (const line of lines.slice(2)) {
  const parts = line.trim().split(/\s+/);
  assert(parts.length === 2, "malformed strategy row");
  const [hex,moveText] = parts;
  assert(/^[0-9a-f]{32}$/.test(hex) && hex > previous, "unsorted or duplicate strategy row");
  previous = hex;
  const board = BigInt("0x" + hex), move = Number(moveText);
  assert(board <= FULL && popcount(board) >= 8 && popcount(board) % 2 === 0, "invalid strategy state");
  assert(Number.isInteger(move) && move >= 0 && move < 121, "invalid strategy move");
  strategy.set(hex,move);
}

const rootOptions = legalMask(sourcePoints);
const mobility = popcount(rootOptions);
let subroots = 0, seenSum = 0, terminals = 0, opponentEdges = 0, terminalMin = 99, terminalMax = 0;
const consumed = new Set();
for (let rest=rootOptions;rest;) {
  const bit = rest & -rest;
  rest -= bit;
  const stats = verifySubroot(strategy,sourceRoot | bit);
  subroots++;
  seenSum += stats.seen;
  terminals += stats.terminals;
  opponentEdges += stats.opponentEdges;
  terminalMin = Math.min(terminalMin,stats.terminalRange[0]);
  terminalMax = Math.max(terminalMax,stats.terminalRange[1]);
  for (const key of stats.consumed) consumed.add(key);
}
assert(subroots === mobility, "subroot count differs from root mobility");
assert(consumed.size === strategy.size, "strategy row union size mismatch");
for (const key of strategy.keys()) assert(consumed.has(key), "unconsumed strategy row: " + key);
assert(terminalMin >= 13 && terminalMax <= 17, "terminal stone range mismatch");
assert(strategy.size === 39159 && mobility === 49 && seenSum === 88265 && terminals === 13150 && opponentEdges === 82167, "certificate metrics differ from audited values");

const targetRoot = child | (1n << BigInt(TARGET_BIT));
assert(legalBits.includes(TARGET_BIT), "target bit 79 is not legal");
assert(canonicalD4(targetRoot) === canonicalD4(sourceRoot), "source certificate is not D4-equivalent to target candidate");
assert(transformMask(sourceRoot,TRANSFORM_INDEX) === targetRoot, "expected D4 transform does not map source root to target root");
const mappedSourceBit = sourcePoints.find(p=>transformPoint(p,TRANSFORM_INDEX)===TARGET_BIT);
assert(mappedSourceBit === SOURCE_ADDED_BIT, "source added bit does not map to target bit 79");
const sourceParent = sourceRoot & ~(1n << BigInt(SOURCE_ADDED_BIT));
assert(transformMask(sourceParent,TRANSFORM_INDEX) === child, "source six-stone parent does not map to cost65j S6 child");
assert(isSafe(pointsOf(sourceParent)), "source six-stone parent is unsafe");
assert((legalMask(pointsOf(sourceParent)) & (1n << BigInt(SOURCE_ADDED_BIT))) !== 0n, "source added bit is not legal");
assert((legalMask(childPoints) & (1n << BigInt(TARGET_BIT))) !== 0n, "target bit 79 is not legal");

const result = {
  schema: "n11-class2-cost65j-candidate-reuse-audit-v1",
  source_claim: CLAIM_PATH,
  source_certificate_parts: [
    { path:PART1, git_blob_sha:partBlobs[0], bytes:raw1.length, commit:SOURCE_COMMITS[0] },
    { path:PART2, git_blob_sha:partBlobs[1], bytes:raw2.length, commit:SOURCE_COMMITS[1] },
  ],
  candidate_enumeration: {
    s5_hex:claim.s5, s6_hex:claim.s6_child,
    s5_stones:5, s6_stones:6, s5_to_s6_added_bit:s5AddedBit,
    exact_integer_determinant:"4x4 cofactor expansion over BigInt",
    legal_candidate_count:legalBits.length,
    claim_bits_match:true,
    candidate_bits:legalBits,
    distinct_d4_candidate_orbits:candidateD4.size,
  },
  independently_verified_win7_certificate: {
    root_hex:EXPECTED_SOURCE_ROOT,
    root_stones:7, root_safe:true, root_mobility:mobility,
    strategy_rows:strategy.size, subroots_verified:subroots,
    subroot_seen_states_sum:seenSum, terminal_visits:terminals,
    opponent_reply_edges:opponentEdges, terminal_range:[terminalMin,terminalMax],
    consumed_rows:consumed.size, missing_rows:0, extra_rows:0,
    exact_geometry:"BigInt Cramer circle equation and exact collinear-line cross products",
  },
  d4_reuse: {
    target_bit:TARGET_BIT,
    target_root_hex:targetRoot.toString(16).padStart(32,"0"),
    source_root_hex:EXPECTED_SOURCE_ROOT,
    transform_index:TRANSFORM_INDEX,
    transform:"(x,y) -> (x,10-y)",
    source_added_bit:SOURCE_ADDED_BIT,
    source_parent_hex:sourceParent.toString(16).padStart(32,"0"),
    target_parent_hex:claim.s6_child,
    parent_maps_exactly:true,
  },
  effect: {
    candidate_roots_before:legalBits.length,
    candidates_reused_from_this_certificate:1,
    candidates_needing_new_win7_evidence_after_this_reuse:legalBits.length-1,
    s6_parent_closed:false,
    frontier_changed:false,
  },
  interpretation_guard:"This reuses one individual WIN7 seven-stone root. It does not classify the six-stone parent: all of its legal seven-stone children must be covered before the parent can be closed. No S6 frontier count or 11x11 winner is changed.",
};
const outputPath = OUT + "/class2-lane-cost65j-candidate-reuse-audit-20261115.json";
fs.writeFileSync(outputPath,JSON.stringify(result,null,2)+"\n");
process.stdout.write(JSON.stringify(result,null,2)+"\n");
