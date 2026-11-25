// K0568 counter-semantics isolation control (Sinz sequential counters only,
// no circuit clauses): pins the meaning of the exactly-K encoding used by
// the K_6 circuit CNF, independent of the circuit family.
//
// Generates counters-only CNFs (both counters of the real CNF: at-most-K on
// the positives and at-most-(64-K) on the negatives) plus unit clauses:
//   posN  : N positive units (witness stones), all other vars free
//   fullN : complete assignment with exactly N positives fixed
// Expected with K = 9: pos10 UNSAT, pos9 SAT, pos8 SAT (at-most-9 side);
// full8/full10 UNSAT, full9 SAT (exactly-9 semantics, both counters).
//
// Usage: node counter_control.js --k 9 --witness v1,v2,... [--kissat PATH]
'use strict';
const fs = require('fs');
const { execFileSync } = require('child_process');

const args = process.argv.slice(2);
const K = parseInt(args[args.indexOf('--k') + 1], 10);
const wit = args[args.indexOf('--witness') + 1].split(',').map((x) => parseInt(x, 10));
const kissat = args.includes('--kissat') ? args[args.indexOf('--kissat') + 1] : './kissat-4.0.4-linux-amd64';
if (wit.length !== 10) throw new Error('need a 10-vertex witness list');

function atMostKClauses(lits, k, nextVar, out) {
  const n = lits.length;
  if (k === 0) { for (const lit of lits) out.push([-lit]); return nextVar; }
  if (k >= n) return nextVar;
  const s = [];
  for (let i = 0; i < n; i++) { s.push([]); for (let j = 0; j < k; j++) s[i].push(nextVar++); }
  out.push([-lits[0], s[0][0]]);
  for (let j = 1; j < k; j++) out.push([-s[0][j]]);
  for (let i = 1; i < n; i++) {
    out.push([-lits[i], s[i][0]]);
    out.push([-s[i - 1][0], s[i][0]]);
    for (let j = 1; j < k; j++) {
      out.push([-s[i - 1][j], s[i][j]]);
      out.push([-lits[i], -s[i - 1][j - 1], s[i][j]]);
    }
    out.push([-lits[i], -s[i - 1][k - 1]]);
  }
  return nextVar;
}

let nextVar = 65;
const counterClauses = [];
{
  const lits = []; for (let i = 0; i < 64; i++) lits.push(i + 1);
  nextVar = atMostKClauses(lits, K, nextVar, counterClauses);
}
{
  const lits = []; for (let i = 0; i < 64; i++) lits.push(-(i + 1));
  nextVar = atMostKClauses(lits, 64 - K, nextVar, counterClauses);
}

function writeCnf(path, units) {
  const total = counterClauses.length + units.length;
  let out = `p cnf ${nextVar - 1} ${total}\n`;
  for (const u of units) out += `${u} 0\n`;
  for (const c of counterClauses) { for (const l of c) out += l + ' '; out += '0\n'; }
  fs.writeFileSync(path, out);
  return total;
}

function solve(path) {
  let res = '';
  try {
    res = execFileSync(kissat, [path], { encoding: 'utf8', timeout: 60000, maxBuffer: 16 * 1024 * 1024 });
  } catch (e) {
    // kissat exits 10 (SAT) / 20 (UNSAT): nonzero exit is expected, parse output
    res = (e.stdout || '') + (e.stderr || '');
  }
  const line = res.split('\n').find((l) => l.startsWith('s '));
  if (!line) throw new Error(`no result line for ${path}`);
  return line.slice(2).trim();
}

const results = {};
for (const n of [8, 9, 10]) {
  // posN: positive units only (witness prefix), rest free
  const posUnits = wit.slice(0, n).map((v) => v + 1);
  const p1 = `ctr_pos${n}.cnf`;
  const c1 = writeCnf(p1, posUnits);
  const r1 = solve(p1);
  // fullN: complete assignment with exactly n true
  const fullUnits = [];
  const tr = new Set(wit.slice(0, n));
  for (let v = 0; v < 64; v++) fullUnits.push(tr.has(v) ? v + 1 : -(v + 1));
  const p2 = `ctr_full${n}.cnf`;
  const c2 = writeCnf(p2, fullUnits);
  const r2 = solve(p2);
  results[`pos${n}`] = { clauses: c1, result: r1, expected: n > K ? 'UNSATISFIABLE' : 'SATISFIABLE' };
  results[`full${n}`] = { clauses: c2, result: r2, expected: n === K ? 'SATISFIABLE' : 'UNSATISFIABLE' };
}
let ok = true;
for (const [k, v] of Object.entries(results)) {
  const pass = v.result === v.expected;
  if (!pass) ok = false;
  console.log(`${k}: clauses=${v.clauses} result=${v.result} expected=${v.expected} ${pass ? 'PASS' : 'FAIL'}`);
}
console.log(JSON.stringify({ k: K, witness10: wit, counter_clauses: counterClauses.length, all_pass: ok }));
process.exit(ok ? 0 : 1);
