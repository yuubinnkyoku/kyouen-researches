#!/usr/bin/env node
// Third independent replay of the two cost-63f WIN7 certificates.
// Geometry is tested by an exact integer circumcenter equation; collinear triples
// are handled as lines. This imports neither search engines nor existing verifiers.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../..");
const EXP = resolve(ROOT, "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113");
const manifestPath = resolve(EXP, "output/class2-lane-cost63f-win7-certificates-20261115.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
const foldPath = resolve(EXP, "output/class-frontier-cost63f-receipts-recompute-20261115.json");
const fold = JSON.parse(readFileSync(foldPath, "utf8"));
const foldClaimPath = resolve(EXP, "output/class2-lane-cost63f-fold-inflight-20261115.json");
const foldClaim = JSON.parse(readFileSync(foldClaimPath, "utf8"));
const N = 121;
const FULL = (1n << 121n) - 1n;
const X = Array.from({ length: N }, (_, i) => i % 11);
const Y = Array.from({ length: N }, (_, i) => Math.floor(i / 11));
const Q = Array.from({ length: N }, (_, i) => X[i] * X[i] + Y[i] * Y[i]);
const tripleCache = new Map();
const legalCache = new Map();

function forbiddenByTriple(a, b, c) {
  const key = a * 14641 + b * 121 + c;
  if (tripleCache.has(key)) return tripleCache.get(key);
  const ux = X[b] - X[a], uy = Y[b] - Y[a];
  const vx = X[c] - X[a], vy = Y[c] - Y[a];
  const D = ux * vy - uy * vx;
  let mask = 0n;
  if (D === 0) {
    // Three collinear points determine their line, not an arbitrary circle.
    for (let d = 0; d < N; d++) {
      if (d === a || d === b || d === c) continue;
      const dx = X[d] - X[a], dy = Y[d] - Y[a];
      if (ux * dy - uy * dx === 0) mask |= 1n << BigInt(d);
    }
  } else {
    // Rational circumcenter C=(cxNum,cyNum)/(2D); test
    // D*(|d|^2-|a|^2) - cxNum*(xd-xa) - cyNum*(yd-ya) == 0.
    const qb = Q[b] - Q[a], qc = Q[c] - Q[a];
    const cxNum = qb * vy - qc * uy;
    const cyNum = ux * qc - vx * qb;
    for (let d = 0; d < N; d++) {
      if (d === a || d === b || d === c) continue;
      const dx = X[d] - X[a], dy = Y[d] - Y[a];
      if (D * (Q[d] - Q[a]) - cxNum * dx - cyNum * dy === 0) {
        mask |= 1n << BigInt(d);
      }
    }
  }
  tripleCache.set(key, mask);
  return mask;
}

function pointsOf(mask) {
  const out = [];
  for (let i = 0; i < N; i++) if ((mask >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function hexOf(mask) { return mask.toString(16).padStart(32, "0"); }
function legalMask(points) {
  const key = points.map(x => x.toString(16).padStart(2, "0")).join("");
  if (legalCache.has(key)) return legalCache.get(key);
  let banned = 0n;
  for (const p of points) banned |= 1n << BigInt(p);
  for (let i = 0; i < points.length; i++)
    for (let j = i + 1; j < points.length; j++)
      for (let k = j + 1; k < points.length; k++)
        banned |= forbiddenByTriple(points[i], points[j], points[k]);
  const result = FULL & ~banned;
  legalCache.set(key, result);
  return result;
}
function bitsOf(mask) {
  const out = [];
  for (let i = 0; i < N; i++) if ((mask >> BigInt(i)) & 1n) out.push(i);
  return out;
}
function assertRootSafe(points) {
  for (let i = 0; i < points.length; i++)
    for (let j = i + 1; j < points.length; j++)
      for (let k = j + 1; k < points.length; k++) {
        const bad = forbiddenByTriple(points[i], points[j], points[k]);
        for (let z = k + 1; z < points.length; z++) {
          if ((bad >> BigInt(points[z])) & 1n) throw new Error("unsafe root");
        }
      }
}

function verifyCertificate(bit) {
  const spec = manifest.certificates[String(bit)];
  const filePath = resolve(ROOT, spec.path);
  const bytes = readFileSync(filePath);
  const text = bytes.toString("utf8");
  const md5 = createHash("md5").update(bytes).digest("hex");
  const sha256 = createHash("sha256").update(bytes).digest("hex");
  const gitBlobSha = createHash("sha1")
    .update(Buffer.concat([Buffer.from("blob " + bytes.length + "\0"), bytes]))
    .digest("hex");
  if (bytes.length !== spec.bytes) throw new Error("byte length mismatch for bit " + bit);
  if (md5 !== spec.md5 || sha256 !== spec.sha256 || gitBlobSha !== spec.whole_git_blob_sha) {
    throw new Error("content hash mismatch for bit " + bit);
  }

  const lines = text.split(/\r?\n/).filter(Boolean);
  if (lines[0] !== "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS") {
    throw new Error("bad certificate header for bit " + bit);
  }
  if (lines[1] !== "root " + spec.root_hex) throw new Error("bad root line for bit " + bit);
  const strategy = new Map();
  let previous = "";
  for (const line of lines.slice(2)) {
    const match = line.match(/^([0-9a-f]{32})\s+(\d+)$/);
    if (!match) throw new Error("bad strategy row for bit " + bit);
    if (match[1] <= previous) throw new Error("unsorted or duplicate rows for bit " + bit);
    previous = match[1];
    const move = Number(match[2]);
    if (move < 0 || move >= N) throw new Error("move outside board for bit " + bit);
    strategy.set(match[1], move);
  }
  if (strategy.size !== spec.rows) throw new Error("row count mismatch for bit " + bit);

  const root = BigInt("0x" + spec.root_hex);
  const rootCanonical = canonicalD4(root);
  if (rootCanonical !== spec.d4_canonical_hex) throw new Error("D4 canonical root mismatch for bit " + bit);
  const rootPoints = pointsOf(root);
  if (rootPoints.length !== 7) throw new Error("root is not seven stones");
  assertRootSafe(rootPoints);
  const rootReplies = bitsOf(legalMask(rootPoints));
  if (rootReplies.length !== spec.root_check.loser_mobility) {
    throw new Error("root mobility mismatch for bit " + bit);
  }

  const consumed = new Set();
  let visited = 0, winner = 0, loser = 0, loserReplyEdges = 0;
  let terminals = 0, minTerminal = 999, maxTerminal = 0, maxPlies = 0;
  for (const reply of rootReplies) {
    const stack = [[root | (1n << BigInt(reply)), 0]];
    const seen = new Set();
    while (stack.length) {
      const entry = stack.pop();
      const board = entry[0], depth = entry[1];
      const hex = hexOf(board);
      if (seen.has(hex)) continue;
      seen.add(hex);
      visited++;
      const points = pointsOf(board);
      const options = legalMask(points);
      if (options === 0n) {
        if (depth % 2 !== 1) throw new Error("winner stuck at " + hex);
        if (strategy.has(hex)) throw new Error("terminal row at " + hex);
        terminals++;
        minTerminal = Math.min(minTerminal, points.length);
        maxTerminal = Math.max(maxTerminal, points.length);
        maxPlies = Math.max(maxPlies, depth + 1);
        continue;
      }
      if (depth % 2 === 0) {
        winner++;
        const move = strategy.get(hex);
        if (move === undefined) throw new Error("missing winner row at " + hex);
        if (((options >> BigInt(move)) & 1n) === 0n) {
          throw new Error("illegal strategy move at " + hex);
        }
        consumed.add(hex);
        stack.push([board | (1n << BigInt(move)), depth + 1]);
      } else {
        loser++;
        if (strategy.has(hex)) throw new Error("strategy row on loser turn at " + hex);
        for (const move of bitsOf(options)) {
          loserReplyEdges++;
          stack.push([board | (1n << BigInt(move)), depth + 1]);
        }
      }
    }
  }
  const missing = [...strategy.keys()].filter(hex => !consumed.has(hex));
  const extra = [...consumed].filter(hex => !strategy.has(hex));
  if (missing.length || extra.length) throw new Error("certificate/consumed union mismatch for bit " + bit);
  if (minTerminal < 13 || maxTerminal > 17 || maxPlies > 10) {
    throw new Error("terminal bound mismatch for bit " + bit);
  }

  const result = {
    bit,
    root_hex: spec.root_hex,
    root_d4_canonical_hex: canonicalD4(root),
    bytes: bytes.length,
    md5,
    sha256,
    git_blob_sha: gitBlobSha,
    rows: strategy.size,
    root_mobility: rootReplies.length,
    sub_roots: rootReplies.length,
    visited_states_across_subroots: visited,
    winner_states: winner,
    loser_states: loser,
    loser_reply_edges: loserReplyEdges,
    terminal_count: terminals,
    terminal_range: [minTerminal, maxTerminal],
    max_plies_from_root: maxPlies,
    union_missing: missing.length,
    union_extra: extra.length
  };
  for (const key of ["visited_states_across_subroots", "winner_states", "loser_states", "loser_reply_edges", "terminal_count"]) {
    if (result[key] !== spec[key]) throw new Error("manifest count mismatch for bit " + bit + ": " + key);
  }
  return result;
}

function canonicalD4(mask) {
  let best = null;
  for (let t = 0; t < 8; t++) {
    let transformed = 0n;
    for (const p of pointsOf(mask)) {
      const x = X[p], y = Y[p];
      let a, b;
      switch (t) {
        case 0: a = x; b = y; break;
        case 1: a = 10 - y; b = x; break;
        case 2: a = 10 - x; b = 10 - y; break;
        case 3: a = y; b = 10 - x; break;
        case 4: a = 10 - x; b = y; break;
        case 5: a = x; b = 10 - y; break;
        case 6: a = y; b = x; break;
        default: a = 10 - y; b = 10 - x; break;
      }
      transformed |= 1n << BigInt(b * 11 + a);
    }
    const hex = hexOf(transformed);
    if (best === null || hex < best) best = hex;
  }
  return best;
}

const foldFrontier = fold.frontier_after_cost63f;
if (foldClaim.status !== "completed") throw new Error("cost63f receipt fold claim is not completed");
if (foldFrontier.solved_s6_in_manifest !== 1199 ||
    foldFrontier.unique_remaining_s6 !== 6648 ||
    foldFrontier.sum_remaining_cost !== 524616 ||
    foldFrontier.s6_needed_by_open_classes !== 4918 ||
    foldFrontier.cost_needed_by_open_classes !== 388339 ||
    fold.totals.total_marginal !== 12 ||
    fold.totals.total_marginal_in_manifest !== 4 ||
    fold.totals.child_closed_by_bit !== 85 ||
    fold.controls.set_equality_after_2 !== "s == s_1195 UNION covers(2 cost-63f roots)") {
  throw new Error("post-audit cost63f fold record mismatch");
}
const certificates = [verifyCertificate(85), verifyCertificate(91)];
const parentOrbits = new Map();
for (const bit of [85, 91]) {
  const root = BigInt("0x" + manifest.certificates[String(bit)].root_hex);
  for (const removed of pointsOf(root)) {
    const parent = root & ~(1n << BigInt(removed));
    const key = canonicalD4(parent);
    if (!parentOrbits.has(key)) parentOrbits.set(key, []);
    parentOrbits.get(key).push({ bit, removed });
  }
}
const childOrbit = canonicalD4(BigInt("0x" + manifest.sweep_source.s6_child_hex));
const childIncidences = parentOrbits.get(childOrbit) || [];
const repeatedParents = [...parentOrbits.entries()]
  .filter((entry) => entry[1].length > 1)
  .map((entry) => ({ parent: entry[0], incidences: entry[1] }));
if (parentOrbits.size !== 13 || childIncidences.length !== 2 || repeatedParents.length !== 1) {
  throw new Error("unexpected D4 parent-lift multiplicity");
}
const baselineClosedParentOrbits = parentOrbits.size - fold.totals.total_marginal;
if (baselineClosedParentOrbits !== 1) {
  throw new Error("D4 parent-orbit count does not reconcile with fold marginal");
}
if (certificates[0].root_d4_canonical_hex === certificates[1].root_d4_canonical_hex) {
  throw new Error("the two WIN7 roots unexpectedly share a D4 orbit");
}

const result = {
  schema: "n11-cost63f-rational-independent-certificate-audit-v1",
  date: "2026-11-15",
  method: "Exact integer rational-circumcenter equation for noncollinear triples and exact cross-product line test for collinear triples; no floating point, no search engine, no verdict cache, no existing verifier imported",
  source_manifest: "class2-lane-cost63f-win7-certificates-20261115.json",
  certificates,
  parent_lifts: {
    deletion_edges: 14,
    unique_d4_parent_orbits: parentOrbits.size,
    baseline_closed_parent_orbits: baselineClosedParentOrbits,
    shared_child_orbit: childOrbit,
    shared_child_incidences: childIncidences,
    repeated_parent_orbits: repeatedParents
  },
  aggregate: {
    rows: certificates.reduce((s, x) => s + x.rows, 0),
    visited_states_across_subroots: certificates.reduce((s, x) => s + x.visited_states_across_subroots, 0),
    winner_states: certificates.reduce((s, x) => s + x.winner_states, 0),
    loser_states: certificates.reduce((s, x) => s + x.loser_states, 0),
    loser_reply_edges: certificates.reduce((s, x) => s + x.loser_reply_edges, 0),
    terminal_count: certificates.reduce((s, x) => s + x.terminal_count, 0)
  },
  frontier_impact: {
    at_audit: {
      manifest_s6_contribution: 0,
      chain_head: "1195/6652/524884/4922/388607",
      receipt_fold_status: "in_flight"
    },
    subsequent_fold: {
      chain_head: fold.frontier_after_cost63f.solved_s6_in_manifest + "/" +
        fold.frontier_after_cost63f.unique_remaining_s6 + "/" +
        fold.frontier_after_cost63f.sum_remaining_cost + "/" +
        fold.frontier_after_cost63f.s6_needed_by_open_classes + "/" +
        fold.frontier_after_cost63f.cost_needed_by_open_classes,
      marginal: fold.totals.total_marginal,
      marginal_in_manifest: fold.totals.total_marginal_in_manifest,
      child_closed_by_bit: fold.totals.child_closed_by_bit,
      remaining_s6: fold.frontier_after_cost63f.unique_remaining_s6,
      remaining_cost: fold.frontier_after_cost63f.sum_remaining_cost,
      s6_needed: fold.frontier_after_cost63f.s6_needed_by_open_classes,
      cost_needed: fold.frontier_after_cost63f.cost_needed_by_open_classes
    }
  },
  interpretation_guard: "The two certificates prove only the individual seven-stone roots WIN within ten plies. The later cost-63f receipt fold closes their shared S6 child in the manifest but does not solve either S5 parent. The 11x11 empty root, both two-stone roots, S2, class2 and class4 remain UNKNOWN."
};

const out = JSON.stringify(result, null, 2) + "\n";
const outIndex = process.argv.indexOf("--out");
if (outIndex >= 0 && process.argv[outIndex + 1]) writeFileSync(resolve(process.argv[outIndex + 1]), out);
else process.stdout.write(out);
