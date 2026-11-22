#!/usr/bin/env node
// Independent verifier family 3: BigInt 4x4 determinant (Bareiss) safety
// + BigInt line/circle blocking. Pure ECMAScript, no dependencies.
//
// Usage: node verify_node.mjs <bank.json>
// bank.json: {w, q, items: [{tag, m, stones}, ...]}
'use strict';
import { readFileSync } from 'fs';

const big = (x) => BigInt(x);

function det4(rows) { // Bareiss fraction-free elimination with pivoting
  const a = rows.map(r => r.map(big));
  let sign = 1n, prev = 1n;
  for (let k = 0; k < 3; k++) {
    if (a[k][k] === 0n) {
      let sw = -1;
      for (let i = k + 1; i < 4; i++) if (a[i][k] !== 0n) { sw = i; break; }
      if (sw < 0) return 0n;
      [a[k], a[sw]] = [a[sw], a[k]];
      sign = -sign;
    }
    for (let i = k + 1; i < 4; i++) {
      for (let j = k + 1; j < 4; j++) {
        a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) / prev;
      }
    }
    prev = a[k][k];
  }
  return sign * a[3][3];
}

function concyclicOrCollinear(p1, p2, p3, p4) {
  const rows = [p1, p2, p3, p4].map(([x, y]) =>
    [big(x), big(y), big(x) * big(x) + big(y) * big(y), 1n]);
  return det4(rows) === 0n;
}

function lineOf(p, q) { // primitive integer direction
  let dx = big(q[0]) - big(p[0]), dy = big(q[1]) - big(p[1]);
  const g = gcd(abs(dx), abs(dy)) || 1n;
  dx /= g; dy /= g;
  return { x0: big(p[0]), y0: big(p[1]), dx, dy };
}
function abs(x) { return x < 0n ? -x : x; }
function gcd(a, b) { while (b) { [a, b] = [b, a % b]; } return a; }
function onLine(ln, c) {
  return ln.dx * (big(c[1]) - ln.y0) === ln.dy * (big(c[0]) - ln.x0);
}
function lineCells(p, q, w, m) {
  const ln = lineOf(p, q);
  const out = [];
  let x = ln.x0, y = ln.y0;
  while (x >= 0n && x < big(m) && y >= 0n && y < big(w)) {
    out.push([Number(x), Number(y)]); x += ln.dx; y += ln.dy;
  }
  x = ln.x0 - ln.dx; y = ln.y0 - ln.dy;
  while (x >= 0n && x < big(m) && y >= 0n && y < big(w)) {
    out.push([Number(x), Number(y)]); x -= ln.dx; y -= ln.dy;
  }
  return out;
}
function circleOf(p1, p2, p3) {
  // det*(x^2+y^2) + Nd*x + Ne*y + Fnum = 0 through the 3 points
  // (Cramer; coefficients kept exact by clearing the denominator `det`)
  const [x1, y1] = p1, [x2, y2] = p2, [x3, y3] = p3;
  const A = [[big(x2 - x1), big(y2 - y1)],
             [big(x3 - x1), big(y3 - y1)]];
  const det = A[0][0] * A[1][1] - A[0][1] * A[1][0];
  if (det === 0n) return null; // collinear
  const v1 = big(x2*x2 + y2*y2 - x1*x1 - y1*y1);
  const v2 = big(x3*x3 + y3*y3 - x1*x1 - y1*y1);
  // Dp = Nd/det with Dp*A11 + Ep*A12 = -v1, Dp*A21 + Ep*A22 = -v2
  const Nd = (v2 * A[0][1] - v1 * A[1][1]);
  const Ne = (v1 * A[1][0] - v2 * A[0][0]);
  const Fnum = -det * (big(x1) * big(x1) + big(y1) * big(y1))
                - Nd * big(x1) - Ne * big(y1);
  return [det, Nd, Ne, Fnum];
}
function onCircle(cc, c) {
  const [a, b, d, f] = cc;
  const x = big(c[0]), y = big(c[1]);
  return a * (x * x + y * y) + b * x + d * y + f === 0n;
}

function verify(stones, w, m, q) {
  const st = stones.map(s => [s[0] | 0, s[1] | 0]).sort((p, r) => p[0] - r[0] || p[1] - r[1]);
  const res = { safe: true, maximal: true, rows: new Array(w).fill(0), ok: null,
                uncovered: [], tamperAddFails: null };
  const stset = new Set(st.map(p => p.join(',')));
  for (const [, y] of st) res.rows[y]++;
  res.rowDeficient = Math.min(...res.rows) < q - 1;
  // safety via det4 over all q-subsets (q=4)
  const n = st.length;
  outer:
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++)
  for (let k2 = j+1; k2 < n; k2++) for (let l = k2+1; l < n; l++) {
    if (concyclicOrCollinear(st[i], st[j], st[k2], st[l])) {
      res.safe = false; break outer;
    }
  }
  // blocking via triple descriptors
  const descs = [];
  for (let i = 0; i < n; i++) for (let j = i+1; j < n; j++)
  for (let k2 = j+1; k2 < n; k2++) {
    const tri = [st[i], st[j], st[k2]];
    const ln = lineOf(tri[0], tri[1]);
    if (onLine(ln, tri[2])) descs.push({ kind: 'L', ln });
    else descs.push({ kind: 'C', cc: circleOf(...tri) });
  }
  const unc = [];
  for (let x = 0; x < m; x++) for (let y = 0; y < w; y++) {
    const c = [x, y];
    if (stset.has(c.join(','))) continue;
    let blocked = false;
    for (const d of descs) {
      if (d.kind === 'L') { if (onLine(d.ln, c)) { blocked = true; break; } }
      else { if (onCircle(d.cc, c)) { blocked = true; break; } }
    }
    if (!blocked) unc.push(c);
  }
  res.uncovered = unc;
  res.maximal = unc.length === 0;
  res.ok = !!(res.safe && res.maximal && res.rowDeficient);
  // tamper: add a stone at a deterministic sample of (blocked) empty cells
  if (res.maximal) {
    const empty = [];
    for (let x = 0; x < m; x++) for (let y = 0; y < w; y++)
      if (!stset.has(x + ',' + y)) empty.push([x, y]);
    const step = Math.max(1, Math.floor(empty.length / 5));
    let checked = 0, fails = 0;
    for (let i = 0; i < empty.length && checked < 5; i += step) {
      const c = empty[i];
      let safe = true;
      const s2 = [...st, c].sort((p, r) => p[0] - r[0] || p[1] - r[1]);
      outer2:
      for (let a = 0; a < s2.length; a++) for (let b = a+1; b < s2.length; b++)
      for (let cc2 = b+1; cc2 < s2.length; cc2++) for (let d2 = cc2+1; d2 < s2.length; d2++) {
        if (concyclicOrCollinear(s2[a], s2[b], s2[cc2], s2[d2])) {
          safe = false; break outer2;
        }
      }
      checked++; if (!safe) fails++;
    }
    res.tamperAddFails = checked > 0 && fails === checked;
    res.tamperChecked = checked;
  }
  return res;
}

const bank = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const results = [];
for (const it of bank.items) {
  const r = verify(it.stones, bank.w, it.m, bank.q);
  r.tag = it.tag;
  results.push({ tag: it.tag, ok: r.ok, safe: r.safe, maximal: r.maximal,
                 rows: r.rows, rowDeficient: r.rowDeficient,
                 uncoveredCount: r.uncovered.length,
                 tamperAddFails: r.tamperAddFails, tamperChecked: r.tamperChecked });
}
process.stdout.write(JSON.stringify({ w: bank.w, q: bank.q, results },
                                    null, 1) + '\n');
