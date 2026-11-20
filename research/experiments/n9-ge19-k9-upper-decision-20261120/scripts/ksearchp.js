#!/usr/bin/env node
// ksearch.js (v3) - specialized complete DFS for maximum-safe-set decision on n x n kyouen (q=4).
// ksearchp.js (v3d) - identical engine + generalized --prefix chunking (superset of v3c --min).
//   --prefix=p1,p2,...,pm (strictly ascending 0-based cells) restricts the search to the chunk
//   {chosen sets of size target whose m smallest elements are exactly p1..pm}: cells below p1
//   are pre-excluded, then p1 fixed, then cells in (p1,p2) excluded, p2 fixed, ... (same
//   ban/fix/saturate semantics as the v3c --min block, iterated). Chunks over all prefixes of a
//   given length m form a sound disjoint complete partition of the whole space. --min=c is
//   equivalent to --prefix=c (single-element prefix).
// Safety: no 4 chosen cells concyclic or collinear <=> at most 3 chosen per dangerous curve
//         (line or circle with >= 4 grid cells; every forbidden quad lies on exactly one).
// Complete include/exclude DFS over a FIXED cell order with:
//   - per-curve counters (4th stone refused), eager future-ban at cnt==3
//   - aliveFuture bound
//   - cnt==2 curve greedy partition bound (sound; stale/evicted window entries only weaken it)
//   - optional min(S)=c chunking with order=index (sound disjoint complete partition)
//   - caps (--maxsec/--maxnodes) with honest CAP report
// Deterministic. No randomness.
'use strict';
const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
}
const N = parseInt(OPT.n || '9', 10);
const TARGET = parseInt(OPT.target || '0', 10);
const MINC = OPT.min !== undefined ? parseInt(OPT.min, 10) : -1;
let PREF;
if (OPT.prefix !== undefined) {
  PREF = OPT.prefix === '' ? [] : OPT.prefix.split(',').map(Number);
  for (const p of PREF) if (!Number.isInteger(p) || p < 0 || p >= N * N) throw new Error('bad prefix cell ' + p);
  for (let q = 1; q < PREF.length; q++) if (PREF[q] <= PREF[q - 1]) throw new Error('prefix must be strictly ascending');
} else {
  PREF = MINC >= 0 ? [MINC] : [];
}

const ORDER = OPT.order || 'index';
const MODE = OPT.mode || 'solve';
const MAXSEC = OPT.maxsec ? parseFloat(OPT.maxsec) : 0;
const MAXNODES = OPT.maxnodes ? parseFloat(OPT.maxnodes) : 0;
const USEBOUND = !OPT.nobound;

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function det3(m) { return m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6]) + m[2] * (m[3] * m[7] - m[4] * m[6]); }
function det4(m) {
  const M1 = [m[5], m[6], m[7], m[9], m[10], m[11], m[13], m[14], m[15]];
  const M2 = [m[4], m[6], m[7], m[8], m[10], m[11], m[12], m[14], m[15]];
  const M3 = [m[4], m[5], m[7], m[8], m[9], m[11], m[12], m[13], m[15]];
  const M4 = [m[4], m[5], m[6], m[8], m[9], m[10], m[12], m[13], m[14]];
  return m[0] * det3(M1) - m[1] * det3(M2) + m[2] * det3(M3) - m[3] * det3(M4);
}

function buildCensus(n) {
  const NCELL = n * n;
  const px = new Uint8Array(NCELL), py = new Uint8Array(NCELL);
  for (let p = 0; p < NCELL; p++) { px[p] = p % n; py[p] = (p / n) | 0; }
  const dirSet = new Set();
  for (let a = 0; a < NCELL; a++) for (let b = a + 1; b < NCELL; b++) {
    let dx = px[b] - px[a], dy = py[b] - py[a];
    const g = gcd(dx, dy); dx /= g; dy /= g;
    if (dx < 0 || (dx === 0 && dy < 0)) { dx = -dx; dy = -dy; }
    dirSet.add(dx * 100 + dy);
  }
  const lines = [], seen = new Set();
  for (const d of dirSet) {
    const dx = Math.round(d / 100), dy = d - dx * 100;
    const local = new Map();
    for (let p = 0; p < NCELL; p++) { const cr = px[p] * dy - py[p] * dx; if (!local.has(cr)) local.set(cr, []); local.get(cr).push(p); }
    for (const arr of local.values()) if (arr.length >= 4) {
      arr.sort((a, b) => a - b);
      const kk = 'L(' + arr.join(',') + ')';
      if (!seen.has(kk)) { seen.add(kk); lines.push(arr); }
    }
  }
  const circSet = new Set();
  for (let a = 0; a < NCELL; a++) for (let b = a + 1; b < NCELL; b++) for (let c = b + 1; c < NCELL; c++) {
    const x1 = px[a], y1 = py[a], x2 = px[b], y2 = py[b], x3 = px[c], y3 = py[c];
    const dA = x1 * (y2 - y3) - y1 * (x2 - x3) + (x2 * y3 - x3 * y2);
    if (dA === 0) continue;
    const b1 = -(x1 * x1 + y1 * y1), b2 = -(x2 * x2 + y2 * y2), b3 = -(x3 * x3 + y3 * y3);
    const u = det3([b1, y1, 1, b2, y2, 1, b3, y3, 1]);
    const v = det3([x1, b1, 1, x2, b2, 1, x3, b3, 1]);
    const w = det3([x1, y1, b1, x2, y2, b2, x3, y3, b3]);
    let g = dA, gu = u, gv = v, gw = w;
    const gg = gcd(gcd(gcd(g, gu), gv), gw);
    g /= gg; gu /= gg; gv /= gg; gw /= gg;
    if (g < 0) { g = -g; gu = -gu; gv = -gv; gw = -gw; }
    circSet.add(g + ',' + gu + ',' + gv + ',' + gw);
  }
  const circles = [];
  for (const key of circSet) {
    const [g, u, v, w] = key.split(',').map(Number);
    const cells = [];
    for (let p = 0; p < NCELL; p++) { const x = px[p], y = py[p]; if (g * (x * x + y * y) + u * x + v * y + w === 0) cells.push(p); }
    if (cells.length >= 4) circles.push(cells);
  }
  const curves = lines.concat(circles);
  let Fq = 0, Fline = 0, Fcirc = 0;
  for (const cv of lines) { const t = cv.length; Fline += (t * (t - 1) * (t - 2) * (t - 3)) / 24; }
  for (const cv of circles) { const t = cv.length; Fcirc += (t * (t - 1) * (t - 2) * (t - 3)) / 24; }
  Fq = Fline + Fcirc;
  return { NCELL, px, py, curves, Fq, Fline, Fcirc, nLines: lines.length, nCirc: circles.length };
}

function solve(n, target, pref, order) {
  const { NCELL, curves } = buildCensus(n);
  const curMem = curves.map(cv => Int32Array.from(cv));
  const cellCurves = Array.from({ length: NCELL }, () => []);
  curMem.forEach((cv, ci) => { for (const c of cv) cellCurves[c].push(ci); });
  let perm = Array.from({ length: NCELL }, (_, i) => i);
  if (order === 'degdesc') perm.sort((a, b) => cellCurves[b].length - cellCurves[a].length || a - b);
  else if (order === 'degrev') perm.sort((a, b) => cellCurves[a].length - cellCurves[b].length || a - b);
  const inv = new Int32Array(NCELL);
  for (let k = 0; k < NCELL; k++) inv[perm[k]] = k;
  const W = Math.ceil(NCELL / 32);
  const nCurves = curves.length;
  const cnt = new Uint8Array(nCurves);
  const alive = new Uint32Array(W);
  for (let i = 0; i < NCELL; i++) alive[(i / 32) | 0] |= 1 << (i % 32);
  let aliveFuture = NCELL;
  // exact cnt==2 stack: push at 1->2 transition of each include, pop on its undo (LIFO-consistent)
  const bucket2 = new Int32Array(nCurves * 4); // stack storage
  let b2n = 0; // stack size == number of curves with cnt==2 on the current path
  const B2P = new Int32Array(NCELL); // generation stamps per cell for bound grouping
  let b2gen = 0;
  const BOUNDBGATE = OPT.boundgate ? parseInt(OPT.boundgate, 10) : 16;
  let nodes = 0, capsHit = false, boundChecks = 0, boundPrunes = 0;
  let found = null;
  const chosen = [];
  const t0 = Date.now();
  function pushB2(ci) { bucket2[b2n++] = ci; }
  function popB2() { b2n--; }
  function dfs(pos, k) {
    nodes++;
    if (MAXNODES && nodes > MAXNODES) { capsHit = true; return true; }
    if ((nodes & 0x3FFFF) === 0 && MAXSEC && (Date.now() - t0) > MAXSEC * 1000) { capsHit = true; return true; }
    if (k === target) { found = chosen.slice(); return true; }
    if (aliveFuture < target - k) return false;
    if (USEBOUND && aliveFuture - (target - k) <= BOUNDBGATE) {
      boundChecks++;
      // greedy disjoint grouping (sound): each cnt==2 curve group admits <=1 more future stone;
      // generation stamps avoid per-node clearing; early exit once no prune possible
      b2gen++;
      let groups = 0;
      scan: {
        for (let x = 0; x < b2n; x++) {
          const ci = bucket2[x];
          const mem = curMem[ci];
          let toc = false;
          for (let q = 0; q < mem.length; q++) {
            const c2 = mem[q];
            if (inv[c2] < pos) continue;
            const w2 = (c2 / 32) | 0;
            if ((alive[w2] & (1 << (c2 % 32))) && B2P[c2] !== b2gen) { toc = true; break; }
          }
          if (toc) {
            groups++; if (k + groups >= target) break scan;
            for (let q = 0; q < mem.length; q++) {
              const c2 = mem[q];
              if (inv[c2] < pos) continue;
              const w2 = (c2 / 32) | 0;
              if (alive[w2] & (1 << (c2 % 32))) B2P[c2] = b2gen;
            }
          }
        }
        const needExtra = target - k - groups;
        for (let q = pos; q < NCELL; q++) {
          const cell2 = perm[q];
          const w2 = (cell2 / 32) | 0;
          if ((alive[w2] & (1 << (cell2 % 32))) && B2P[cell2] !== b2gen) { groups++; if (k + groups >= target) break; }
        }
      }
      if (k + groups < target) { boundPrunes++; return false; }
    }
    if (pos >= NCELL) return false;
    const cell = perm[pos];
    const wb = (cell / 32) | 0, bit = 1 << (cell % 32);
    const inc = (alive[wb] & bit) !== 0;
    if (inc) {
      const cvs = cellCurves[cell];
      let ok = true;
      for (let j = 0; j < cvs.length; j++) if (cnt[cvs[j]] === 3) { ok = false; break; }
      if (ok) {
        const pushed2 = [];
        for (const ci of cvs) { const was = cnt[ci]++; if (was === 1 && cnt[ci] === 2) { pushB2(ci); pushed2.push(ci); } }
        const bans = [];
        for (const ci of cvs) if (cnt[ci] === 3) bans.push(ci);
        const undoW = [], undoB = [];
        for (const ci of bans) for (const c2 of curMem[ci]) {
          if (c2 === cell || inv[c2] <= pos) continue;
          const w = (c2 / 32) | 0, b2 = 1 << (c2 % 32);
          if (alive[w] & b2) { alive[w] &= ~b2; undoW.push(w); undoB.push(b2); aliveFuture--; }
        }
        aliveFuture--; chosen.push(cell);
        if (dfs(pos + 1, k + 1)) return true;
        chosen.pop(); aliveFuture++;
        for (let t = undoW.length - 1; t >= 0; t--) alive[undoW[t]] |= undoB[t];
        aliveFuture += undoW.length;
        for (let j = cvs.length - 1; j >= 0; j--) cnt[cvs[j]]--;
        for (let j = pushed2.length - 1; j >= 0; j--) popB2();
      } else {
        // forced exclude (include would violate a saturated curve)
        alive[wb] &= ~bit; aliveFuture--;
        const r = dfs(pos + 1, k);
        alive[wb] |= bit; aliveFuture++;
        return r;
      }
    }
    if (inc) {
      alive[wb] &= ~bit; aliveFuture--;
      const r = dfs(pos + 1, k);
      alive[wb] |= bit; aliveFuture++;
      return r;
    }
    return dfs(pos + 1, k);
  }
  let sat = null;
  if (pref.length > 0) {
    if (order !== 'index') throw new Error('prefix chunking requires order=index');
    const m = pref.length;
    if (m > target) { sat = false; }
    else {
      let viol = false;
      let prev = -1;
      for (let i = 0; i < m && !viol; i++) {
        const p = pref[i];
        for (let c = prev + 1; c < p; c++) { const w = (c / 32) | 0, b = 1 << (c % 32); if (alive[w] & b) { alive[w] &= ~b; aliveFuture--; } }
        const cvs = cellCurves[p];
        for (const ci of cvs) if (cnt[ci] === 3) { viol = true; break; }
        if (!viol) {
          for (const ci of cvs) { const was = cnt[ci]++; if (was === 1 && cnt[ci] === 2) pushB2(ci); }
          const bans = [];
          for (const ci of cvs) if (cnt[ci] === 3) bans.push(ci);
          for (const ci of bans) for (const c2 of curMem[ci]) {
            if (c2 <= p) continue;
            let isLaterFixed = false;
            for (let q2 = i + 1; q2 < m; q2++) if (pref[q2] === c2) { isLaterFixed = true; break; }
            if (isLaterFixed) continue; // later fixed cells stay alive; their own fix-time check rejects saturation
            const w = (c2 / 32) | 0, b2 = 1 << (c2 % 32);
            if (alive[w] & b2) { alive[w] &= ~b2; aliveFuture--; }
          }
          chosen.push(p); aliveFuture--;
        }
        prev = p;
      }
      if (viol || target < 1) { sat = false; }
      else if (m === target) { sat = true; found = chosen.slice(); }
      else {
        const r = dfs(prev + 1, m);
        sat = capsHit ? null : r;
      }
    }
  } else {
    const r = dfs(0, 0);
    sat = capsHit ? null : r;
  }
  return { n, target, prefix: pref, order, NCELL, nCurves, sat, witness: sat ? found : null, nodes, ms: Date.now() - t0, capped: capsHit, boundChecks, boundPrunes };
}

if (MODE === 'census') {
  const res = buildCensus(N);
  console.log(JSON.stringify({ n: N, NCELL: res.NCELL, nLines: res.nLines, nCircles: res.nCirc, Fq: res.Fq, Fline: res.Fline, Fcirc: res.Fcirc }));
} else if (MODE === 'fcensus') {
  for (const n of [7, 8, 9]) {
    const NCELL = n * n;
    const bx = new Uint8Array(NCELL), by = new Uint8Array(NCELL);
    for (let p = 0; p < NCELL; p++) { bx[p] = p % n; by[p] = (p / n) | 0; }
    const pt = new Uint32Array(NCELL);
    for (let p = 0; p < NCELL; p++) pt[p] = bx[p] * bx[p] + by[p] * by[p];
    let Fbr = 0;
    const t0 = Date.now();
    for (let a = 0; a < NCELL; a++) for (let b = a + 1; b < NCELL; b++) for (let c = b + 1; c < NCELL; c++) for (let d = c + 1; d < NCELL; d++) {
      if (det4([pt[a], bx[a], by[a], 1, pt[b], bx[b], by[b], 1, pt[c], bx[c], by[c], 1, pt[d], bx[d], by[d], 1]) === 0) Fbr++;
    }
    const cu = buildCensus(n);
    console.log(JSON.stringify({ n, Fbrute: Fbr, Fcurves: cu.Fq, match: Fbr === cu.Fq, nLines: cu.nLines, nCircles: cu.nCirc, ms: Date.now() - t0 }));
  }
} else {
  const res = solve(N, TARGET, PREF, ORDER);
  console.log(JSON.stringify(res));
}
