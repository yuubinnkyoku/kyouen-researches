#!/usr/bin/env node
/**
 * Third-implementation cross-check of the cost-16 parent A16/B16
 * minimum-cover totals (Node.js / ECMAScript, independent of the published
 * Python implementations).
 *
 * The published pipeline computes A16/B16 with weighted perfect-matching
 * counts over induced row subsets (PmLazy memo DP) in two Python
 * implementations (checkpoint fresh-slice and shared-memo). This module
 * re-implements the entire computation from the pinned inputs in JavaScript:
 *
 *  - rows are rebuilt from the worklist / census / ledger pins,
 *  - candidate 7-stone roots are regenerated with integer det4 on 11x11
 *    coordinates and D4-canonicalized with BigInt masks,
 *  - weighted perfect-matching counts use a lazily evaluated memo DP over
 *    row-subset bitmasks stored as JS Numbers (all memo values are asserted
 *    < 2^53 so every stored value is exact),
 *  - outer products and sums (B_d, A16, B16) are accumulated in BigInt,
 *    so no rounding enters the published magnitudes.
 *
 * Modes (no game-tree search, no verdict):
 *   --anchor11          full 11-row anchor: graph, A/B/total, per-row ways10,
 *                       per-root membership for every root (757 expected)
 *   --graph31           31-row graph structure only
 *   --bslice <d>        fresh-memo B_d for doubled row d (0..30)
 *   --aslice <s>        fresh-memo pm(full ^ (1<<s)) for row s (0..30)
 *
 * Output: one JSON document on stdout.
 */
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..", "..", "..");
const N = 11;

const TARGET31 = "00000000000000003800000008001000";
const TARGET11 = "00000000000000403800000008000000";
const STATE_CAP = 48_000_000;
const PM_LIMIT = 2 ** 53;

const PINS = {
  worklist: [
    "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
    "2fee1d0718547a62e346d35f5858d7913e37c097",
  ],
  census: [
    "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
    "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
  ],
  ledger: [
    "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
    "e8785d509e8a11a37c0d03cc450455a14708c34d",
  ],
};

function gitBlobSha(data) {
  return createHash("sha1").update(`blob ${Buffer.byteLength(data)}\0`).update(data).digest("hex");
}

function readPinned(name) {
  const [rel, pin] = PINS[name];
  const data = readFileSync(join(ROOT, rel));
  const actual = gitBlobSha(data);
  if (actual !== pin) {
    throw new Error(`pin mismatch for ${name}: expected ${pin} got ${actual}`);
  }
  return data;
}

const TRANSFORMS = [
  (x, y) => [x, y],
  (x, y) => [y, N - 1 - x],
  (x, y) => [N - 1 - x, N - 1 - y],
  (x, y) => [N - 1 - y, x],
  (x, y) => [N - 1 - x, y],
  (x, y) => [x, N - 1 - y],
  (x, y) => [y, x],
  (x, y) => [N - 1 - y, N - 1 - x],
];
// TO[k][i] = image of square i under transform k
const TO = TRANSFORMS.map((t) => {
  const row = new Int32Array(121);
  for (let i = 0; i < 121; i++) {
    const [qx, qy] = t(i % N, Math.floor(i / N));
    row[i] = qy * N + qx;
  }
  return row;
});

function orbitMasks(mask) {
  const out = [];
  for (const to of TO) {
    let v = 0n;
    let m = mask;
    while (m) {
      const low = m & -m;
      const i = Number(low.toString(2).length - 1);
      v |= 1n << BigInt(to[i]);
      m ^= low;
    }
    out.push(v);
  }
  return out;
}

function canon(mask) {
  let best = null;
  for (const v of orbitMasks(mask)) {
    if (best === null || v < best) best = v;
  }
  return best;
}

function hexOf(big) {
  return big.toString(16).padStart(32, "0");
}

function det3(a, b, c) {
  const x1 = a % N, y1 = Math.floor(a / N);
  const x2 = b % N, y2 = Math.floor(b / N);
  const x3 = c % N, y3 = Math.floor(c / N);
  const A = x1 * x1 + y1 * y1, B = x1, C = y1;
  const D = x2 * x2 + y2 * y2, E = x2, F = y2;
  const G = x3 * x3 + y3 * y3, H = x3, I = y3;
  return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G);
}

function det4(a, b, c, d) {
  return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d);
}

function deriveParentRows(targetHex) {
  const worklist = readPinned("worklist").toString("utf8").trim().split(/\r?\n/);
  const census = JSON.parse(readPinned("census").toString("utf8"));
  const ledger = JSON.parse(readPinned("ledger").toString("utf8"));
  const sterile = new Set(census.sterile_row_registry.map((x) => x.hex));
  const closed = new Set(ledger.derived.closed_rows_66);
  const parentOrbit = new Set(orbitMasks(BigInt("0x" + targetHex)));
  const headers = worklist[0].split(",").map((h) => h.trim());
  const rows = [];
  const costIdx = {};
  headers.forEach((h, i) => { costIdx[h] = i; });
  for (let li = 1; li < worklist.length; li++) {
    const vals = worklist[li].split(",");
    const rec = {};
    headers.forEach((h, i) => { rec[h] = (vals[i] || "").trim(); });
    const h = rec.s6_canonical_hex;
    if (!h || sterile.has(h) || closed.has(h)) continue;
    const mask = BigInt("0x" + h);
    let hit = false;
    for (let b = 0; b < 121 && !hit; b++) {
      if ((mask >> BigInt(b)) & 1n) {
        if (parentOrbit.has(mask ^ (1n << BigInt(b)))) hit = true;
      }
    }
    if (hit) {
      rows.push({ hex: h, cost: parseInt(rec.own_candidates_s6_s7_edge_cost, 10) });
    }
  }
  rows.sort((a, b) => (a.hex < b.hex ? -1 : a.hex > b.hex ? 1 : 0));
  return rows;
}

function buildGraph(targetRows) {
  const r = targetRows.length;
  const prootRows = new Map(); // root BigInt -> Set of row indices
  const candidateCounts = [];
  for (let ri = 0; ri < r; ri++) {
    const mask = BigInt("0x" + targetRows[ri].hex);
    const stones = [];
    let m = mask;
    while (m) {
      const low = m & -m;
      stones.push(Number(low.toString(2).length - 1));
      m ^= low;
    }
    if (stones.length !== 6) throw new Error(`row ${ri} has ${stones.length} stones`);
    let count = 0;
    for (let d = 0; d < 121; d++) {
      if ((mask >> BigInt(d)) & 1n) continue;
      let legal = true;
      for (let i = 0; i < 6 && legal; i++) {
        for (let j = i + 1; j < 6 && legal; j++) {
          for (let k = j + 1; k < 6 && legal; k++) {
            if (det4(stones[i], stones[j], stones[k], d) === 0) legal = false;
          }
        }
      }
      if (legal) {
        const root = canon(mask | (1n << BigInt(d)));
        if (!prootRows.has(root)) prootRows.set(root, new Set());
        prootRows.get(root).add(ri);
        count++;
      }
    }
    candidateCounts.push(count);
    if (count !== targetRows[ri].cost) {
      throw new Error(`row ${ri} candidate count ${count} != cost ${targetRows[ri].cost}`);
    }
  }
  const pairRoots = new Map(); // "a,b" -> count
  const singletonRoots = new Map(); // root -> row index
  const w1 = new Array(r).fill(0);
  const spanHist = new Map();
  for (const [root, covered] of prootRows) {
    const size = covered.size;
    spanHist.set(size, (spanHist.get(size) || 0) + 1);
    if (size === 2) {
      const [a, b] = [...covered].sort((x, y) => x - y);
      const key = a + "," + b;
      pairRoots.set(key, (pairRoots.get(key) || 0) + 1);
    } else if (size === 1) {
      const s = [...covered][0];
      singletonRoots.set(root, s);
      w1[s]++;
    } else {
      throw new Error(`root covers ${size} rows`);
    }
  }
  const adj = Array.from({ length: r }, () => []);
  for (const [key, weight] of pairRoots) {
    const [a, b] = key.split(",").map(Number);
    adj[a].push([b, weight]);
    adj[b].push([a, weight]);
  }
  for (const row of adj) row.sort((x, y) => x[0] - y[0]);
  return { prootRows, pairRoots, singletonRoots, w1, adj, candidateCounts, spanHist };
}

function popcount(v) {
  v = v - ((v >> 1) & 0x55555555);
  v = (v & 0x33333333) + ((v >> 2) & 0x33333333);
  return ((v + (v >> 4)) & 0x0f0f0f0f) * 0x01010101 >> 24;
}

class PmLazy {
  constructor(adj) {
    this.adj = adj;
    this.memo = new Map([[0, 1]]);
  }
  get(mask) {
    const memo = this.memo;
    if (memo.has(mask)) return memo.get(mask);
    const stack = [mask];
    const seen = new Set([mask]);
    const order = [];
    while (stack.length) {
      const m = stack.pop();
      if (memo.has(m)) continue;
      order.push(m);
      if (memo.size + seen.size > STATE_CAP) {
        throw new Error(`PmLazy state cap exceeded: ${memo.size} + ${seen.size}`);
      }
      const low = m & -m;
      const first = Math.log2(low);
      const rest = m ^ low;
      for (const [j] of this.adj[first]) {
        const bit = 1 << j;
        if (rest & bit) {
          const sub = rest ^ bit;
          if (!memo.has(sub) && !seen.has(sub)) {
            seen.add(sub);
            stack.push(sub);
          }
        }
      }
    }
    order.sort((a, b) => popcount(a) - popcount(b));
    seen.clear();
    for (const m of order) {
      if (memo.has(m)) continue;
      const low = m & -m;
      const first = Math.log2(low);
      const rest = m ^ low;
      let acc = 0;
      for (const [j, weight] of this.adj[first]) {
        const bit = 1 << j;
        if (rest & bit) {
          acc += weight * memo.get(rest ^ bit);
        }
      }
      if (acc >= PM_LIMIT) {
        throw new Error(`pm value ${acc} >= 2^53 for mask ${m}; Number storage no longer exact`);
      }
      memo.set(m, acc);
    }
    return memo.get(mask);
  }
}

function out(obj) {
  process.stdout.write(JSON.stringify(obj) + "\n");
}

function graphStructureJson(targetHex, rows, g) {
  const multiplicity = new Map();
  for (const [, w] of g.pairRoots) multiplicity.set(w, (multiplicity.get(w) || 0) + 1);
  const hist = {};
  for (const [k, v] of [...g.spanHist].sort((a, b) => a[0] - b[0])) hist[String(k)] = v;
  const mult = {};
  for (const [k, v] of [...multiplicity].sort((a, b) => a[0] - b[0])) mult[String(k)] = v;
  return {
    target_parent: targetHex,
    row_count: rows.length,
    rows: rows.map((x) => ({ hex: x.hex, cost: x.cost })),
    candidate_occurrences: g.candidateCounts.reduce((a, b) => a + b, 0),
    distinct_D4_roots: g.prootRows.size,
    root_coverage_histogram: hist,
    pair_types: g.pairRoots.size,
    pair_type_multiplicity_histogram: mult,
    singleton_root_count: g.singletonRoots.size,
    per_row_singleton_root_count: g.w1,
    per_row_pair_root_degree: g.adj.map((a) => a.length),
  };
}

function main() {
  const args = process.argv.slice(2);
  const t0 = Date.now();
  if (args[0] === "--anchor11") {
    const rows = deriveParentRows(TARGET11);
    const g = buildGraph(rows);
    const r = rows.length;
    const full = (1 << r) - 1;
    const pm = new PmLazy(g.adj);
    const perRow = [];
    for (let s = 0; s < r; s++) {
      perRow.push({ row: rows[s].hex, singleton_roots: g.w1[s], ways10: pm.get(full ^ (1 << s)) });
    }
    let A = 0n;
    for (let s = 0; s < r; s++) A += BigInt(g.w1[s]) * BigInt(pm.get(full ^ (1 << s)));
    const bByD = [];
    let B = 0n;
    for (let d = 0; d < r; d++) {
      const neighbors = g.adj[d];
      let bd = 0n;
      for (let i = 0; i < neighbors.length; i++) {
        for (let j = i + 1; j < neighbors.length; j++) {
          const [a, wa] = neighbors[i];
          const [b, wb] = neighbors[j];
          bd += BigInt(wa) * BigInt(wb) * BigInt(pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b)));
        }
      }
      bByD.push(bd.toString());
      B += bd;
    }
    // per-root membership over every root of the 11-row universe
    // dp2[mask][j] = number of j-subsets of distinct pair roots with union exactly mask
    const pairRootList = [];
    for (const [root, coveredSet] of g.prootRows) {
      if (coveredSet.size === 2) {
        const [a, b] = [...coveredSet].sort((x, y) => x - y);
        pairRootList.push([a, b]);
      }
    }
    const dp2 = Array.from({ length: 1 << r }, () => new Map());
    dp2[0].set(0, 1);
    for (const [a, b] of pairRootList) {
      const cm = (1 << a) | (1 << b);
      const updates = [];
      for (let mask = 0; mask < 1 << r; mask++) {
        const bucket = dp2[mask];
        if (bucket.size === 0) continue;
        for (const [j, w] of bucket) {
          if (j < 6) updates.push([mask | cm, j + 1, w]);
        }
      }
      for (const [nxt, j, w] of updates) {
        const bucket = dp2[nxt];
        bucket.set(j, (bucket.get(j) || 0) + w);
      }
    }
    const rowIndexOf = new Map(rows.map((x, i) => [x.hex, i]));
    const memberships = [];
    for (const [root, coveredSet] of g.prootRows) {
      const covered = [...coveredSet];
      const rootHex = hexOf(root);
      let singletonCovers = 0n;
      let pairCovers = 0n;
      if (covered.length === 1) {
        const s = covered[0];
        singletonCovers = BigInt(pm.get(full ^ (1 << s)));
      } else {
        const [a, b] = covered;
        // type A: singleton s not in {a,b}, perfect matching on rows \ {s,a,b}
        for (let s = 0; s < r; s++) {
          if (s === a || s === b) continue;
          singletonCovers += BigInt(g.w1[s]) * BigInt(pm.get(full ^ (1 << s) ^ (1 << a) ^ (1 << b)));
        }
        // type B, doubled row d:
        //   d in R = full \ {a,b}: the other 5 pair roots have union exactly R
        //   d == a: the other 5 roots perfectly match full \ {b}
        //   d == b: symmetric, pm(full \ {a})
        const R = full ^ (1 << a) ^ (1 << b);
        const dR = dp2[R].get(5) || 0;
        pairCovers += BigInt(dR) + BigInt(pm.get(full ^ (1 << b))) + BigInt(pm.get(full ^ (1 << a)));
      }
      memberships.push({
        root: rootHex,
        membership: (singletonCovers + pairCovers).toString(),
        singleton_type_covers: singletonCovers.toString(),
        six_pair_type_covers: pairCovers.toString(),
        cover_rows: covered.map((i) => rows[i].hex).sort(),
      });
    }
    memberships.sort((x, y) => (x.root < y.root ? -1 : x.root > y.root ? 1 : 0));
    out({
      mode: "anchor11",
      input_pins: Object.fromEntries(Object.entries(PINS).map(([k, [rel, pin]]) => [k, pin])),
      graph: graphStructureJson(TARGET11, rows, g),
      cover_space: {
        singleton_type_covers: A.toString(),
        six_pair_covers: B.toString(),
        total_minimum_covers: (A + B).toString(),
        minimum_root_count: 6,
      },
      per_row: perRow,
      all_root_memberships: memberships,
      memo_states: pm.memo.size,
      elapsed_ms: Date.now() - t0,
    });
    return;
  }
  if (args[0] === "--graph31") {
    const rows = deriveParentRows(TARGET31);
    const g = buildGraph(rows);
    out({
      mode: "graph31",
      input_pins: Object.fromEntries(Object.entries(PINS).map(([k, [rel, pin]]) => [k, pin])),
      graph: graphStructureJson(TARGET31, rows, g),
      elapsed_ms: Date.now() - t0,
    });
    return;
  }
  if (args[0] === "--bslice") {
    const d = parseInt(args[1], 10);
    const rows = deriveParentRows(TARGET31);
    const g = buildGraph(rows);
    const r = rows.length;
    const full = (1 << r) - 1;
    const pm = new PmLazy(g.adj);
    const neighbors = g.adj[d];
    let bd = 0n;
    for (let i = 0; i < neighbors.length; i++) {
      for (let j = i + 1; j < neighbors.length; j++) {
        const [a, wa] = neighbors[i];
        const [b, wb] = neighbors[j];
        bd += BigInt(wa) * BigInt(wb) * BigInt(pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b)));
      }
    }
    out({
      mode: "bslice",
      double_row_index: d,
      row_hex: rows[d].hex,
      degree: neighbors.length,
      anchors: (neighbors.length * (neighbors.length - 1)) / 2,
      B_d: bd.toString(),
      fresh_memo_states: pm.memo.size,
      elapsed_ms: Date.now() - t0,
    });
    return;
  }
  if (args[0] === "--aslice") {
    const s = parseInt(args[1], 10);
    const rows = deriveParentRows(TARGET31);
    const g = buildGraph(rows);
    const r = rows.length;
    const full = (1 << r) - 1;
    const pm = new PmLazy(g.adj);
    const value = pm.get(full ^ (1 << s));
    out({
      mode: "aslice",
      row_index: s,
      row_hex: rows[s].hex,
      singleton_root_count: g.w1[s],
      pm_value: value,
      pm_value_str: value.toString(),
      fresh_memo_states: pm.memo.size,
      elapsed_ms: Date.now() - t0,
    });
    return;
  }
  process.stderr.write("usage: --anchor11 | --graph31 | --bslice <d> | --aslice <s>\n");
  process.exit(2);
}

main();
