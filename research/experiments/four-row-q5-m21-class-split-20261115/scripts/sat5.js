// sat5.js — blocker-circle pin split (--gpin/--emptytail) on top of sat3.js dumpClass.
// Case analysis on the right-end cell (y0, m-1) of the first deficient row y0=D[0],
// for a single-deficient-row instance with --krow=y0:k (k>=2) and --minpos=p:
//   A) cell (y0, m-1) is a stone : --gpin=(m-1):y0   (one instance)
//   B) cell (y0, m-1) is empty   : --emptytail + --gpin=<cells of a blocker circle>.
//      Maximality forces some count-4 circle g through (y0, m-1); safety forces
//      exactly 4 stones on g (5 would violate q). listcases enumerates (g, S):
//        S ⊆ g minus (y0,m-1) minus the cells forced empty by minpos (row y0, cols < p).
//        adapted (default): if the minpos stone (y0,p) lies on g, it is one of the
//          4 stones (already pinned by dumpClass), so S lists the other 3 cells.
//        plain: S always has 4 cells (p0 keeps the (0,0)-on-g special case) — used
//          only to cross-check the SA pin-sweep record (p1 83 / p0 86 cases).
//      Geometry: a circle meets a row (line) in <=2 points, so besides (y0,m-1)
//      the circle has at most one row-y0 cell; no extra feasibility filter needed.
//   Complete: any maximal config in the bucket has (y0,m-1) as a stone (covered by A)
//   or empty with a blocker circle whose stone set is pinned by some B instance.
//   All-UNSAT over A + B proves the bucket UNSAT.
// NOTE: like sat4 --x2, do not combine --gpin with --lex (unsound for the same
// reason); --minpos is required with --gpin/--emptytail.
// listcases is standalone (own counting census with a C(k,3) run-length sanity check;
// verified 2026-11-15 in TS sandbox: plain p1=83 / p0=86 reproduces the SA sweep
// record; adapted p1=81 / p0=86; g* yields exactly one case with pins 4:2,9:3,11:3,16:2).
'use strict';
const fs = require('fs');
const path = require('path');

// ---- standalone counting census: >=5-point circles as [x,y] point lists ----
function buildCircles5(w, m) {
  const gcd2 = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { const t = a % b; a = b; b = t; } return a; };
  const N = w * m;
  const xsOf = (c) => c % m;
  const ysOf = (c) => (c - (c % m)) / m;
  const A = [], B = [], C = [], D = [];
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) for (let k = j + 1; k < N; k++) {
    const x1 = xsOf(i), y1 = ysOf(i), x2 = xsOf(j), y2 = ysOf(j), x3 = xsOf(k), y3 = ysOf(k);
    const Dd = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
    if (Dd === 0) continue;
    const r1 = -(x1 * x1 + y1 * y1), r2 = -(x2 * x2 + y2 * y2), r3 = -(x3 * x3 + y3 * y3);
    let U = r1 * (y2 - y3) - y1 * (r2 - r3) + (r2 * y3 - r3 * y2);
    let V = x1 * (r2 - r3) - r1 * (x2 - x3) + (x2 * r3 - x3 * r2);
    let W = x1 * (y2 * r3 - y3 * r2) - y1 * (x2 * r3 - x3 * r2) + r1 * (x2 * y3 - x3 * y2);
    let Dn = Dd;
    if (Dn < 0) { Dn = -Dn; U = -U; V = -V; W = -W; }
    const g0 = gcd2(gcd2(Dn, U), gcd2(V, W)) || 1;
    A.push(Dn / g0); B.push(U / g0); C.push(V / g0); D.push(W / g0);
  }
  const T = A.length;
  const order = new Array(T);
  for (let i = 0; i < T; i++) order[i] = i;
  order.sort((p, q) => A[p] - A[q] || B[p] - B[q] || C[p] - C[q] || D[p] - D[q]);
  const circles = [];
  let t = 0;
  while (t < T) {
    const i0 = order[t]; const a0 = A[i0], b0 = B[i0], c0 = C[i0], d0 = D[i0];
    let u = t;
    while (u < T) { const i = order[u]; if (A[i] !== a0 || B[i] !== b0 || C[i] !== c0 || D[i] !== d0) break; u++; }
    const nTrip = u - t;
    if (nTrip >= 10) {
      const pts = [];
      for (let c = 0; c < N; c++)
        if (a0 * (xsOf(c) * xsOf(c) + ysOf(c) * ysOf(c)) + b0 * xsOf(c) + c0 * ysOf(c) + d0 === 0)
          pts.push([xsOf(c), ysOf(c)]);
      const kk = pts.length;
      if (kk * (kk - 1) * (kk - 2) / 6 !== nTrip) throw new Error('census sanity failure');
      circles.push(pts);
    }
    t = u;
  }
  return circles;
}

function kSubsets5(arr, k) {
  const res = [], cur = [];
  const rec = (start) => {
    if (cur.length === k) { res.push(cur.slice()); return; }
    for (let i = start; i < arr.length; i++) { cur.push(arr[i]); rec(i + 1); cur.pop(); }
  };
  rec(0);
  return res;
}

// (g, S) enumeration for --minpos=p on row y0=D[0]; target cell = (m-1, y0).
function enumerateGpinCases(w, m, D, p, mode) {
  const y0 = D[0];
  if (mode === 'plain' && p > 1) throw new Error('plain mode is a p0/p1 record cross-check only');
  const circles = buildCircles5(w, m);
  const cases = [];
  for (const pts of circles) {
    const onG = (x, y) => pts.some((q) => q[0] === x && q[1] === y);
    if (!onG(m - 1, y0)) continue;
    const forcedStoneOnG = onG(p, y0);
    let rest = pts.filter((q) => !(q[0] === m - 1 && q[1] === y0));
    let k;
    if (mode === 'plain') {
      rest = rest.filter((q) => !(q[1] === y0 && q[0] < p));
      if (p === 0 && forcedStoneOnG) { rest = rest.filter((q) => !(q[0] === 0 && q[1] === y0)); k = 3; }
      else k = 4;
    } else {
      if (forcedStoneOnG) { rest = rest.filter((q) => !(q[0] === p && q[1] === y0)); k = 3; }
      else k = 4;
      rest = rest.filter((q) => !(q[1] === y0 && q[0] < p));
    }
    for (const S of kSubsets5(rest, k)) {
      cases.push({ circle: pts, pins: S.map((q) => q[0] + ':' + q[1]).join(',') });
    }
  }
  return cases;
}

function dumpClassGpin(w, m, q, D, opts) {
  const S3 = require(path.join(__dirname, 'sat3.js'));
  if (opts.minpos == null) throw new Error('--minpos required with --gpin/--emptytail');
  if (opts.lex && opts.lex.length) throw new Error('--gpin with --lex is unsound');
  const { enc, cell } = S3.dumpClass(w, m, q, D, opts);
  const y0 = D[0];
  if (opts.emptytail) enc.add([[-cell[y0 * m + (m - 1)]]]);
  for (const xy of (opts.gpin || [])) enc.add([[cell[xy[1] * m + xy[0]]]]);
  const meta = { w, m, q, class: D.slice().sort((a, b) => a - b), krow: opts.krow || [], minpos: opts.minpos,
    gpin: (opts.gpin || []).map((xy) => xy.join(':')).join(','), emptytail: !!opts.emptytail, lex: [],
    vars: enc.nv, clauses: enc.clauses.length };
  return { enc, meta };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'listcases') {
    const w = Number(args[1]), m = Number(args[2]), q = Number(args[3]);
    let cls = null, minpos = null, mode = 'adapted';
    for (let i = 4; i < args.length; i++) {
      const a = args[i];
      if (a.startsWith('--class=')) cls = a.slice(8).split(',').map(Number);
      else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
      else if (a.startsWith('--mode=')) mode = a.slice(7);
    }
    if (cls == null || minpos == null) throw new Error('--class= and --minpos= required');
    const cases = enumerateGpinCases(w, m, cls, minpos, mode);
    console.log(JSON.stringify({ w: w, m: m, q: q, class: cls, minpos: minpos, mode: mode, caseCount: cases.length, cases: cases }));
  } else if (args[0] === 'decode') {
    const S3 = require(path.join(__dirname, 'sat3.js'));
    const w = Number(args[1]), m = Number(args[2]), q = Number(args[3]);
    const txt = fs.readFileSync(args[4], 'utf8');
    const out = S3.decode(w, m, q, txt);
    const jo = args.find((a) => a.startsWith('--json='));
    if (jo) fs.writeFileSync(jo.slice(7), JSON.stringify(out, null, 1));
    console.log(JSON.stringify({ nStones: out.nStones, verify: out.verify, ok: out.verify.ok }));
  } else {
    const w = Number(args[0]), m = Number(args[1]), q = Number(args[2]);
    const S2 = require(path.join(__dirname, 'sat2.js'));
    let i = 3, cls = null, out = null, krow = [], minpos = null, gpin = null, emptytail = false;
    for (; i < args.length; i++) {
      const a = args[i];
      if (a.startsWith('--class=')) cls = a.slice(8).split(',').map(Number);
      else if (a.startsWith('--krow=')) krow = a.slice(7).split(',');
      else if (a.startsWith('--minpos=')) minpos = Number(a.slice(9));
      else if (a.startsWith('--gpin=')) gpin = a.slice(7).split(',').map((t) => t.split(':').map(Number));
      else if (a === '--emptytail') emptytail = true;
      else if (!out) out = a;
    }
    if (cls == null) throw new Error('--class= required');
    const dg = dumpClassGpin(w, m, q, cls, { krow: krow, minpos: minpos, gpin: gpin, emptytail: emptytail });
    fs.writeFileSync(out, S2.toDimacs2(dg.enc));
    dg.meta.file = out;
    console.log(JSON.stringify(dg.meta));
  }
}
module.exports = { dumpClassGpin, enumerateGpinCases, buildCircles5 };
