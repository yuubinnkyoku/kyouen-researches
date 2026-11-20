#!/usr/bin/env node
// naive reference solver: include/exclude DFS, violation check ONLY via direct forbidden-quad
// membership (4x4 det over (x^2+y^2,x,y,1) == 0), no curve census, no ban propagation.
// Slow but minimal-assumption reference to cross-check ksearch.js.
'use strict';
const OPT = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) { const eq = a.indexOf('='); OPT[a.slice(2, eq)] = a.slice(eq + 1); }
}
const N = parseInt(OPT.n || '5', 10);
const TARGET = parseInt(OPT.target || '9', 10);
const MAXSEC = OPT.maxsec ? parseFloat(OPT.maxsec) : 120;

function det3(m) { return m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6]) + m[2] * (m[3] * m[7] - m[4] * m[6]); }
function det4(m) {
  const M1 = [m[5], m[6], m[7], m[9], m[10], m[11], m[13], m[14], m[15]];
  const M2 = [m[4], m[6], m[7], m[8], m[10], m[11], m[12], m[14], m[15]];
  const M3 = [m[4], m[5], m[7], m[8], m[9], m[11], m[12], m[13], m[15]];
  const M4 = [m[4], m[5], m[6], m[8], m[9], m[10], m[12], m[13], m[14]];
  return m[0] * det3(M1) - m[1] * det3(M2) + m[2] * det3(M3) - m[3] * det3(M4);
}
const NCELL = N * N;
const bx = new Uint8Array(NCELL), by = new Uint8Array(NCELL), pt = new Uint32Array(NCELL);
for (let p = 0; p < NCELL; p++) { bx[p] = p % N; by[p] = (p / N) | 0; pt[p] = bx[p] * bx[p] + by[p] * by[p]; }
// forbidden quads per cell (quads containing cell)
const quadsOf = Array.from({ length: NCELL }, () => []);
let F = 0;
for (let a = 0; a < NCELL; a++) for (let b = a + 1; b < NCELL; b++) for (let c = b + 1; c < NCELL; c++) for (let d = c + 1; d < NCELL; d++) {
  if (det4([pt[a], bx[a], by[a], 1, pt[b], bx[b], by[b], 1, pt[c], bx[c], by[c], 1, pt[d], bx[d], by[d], 1]) === 0) {
    F++;
    for (const x of [[a, b, c, d], [a, b, d, c], [a, c, d, b]]) { void x; }
    quadsOf[a].push(b * NCELL * NCELL + c * NCELL + d); // encode triple relative to a
  }
}
// decode helper
function tripleOf(base, code) {
  const b = (code / (NCELL * NCELL)) | 0, c = ((code / NCELL) | 0) % NCELL, d = code % NCELL;
  return [b + base * 0, c, d]; // no
}
void tripleOf;
// simpler storage: 3 separate arrays appended per cell
const qA = [], qB = [], qC = []; // parallel; rebuilt below
{
  quadsOf.forEach((_, i) => { quadsOf[i] = []; });
  for (let a = 0; a < NCELL; a++) for (let b = a + 1; b < NCELL; b++) for (let c = b + 1; c < NCELL; c++) for (let d = c + 1; d < NCELL; d++) {
    if (det4([pt[a], bx[a], by[a], 1, pt[b], bx[b], by[b], 1, pt[c], bx[c], by[c], 1, pt[d], bx[d], by[d], 1]) === 0) {
      quadsOf[a].push([b, c, d]);
      quadsOf[b].push([a, c, d]);
      quadsOf[c].push([a, b, d]);
      quadsOf[d].push([a, b, c]);
    }
  }
  void qA;
}
const inS = new Uint8Array(NCELL);
const chosen = [];
let nodes = 0;
const t0 = Date.now();
let sat = false, wit = null;
function dfs(pos, k) {
  nodes++;
  if ((nodes & 0xFFFFF) === 0 && (Date.now() - t0) > MAXSEC * 1000) return 'CAP';
  if (k === TARGET) { sat = true; wit = chosen.slice(); return true; }
  if (pos >= NCELL) return false;
  if (k + (NCELL - pos) < TARGET) return false;
  // try include
  const cell = pos;
  let ok = true;
  for (const [b, c, d] of quadsOf[cell]) {
    if (inS[b] && inS[c] && inS[d]) { ok = false; break; }
  }
  if (ok) {
    inS[cell] = 1; chosen.push(cell);
    if (dfs(pos + 1, k + 1)) return true;
    chosen.pop(); inS[cell] = 0;
  }
  const r = dfs(pos + 1, k);
  return r;
}
const res = dfs(0, 0);
console.log(JSON.stringify({ n: N, target: TARGET, F, sat, witness: wit, nodes, ms: Date.now() - t0, verdict: res === true ? (sat ? 'SAT' : 'done') : String(res) }));
