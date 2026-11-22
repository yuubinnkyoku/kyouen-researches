// enc_sat.mjs — SAT encoding of "at-most-k maximal safe configuration" on the
// n x n standard kyouen board (q=4: forbidden = 4 stones on a common line or circle).
//
// Decision predicate encoded:
//   EXISTS S subset of cells with |S| <= k such that
//     (safe)    no forbidden quartet has all 4 cells in S
//     (maximal) every cell c NOT in S is attacked: some forbidden quartet q
//               containing c has all its other 3 cells in S.
// A satisfying assignment decodes to a witness => s_n <= |S| (<= k).
// UNSAT under this exact encoding => no maximal safe configuration with <= k
// stones exists on this board => s_n >= k+1.
//
// Encoding (one-way aux variables, sound in both directions):
//   x_c in {1..N}         cell stone indicators
//   t_q  in {N+1..N+F}    "quartet q carries >= 3 stones" (one-way implication only)
//   s_{i,j}               Sinz sequential counter for at-most-k over x_1..x_N
// Clauses:
//   (S1) safety:    -x_a -x_b -x_c -x_d                     per quartet q={a,b,c,d}
//   (S2) coverage:  -t_q  x_i  x_j   for each pair {i,j} subseteq q  (6 per quartet)
//                   (t_q -> at most one of q's cells is a non-stone)
//   (S3) maximality: x_e  t_{q1} ... t_{qm}  per cell e, over all quartets through e
//   (S4) counter:   Sinz at-most-k sequential counter (one-way, exact-semantics sound)
//
// For an empty cell e in a satisfying assignment, some t_q with q containing e is
// true, and (S2) forces >= 3 stones in q; since x_e is false the stones are
// exactly q\{e}: a genuine attack. Conversely a genuine <=k maximal safe S gives
// a model: set t_q precisely for quartets with exactly 3 stones in S (safety
// forbids 4) and the counter to exact prefix counts.
//
// --shuffle=<seed> deterministically permutes variable ids (independent second
// encoding for UNSAT cross-checking; satisfiability is invariant).
//
// Usage: node enc_sat.mjs <n> <k> --out=path.dimacs --meta=path.json [--shuffle=seed]
import { census, quartetList, verifyAgainstAnchors } from './census.mjs';
import { writeFileSync, openSync, writeSync, closeSync, mkdirSync } from 'node:fs';

function parseArgs() {
  const argv = process.argv.slice(2);
  const n = parseInt(argv[0], 10);
  const k = parseInt(argv[1], 10);
  const opt = {};
  for (const a of argv.slice(2)) {
    const m = a.match(/^--([a-z]+)=(.*)$/);
    if (m) opt[m[1]] = m[2];
  }
  if (!(n >= 4 && n <= 16)) throw new Error('bad n');
  if (!(k >= 1)) throw new Error('bad k');
  return { n, k, opt };
}

// deterministic PRG for shuffle (mulberry32) — reproducible CNF
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0);
  };
}

const { n, k, opt } = parseArgs();

const cen = census(n);
const issues = verifyAgainstAnchors(cen);
if (issues.length) { console.error(JSON.stringify({ FATAL: 'census anchor mismatch', issues })); process.exit(1); }
const q = quartetList(cen); // Uint16Array, 4*F
const F = cen.F, N = n * n;
if (q.length / 4 !== F) throw new Error('quartet mismatch');

// ---- variable allocation (logical ids BEFORE optional shuffle) ----
const nCounter = N * k;
const nVars = N + F + nCounter;
let perm = null;
if (opt.shuffle !== undefined) {
  const seed = parseInt(opt.shuffle, 10) >>> 0;
  const r = rng(seed);
  const ids = new Int32Array(nVars);
  for (let i = 0; i < nVars; i++) ids[i] = i + 1;
  for (let i = nVars - 1; i > 0; i--) { const j = (r() % (i + 1)); const t = ids[i]; ids[i] = ids[j]; ids[j] = t; }
  perm = ids; // logical id L (1-based) -> emitted id ids[L-1]
}
const X = (c) => c + 1;            // cell index (0-based) -> cell var (logical)
const T = (fi) => N + 1 + fi;       // quartet index -> t var
const C = (i, j) => N + F + (i * k + (j - 1)) + 1; // counter: prefix ending at cell i (0-based), count j (1..k)

const clauses = [];
function add(...lits) { clauses.push(lits); }

// (S1) safety + (S2) coverage
const PAIRS = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for (let fi = 0; fi < F; fi++) {
  const a = q[4*fi], b = q[4*fi+1], c = q[4*fi+2], d = q[4*fi+3];
  add(-X(a), -X(b), -X(c), -X(d));
  const tv = -T(fi);
  const xs = [X(a), X(b), X(c), X(d)];
  for (const [i, j] of PAIRS) add(tv, xs[i], xs[j]);
}

// (S3) maximality: incidence lists
const deg = new Uint32Array(N);
for (let i = 0; i < 4 * F; i++) deg[q[i]]++;
const qOff = new Uint32Array(N + 1);
for (let c = 0; c < N; c++) qOff[c + 1] = qOff[c] + deg[c];
const qThrough = new Uint32Array(4 * F);
{ const tmp = qOff.slice(0, N);
  for (let fi = 0; fi < F; fi++) for (let j = 0; j < 4; j++) { const c = q[4*fi + j]; qThrough[tmp[c]++] = fi; } }
for (let e = 0; e < N; e++) {
  const cl = [X(e)];
  for (let i = qOff[e]; i < qOff[e + 1]; i++) cl.push(T(qThrough[i]));
  add(...cl);
}

// (S4) Sinz at-most-k sequential counter: s_{i,j} = ">= j stones among cells 0..i"
for (let i = 0; i < N; i++) {
  add(-X(i), C(i, 1));                                        // C1
  if (i > 0) {
    for (let j = 1; j <= k; j++) add(-C(i-1, j), C(i, j));    // C2
    for (let j = 2; j <= k; j++) {
      add(-X(i), -C(i - 1, j - 1), C(i, j));                  // C3
    }
    add(-X(i), -C(i - 1, k));                                 // C4: at-most-k guard
  }
}

// ---- emit DIMACS ----
function emitId(logical) { return perm ? perm[Math.abs(logical) - 1] : Math.abs(logical); }
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
  if (bufLen > (1 << 24)) flush();
}
flush();
closeSync(fd);

const meta = {
  n, k, N, F: cen.F, D: cen.D, C: cen.C, lines: cen.lines.length, circles: cen.circles.length,
  nVars, nClauses: clauses.length, shuffle: opt.shuffle !== undefined ? parseInt(opt.shuffle, 10) : null,
  varLayout: 'cells 1..N; t_q N+1..N+F (quartet order = quartetList); counter N+F+1.. (s_{i,j}=N+F+i*k+(j-1)+1)',
  encoding: 'S1 safety 4-clauses; S2 t->pairs 6 per quartet; S3 maximality per cell; S4 Sinz at-most-k one-way',
  anchors: 'census anchors verified against K0057 published F/D/C/lines/circles values',
};
if (opt.meta) { mkdirSync(opt.meta.split('/').slice(0, -1).join('/'), { recursive: true }); writeFileSync(opt.meta, JSON.stringify(meta, null, 1)); }
console.error(JSON.stringify(meta));
