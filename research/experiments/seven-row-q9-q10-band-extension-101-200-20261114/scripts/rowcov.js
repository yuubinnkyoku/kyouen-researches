// rowcov.js — per-row coverage census: for each row y, count cells of row y that
// lie on >=1 circle with >=q grid points (only circles can block cells of a
// deficient row; the row line itself has <= q-2 stones there and no other line
// has >=q points on a w-row board when q > w).
// Usage: node rowcov.js W M Q
'use strict';
const path = require('path');
process.env.SEVEN_SCRIPTS = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const SEVEN = process.env.SEVEN_SCRIPTS;
require(path.join(__dirname, 'genfast.js')); // patches S.buildCensus with fastCensus
const S2 = require(path.join(SEVEN, 'sat2.js'));
const [W, M, Q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const { curves } = S2.encodeCore(W, M, Q);
const circles = curves.filter(c => c.type === 'circle');
const lines = curves.filter(c => c.type === 'line');
const cov = Array.from({ length: W }, () => new Set());
const per = Array.from({ length: W }, () => 0); // circles meeting each row
for (const c of circles) {
  const rows = new Set();
  for (const p of c.pts) {
    const [x, y] = [p % M, Math.floor(p / M)];
    cov[y].add(x); rows.add(y);
  }
  for (const y of rows) per[y]++;
}
const out = { w: W, m: M, q: Q, lines: lines.length, circles: circles.length,
  rowCircles: per, rowCover: cov.map(s => s.size), rowNeed: M - (Q - 2),
  allRowsCoveredLtNeed: cov.every(s => s.size < M - (Q - 2)) };
console.log(JSON.stringify(out));
