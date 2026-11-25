#!/usr/bin/env node
// Worker-partition witness search (2026-11-21). Deterministic xorshift128 PRNG,
// balanced simulated annealing + 1-swap descent. Modes:
//   t1class | t1pair | t2class | t2pair   (search; witness if it beats candidate)
//   oneswapT2class | oneswapT2pair        (exhaustive 1-swap certificate, candidate-centered)
//   oneswapT1class | oneswapT1pair        (exhaustive 1-swap certificate, T1)
// Objective "class"  = sum over multi-root 10-stone classes of (span-1)   [candidate published: 1998]
// Objective "pair"    = sum over pairs of roots in different groups, weighted by shared D4 classes [candidate: 2000]
// Constraints: T1 = exactly 9 roots per worker; T2 = T1 + d4-load spread <= 8.0%.
// Fail-closed: input pins verified; candidate reproduction cross-check before search output.
import fs from "node:fs";
import { createHash } from "node:crypto";

const PINS = {
  "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json":   "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",
  "research/experiments/n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json": "09b394b88cfb0246c278b335b82cfc5f8763f551c0f42c89403977b5e273918b",
  "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-10stone-20261121.json":     "5fec87afda5011243403d5efc71209cb9cd602eb3bb02bd833bd9341cb218b08",
  "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-09stone-20261121.json":     "68aa7df1e7b42c3661f404a6949439c31a3619140ae1ddf361001b375c0b6f9f",
  "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/exact-class-membership-20261121.json":"37ea472ed5dfadbc6edbad0b55116ddba41300b834ff8fef0cda5a31ba33ee64",
};
for (const [n, w] of Object.entries(PINS))
  if (createHash("sha256").update(fs.readFileSync(n)).digest("hex") !== w) { console.error("PIN FAIL " + n); process.exit(1); }

const census = JSON.parse(fs.readFileSync("research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json"));
const partcand = JSON.parse(fs.readFileSync("research/experiments/n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json"));
const mr10 = JSON.parse(fs.readFileSync("research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-10stone-20261121.json"));
const N = 36, W = 4;
const perRoot = census.per_root;
const rootName = perRoot.map(r => r.root);
const idxOf = new Map(rootName.map((n, i) => [n, i]));
const d4 = Int32Array.from(perRoot.map(r => r.d4));
const raw10 = Int32Array.from(perRoot.map(r => r.raw10));
const D4TOTAL = 733800, SPREADCAP = 8.0;

// adjacency
const pm = new Int32Array(N * N);   // pair weights: #classes containing both
const ce = new Int32Array(N * N);   // 2-root class multiplicity per pair
const triples = [];
for (const c of mr10) {
  const m = c.roots;
  if (m.length === 2) { const [i, j] = m; ce[i * N + j]++; ce[j * N + i]++; pm[i * N + j]++; pm[j * N + i]++; }
  else { triples.push(m.slice()); for (let a = 0; a < m.length; a++) for (let b = a + 1; b < m.length; b++) { pm[m[a] * N + m[b]]++; pm[m[b] * N + m[a]]++; } }
}
if (pm.reduce((s, v) => s + v) !== 2 * 5435) { console.error("pair weight total mismatch"); process.exit(1); }
const tripleIncident = Array.from({ length: N }, () => []);
triples.forEach((t, k) => t.forEach(r => tripleIncident[r].push(k)));

function classCross(a) { let s = 0; for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) if (a[i] !== a[j]) s += ce[i * N + j];
  for (const t of triples) { const w = new Set(t.map(r => a[r])); s += w.size - 1; } return s; }
function pairCross(a) { let s = 0; for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) if (a[i] !== a[j]) s += pm[i * N + j]; return s; }
function loadsOf(a, v) { const L = [0, 0, 0, 0]; for (let i = 0; i < N; i++) L[a[i]] += v[i]; return L; }
function spreadPct(L) { const mx = Math.max(...L), mn = Math.min(...L); return 100 * (mx - mn) / (L.reduce((s, x) => s + x, 0) / 4); }
function balanced(a) { const c = [0, 0, 0, 0]; for (const g of a) c[g]++; return c.every(x => x === 9); }

// candidate + baseline reproduction cross-check
const groups = partcand.candidate.root_groups;
const candw = new Array(36).fill(-1); let once = true;
groups.forEach((g, w) => { if (g.length !== 9) once = false; for (const rn of g) { const i = idxOf.get(rn); if (candw[i] !== -1) once = false; candw[i] = w; } });
if (!once || candw.includes(-1)) { console.error("candidate assignment invalid"); process.exit(1); }
const candClass = classCross(candw), candPair = pairCross(candw), candSpread = spreadPct(loadsOf(candw, d4));
if (candClass !== 1998 || candPair !== 2000 || Math.abs(candSpread - 7.506677568819842) > 1e-9 || candSpread > SPREADCAP) {
  console.error("candidate reproduction mismatch: class=" + candClass + " pair=" + candPair + " spread=" + candSpread); process.exit(1); }
const basew = Array.from({ length: N }, (_, i) => i % 4);
if (classCross(basew) !== 4189 || pairCross(basew) !== 4193) { console.error("baseline reproduction mismatch"); process.exit(1); }

// deterministic PRNG
function xorshift128(seed) { let x = seed >>> 0; if (x === 0) x = 0xA341316C; let y = 0x9E3779B9, z = 0xBB67AE85, w = 0x66826519;
  return function () { const t = (x ^ (x << 11)) >>> 0; x = y; y = z; z = w; const r = (w ^ (w >>> 19) ^ t ^ (t >>> 8)) >>> 0; w = r; return r / 4294967296; }; }

const objFn = { class: classCross, pair: pairCross };

function deltaOf(a, i, j, which) {
  const g = a[i], h = a[j]; let d = 0;
  const M = which === "class" ? ce : pm;
  const base = i * N, basej = j * N;
  for (let k = 0; k < N; k++) {
    if (k === i || k === j) continue;
    const ak = a[k], wik = M[base + k], wjk = M[basej + k];
    if (!wik && !wjk) continue;
    // i moves g->h, j moves h->g. For k in a third group, cross-ness of (i,k) and (j,k) is UNCHANGED.
    // Only collateral k in group g or h (k != i,j) change contribution:
    if (ak === g) d += wik - wjk;       // (i,k) within->cross : +wik ; (j,k) cross->within : -wjk
    else if (ak === h) d += wjk - wik;  // (j,k) within->cross : +wjk ; (i,k) cross->within : -wik
  }
  if (which === "class") { for (const k of new Set([...tripleIncident[i], ...tripleIncident[j]])) { const t = triples[k]; const before = new Set(t.map(r => a[r])).size - 1;
    const after = new Set(t.map(r => r === i ? h : r === j ? g : a[r])).size - 1; d += after - before; } }
  return d;
}
function doSwap(a, i, j) { const t = a[i]; a[i] = a[j]; a[j] = t; }

function randBalanced(rnd) { const ord = Array.from({ length: N }, (_, i) => i); for (let k = N - 1; k > 0; k--) { const p = Math.floor(rnd() * (k + 1)); [ord[k], ord[p]] = [ord[p], ord[k]]; }
  const a = new Array(N); ord.forEach((r, k) => a[r] = Math.floor(k / 9)); return a; }

function anneal(seedPair, mode, itersPerRestart, restarts) {
  const rnd = xorshift128(seedPair);
  const which = mode.includes("pair") ? "pair" : "class";
  const T2 = mode.startsWith("t2");
  const f = objFn[which];
  let best = null, bestCost = Infinity;
  const loads = [0, 0, 0, 0];
  const history = [];
  outer: for (let r = 0; r < restarts; r++) {
    const a = randBalanced(rnd);
    loads.fill(0); for (let i = 0; i < N; i++) loads[a[i]] += d4[i];
    let cost = f(a);
    let rBest = a.slice(), rBestCost = cost;
    for (let it = 0; it < itersPerRestart; it++) {
      const i = Math.floor(rnd() * N); let j = Math.floor(rnd() * N);
      if (a[i] === a[j]) { if (rnd() < 0.5) continue; j = (j + 9) % N; if (a[i] === a[j]) continue; }
      const g = a[i], h = a[j];
      if (T2) { const L = loads.slice(); L[g] += d4[j] - d4[i]; L[h] += d4[i] - d4[j]; if (spreadPct(L) > SPREADCAP) { it--; continue; } }
      const d = deltaOf(a, i, j, which);
      const T = 45 * Math.pow(0.01, it / itersPerRestart) + 0.05;
      if (d <= 0 || rnd() < Math.exp(-d / T)) {
        doSwap(a, i, j);
        if (T2) { loads[g] += d4[j] - d4[i]; loads[h] += d4[i] - d4[j]; }
        cost += d;
        if (cost < rBestCost) { rBestCost = cost; rBest = a.slice(); }
      }
    }
    // full 1-swap descent from rBest
    let cur = rBest, curCost = f(cur), improved = true;
    while (improved) { improved = false;
      for (let i = 0; i < N && !improved; i++) for (let j = i + 1; j < N; j++) {
        if (cur[i] === cur[j]) continue;
        if (T2) { const L = loadsOf(cur, d4); const g = cur[i], h = cur[j]; L[g] += d4[j] - d4[i]; L[h] += d4[i] - d4[j]; if (spreadPct(L) > SPREADCAP) continue; }
        const d = deltaOf(cur, i, j, which);
        if (d < 0) { doSwap(cur, i, j); curCost += d; improved = true; break; }
      } }
    // feasibility+consistency
    if (!balanced(cur)) continue;
    if (T2 && spreadPct(loadsOf(cur, d4)) > SPREADCAP) continue;
    if (f(cur) !== curCost) { console.error("cost corrupted at restart " + r); process.exit(1); }
    history.push(curCost);
    if (curCost < bestCost) { bestCost = curCost; best = cur.slice(); }
    if (bestCost === 0) break outer;
  }
  return { best, bestCost, history };
}

function enumOneswap(mode) {
  const which = mode.includes("pair") ? "pair" : "class";
  const T2 = mode.includes("T2");
  const f = objFn[which];
  const a = candw.slice();
  const results = [];
  let feasible = 0, improving = 0, bestNeighbor = f(a), bestSw = null;
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    if (a[i] === a[j]) continue;
    const b = a.slice(); doSwap(b, i, j);
    if (T2 && spreadPct(loadsOf(b, d4)) > SPREADCAP) continue;
    feasible++;
    const v = f(b);
    if (v < bestNeighbor) { improving++; bestNeighbor = v; bestSw = [i, j]; }
  }
  return { feasible_swaps: feasible, improving_swaps: improving, best_neighbor_score: bestNeighbor, best_swap: bestSw, base_score: f(a) };
}

const mode = process.argv[2];
const meta = {
  t1class: { seed: 3735928559, iters: 60000, restarts: Number(process.argv[3] || 60) },
  t1pair:  { seed: 781605401,  iters: 60000, restarts: Number(process.argv[3] || 60) },
  t2class: { seed: 1147007893, iters: 60000, restarts: Number(process.argv[3] || 60) },
  t2pair:  { seed: 2245932117, iters: 60000, restarts: Number(process.argv[3] || 60) },
}[mode];
if (meta) {
  const t0 = Date.now();
  const res = anneal(meta.seed, mode, meta.iters, meta.restarts);
  const ms = Date.now() - t0;
  const any = { status: "witness-search", mode, seed: meta.seed, iters_per_restart: meta.iters, restarts: meta.restarts,
    wall_ms: ms, found: !!res.best, best_cost: res.bestCost,
    candidate_costs: { class: candClass, pair: candPair, spread_d4_pct: candSpread } };
  if (res.best) {
    const a = res.best;
    // verify from scratch
    const fromScratch = objFn[mode.includes("pair") ? "pair" : "class"](a);
    if (fromScratch !== res.bestCost) { console.error("scratch mismatch"); process.exit(1); }
    const cc = classCross(a), pc = pairCross(a), sp = spreadPct(loadsOf(a, d4)), spr = spreadPct(loadsOf(a, raw10));
    const L9 = [0,0,0,0]; for (let i=0;i<N;i++) L9[a[i]] += perRoot[i].n9;
    Object.assign(any, { witness: { assignment_groups: groupsOf(a), class_cross: cc, pair_cross: pc, d4_spread_pct: sp, raw10_spread_pct: spr, n9_spread_pct: spreadPct(L9), n9_loads: L9, d4_loads: loadsOf(a, d4) },
      beats_candidate_class: cc < candClass, beats_candidate_pair: pc < candPair,
      t2_feasible: sp <= SPREADCAP });
  }
  console.log(JSON.stringify(any));
} else if (mode && mode.startsWith("oneswap")) {
  console.log(JSON.stringify({ status: "oneswap-exhaustive", mode, result: enumOneswap(mode) }));
} else { console.error("unknown mode"); process.exit(1); }
function groupsOf(a) { const out = [[], [], [], []]; for (let i = 0; i < N; i++) out[a[i]].push(rootName[i]); return out; }
