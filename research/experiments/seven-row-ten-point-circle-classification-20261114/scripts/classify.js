// classify.js — classify all >=q-point circles of a w x m grid by (rho^2, center y),
// reporting per-family: rows hit, point counts, x-center parity/integrality, members.
// Usage: node classify.js W M Q
'use strict';
const path = require('path');
process.env.SEVEN_SCRIPTS = process.env.SEVEN_SCRIPTS || '/home/user/krwork/seven/scripts';
const SEVEN = process.env.SEVEN_SCRIPTS;
const g2 = require(path.join(__dirname, 'genfast2.js')); // patches S.buildCensus (fastCensus)
const S2 = require(path.join(SEVEN, 'sat2.js'));
const [W, M, Q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];

// circles: S2.encodeCore gives curves with co=[a,b,c,d], pts (grid indices)
const { curves } = S2.encodeCore(W, M, Q);
const circles = curves.filter(c => c.type === 'circle');

function rat(num, den) { // canonical rational string
  let g = 1n; const n = BigInt(num), d = BigInt(den);
  if (d < 0n) { return rat(-num, -den); }
  g = (function gcd2(a, b) { while (b) { const t = a % b; a = b; b = t; } return a; })(n < 0n ? -n : n, d);
  return (n / g) + '/' + (d / g);
}

const fams = new Map();
const all = [];
for (const c of circles) {
  const [a, b, cc, d] = c.co;
  // center (bx: -b/(2a), by: -cc/(2a)); rho^2 = (b^2+cc^2)/(4a^2) - d/a
  const cx = rat(-b, 2 * a), cy = rat(-cc, 2 * a);
  const rho2 = rat(b * b + cc * cc - 4 * a * d, 4 * a * a);
  const rows = new Set(); let np = 0;
  for (const idx of c.pts) { rows.add(Math.floor(idx / M)); np++; }
  const key = rho2 + '|' + cy;
  const f = fams.get(key) || { rho2, cy, rows: [...rows].sort((x, y) => x - y), np: [], n: 0 };
  f.n++; f.np.push(np);
  fams.set(key, f);
  all.push({ cx, cy, rho2, np, rows: [...rows].sort((x, y) => x - y) });
}
const famsArr = [...fams.values()].map(f => ({
  rho2: f.rho2, cy: f.cy, rows: f.rows, count: f.n,
  npMin: Math.min(...f.np), npMax: Math.max(...f.np)
})).sort((x, y) => y.count - x.count);
console.log(JSON.stringify({ w: W, m: M, q: Q, circles: circles.length, families: famsArr }));
if (process.argv[5] === '--dump') console.log(JSON.stringify(all));
