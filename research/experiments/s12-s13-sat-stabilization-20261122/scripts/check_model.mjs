// check_model.mjs — evaluate the enc_sat.mjs decision predicate for an EXPLICIT
// configuration (list of stone cells), recomputing safety/coverage/counters from
// the census. Used to prove a known witness is a model of the encoding and to
// double-check decoded SAT models before the independent verifiers run.
// Usage: node check_model.mjs <n> <k> <cells-csv>   (cells are 0-based x + y*n)
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
if (S.size > k) { console.log(JSON.stringify({ model: false, reason: 'size>k', size: S.size, k })); process.exit(0); }

let tTrue = 0, viol = 0, emptyCovered = 0, emptyUncovered = 0;
const covCount = new Uint16Array(N);
for (let fi = 0; fi < F; fi++) {
  const a = q[4*fi], b = q[4*fi+1], c = q[4*fi+2], d = q[4*fi+3];
  const cnt = (S.has(a)?1:0)+(S.has(b)?1:0)+(S.has(c)?1:0)+(S.has(d)?1:0);
  if (cnt === 4) viol++;
  if (cnt >= 3) { tTrue++; for (const p of [a,b,c,d]) covCount[p]++; }
}
for (let e = 0; e < N; e++) {
  if (!S.has(e)) { if (covCount[e] > 0) emptyCovered++; else emptyUncovered++; }
}
const res = {
  n, k, size: S.size, quartets: F,
  safety_violations: viol,
  t_true: tTrue,
  empty_covered: emptyCovered, empty_uncovered: emptyUncovered,
  maximal: emptyUncovered === 0,
  model: viol === 0 && emptyUncovered === 0 && S.size <= k,
};
console.log(JSON.stringify(res));
