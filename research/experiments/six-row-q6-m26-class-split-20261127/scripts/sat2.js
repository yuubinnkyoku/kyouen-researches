// sat2.js — extended deficient-maximal SAT machinery on top of K0810 encode()/toDimacs (verbatim census + counter + maximality).
// New vs research/experiments/row-deficient-sat-witnesses-20261114/scripts/row_deficient_sat.js:
//   1. totalizer (Bailleux-Boufkhad) encoding option for the maxStones total cap (--counter=tot)
//   2. lex-leader symmetry breaking for board isometries H (column reflection), V (row reflection), HV (180deg)
//      (sound: the orbit-wise lex-min solution satisfies S <=lex sigma(S) for every sigma in the group;
//       deficient/cap constraints are invariant under these isometries)
//   3. deficientRow 'some' single-clause mode (identical to K0810 encode() default; DIMACS byte-identical)
// Usage: node sat2.js w m q [--deficient|--cap=K] [--counter=seq|tot] [--lex=H,V,HV] [--rowY=Y] out.cnf
'use strict';
const S = require('./sat.js');

function totalizerAtMost(enc, xs, K) {
  // at-most-K over xs via totalizer; aux ">=j" outputs per node; forbid >=K+1.
  function leaf(x) {
    const o1 = enc.v();
    enc.add([[x, -o1]]);      // x -> >=1
    enc.add([[-x, o1]]);      // >=1 -> x
    return [0, o1];           // index 0 dummy (>=0 = true)
  }
  function merge(a, b, cap) {
    const p = a.length - 1, qq = b.length - 1;
    const mx = Math.min(cap, p + qq);
    const o = new Array(mx + 1).fill(0);
    for (let j = 1; j <= mx; j++) o[j] = enc.v();
    for (let i = 0; i <= p; i++) for (let j = 0; j <= qq; j++) {
      const t = i + j;
      if (t >= 1 && t <= mx) {
        // (a_i & b_j) -> o_t   (a_0/b_0 mean "true")
        const cl = [o[t]];
        if (i >= 1) cl.push(-a[i]); if (j >= 1) cl.push(-b[j]);
        enc.add([cl]);
      }
      if (t + 1 <= mx) {
        // o_{t+1} -> a_{i+1} | b_{j+1}   (whichever exist)
        const ai1 = i + 1 <= p ? a[i + 1] : 0;
        const bj1 = j + 1 <= qq ? b[j + 1] : 0;
        if (ai1 && bj1) enc.add([[-o[t + 1], ai1, bj1]]);
        else if (ai1) enc.add([[-o[t + 1], ai1]]);
        else if (bj1) enc.add([[-o[t + 1], bj1]]);
      }
    }
    return o;
  }
  let nodes = xs.map(leaf);
  const cap = K + 1; // need outputs up to K+1 to forbid >=K+1
  while (nodes.length > 1) {
    const nxt = [];
    for (let i = 0; i + 1 < nodes.length; i += 2) nxt.push(merge(nodes[i], nodes[i + 1], cap));
    if (nodes.length % 2) nxt.push(nodes[nodes.length - 1]);
    nodes = nxt;
  }
  const root = nodes[0];
  if (root.length - 1 >= K + 1) enc.add([[-root[K + 1]]]); // forbid >= K+1 => at most K
  return root;
}

// lex-leader S <=lex sigma(S) over cell vars in row-major order (i = y*m + x)
function lexLeader(enc, cellVars, m, w, sigma) {
  const n = cellVars.length;
  const perm = new Array(n);
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) {
    const [x2, y2] = sigma(x, y);
    perm[y * m + x] = y2 * m + x2;
  }
  let e = enc.v(); // prefix-equal up to position 0
  enc.add([[e]]);
  for (let i = 0; i < n; i++) {
    const b = cellVars[i], c = cellVars[perm[i]];
    if (b === c) continue; // fixed point: prefix-equal unchanged
    // forbid first-difference favoring image: e_i & b & !c -> false
    enc.add([[-e, -b, c]]);
    const e2 = enc.v();
    enc.add([[-e2, e]]);            // e2 -> e
    enc.add([[-e2, -b, c]]);        // e2 -> (b->c)
    enc.add([[-e2, -c, b]]);        // e2 -> (c->b)
    enc.add([[-e, -b, -c, e2]]);    // e & b & c -> e2
    enc.add([[-e, b, c, e2]]);      // e & !b & !c -> e2
    e = e2;
  }
}

class Enc2 {
  constructor() { this.nv = 0; this.clauses = []; }
  v() { return ++this.nv; }
  add(cls) { for (let c of cls) { c = c.filter(l => l !== 0); if (c.length) this.clauses.push(c); } }
}
// K0810 sequential counter, replicated verbatim (not exported by sat.js)
function counter(enc, xs, K) {
  const nE = xs.length;
  const s = Array.from({ length: nE }, () => new Array(K + 1).fill(0));
  for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) s[i][j] = enc.v();
  for (let i = 0; i < nE; i++) for (let j = 1; j <= Math.min(K, i + 1); j++) {
    const Sv = s[i][j];
    if (i === 0) {
      enc.add([[xs[0], -Sv]]); enc.add([[-xs[0], Sv]]);
    } else {
      const Sp = (j <= i) ? s[i - 1][j] : 0;
      const Spp = (j >= 2 && j - 1 <= i) ? s[i - 1][j - 1] : 0;
      if (j <= i) {
        enc.add([[-Sv, Sp, xs[i]]]);
        if (Spp) enc.add([[-Sv, Sp, Spp]]);
        enc.add([[-Sp, Sv]]);
        if (Spp) enc.add([[-xs[i], -Spp, Sv]]);
        else enc.add([[-xs[i], Sv]]);
      } else {
        enc.add([[-Sv, xs[i]]]);
        enc.add([[-Sv, Spp]]);
        enc.add([[-xs[i], -Spp, Sv]]);
      }
    }
  }
  return s;
}

function encodeCore(w, m, q) {
  const { P, n, curves } = S.buildCensus(w, m, q);
  const enc = new Enc2();
  const cell = new Array(n).fill(0).map(() => enc.v());
  const geVars = [];
  const rowGe = {};
  for (const cu of curves) {
    const s = counter(enc, cu.pts.map(p => cell[p]), q);
    const last = s[cu.pts.length - 1];
    enc.add([[-last[q]]]);
    geVars.push(last[q - 1]);
    if (cu.type === 'line' && cu.co[0] === 0 && cu.co[1] === 1) rowGe[-cu.co[2]] = last[q - 1];
  }
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(geVars[ci]); });
  for (let i = 0; i < n; i++) enc.add([[cell[i], ...through[i]]]);
  return { enc, cell, P, n, curves, rowGe };
}

function toDimacs2(enc) {
  const out = ['p cnf ' + enc.nv + ' ' + enc.clauses.length];
  for (const c of enc.clauses) out.push(c.join(' ') + ' 0');
  return out.join('\n');
}

const SIG = {
  H: (x, y, m, w) => [m - 1 - x, y],
  V: (x, y, m, w) => [x, w - 1 - y],
  HV: (x, y, m, w) => [m - 1 - x, w - 1 - y],
};

function dump(w, m, q, opts) {
  const { enc, cell, P, n, curves, rowGe } = encodeCore(w, m, q);
  const meta = { w, m, q, curves: curves.length, mode: opts.mode, counter: null, lex: opts.lex || [], vars: 0, clauses: 0 };
  if (opts.mode === 'deficient') {
    const lits = Object.keys(rowGe).map(y => -rowGe[y]);
    if (lits.length !== w) throw new Error('row curves miscount ' + lits.length + ' (requires m >= q)');
    enc.add([lits]);
  } else if (opts.mode === 'cap') {
    if (opts.counter === 'tot') { totalizerAtMost(enc, cell.slice(), opts.cap); meta.counter = 'tot'; }
    else { const K = opts.cap + 1; const s = counter(enc, cell.slice(), K); enc.add([[-s[n - 1][K]]]); meta.counter = 'seq'; }
  } else if (opts.mode === 'rowfixed') {
    const rv = rowGe[opts.rowY];
    if (!rv) throw new Error('row not found ' + opts.rowY);
    enc.add([[-rv]]);
  }
  for (const nm of (opts.lex || [])) lexLeader(enc, cell, m, w, (x, y) => SIG[nm](x, y, m, w));
  meta.vars = enc.nv; meta.clauses = enc.clauses.length;
  return { enc, meta, P };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
  let i = 3, mode = 'deficient', cap = null, cnt = 'seq', lex = [], rowY = null, out = null;
  for (; i < args.length; i++) {
    const a = args[i];
    if (a === '--deficient') mode = 'deficient';
    else if (a.startsWith('--cap=')) { mode = 'cap'; cap = Number(a.slice(6)); }
    else if (a.startsWith('--counter=')) cnt = a.slice(10);
    else if (a.startsWith('--lex=')) lex = a.slice(6).split(',').filter(s => SIG[s]);
    else if (a.startsWith('--rowY=')) { mode = 'rowfixed'; rowY = Number(a.slice(7)); }
    else if (!out) out = a;
  }
  const opts = { mode, cap, counter: cnt, lex, rowY };
  const { enc, meta } = dump(w, m, q, opts);
  require('fs').writeFileSync(out, toDimacs2(enc));
  meta.file = out;
  console.log(JSON.stringify(meta));
}
module.exports = { dump, toDimacs2, encodeCore, totalizerAtMost, lexLeader, S };
