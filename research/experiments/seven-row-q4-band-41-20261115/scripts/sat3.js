// sat3.js — sat2.js with streaming clause emission: the q <= w all-triples census
// unblocked for m >= 28 where sat2.js OOMs (rc 137 at 7x28 q4, 2560MB heap) because
// enc.clauses[] holds every clause as a JS array and toDimacs() joins a ~GB string.
// Changes vs sat2.js (everything else verbatim, incl. counter/totalizer/lexLeader/CLI):
//   1. Enc3 streams clause lines to `<out>.body` with bounded memory; the final DIMACS
//      (= 'p cnf NV NC\n' + clauses joined by '\n', no trailing newline) is assembled
//      afterwards by chunked copy -> byte-identical to sat2.js output.
//   2. Circles are processed at first triple-encounter (circMap insertion order =
//      first-encounter order) with pts computed per row via the quadratic root solve
//      (O(w) per circle instead of O(n) scan); row-major ascending order preserved.
//      Lines keep the sat2.js full scan (lineMap is small).
//   3. Dedup Set stores canonical (A,B,C,D) keys only (no co arrays retained).
// Verified byte-identical (md5) vs sat2.js on controls: see controls_sat3.json.
// Usage: node sat3.js w m q [--deficient|--cap=K] [--counter=seq|tot] [--lex=H,V,HV] [--rowY=Y] out.cnf
'use strict';
const S = require('./sat.js');
const fs = require('fs');

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

// streaming encoder: clause lines to fd; '\n'-separated, no trailing newline at EOF
class Enc3 {
  constructor(fd) { this.nv = 0; this.nc = 0; this.fd = fd; this.pend = []; }
  v() { return ++this.nv; }
  add(cls) {
    for (const c0 of cls) {
      let s = '';
      for (let i = 0; i < c0.length; i++) {
        const l = c0[i];
        if (l !== 0) { if (s) s += ' '; s += l; }
      }
      if (s.length) {
        this.pend.push(s + ' 0');
        this.nc++;
        if (this.pend.length >= 32768) {
          fs.writeSync(this.fd, this.pend.join('\n') + '\n');
          this.pend.length = 0;
        }
      }
    }
  }
  end() {
    if (this.pend.length) { fs.writeSync(this.fd, this.pend.join('\n')); this.pend.length = 0; }
  }
}

// pts on circle co=[A,B,C,D] (A>0 by circleABC sign normalization), row-quadratic:
// per row y solve A x^2 + B x + (A y^2 + C y + D) = 0 exactly over the integers.
// Returns point indices in row-major ascending order (identical to the sat2.js full scan).
function circlePts(co, w, m) {
  const A = co[0], B = co[1], C = co[2], D = co[3];
  const twoA = 2 * A;
  const set = [];
  for (let y = 0; y < w; y++) {
    const t = A * y * y + C * y + D;
    const disc = B * B - 4 * A * t;
    if (disc < 0) continue;
    let r = Math.round(Math.sqrt(disc));
    while (r > 0 && r * r > disc) r--;
    while ((r + 1) * (r + 1) <= disc) r++;
    if (r * r !== disc) continue;
    const n1 = -B - r, n2 = -B + r;
    if (n1 % twoA === 0) {
      const x = n1 / twoA;
      if (x >= 0 && x < m) set.push(y * m + x);
    }
    if (r > 0 && n2 % twoA === 0) {
      const x = n2 / twoA;
      if (x >= 0 && x < m) set.push(y * m + x);
    }
  }
  return set;
}

// streaming encodeCore: line curves first (lineMap insertion order), then circle curves
// at first triple-encounter (circMap insertion order), then through clauses.
function encodeCore3(w, m, q, enc) {
  const P = S.pts(w, m), n = P.length;
  const cell = new Array(n);
  for (let i = 0; i < n; i++) cell[i] = enc.v();
  const geVars = [];
  const rowGe = {};
  let nCurves = 0;
  const through = Array.from({ length: n }, () => []);

  // lines (verbatim sat2.js logic, full scan)
  const lineMap = new Map();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const lo = S.lineABC(P[i], P[j]);
    const key = lo[0] + ',' + lo[1] + ',' + lo[2];
    if (!lineMap.has(key)) lineMap.set(key, lo);
  }
  for (const lo of lineMap.values()) {
    const set = [];
    for (let idx = 0; idx < n; idx++) if (S.onLine(lo, P[idx][0], P[idx][1])) set.push(idx);
    if (set.length >= q) {
      const s = counter(enc, set.map(p => cell[p]), q);
      const last = s[set.length - 1];
      enc.add([[-last[q]]]);
      const ge = last[q - 1];
      geVars.push(ge);
      nCurves++;
      if (lo[0] === 0 && lo[1] === 1) rowGe[-lo[2]] = ge;
      for (const p of set) through[p].push(ge);
    }
  }

  // circles streamed at first encounter (key set only; no co retention)
  const seen = new Set();
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const pi = P[i], pj = P[j];
    for (let k = j + 1; k < n; k++) {
      const co = S.circleABC(pi, pj, P[k]);
      if (co === null) continue;
      const key = co[0] + ',' + co[1] + ',' + co[2] + ',' + co[3];
      if (seen.has(key)) continue;
      const set = circlePts(co, w, m);
      if (set.length >= q) {
        seen.add(key); // register only >=q circles: <q circles have <= q-1 grid
        // points, hence at most C(q-1,3) triples... with q=4: exactly one triple
        // per 3-point circle, so they are never re-encountered (output-identical,
        // but the Set no longer stores ~10x more keys than needed at large m).
        const s = counter(enc, set.map(p => cell[p]), q);
        const last = s[set.length - 1];
        enc.add([[-last[q]]]);
        const ge = last[q - 1];
        geVars.push(ge);
        nCurves++;
        for (const p of set) through[p].push(ge);
      }
    }
  }

  for (let i = 0; i < n; i++) enc.add([[cell[i], ...through[i]]]);
  return { cell, P, n, rowGe, nCurves };
}

const SIG = {
  H: (x, y, m, w) => [m - 1 - x, y],
  V: (x, y, m, w) => [x, w - 1 - y],
  HV: (x, y, m, w) => [m - 1 - x, w - 1 - y],
};

function dump(w, m, q, opts) {
  const bodyPath = opts.out + '.body';
  const fd = fs.openSync(bodyPath, 'w');
  const enc = new Enc3(fd);
  const { cell, rowGe, nCurves } = encodeCore3(w, m, q, enc);
  const meta = { w, m, q, curves: nCurves, mode: opts.mode, counter: null, lex: opts.lex || [], vars: 0, clauses: 0 };
  if (opts.mode === 'deficient') {
    const lits = Object.keys(rowGe).map(y => -rowGe[y]);
    if (lits.length !== w) throw new Error('row curves miscount ' + lits.length + ' (requires m >= q)');
    enc.add([lits]);
  } else if (opts.mode === 'cap') {
    if (opts.counter === 'tot') { totalizerAtMost(enc, cell.slice(), opts.cap); meta.counter = 'tot'; }
    else { const K = opts.cap + 1; const s = counter(enc, cell.slice(), K); enc.add([[-s[cell.length - 1][K]]]); meta.counter = 'seq'; }
  } else if (opts.mode === 'rowfixed') {
    const rv = rowGe[opts.rowY];
    if (!rv) throw new Error('row not found ' + opts.rowY);
    enc.add([[-rv]]);
  }
  for (const nm of (opts.lex || [])) lexLeader(enc, cell, m, w, (x, y) => SIG[nm](x, y, m, w));
  enc.end();
  fs.closeSync(fd);
  meta.vars = enc.nv;
  meta.clauses = enc.nc;
  // assemble final DIMACS: header + '\n' + body (chunked copy)
  const out = fs.openSync(opts.out, 'w');
  fs.writeSync(out, 'p cnf ' + meta.vars + ' ' + meta.clauses + '\n');
  const bfd = fs.openSync(bodyPath, 'r');
  const CH = 1 << 24;
  const buf = Buffer.allocUnsafe(CH);
  for (;;) {
    const got = fs.readSync(bfd, buf, 0, CH, null);
    if (!got) break;
    fs.writeSync(out, buf, 0, got);
  }
  fs.closeSync(bfd);
  fs.closeSync(out);
  fs.unlinkSync(bodyPath);
  meta.file = opts.out;
  return { meta };
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
  const opts = { mode, cap, counter: cnt, lex, rowY, out };
  const { meta } = dump(w, m, q, opts);
  console.log(JSON.stringify(meta));
}
module.exports = { dump, encodeCore3, circlePts, totalizerAtMost, lexLeader, counter, S };
