// run_case.js — dump CNF with sat2.js encoding, run kissat, verify SAT models with census-free verifier + python independent verifier.
// Usage: node run_case.js <w> <m> <q> <enc-args...> --out=<prefix> [--tlim=<sec>]
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const args = process.argv.slice(2);
const [w, m, q] = [Number(args[0]), Number(args[1]), Number(args[2])];
const encArgs = [];
let prefix = 'case', tlim = 275;
for (const a of args.slice(3)) {
  if (a.startsWith('--out=')) prefix = a.slice(6);
  else if (a.startsWith('--tlim=')) tlim = Number(a.slice(7));
  else encArgs.push(a);
}
const kissat = path.join(__dirname, '..', 'kissat-4.0.4-linux-amd64');
const cnf = '/tmp/' + prefix + '.cnf';
const outp = '/tmp/' + prefix + '.kout';

const meta = JSON.parse(execFileSync('node', [path.join(__dirname, 'sat2.js'), w, m, q, ...encArgs, cnf], { maxBuffer: 1 << 26 }).toString());
const t0 = Date.now();
let res, timedOut = false;
try {
  res = execFileSync(kissat, [cnf, '--time=' + tlim], { maxBuffer: 1 << 26, timeout: (tlim + 20) * 1000 });
} catch (e) {
  // kissat exit codes: 10 = SAT, 20 = UNSAT (competition convention) — not errors
  res = (e.stdout || Buffer.alloc(0));
  if (e.killed) timedOut = true;
}
fs.writeFileSync(outp, res);
const sout = res.toString();
const sat = sout.includes('s UNSATISFIABLE') ? 'UNSAT' : sout.includes('s SATISFIABLE') ? 'SAT' : 'TIMEOUT';
const conflicts = (sout.match(/conflicts:\s+(\d+)/) || [])[1];
const decisions = (sout.match(/decisions:\s+(\d+)/) || [])[1];
const rec = { w, m, q, encArgs: encArgs.join(' '), vars: meta.vars, clauses: meta.clauses, mode: meta.mode, counter: meta.counter, lex: meta.lex, result: sat, conflicts: conflicts ? Number(conflicts) : null, decisions: decisions ? Number(decisions) : null, seconds: (Date.now() - t0) / 1000, date: new Date().toISOString() };
if (sat === 'SAT') {
  const lits = [];
  for (const line of sout.split('\n')) if (line.startsWith('v ')) lits.push(...line.slice(2).trim().split(/\s+/).map(Number));
  const n = w * m;
  const modelMap = new Map(); for (const l of lits) modelMap.set(Math.abs(l), l > 0);
  const stones = [];
  for (let i = 0; i < n; i++) if (modelMap.get(i + 1)) stones.push([i % m, Math.floor(i / m)]);
  rec.stones = stones; rec.size = stones.length;
  rec.rows = stones.reduce((a, [x, y]) => (a[y] = (a[y] || 0) + 1, a), {});
  const V = require('./sat.js');
  rec.verify_js = V.verifyConfig(w, m, q, stones);
  try {
    const py = execFileSync('python3', [path.join(__dirname, 'verify_input.py'), JSON.stringify({ w, m, q, stones })], { maxBuffer: 1 << 24 }).toString().trim();
    rec.verify_py = JSON.parse(py);
  } catch (e) { rec.verify_py = { error: String(e).slice(0, 200) }; }
  fs.writeFileSync('/tmp/model_' + prefix + '.json', JSON.stringify({ w, m, q, stones }));
}
fs.writeFileSync(path.join(__dirname, '..', 'results', prefix + '.json'), JSON.stringify(rec, null, 1));
console.log(JSON.stringify({ prefix, result: sat, conflicts: rec.conflicts, seconds: rec.seconds, verify_js: rec.verify_js ? rec.verify_js.ok : undefined, verify_py: rec.verify_py ? rec.verify_py.ok : undefined, size: rec.size, rows: rec.rows }));
