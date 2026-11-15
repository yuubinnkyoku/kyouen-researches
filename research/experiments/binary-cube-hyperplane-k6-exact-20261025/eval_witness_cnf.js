// K0568 positive control: direct evaluation of the regenerated exactly-9
// circuit CNF under the known 9-point witness assignment.  A satisfying
// assignment verified clause-by-clause IS a SAT proof for the file -- no
// solver trust required (kissat's 23s SAT run on the equivalent CNF is the
// previously recorded cross-check; this sandbox's cgroup memory cap makes a
// fresh 19.5M-clause solver run infeasible).
//
// Assignment: stone v (0-based) <-> CNF var v+1; the witness stones are
// true, everything else false.  The two Sinz sequential-counter blocks have
// auxiliary variables whose satisfying values are COMPUTED from the prefix-
// count semantics (s[i][j] = "at least j+1 of lits[0..i] are true"):
//   counter 1 (at-most-9 on positives):  s1[i][j] = 65 + i*9  + j, j<9
//   counter 2 (at-most-55 on negatives): s2[i][j] = 641 + i*55 + j, j<55
// This derived assignment is itself verified: any clause it would violate
// is reported, so a wrong derivation cannot produce a false PASS.
//
// Usage: node eval_witness_cnf.js CNF v1,v2,... (exactly 9 witness stones)
'use strict';
const fs = require('fs');

const cnfPath = process.argv[2];
const wit = process.argv[3].split(',').map((x) => parseInt(x, 10));
if (wit.length !== 9) throw new Error('need exactly 9 witness stones');
const K = 9;
const N = 64;

// value of every variable under the constructed assignment
const val = new Uint8Array(65 + N * K + N * (N - K));
const stoneTrue = new Uint8Array(N);
for (const v of wit) stoneTrue[v] = 1;
for (let v = 0; v < N; v++) val[v + 1] = stoneTrue[v];
// counter 1: lits[i] = i+1 (positive), k = K
{
  let cnt = 0;
  for (let i = 0; i < N; i++) {
    cnt += stoneTrue[i];
    for (let j = 0; j < K; j++) val[65 + i * K + j] = cnt >= j + 1 ? 1 : 0;
  }
}
// counter 2: lits[i] = -(i+1) ("true" = stone i false), k = N-K
{
  let cnt = 0;
  for (let i = 0; i < N; i++) {
    cnt += stoneTrue[i] ? 0 : 1;
    for (let j = 0; j < N - K; j++) val[65 + N * K + i * (N - K) + j] = cnt >= j + 1 ? 1 : 0;
  }
}
if (65 + N * K + N * (N - K) - 1 !== 4160) throw new Error('variable bound mismatch');

const fd = fs.openSync(cnfPath, 'r');
const CHUNK = 1 << 24;
const buf = Buffer.alloc(CHUNK);
let clauses = 0, violated = 0, headerClauses = -1, headerVars = -1;
let litSign = 1, litVal = 0, inLit = false, clauseSat = false;
let violatedSamples = [];

function feedLit(signed) {
  if (signed === 0) return; // clause terminator
  if (signed > 0) { if (val[signed]) clauseSat = true; }
  else { if (!val[-signed]) clauseSat = true; }
}
function endClause() {
  clauses++;
  if (!clauseSat) {
    violated++;
    if (violatedSamples.length < 5) violatedSamples.push(clauses);
  }
  clauseSat = false;
}
function feedByte(ch) {
  if (ch === 0x20) { // space: a (nonzero) literal token is complete
    if (inLit) {
      const lit = litSign * litVal;
      if (lit !== 0) feedLit(lit); // defensive: mid-clause tokens are nonzero
      inLit = false; litSign = 1; litVal = 0;
    }
    return;
  }
  if (ch === 0x2d) { litSign = -1; inLit = true; litVal = 0; return; } // '-'
  if (ch >= 0x30 && ch <= 0x39) { litVal = litVal * 10 + (ch - 0x30); inLit = true; return; }
  if (ch === 0x0a) { // newline: pending token is the clause terminator "0"
    inLit = false; litSign = 1; litVal = 0;
    endClause();
    return;
  }
  throw new Error(`unexpected byte ${ch} at clause ${clauses}`);
}

// header (first chunk only)
let off = 0;
{
  const hbuf = Buffer.alloc(4096);
  const n = fs.readSync(fd, hbuf, 0, 4096, 0);
  const head = hbuf.toString('ascii', 0, n);
  const m = head.match(/p cnf (\d+) (\d+)/);
  if (!m) throw new Error('no header');
  headerVars = parseInt(m[1], 10); headerClauses = parseInt(m[2], 10);
  off = head.indexOf('\n') + 1;
}
let pos = off;
for (;;) {
  const n = fs.readSync(fd, buf, 0, CHUNK, pos);
  if (n <= 0) break;
  for (let i = 0; i < n; i++) feedByte(buf[i]);
  pos += n;
}
fs.closeSync(fd);
const ok = violated === 0 && clauses === headerClauses;
console.log(JSON.stringify({
  cnf: cnfPath, header_vars: headerVars, header_clauses: headerClauses,
  clauses_scanned: clauses, violated: violated, violated_at: violatedSamples,
  witness_stones: wit.slice().sort((a, b) => a - b),
  result: ok ? 'WITNESS SATISFIES ALL CLAUSES (SAT proven by direct evaluation)' : 'CONTROL FAILED',
}));
process.exit(ok ? 0 : 1);
