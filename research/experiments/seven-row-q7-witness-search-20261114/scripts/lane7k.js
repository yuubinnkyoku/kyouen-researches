// lane7k.js — run one deficient-maximal SAT instance (w,m,q) with kissat 4.0.4:
//   sat2.js (--deficient | --lex=H,V,HV) -> DIMACS -> kissat (raw log saved) -> verdict
//   SAT: stones extracted from the "v " model lines; dual-verified by sat.js
//        verifyConfig (census-free JS) AND verify_witness.py (Python Fraction).
//   Appends one JSON line to output/results.jsonl.
// Usage: node lane7k.js w m q [maxsec] [tag] [--lex=H,V,HV]
// Adapted from research/experiments/seven-row-inband-families-20261114/scripts/lane7.js
// (same sat2.js encoder, same dual verification); solver replaced by kissat 4.0.4.
'use strict';
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const KISSAT = process.env.KISSAT || '/tmp/kissat-4.0.4-linux-amd64';
const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const maxsec = Number(process.argv[5] || 120);
let tag = process.argv[6] || 'run';
const lexA = process.argv.slice(6).find(a => a.startsWith('--lex='));
const lex = lexA ? lexA.slice(6).split(',').filter(t => ['H', 'V', 'HV'].includes(t)) : [];
const modeArgs = ['--deficient'].concat(lex.length ? ['--lex=' + lex.join(',')] : []);
const DIR = __dirname + '/..';
const base = `${tag}_${w}x${m}q${q}${lex.length ? '_lex' + lex.join('') : ''}`;
const cnf = `${DIR}/output/cnf_${base}.cnf`;
const log = `${DIR}/output/${base}.kissat.txt`;

const meta = JSON.parse(execFileSync('node', [`${DIR}/scripts/sat2.js`, String(w), String(m), String(q), ...modeArgs, cnf], { encoding: 'utf8' }));
const t0 = Date.now();
let raw;
try {
  raw = execFileSync(KISSAT, [cnf], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, timeout: maxsec * 1000 });
} catch (e) {
  // kissat exits 10 on SAT and 20 on UNSAT; treat both as normal completion
  if (e.status === 10 || e.status === 20) raw = e.stdout;
  else throw e;
}
fs.writeFileSync(log, raw);
const wall = Date.now() - t0;
const status = /^s SATISFIABLE/m.test(raw) ? 'SAT' : (/^s UNSATISFIABLE/m.test(raw) ? 'UNSAT' : 'UNKNOWN');
const conf = Number((/c conflicts:\s+(\d+)/.exec(raw) || [0, 0])[1]);
const deci = Number((/c decisions:\s+(\d+)/.exec(raw) || [0, 0])[1]);
const mem = Number((/maximum-resident-set-size:\s+(\d+)/.exec(raw) || [0, 0])[1]);

const rec = { w, m, q, tag, lex, encoding: { vars: meta.vars, clauses: meta.clauses, curves: meta.curves, mode: meta.mode, lex: meta.lex },
  solver: 'kissat-4.0.4', status, conflicts: conf, decisions: deci, maxrssKB: mem, wallMs: wall, cnfBytes: fs.statSync(cnf).length };

if (status === 'SAT') {
  const lits = raw.split('\n').filter(l => l.startsWith('v ')).join(' ').trim().split(/\s+/).map(s => s.replace(/^v /, '')).map(Number).filter(v => v !== 0);
  const pos = new Set(lits.filter(v => v > 0));
  const stones = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) if (pos.has(y * m + x + 1)) stones.push([x, y]);
  const S = require(path.join(DIR, 'scripts/sat.js'));
  rec.stones = stones;
  rec.rows = Array.from({ length: w }, (_, y) => stones.filter(s => s[1] === y).length);
  rec.nStones = stones.length;
  rec.jsVerify = S.verifyConfig(w, m, q, stones);
  rec.pyVerify = JSON.parse(execFileSync('python3', [`${DIR}/scripts/verify_witness.py`, String(w), String(m), String(q)], { input: JSON.stringify(stones), encoding: 'utf8' }));
  if (rec.jsVerify !== true && rec.jsVerify !== 'OK' && !(rec.jsVerify && rec.jsVerify.ok)) { rec.jsVerifyRaw = rec.jsVerify; }
  if (!rec.pyVerify || rec.pyVerify.ok !== true) { rec.pyVerifyRaw = rec.pyVerify; }
}
fs.appendFileSync(`${DIR}/output/results.jsonl`, JSON.stringify(rec) + '\n');
fs.unlinkSync(cnf);
console.log(JSON.stringify({ w, m, q, status, conflicts: conf, wallMs: wall, nStones: rec.nStones || null, rows: rec.rows || null }));
