#!/usr/bin/env node
// gen_strong_cnf.js - at-least-k CNF for the n x n maximum-safe-set problem with REDUNDANT
// strengthening clauses (logically implied by the forbidden quads, so the SAT/UNSAT verdict
// over the cell variables is unchanged):
//   (S1) per-dangerous-curve sequential counter at-most-3 (every subset of 4 cells on a
//        curve is a forbidden quad, so at most 3 cells of each curve can be chosen)
//   (S2) reverse-order at-least-k sequential counter (same constraint, opposite scan order)
// Positive/negative controls and the published-plain-CNF equivalence anchors are checked
// by eval_strong.js. Deterministic output (fixed algorithms, no randomness).
'use strict';
const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
}
const N = parseInt(OPT.n || '9', 10);
const K = parseInt(OPT.k || '19', 10);
const OUT = OPT.out || 'output';

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a || 1; }
function det3(m) { return m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6]) + m[2] * (m[3] * m[7] - m[4] * m[6]); }

// census (same algorithm as ksearch.js)
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
  let Fq = 0;
  for (const cv of curves) { const t = cv.length; Fq += (t * (t - 1) * (t - 2) * (t - 3)) / 24; }
  return { NCELL, curves, Fq, nLines: lines.length, nCirc: circles.length };
}

const { NCELL, curves, Fq, nLines, nCirc } = buildCensus(N);
// vars: cell p (0-based) -> p+1. then global counter, then per-curve counters, then reverse counter.
let nv = NCELL;
const clauseRe = [];
function lit(v) { return v; }
function clause(...ls) { clauseRe.push(ls.map(x => (x < 0 ? -(-x) : x)).join(' ') + ' 0'); }
// ---- forbidden quads (sorted tuples from curves) ----
let quadCnt = 0;
for (const cv of curves) {
  const t = cv.length;
  if (t < 4) continue;
  const c = cv.slice().sort((a, b) => a - b);
  // all 4-subsets
  for (let i = 0; i < t - 3; i++) for (let j = i + 1; j < t - 2; j++) for (let k = j + 1; k < t - 1; k++) for (let l = k + 1; l < t; l++) {
    clause(-(c[i] + 1), -(c[j] + 1), -(c[k] + 1), -(c[l] + 1));
    quadCnt++;
  }
}
// ---- global at-least-K sequential counter (forward order), house convention ----
let fwdMap = {};
{
  // a[i][j] with i in 1..NCELL, j in 1..min(i,K); ids assigned i-ascending then j
  const idOf = new Int32Array((NCELL + 1) * (K + 1)).fill(0);
  let next = nv + 1;
  for (let i = 1; i <= NCELL; i++) for (let j = 1; j <= Math.min(i, K); j++) { idOf[i * (K + 1) + j] = next++; }
  nv = next - 1;
  const g = (i, j) => idOf[i * (K + 1) + j];
  for (let i = 1; i <= NCELL; i++) {
    for (let j = 1; j <= Math.min(i, K); j++) {
      const gi = g(i, j), gim = (i >= 1 && j <= i - 1) ? g(i - 1, j) : 0;
      const gim1 = (j >= 2 && j - 1 <= i - 1) ? g(i - 1, j - 1) : 0;
      const xi = i; // cell var p+1 with p = i-1
      // definitional: s(i,j) <-> s(i-1,j) OR (x_i AND s(i-1,j-1))
      if (gim) clause(-gim, gi); // s(i-1,j) -> s(i,j)
      if (gim1) clause(-xi, -gim1, gi); // (x_i AND s(i-1,j-1)) -> s(i,j)
      else if (j === 1) clause(-xi, gi); // x_i -> s(i,1)
      if (gim) clause(-gi, gim, xi);
      else clause(-gi, xi); // gim==0 (i.e. j==i): s(i,j) -> x_i — the diagonal/boundary upper mirror, required for soundness
      if (gim1) { if (gim) clause(-gi, gim1, gim); else clause(-gi, gim1); } // s(i,j) -> s(i-1,j) OR s(i-1,j-1); when j==i, s(i-1,j) is a false constant
    }
  }
  clause(g(NCELL, K)); // at least K
  for (let i = 1; i <= NCELL; i++) for (let j = 1; j <= Math.min(i, K); j++) fwdMap[i + ',' + j] = idOf[i * (K + 1) + j];
}
// ---- (S1) per-curve at-most-3 sequential counters (redundant strengthening) ----
let curveBlocks = [];
{
  let next = nv + 1;
  let cbi = 0;
  for (const cv of curves) {
    const pts = cv.slice().sort((a, b) => a - b);
    const t = pts.length;
    // s'[i][j]: >= j of pts[0..i] chosen, j in 1..3 (only need up to 3)
    const id = [];
    for (let i = 1; i <= t; i++) { id[i] = [0, next, next + 1, next + 2]; next += 3; }
    const blk = { points: pts, sIds: {} };
    for (let i = 1; i <= t; i++) for (let j = 1; j <= 3; j++) blk.sIds[i + ',' + j] = id[i][j];
    curveBlocks.push(blk);
    void cbi; cbi++;
    for (let i = 1; i <= t; i++) {
      const xi = pts[i - 1] + 1;
      for (let j = 1; j <= Math.min(i, 3); j++) {
        const gi = id[i][j];
        const gim = j <= i - 1 ? id[i - 1][j] : 0;
        const gim1 = (j >= 2 && j - 1 <= i - 1) ? id[i - 1][j - 1] : 0;
        if (gim) clause(-gim, gi);
        if (gim1) clause(-xi, -gim1, gi);
        else if (j === 1) clause(-xi, gi);
        if (gim) clause(-gi, gim, xi);
        else clause(-gi, xi);
        if (gim1) { if (gim) clause(-gi, gim, gim1); else clause(-gi, gim1); }
      }
      // at-most-3: x_i AND s(i-1,3) forbidden
      if (i >= 2) clause(-xi, -id[i - 1][3]);
      if (i === 1) { /* fine */ }
    }
  }
  nv = next - 1;
}
// ---- (S2) reverse-order at-least-K counter (redundant) ----
let revMap = {};
{
  const idOf = new Int32Array((NCELL + 1) * (K + 1)).fill(0);
  let next = nv + 1;
  // r[u][j]: >= j among the last u cells (reverse scan); the u-th cell in reverse order
  // is cell p = NCELL-u (var NCELL-u+1)
  for (let u = 1; u <= NCELL; u++) for (let j = 1; j <= Math.min(u, K); j++) { idOf[u * (K + 1) + j] = next++; }
  nv = next - 1;
  const g = (u, j) => idOf[u * (K + 1) + j];
  for (let u = 1; u <= NCELL; u++) {
    const xv = NCELL - u + 1; // cell var of the u-th cell in reverse order (p = NCELL-u, var p+1)
    for (let j = 1; j <= Math.min(u, K); j++) {
      const gi = g(u, j);
      const gim = j <= u - 1 ? g(u - 1, j) : 0;
      const gim1 = (j >= 2 && j - 1 <= u - 1) ? g(u - 1, j - 1) : 0;
      if (gim) clause(-gim, gi);
      if (gim1) clause(-xv, -gim1, gi);
      else if (j === 1) clause(-xv, gi);
      if (gim) clause(-gi, gim, xv);
      else clause(-gi, xv);
      if (gim1) { if (gim) clause(-gi, gim, gim1); else clause(-gi, gim1); }
    }
  }
  clause(g(NCELL, K));
  for (let u = 1; u <= NCELL; u++) for (let j = 1; j <= Math.min(u, K); j++) revMap[u + ',' + j] = idOf[u * (K + 1) + j];
}
const header = `p cnf ${nv} ${clauseRe.length}`;
const { writeFileSync, mkdirSync } = require('fs');
mkdirSync(OUT, { recursive: true });
const fn = `${OUT}/n${N}_ge${K}_strong.cnf`;
writeFileSync(fn, header + '\n' + clauseRe.join('\n') + '\n');
const mapFn = `${OUT}/n${N}_ge${K}_strong.map.json`;
writeFileSync(mapFn, JSON.stringify({ n: N, K, NCELL, nv, nClauses: clauseRe.length, fwd: fwdMap, rev: revMap, curves: curveBlocks }));
// fnv1a-64 for integrity
function fnv1a64(str) {
  let h = 0xcbf29ce484222325n;
  let p = 0; const prime = 0x100000001b3n;
  while (p < str.length) {
    h ^= BigInt(str.charCodeAt(p));
    h = BigInt.asUintN(64, h * prime);
    p++;
  }
  return h.toString(16).padStart(16, '0');
}
const fs2 = require('fs');
const bytes = fs2.readFileSync(fn, 'utf8');
console.log(JSON.stringify({ file: fn, n: N, K, vars: nv, clauses: clauseRe.length, quadClauses: quadCnt, nCurves: curves.length, nLines, nCirc, Fcurves: Fq, fnv1a64: fnv1a64(bytes) }));
