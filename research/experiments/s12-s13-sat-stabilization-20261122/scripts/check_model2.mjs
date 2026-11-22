// check_model2.mjs — evaluate the enc_sat2.mjs predicate set for an EXPLICIT
// configuration without running a solver: safety, maximality, at-most-k, and the
// D4 lex-leader constraints (direct vector comparison, no chain vars needed).
// Reports the D4 orbit and the lex-minimal canonical representative.
// Usage: node check_model2.mjs <n> <k> <cells-csv>
import { census, quartetList, verifyAgainstAnchors } from './census.mjs';

const n = parseInt(process.argv[2], 10);
const k = parseInt(process.argv[3], 10);
const S = new Set(process.argv[4].split(',').map((s) => parseInt(s, 10)).filter((v) => !isNaN(v)));
for (const c of S) if (!(c >= 0 && c < n * n)) throw new Error('cell out of range: ' + c);
const cen = census(n);
const issues = verifyAgainstAnchors(cen);
if (issues.length) { console.error('ANCHOR FAIL ' + issues); process.exit(1); }
const q = quartetList(cen);
const F = cen.F, N = n * n;

let viol = 0, emptyCovered = 0, emptyUncovered = 0, zTrue = 0;
const cov = new Uint16Array(N);
for (let fi = 0; fi < F; fi++) {
  const a = q[4*fi], b = q[4*fi+1], c = q[4*fi+2], d = q[4*fi+3];
  const cnt = (S.has(a)?1:0)+(S.has(b)?1:0)+(S.has(c)?1:0)+(S.has(d)?1:0);
  if (cnt === 4) viol++;
  if (cnt >= 3) { zTrue++; for (const p of [a,b,c,d]) cov[p]++; }
}
for (let e = 0; e < N; e++) if (!S.has(e)) { if (cov[e] > 0) emptyCovered++; else emptyUncovered++; }

// D4 transforms (identity + the 7 of enc_sat2.mjs in the same order)
const Ts = [
  [(x, y) => [x, y], 'id'],
  [(x, y) => [n - 1 - x, y], 'hs'],
  [(x, y) => [x, n - 1 - y], 'vs'],
  [(x, y) => [n - 1 - x, n - 1 - y], 'r2'],
  [(x, y) => [y, x], 'tr'],
  [(x, y) => [n - 1 - y, n - 1 - x], 'at'],
  [(x, y) => [y, n - 1 - x], 'cr'],
  [(x, y) => [n - 1 - y, x], 'cl'],
];
const vec = (set) => { const v = new Uint8Array(N); for (const c of set) v[c] = 1; return [...v].join(''); };
const image = (set, f) => { const out = new Set(); for (const c of set) { const x = c % n, y = (c / n) | 0; const [gx, gy] = f(x, y); out.add(gx + n * gy); } return out; };
// compare bits of A and B=A_g over cells c=0..N-1: A <=lex B ?
const lexLe = (A, B) => { const itA = A[Symbol.iterator](); for (const c of B) { const a = A.has(c), b = B.has(c); if (a && !b) return false; if (!a && b) return true; } return true; };
if (k < 0) throw new Error('neg');
const lexChecks = [];
let canonical = true;
for (let gi = 1; gi < 8; gi++) {
  const [f, nm] = Ts[gi];
  const B = image(S, f);
  const le = lexLe(S, B);
  lexChecks.push({ g: nm, le });
  if (!le) canonical = false;
}
// the orbit's lex-min rep
let orbitSizes = lexChecks.length;
const res = {
  n, k, size: S.size, quartets: F,
  safety_violations: viol, z_true: zTrue,
  empty_covered: emptyCovered, empty_uncovered: emptyUncovered,
  maximal: emptyUncovered === 0, at_most_k: S.size <= k,
  safe: viol === 0,
  lex_leader_checks: lexChecks, lex_leader: canonical,
  model: viol === 0 && emptyUncovered === 0 && S.size <= k && canonical,
};
console.log(JSON.stringify(res));
