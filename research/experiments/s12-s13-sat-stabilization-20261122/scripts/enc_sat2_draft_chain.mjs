// enc_sat2.mjs — SAT encoding v2 of "at-most-k maximal safe configuration" on the
// n x n standard kyouen board (q = 4), with:
//   (Z)  Tseitin-COMPLETE coverage variables z_{q,e} for each (quartet q, cell e in q):
//        z_{q,e} <=> (all three other cells of q are stones).
//        Full two-way equivalence gives unit propagation from stones to coverage
//        (v1's one-way t_q weakens UNSAT search badly: n=7 k<=6 did not finish in 200s).
//   (LX) D4 lex-leader symmetry breaking: for each of the 7 non-identity board
//        symmetries g, require the stone-indicator vector A to satisfy
//        A <=lex g(A) (equality allowed, so symmetric configurations are kept).
//        Every D4 orbit contains lex-minimal representatives, so satisfiability
//        of "exists maximal safe with <=k stones" is unchanged; expected UNSAT
//        speedup is large because the search space is 8x smaller.
// Decision predicate and soundness argument: same as enc_sat.mjs v1 (S1 safety,
// per-quartet 4-literal clauses; maximality per cell over z vars; Sinz one-way
// at-most-k sequential counter with exact-count semantics).
//
// Lex-leader encoding (per transform g, cells in fixed index order c=0..N-1,
// B_c := A_{g^{-1}(c)}): prefix-equal chain d_c, clauses per position:
//   (L1) -d_{c-1} -A_c  B_c  d_c        (prefix equal & bits differ -> d_c forced... see note)
//   (L2) -d_{c-1}  A_c -B_c  d_c
//   (L3) -d_{c-1} -A_c  B_c             (blocking: prefix equal and A_c=1, B_c=0 forbidden)
// d_{-1} = true (first position drops the -d literal). d_c only needs the "<="
// direction (forced true along equal prefixes); soundness for both polarities is
// proven in the experiment README.
//
// Usage: node enc_sat2.mjs <n> <k> --out=... --meta=... [--shuffle=seed] [--nolex]
import { census, quartetList, verifyAgainstAnchors } from './census.mjs';
import { writeFileSync, openSync, writeSync, closeSync, mkdirSync } from 'node:fs';

function parseArgs() {
  const argv = process.argv.slice(2);
  const n = parseInt(argv[0], 10), k = parseInt(argv[1], 10);
  const opt = {};
  for (const a of argv.slice(2)) { const m = a.match(/^--([a-z]+)(?:=(.*))?$/); if (m) opt[m[1]] = m[2] ?? true; }
  if (!(n >= 4 && n <= 16)) throw new Error('bad n');
  if (!(k >= 1 && k <= n * n)) throw new Error('bad k');
  return { n, k, opt };
}
function rng(seed) {
  let a = seed >>> 0;
  return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0); };
}

const { n, k, opt } = parseArgs();
const cen = census(n);
const issues = verifyAgainstAnchors(cen);
if (issues.length) { console.error(JSON.stringify({ FATAL: 'census anchor mismatch', issues })); process.exit(1); }
const q = quartetList(cen);
const F = cen.F, N = n * n;

// ---- logical variable layout ----
// cells:      1..N                      x_c
// z vars:     N+1 .. N+4F               z[(fi,e)] at N + 4*fi + e   (e in 0..3 = cell q[4fi+e])
// d vars:     N+4F+1 .. N+4F+7N         d[(g,c)] at N+4F + g*N + c (g in 0..6, cells 0..N-1)
// counter:    N+4F+7N+1 ..               s_{i,j}
const nZ = 4 * F;
const nD = opt.nolex ? 0 : 7 * N;
const nCtr = N * k;
const nVars = N + nZ + nD + nCtr;
const X = (c) => c + 1;
const Z = (fi, e) => N + 4 * fi + e + 1;
const D = (g, c) => N + nZ + g * N + c + 1;
const C = (i, j) => N + nZ + nD + (i * k + (j - 1)) + 1;

const clauses = [];
const add = (...lits) => clauses.push(lits);

// (S1) safety
for (let fi = 0; fi < F; fi++)
  add(-X(q[4*fi]), -X(q[4*fi+1]), -X(q[4*fi+2]), -X(q[4*fi+3]));

// (Z) coverage equivalence + maximality
// z_{q,e} <=> AND_{j != e} x_{q_j}
for (let fi = 0; fi < F; fi++) {
  const idx = [q[4*fi], q[4*fi+1], q[4*fi+2], q[4*fi+3]];
  for (let e = 0; e < 4; e++) {
    const zv = Z(fi, e);
    const others = [0, 1, 2, 3].filter((j) => j !== e);
    for (const j of others) add(-zv, X(idx[j]));                     // z -> stones
    add(zv, ...others.map((j) => -X(idx[j])));                        // stones -> z
  }
}
// maximality: per cell, x_e OR z of quartets through e
{
  const deg = new Uint32Array(N);
  for (let i = 0; i < 4 * F; i++) deg[q[i]]++;
  const qOff = new Uint32Array(N + 1);
  for (let c = 0; c < N; c++) qOff[c + 1] = qOff[c] + deg[c];
  const qThrough = new Uint32Array(4 * F);
  const tmp = qOff.slice(0, N);
  for (let fi = 0; fi < F; fi++) for (let j = 0; j < 4; j++) { const c = q[4*fi + j]; qThrough[tmp[c]++] = fi; }
  for (let e = 0; e < N; e++) {
    const cl = [X(e)];
    for (let i = qOff[e]; i < qOff[e + 1]; i++) {
      const fi = qThrough[i];
      for (let j = 0; j < 4; j++) if (q[4*fi + j] === e) { cl.push(Z(fi, j)); break; }
    }
    add(...cl);
  }
}

// (LX) D4 lex-leader. 7 non-identity transforms as cell permutations.
const T = (x, y) => x + n * y;
function transforms() {
  // returns array of functions cell -> cell
  const f = [];
  const id = (x, y) => [x, y];
  const hs = (x, y) => [n - 1 - x, y];   // horizontal flip
  const vs = (x, y) => [x, n - 1 - y];
  const r2 = (x, y) => [n - 1 - x, n - 1 - y];
  const tr = (x, y) => [y, x];           // transpose
  const at = (x, y) => [n - 1 - y, n - 1 - x]; // anti-transpose
  const cr = (x, y) => [y, n - 1 - x];   // rotate90 then flip
  const cl = (x, y) => [n - 1 - y, x];
  return [hs, vs, r2, tr, at, cr, cl];
}
if (!opt.nolex) {
  const gs = transforms();
  for (let gi = 0; gi < gs.length; gi++) {
    // B_c = A_{g^{-1}(c)}: for transform perm p (p applied to cells), B_c = x_{p^{-1}(c)}
    const p = new Int32Array(N);   // p[c] = image cell of c
    for (let c = 0; c < N; c++) { const x = c % n, y = (c / n) | 0; const [gx, gy] = gs[gi](x, y); p[c] = T(gx, gy); }
    const inv = new Int32Array(N);
    for (let c = 0; c < N; c++) inv[p[c]] = c;
    // B_c = x_{inv[c]} sorted by c; A_c = x_c
    let dPrev = 0; // 0 = "true" sentinel: first position has no -d literal
    for (let c = 0; c < N; c++) {
      const Ac = X(c), Bc = X(inv[c]);
      const dcur = D(gi, c);
      if (dPrev === 0) {
        add(-Ac, Bc, dcur);
        add(Ac, -Bc, dcur);
        add(-Ac, Bc);
      } else {
        add(-dPrev, -Ac, Bc, dcur);
        add(-dPrev, Ac, -Bc, dcur);
        add(-dPrev, -Ac, Bc);
      }
      dPrev = dcur;
    }
  }
}

// (S4) Sinz at-most-k counter (one-way, exact-count sound)
for (let i = 0; i < N; i++) {
  add(-X(i), C(i, 1));
  if (i > 0) {
    for (let j = 1; j <= k; j++) add(-C(i - 1, j), C(i, j));
    for (let j = 2; j <= k; j++) add(-X(i), -C(i - 1, j - 1), C(i, j));
    add(-X(i), -C(i - 1, k));
  }
}

// ---- emit ----
let perm = null;
if (opt.shuffle !== undefined) {
  const seed = parseInt(opt.shuffle, 10) >>> 0;
  const r = rng(seed);
  const ids = new Int32Array(nVars);
  for (let i = 0; i < nVars; i++) ids[i] = i + 1;
  for (let i = nVars - 1; i > 0; i--) { const j = (r() % (i + 1)); const t = ids[i]; ids[i] = ids[j]; ids[j] = t; }
  perm = ids;
}
const emitId = (logical) => (perm ? perm[Math.abs(logical) - 1] : Math.abs(logical));
const outPath = opt.out ?? '/dev/stdout';
let fd = openSync(outPath, 'w');
const buf = [];
let bufLen = 0;
const flush = () => { if (bufLen > 0) { writeSync(fd, buf.join('')); buf.length = 0; bufLen = 0; } };
writeSync(fd, `p cnf ${nVars} ${clauses.length}\n`);
for (const cl of clauses) {
  let s = '';
  for (const lit of cl) s += (lit < 0 ? '-' : '') + emitId(lit) + ' ';
  s += '0\n';
  buf.push(s); bufLen += s.length;
  if (bufLen > (1 << 23)) flush();
}
flush();
closeSync(fd);

const meta = {
  n, k, N, F: cen.F, D: cen.D, C: cen.C, lines: cen.lines.length, circles: cen.circles.length,
  nVars, nClauses: clauses.length,
  encoding: 'v2: S1 safety; Z full Tseitin z_{q,e}; maximality per cell over z; LX D4 lex-leader 7 transforms; S4 Sinz one-way at-most-k',
  nolex: !!opt.nolex,
  shuffle: opt.shuffle !== undefined ? parseInt(opt.shuffle, 10) : null,
  varLayout: `cells 1..${N}; z N+1..${N+nZ}; d ${N+nZ+1}..${N+nZ+nD}; counter ${N+nZ+nD+1}..${nVars}`,
  anchors: 'census anchors verified against K0057 published F/D/C/lines/circles values',
};
if (opt.meta) { mkdirSync(opt.meta.split('/').slice(0, -1).join('/'), { recursive: true }); writeFileSync(opt.meta, JSON.stringify(meta, null, 1)); }
console.error(JSON.stringify(meta));
