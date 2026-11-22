// genfam12.js — family-census CNF generator for the 8xm q=11/q=12 band closure lane.
// Census: 8 horizontal rows + (m-7) twelve-point F1 circles ONLY (sound band-wide for m<=984
// by eight-row-strip-classification-20261115 Theorem A + Corollary 4: every in-board circle
// with >=11 points is a placement member of the F1 family; dropping curves only removes
// constraints, so family-census UNSAT implies full-census UNSAT).
// Everything below encodeCore is sat2.js verbatim via monkey-patched S.buildCensus:
// no encoding drift. Curve insertion order strictly matches buildCensus full enumeration:
// lines first (minimal 2-point occurrence order), then circles (minimal 3-point triple order).
// Original generator was lost before upload; rebuilt 2026-11-22 from the published README spec
// and calibrated 29/29 CNF byte-identity (see records/calibration-takeover-20261122.jsonl).
// Usage: node genfam12.js 8 <m> <q> [--deficient|--cap=K] [--lex=...] out.cnf
'use strict';
const S = require('./sat.js');

S.buildCensus = function familyCensus(w, m, q) {
  if (w !== 8) throw new Error('genfam12 supports w=8 only');
  if (q !== 11 && q !== 12) throw new Error('genfam12 supports q=11/q=12 only');
  if (m < 7) throw new Error('m >= 7 required');
  const P = S.pts(w, m);
  const n = P.length;
  const idx = (x, y) => y * m + x;
  const curves = [];

  // rows first: buildCensus full-census order = per row y asc, lo = lineABC(P[y*m], P[y*m+1]) = [0,1,-y]
  for (let y = 0; y < 8; y++) {
    const lo = S.lineABC(P[y * m], P[y * m + 1]);
    const set = [];
    for (let x = 0; x < m; x++) set.push(idx(x, y));
    curves.push({ type: 'line', co: lo, pts: set }); // m points >= q
  }

  // F1 circles: center (u, 7/2), u = u2/2 with u2 in {7, 9, ..., 2m-9} (half-integers),
  // (2x-u2)^2 + (2y-7)^2 = 50 -> 12 lattice points, rows {0,1,3,4,6,7} x 2 each, rows 2,5 untouched.
  // x offsets per row: 2x = u2 + {-1,+1} (rows 0,7); u2 + {-5,+5} (rows 1,6); u2 + {-7,+7} (rows 3,4).
  const circles = [];
  for (let u2 = 7; u2 <= 2 * m - 9; u2 += 2) {
    const co = S.circleABC([(u2 - 1) / 2, 0], [(u2 + 1) / 2, 0], [(u2 - 5) / 2, 1]);
    if (co === null) throw new Error('degenerate F1 circle u2=' + u2);
    const pts = [
      idx((u2 - 1) / 2, 0), idx((u2 + 1) / 2, 0),
      idx((u2 - 5) / 2, 1), idx((u2 + 5) / 2, 1),
      idx((u2 - 7) / 2, 3), idx((u2 + 7) / 2, 3),
      idx((u2 - 7) / 2, 4), idx((u2 + 7) / 2, 4),
      idx((u2 - 5) / 2, 6), idx((u2 + 5) / 2, 6),
      idx((u2 - 1) / 2, 7), idx((u2 + 1) / 2, 7),
    ].sort((a, c) => a - c);
    if (pts.length !== 12) throw new Error('F1 circle point count != 12');
    // verify all 12 points are on the canonical circle (defensive)
    for (const p of pts) {
      if (!S.onCircle(co, P[p][0], P[p][1])) throw new Error('F1 membership failure u2=' + u2);
    }
    circles.push({ tripleKey: pts.slice(0, 3), cu: { type: 'circle', co, pts } });
  }
  // circles in minimal-3-point-triple order (== full buildCensus circMap insertion order)
  circles.sort((a, c) => {
    for (let i = 0; i < 3; i++) {
      if (a.tripleKey[i] !== c.tripleKey[i]) return a.tripleKey[i] - c.tripleKey[i];
    }
    return 0;
  });
  for (const c of circles) curves.push(c.cu);
  return { P, n, curves };
};

const sat2 = require('./sat2.js');

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let i = 3, mode = 'deficient', cap = null, cnt = 'seq', lex = [], rowY = null, out = null;
  for (; i < args.length; i++) {
    const a = args[i];
    if (a === '--deficient') mode = 'deficient';
    else if (a.startsWith('--cap=')) { mode = 'cap'; cap = Number(a.slice(6)); }
    else if (a.startsWith('--counter=')) cnt = a.slice(10);
    else if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => ['H', 'V', 'HV'].includes(s));
    else if (a.startsWith('--rowY=')) { mode = 'rowfixed'; rowY = Number(a.slice(7)); }
    else if (!out) out = a;
  }
  if (!out) { console.error('usage: node genfam12.js 8 <m> <q> [opts] out.cnf'); process.exit(2); }
  const opts = { mode, cap, counter: cnt, lex, rowY };
  const { enc, meta } = sat2.dump(w, m, q, opts);
  require('fs').writeFileSync(out, sat2.toDimacs2(enc));
  meta.file = out;
  meta.generator = 'genfam12-recreation-20261122';
  console.log(JSON.stringify(meta));
}
module.exports = { S, familyCensus: S.buildCensus };
