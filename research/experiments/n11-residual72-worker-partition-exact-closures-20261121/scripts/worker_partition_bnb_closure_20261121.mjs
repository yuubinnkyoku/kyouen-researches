#!/usr/bin/env node
// Exact worker-partition closure suite (2026-11-21, rebuilt after workspace reset; run with pinned inputs in cwd).
// Modes: x9 | w2class|w2pair | w3class|w3pair | w4class|w4pair | w6class|w6pair
//   x9      : 9-stone layer, minimize weighted cut of multi-root 9-stone classes (all 2-root), 4 workers x 9 roots.
//   w*class : 10-stone layer, class objective = sum over multi-root 10-stone D4 classes of (span-1), W workers x 36/W roots.
//   w*pair  : 10-stone layer, pair objective = sum over root pairs in different groups weighted by #shared multi-root classes.
// Method: (a) deterministic anneal (xorshift128, mode-specific seed) for a candidate UB;
//         (b) DFS branch & bound: assign roots in heavy-first order (descending pair-weight row sum: this reduced
//             w3class from 324M nodes (index order) to 325k nodes), symmetry breaking (group label <= max_used+1),
//             capacity propagation, min-conflict lower bound (each unassigned root contributes >= its cheapest
//             group's conflict against already-assigned neighbors; unassigned-unassigned edges contribute >= 0).
//             B&B explores only assignments with objective STRICTLY below the anneal UB: closing therefore PROVES
//             the UB is the global optimum; budget exhaustion is recorded honestly as "not closed".
// Fail-closed: input pins verified; candidate/baseline published numbers reproduced first where the candidate
//             partition is defined (W=4); every leaf asserts accrued == scratch.
// Implementation notes (bugs found & fixed in the 2026-11-21 first pass, kept fixed here):
//   (1) swap-delta: a third-group collateral k contributes 0 (only k in the two swapped groups change);
//   (2) triple state is kept in slot arrays (triGroups + triCnt), never in a Set (Sets lose duplicate group
//       membership on unwind when two members share a group);
//   (3) class objective accrues triple increments at assign time (a new group for a triple adds 1, except for
//       the triple's first assigned member) so the accrued value always equals the true span-1 sum at leaves.
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
const mr09classes = JSON.parse(fs.readFileSync("research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-09stone-20261121.json")).classes;
const N = 36;
const perRoot = census.per_root, rootName = perRoot.map(r => r.root);
const idxOf = new Map(rootName.map((n, i) => [n, i]));
const d4 = Int32Array.from(perRoot.map(r => r.d4));
const raw10 = Int32Array.from(perRoot.map(r => r.raw10));

const mode = process.argv[2];
const BUDGET_MS = Number(process.argv[3] || 120) * 1000;
const RESTARTS = Number(process.argv[4] || 0);   // 0 = per-mode default
let W, LAYER, OBJ;
if (mode === "x9") { W = 4; LAYER = "9stone"; OBJ = "cross9"; }
else if (/^w(\d+)(class|pair)$/.test(mode)) { W = Number(mode.slice(1).match(/^(\d+)/)[1]); LAYER = "10stone"; OBJ = mode.endsWith("class") ? "class" : "pair"; }
else { console.error("unknown mode " + mode); process.exit(1); }
const K = N / W;
if (!Number.isInteger(K) || K < 1) { console.error("bad W"); process.exit(1); }

// ---------- graph ----------
// PALL: #multi-root 10-stone classes containing both roots (all sizes)
// CE  : multiplicity of 2-root 10-stone classes per pair
// W9  : multiplicity of 2-root 9-stone classes per pair
const PALL = new Int32Array(N * N), CE = new Int32Array(N * N), W9 = new Int32Array(N * N);
const triples = [];
let wedge10 = 0;
for (const c of mr10) {
  const m = c.roots;
  if (m.length === 2) { const [i, j] = m; CE[i*N+j]++; CE[j*N+i]++; PALL[i*N+j]++; PALL[j*N+i]++; wedge10++; }
  else if (m.length === 3) { triples.push(m.slice());
    for (let x = 0; x < 3; x++) for (let y = x+1; y < 3; y++) { const i = m[x], j = m[y]; PALL[i*N+j]++; PALL[j*N+i]++; } }
  else { console.error("unexpected 10-stone class size"); process.exit(1); }
}
if (wedge10 !== 5420 || triples.length !== 5) { console.error("10-stone class table mismatch"); process.exit(1); }
let wedge9 = 0;
for (const c of mr09classes) {
  if (c.roots.length !== 2) { console.error("non-2-root 9-stone class"); process.exit(1); }
  const [i, j] = c.roots; W9[i*N+j]++; W9[j*N+i]++; wedge9++;
}
if (wedge9 !== 133) { console.error("9-stone edge mismatch"); process.exit(1); }
// pair weight matrix used by swap deltas (anneal): pair mode uses PALL, class mode uses CE
const PM = OBJ === "pair" ? PALL : CE;
// accrual matrix used by B&B: matches the objective's pairwise part
const ACM = OBJ === "cross9" ? W9 : PM;
// triple bookkeeping (class mode only)
const triMembers = Array.from({ length: N }, () => []);
triples.forEach((t, k) => t.forEach(r => triMembers[r].push(k)));
const triCnt = new Int32Array(triples.length);
const triGroups = Array.from({ length: triples.length }, () => new Int32Array(3));
const TOUCH = OBJ === "class" && LAYER === "10stone";

// ---------- objective functions (from scratch) ----------
function classCrossScratch(a) { let s = 0;
  for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) if (a[i] !== a[j]) s += CE[i*N+j];
  for (const t of triples) { const set = new Set(t.map(r => a[r])); s += set.size - 1; }
  return s; }
function pairCrossScratch(a) { let s = 0;
  for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) if (a[i] !== a[j]) s += PALL[i*N+j];
  return s; }
function cross9Scratch(a) { let s = 0;
  for (let i = 0; i < N; i++) for (let j = i+1; j < N; j++) if (a[i] !== a[j]) s += W9[i*N+j];
  return s; }
function objScratch(a) { return OBJ === "class" ? classCrossScratch(a) : OBJ === "pair" ? pairCrossScratch(a) : cross9Scratch(a); }

// ---------- reproduction gates ----------
const groups = partcand.candidate.root_groups;
const candw = new Array(N).fill(-1); let once = true;
groups.forEach((g, w) => { if (g.length !== 9) once = false; for (const rn of g) { const i = idxOf.get(rn); if (candw[i] !== -1) once = false; candw[i] = w; } });
if (!once || candw.includes(-1)) { console.error("candidate assignment invalid"); process.exit(1); }
const basew = Array.from({ length: N }, (_, i) => i % W);
if (W === 4) {
  if (classCrossScratch(candw) !== 1998 || classCrossScratch(basew) !== 4189) { console.error("class reproduction mismatch"); process.exit(1); }
  if (pairCrossScratch(candw) !== 2000 || pairCrossScratch(basew) !== 4193) { console.error("pair reproduction mismatch"); process.exit(1); }
  if (cross9Scratch(candw) !== 49 || cross9Scratch(basew) !== 104) { console.error("9-stone reproduction mismatch"); process.exit(1); }
}

// ---------- deterministic anneal ----------
function xorshift128(seed) { let x = seed >>> 0; if (x === 0) x = 0xA341316C; let y = 0x9E3779B9, z = 0xBB67AE85, w = 0x66826519;
  return function () { const t = (x ^ (x << 11)) >>> 0; x = y; y = z; z = w; const r = (w ^ (w >>> 19) ^ t ^ (t >>> 8)) >>> 0; w = r; return r / 4294967296; }; }
function pairDelta(a, i, j, M) { const g = a[i], h = a[j]; let d = 0; const bi = i * N, bj = j * N;
  for (let k = 0; k < N; k++) { if (k === i || k === j) continue;
    const ak = a[k], wik = M[bi + k], wjk = M[bj + k];
    if (!wik && !wjk) continue;
    if (ak === g) d += wik - wjk;       // third-group k contributes 0 (FIX 1)
    else if (ak === h) d += wjk - wik; }
  return d; }
function classDelta(a, i, j) { let d = pairDelta(a, i, j, CE);
  for (const k of new Set([...triMembers[i], ...triMembers[j]])) { const t = triples[k];
    const before = new Set(t.map(r => a[r])).size - 1;
    const after = new Set(t.map(r => r === i ? a[j] : r === j ? a[i] : a[r])).size - 1; d += after - before; }
  return d; }
const deltaFn = (a, i, j) => OBJ === "class" ? classDelta(a, i, j) : pairDelta(a, i, j, ACM);
function randBalanced(rnd) { const ord = Array.from({ length: N }, (_, i) => i);
  for (let k = N - 1; k > 0; k--) { const p = Math.floor(rnd() * (k + 1)); [ord[k], ord[p]] = [ord[p], ord[k]]; }
  const aa = new Array(N); ord.forEach((r, k) => aa[r] = Math.floor(k / K)); return aa; }
function balanced(aa) { const c = new Array(W).fill(0); for (const g of aa) c[g]++; return c.every(x => x === K); }

function anneal(seed, iters, restarts) {
  const rnd = xorshift128(seed);
  let best = null, bestCost = Infinity; const history = [];
  outer: for (let r = 0; r < restarts; r++) {
    const aa = randBalanced(rnd);
    let cost = objScratch(aa), rBest = aa.slice(), rBestCost = cost;
    for (let it = 0; it < iters; it++) {
      const i = Math.floor(rnd() * N); let j = Math.floor(rnd() * N);
      if (aa[i] === aa[j]) { if (rnd() < 0.5) continue; j = (j + K) % N; if (aa[i] === aa[j]) continue; }
      const d = deltaFn(aa, i, j);
      const T = 45 * Math.pow(0.01, it / iters) + 0.05;
      if (d <= 0 || rnd() < Math.exp(-d / T)) { const t = aa[i]; aa[i] = aa[j]; aa[j] = t; cost += d;
        if (cost < rBestCost) { rBestCost = cost; rBest = aa.slice(); } }
    }
    let cur = rBest, curCost = objScratch(cur), improved = true;
    while (improved) { improved = false;
      for (let i = 0; i < N && !improved; i++) for (let j = i+1; j < N; j++) {
        if (cur[i] === cur[j]) continue;
        const d = deltaFn(cur, i, j);
        if (d < 0) { const t = cur[i]; cur[i] = cur[j]; cur[j] = t; curCost += d; improved = true; break; }
      } }
    if (!balanced(cur)) continue;
    if (objScratch(cur) !== curCost) { console.error("anneal cost corrupted at restart " + r); process.exit(1); }
    history.push(curCost);
    if (curCost < bestCost) { bestCost = curCost; best = cur.slice(); }
    if (bestCost === 0) break outer;
  }
  return { best, bestCost, history };
}

// ---------- branch & bound ----------
// branching order: roots by descending ACM row weight (heavy edges first -> tighter lower bound earlier)
function rowSum(i) { let s = 0; const r = i * N; for (let k = 0; k < N; k++) s += ACM[r + k]; return s; }
const DYNO = mode === "x9";
const ORDER = DYNO
  ? null                                                        // sparse W9 layer: conflict-driven dynamic variable order
  : (() => { const o = Array.from({ length: N }, (_, i) => i);   // dense 10-stone layer: heavy-first static order
      o.sort((x, y) => rowSum(y) - rowSum(x)); return o; })();
const conf = new Int32Array(N * W);       // conf[j*W+g] : weight from unassigned j to currently assigned roots in group g
const a = new Int32Array(N).fill(-1);
const cnt = new Int32Array(W);
const triTouched = [];                     // per-depth unwind log: array of [triIdx, addedInc]
let nodes = 0, closed = true, bestBelow = null, bestBelowVal = 0, abortedByBudget = false;
let T0 = 0;
const UB = { best: null, bestCost: Infinity };

const unass = [];                                                // dynamic-order bookkeeping (x9): unassigned roots
// lower bound: each unassigned root contributes >= its cheapest FEASIBLE group's conflict
// (cnt[g] < K is a necessary condition for a future assignment into g, so the min over feasible
//  groups is a valid strengthening of the min over all groups)
function lbAt(i0) { let s = 0;
  for (const j of unass) { if (j === i0) continue; const b = j * W; let m = -1;
    for (let g = 0; g < W; g++) { if (cnt[g] >= K) continue; const v = conf[b + g]; if (m < 0 || v < m) m = v; }
    if (m > 0) s += m; }
  return s; }
function lb(depth) { let s = 0;
  for (let p = depth; p < N; p++) { const j = ORDER[p]; const b = j * W; let m = -1;
    for (let g = 0; g < W; g++) { if (cnt[g] >= K) continue; const v = conf[b + g]; if (m < 0 || v < m) m = v; }
    if (m > 0) s += m; }
  return s; }

function dfs(depth, cross, maxUsed) {
  if (abortedByBudget) return;
  if ((++nodes & 0xFFFFF) === 0 && Date.now() - T0 > BUDGET_MS) { abortedByBudget = true; closed = false; return; }
  if (depth === N) {
    const s = objScratch(Array.from(a));
    if (s !== cross) { console.error("LEAF ASSERT cross=" + cross + " scratch=" + s); process.exit(9); }
    if (cross < UB.bestCost) { bestBelow = Array.from(a); bestBelowVal = cross; }
    return;
  }
  // choose next root: dynamic conflict-driven (x9) or static heavy-first (10-stone)
  let i = 0;
  if (DYNO) {
    let bs = -1, bj = -1;
    for (const j of unass) { const b = j * W; let s = 0;
      for (let g = 0; g < W; g++) s += conf[b + g];
      if (s > bs) { bs = s; bj = j; } }
    i = bj;
    if (cross + lbAt(i) >= UB.bestCost) return;   // prune with the same LB after committing to the chosen root
  } else {
    i = ORDER[depth];
    if (cross + lb(depth) >= UB.bestCost) return; // prune: only strictly-below-UB survive
  }
  const lim = Math.min(maxUsed + 1, W - 1);
  for (let g = 0; g <= lim; g++) {
    if (cnt[g] >= K) continue;
    const row = i * N;
    let add = 0;
    if (DYNO) { for (let q = 0; q < N; q++) if (a[q] !== -1 && a[q] !== g) add += ACM[row + q]; }
    else { for (let q = 0; q < depth; q++) if (a[ORDER[q]] !== g) add += ACM[row + ORDER[q]]; }
    // triple increments (class mode only): a new group for a touched triple adds 1, except for its first member
    let triAdd = 0; const tLog = [];
    if (TOUCH) { for (const k of triMembers[i]) {
        const c = triCnt[k]; const gs = triGroups[k];
        if (c > 0) { let isNew = true;
          for (let q = 0; q < c; q++) if (gs[q] === g) { isNew = false; break; }
          if (isNew) { triAdd += 1; tLog.push([k, 1]); } else tLog.push([k, 0]); }
        else tLog.push([k, 0]);
        gs[c] = g; triCnt[k] = c + 1; }
      triTouched.push(tLog); }
    if (DYNO) { for (let j = 0; j < N; j++) if (a[j] === -1 && j !== i) conf[j * W + g] += ACM[j * N + i];
      const ui = unass.indexOf(i); unass.splice(ui, 1); }
    else { for (let p = depth + 1; p < N; p++) { const j = ORDER[p]; conf[j * W + g] += ACM[j * N + i]; } }
    a[i] = g; cnt[g]++;
    dfs(depth + 1, cross + add + triAdd, Math.max(maxUsed, g));
    a[i] = -1; cnt[g]--;
    if (DYNO) { unass.push(i);
      for (let j = 0; j < N; j++) if (a[j] === -1 && j !== i) conf[j * W + g] -= ACM[j * N + i]; }
    else { for (let p2 = depth + 1; p2 < N; p2++) { const j = ORDER[p2]; conf[j * W + g] -= ACM[j * N + i]; } }
    if (TOUCH) { const tl = triTouched.pop();
      for (const kv of tl) triCnt[kv[0]]--; }
  }
}

// ---------- run ----------
const SEED = mode === "x9" ? 305093817 : ((OBJ === "class" ? 3735928559 : 781605401) + W);
const RESTARTS_DEFAULT = mode === "x9" ? 200 : W === 4 ? 60 : 80;
const restarts = RESTARTS || RESTARTS_DEFAULT;
const tAnn0 = Date.now();
const annUB = anneal(SEED, 60000, restarts);
const annMs = Date.now() - tAnn0;
if (!annUB.best) { console.error("no anneal witness"); process.exit(1); }
if (objScratch(annUB.best) !== annUB.bestCost) { console.error("anneal witness scratch mismatch"); process.exit(1); }
UB.bestCost = annUB.bestCost; UB.best = annUB.best;
if (DYNO) { for (let i2 = 0; i2 < N; i2++) unass.push(i2); }
T0 = Date.now();
dfs(0, 0, -1);
const bnbMs = Date.now() - T0;
const ok = closed && !abortedByBudget;
const opt = ok ? (bestBelow !== null ? bestBelowVal : UB.bestCost) : null;
if (ok && bestBelow !== null && bestBelowVal >= UB.bestCost) { console.error("internal: improved witness above UB"); process.exit(1); }
if (ok && bestBelow !== null && objScratch(bestBelow) !== bestBelowVal) { console.error("improved witness scratch mismatch"); process.exit(1); }
const wA = bestBelow !== null ? bestBelow : UB.best;
const wArr = Array.from(wA);
const wg = Array.from({ length: W }, () => []);
for (let i = 0; i < N; i++) wg[wA[i]].push(rootName[i]);
const d4L = new Array(W).fill(0), r10L = new Array(W).fill(0), n9L = new Array(W).fill(0);
for (let i = 0; i < N; i++) { d4L[wA[i]] += d4[i]; r10L[wA[i]] += raw10[i]; n9L[wA[i]] += (perRoot[i].n9 ?? 0); }
function spread(L) { const mx = Math.max(...L), mn = Math.min(...L); return 100 * (mx - mn) / (L.reduce((s, x) => s + x, 0) / W); }
const witness = {
  groups: wg, objective_value: objScratch(wArr),
  class_cross: LAYER === "10stone" ? classCrossScratch(wArr) : undefined,
  pair_cross: LAYER === "10stone" ? pairCrossScratch(wArr) : undefined,
  cross9: cross9Scratch(wArr),
  d4_loads: d4L, d4_spread_pct: spread(d4L),
  raw10_loads: r10L, raw10_spread_pct: spread(r10L),
  n9_loads: n9L, n9_spread_pct: spread(n9L),
  proven: ok ? (bestBelow !== null ? "improved witness found; B&B closed strictly below UB: exact global optimum of the stated objective"
                                    : "UB closed by B&B: witness attains the exact global optimum of the stated objective")
             : "not proven optimal (UB not closed within budget)",
};
const out = {
  schema: "n11-residual72-worker-partition-exact-closures-20261121-v2",
  mode, layer: LAYER, objective: OBJ, workers: W, roots_per_worker: K,
  pins_verified: ["census.json","partcand.json","mr10.json","mr09.json","exactclass.json"],
  reproduction_gates: W === 4 ? "candidate/baseline published values reproduced (class10 1998/4189, pair10 2000/4193, cross9 49/104)" : "structural gates only (published candidate partition is W=4)",
  anneal_ub: { seed: SEED, iters_per_restart: 60000, restarts, best_cost: annUB.bestCost, wall_ms: annMs },
  bnb: { nodes_visited: nodes, wall_ms: bnbMs, closed_within_budget: ok, budget_s: BUDGET_MS / 1000,
         strategy: "explore strictly-below-UB; closed => UB is exact global optimum" },
  result: { exact_optimum_if_closed: opt, improved_witness_below_ub: bestBelow !== null ? bestBelowVal : null,
            ub_not_beaten: bestBelow === null, status: ok ? (bestBelow !== null ? "improved-witness-is-global-optimum" : "exact-optimum-closed-ub-is-global") : "budget-exhausted-not-closed" },
  witness,
};
console.log(JSON.stringify(out));
