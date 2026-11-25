#!/usr/bin/env node
// verify_witness_det.js — third-system witness verifier (pure integer arithmetic).
// Method-disjoint from sat.js (census counters) and verify_witness.py (Fraction D,E,F):
//   safety: no line (integer cross-product key) or circle (exact 4x4 integer
//           determinant through (x^2+y^2, x, y, 1)) holds >= q stones;
//   maximality: every empty cell lies on a line/circle with >= q-1 stones;
//   deficiency: some row has <= q-2 stones.
// No repo code used. Usage: verify_witness_det.js w m q < stones.json  ([[x,y],...])
'use strict';
const fs = require('fs');

function det4(M) { // exact integer 4x4 determinant, cofactor expansion
  let s = 0n;
  for (let c = 0; c < 4; c++) {
    const minor = [];
    for (let i = 1; i < 4; i++) {
      const row = [];
      for (let j = 0; j < 4; j++) if (j !== c) row.push(M[i][j]);
      minor.push(row);
    }
    const d = minor[0][0] * (minor[1][1] * minor[2][2] - minor[1][2] * minor[2][1])
            - minor[0][1] * (minor[1][0] * minor[2][2] - minor[1][2] * minor[2][0])
            + minor[0][2] * (minor[1][0] * minor[2][1] - minor[1][1] * minor[2][0]);
    s += BigInt(c % 2 === 0 ? 1 : -1) * BigInt(M[0][c]) * BigInt(d);
  }
  return s;
}
function onCircle4(p1, p2, p3, p) { // p on circle through p1,p2,p3 (integer det)
  const row = (a) => [a[0] * a[0] + a[1] * a[1], a[0], a[1], 1];
  return det4([row(p1), row(p2), row(p3), row(p)]) === 0n;
}
function lineKey(p, r) {
  const a = r[1] - p[1], b = p[0] - r[0], c = r[0] * p[1] - p[0] * r[1];
  const g = gcd(gcd(Math.abs(a), Math.abs(b)), Math.abs(c)) || 1;
  let A = a / g, B = b / g, C = c / g;
  if (A < 0 || (A === 0 && B < 0)) { A = -A; B = -B; C = -C; }
  return [A, B, C];
}
function gcd(a, b) { while (b) { const t = a % b; a = b; b = t; } return a; }
function onLine(k, p) { return k[0] * p[0] + k[1] * p[1] + k[2] === 0; }

function main() {
  // built-in self-tests (must pass before any witness verdict)
  const rt = (a) => [a[0] * a[0] + a[1] * a[1], a[0], a[1], 1];
  if (det4([rt([0, 0]), rt([1, 0]), rt([0, 1]), rt([1, 1])]) !== 0n) { console.log('{"ok":false,"err":"selftest-concyclic"}'); return; }
  if (det4([rt([0, 0]), rt([1, 0]), rt([0, 1]), rt([2, 2])]) === 0n) { console.log('{"ok":false,"err":"selftest-generic"}'); return; }
  if (!onCircle4([0, 0], [1, 0], [0, 1], [1, 1])) { console.log('{"ok":false,"err":"selftest-oncircle"}'); return; }
  const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
  const stones = JSON.parse(fs.readFileSync(process.argv[5] ?? 0, 'utf8'));
  if (process.argv[2] === undefined) { console.error('usage: verify_witness_det.js w m q stones.json'); process.exit(2); }
  const st = stones.map(([x, y]) => [Number(x), Number(y)]);
  const S = new Set(st.map(p => p.join(',')));
  const N = st.length;
  const rows = new Array(w).fill(0);
  for (const [x, y] of st) { if (!(x >= 0 && x < m && y >= 0 && y < w)) { console.log('{"ok":false,"err":"bounds"}'); return; } rows[y]++; }

  // safety via line census + circle determinant membership
  const lineCount = new Map();
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    const k = lineKey(st[i], st[j]);
    const kk = k.join(',');
    lineCount.set(kk, (lineCount.get(kk) ?? 0) + 1);
  }
  // number of stones on a line == pairs on it (any two stones determine it) -> stones = (1+sqrt(1+8p))/2
  let maxLine = 0;
  const circleCounts = [];
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k2 = j + 1; k2 < N; k2++) {
    const p1 = st[i], p2 = st[j], p3 = st[k2];
    const a = p2[1] - p1[1], b = p1[0] - p2[0];
    if (a * p3[0] + b * p3[1] + (p2[0] * p1[1] - p1[0] * p2[1]) === 0) continue; // collinear triple
    const cnt = st.filter(p => onCircle4(p1, p2, p3, p)).length;
    circleCounts.push([p1, p2, p3, cnt]);
  }
  for (const [kk, pc] of lineCount) {
    const n = (1 + Math.round(Math.sqrt(1 + 8 * pc))) / 2;
    if (n !== Math.floor(n)) { console.log('{"ok":false,"err":"line-pair-mismatch"}'); return; }
    if (n > maxLine) maxLine = n;
  }
  const maxCircle = circleCounts.reduce((a, c) => Math.max(a, c[3]), 0);
  if (maxLine >= q || maxCircle >= q) { console.log(JSON.stringify({ ok: false, maxLine, maxCircle })); return; }

  // maximality: every empty cell on a curve with >= q-1 stones
  let uncovered = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) {
    const p = [x, y];
    if (S.has(p.join(','))) continue;
    let blocked = false;
    for (const [p1, p2] of pairsOf(st)) {
      if (onLine(lineKey(p1, p2), p)) {
        const cnt = st.filter(s => onLine(lineKey(p1, p2), s)).length;
        if (cnt >= q - 1) { blocked = true; break; }
      }
    }
    if (!blocked) for (const [p1, p2, p3] of triplesOf(st)) {
      const a = p2[1] - p1[1], b = p1[0] - p2[0];
      if (a * p3[0] + b * p3[1] + (p2[0] * p1[1] - p1[0] * p2[1]) === 0) continue;
      if (onCircle4(p1, p2, p3, p)) {
        const cnt = st.filter(s => onCircle4(p1, p2, p3, s)).length;
        if (cnt >= q - 1) { blocked = true; break; }
      }
    }
    if (!blocked) uncovered.push(p);
  }
  const minRow = Math.min(...rows);
  const deficient = rows.some(r => r <= q - 2);
  const ok = uncovered.length === 0 && maxLine < q && maxCircle < q && deficient;
  console.log(JSON.stringify({ ok, n: N, rows, min_row: minRow, maxLine, maxCircle, uncovered: uncovered.length }));
}
function* pairsOf(st) { for (let i = 0; i < st.length; i++) for (let j = i + 1; j < st.length; j++) yield [st[i], st[j]]; }
function* triplesOf(st) { for (let i = 0; i < st.length; i++) for (let j = i + 1; j < st.length; j++) for (let k2 = j + 1; k2 < st.length; k2++) yield [st[i], st[j], st[k2]]; }
main();
