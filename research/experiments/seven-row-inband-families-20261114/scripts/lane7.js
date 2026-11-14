// lane7.js — run one deficient-maximal SAT instance (w,m,q) end-to-end:
//   sat2.js (--deficient | --rowY=Y | --lex=H,V,HV) -> DIMACS -> fastsat.js -> verdict
//   SAT: stones extracted; dual-verified by sat.js verifyConfig (census-free JS)
//        AND scripts/verify_witness.py (independent Python Fraction geometry).
//   Appends one JSON line to results/results.jsonl (append-only, atomic for <4KB lines).
// Usage: node lane7.js w m q [maxsec] [tag] [--rowY=Y] [--seed=S] [--lex=H,V,HV]
'use strict';
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const [w, m, q] = [Number(process.argv[2]), Number(process.argv[3]), Number(process.argv[4])];
const maxsec = Number(process.argv[5] || 120);
let tag = process.argv[6] || 'run';
let rowY = null;
for (const a of process.argv.slice(6)) {
  const mm = /^--rowY=(\d+)$/.exec(a);
  if (mm) { rowY = Number(mm[1]); tag = process.argv[6]; }
}
const seedM = /^(?:--)?seed=(\d+)$/.exec(process.argv.slice(6).find(a => a.includes('seed=')) || '');
const seed = seedM ? seedM[1] : null;
const lexA = process.argv.slice(6).find(a => a.startsWith('--lex='));
const lex = lexA ? lexA.slice(6).split(',').filter(t => ['H', 'V', 'HV'].includes(t)) : [];
const modeArgs = (rowY === null ? ['--deficient'] : ['--rowY=' + rowY]).concat(lex.length ? ['--lex=' + lex.join(',')] : []);
const DIR = __dirname + '/..';
const cnf = `${DIR}/results/cnf_${tag}_${w}_${m}_${q}${rowY === null ? '' : '_r' + rowY}${seed ? '_s' + seed : ''}.cnf`;
const mdl = `${DIR}/results/model_${tag}_${w}_${m}_${q}${rowY === null ? '' : '_r' + rowY}${seed ? '_s' + seed : ''}.txt`;

const meta = JSON.parse(execFileSync('node', [`${DIR}/scripts/sat2.js`, String(w), String(m), String(q), ...modeArgs, cnf], { encoding: 'utf8' }));
const t0 = Date.now();
const fsverdict = execFileSync('node', [`${DIR}/scripts/fastsat.js`, cnf, `--maxseconds=${maxsec}`, `--model=${mdl}`, ...(seed ? ['--seed=' + seed] : [])], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
const solver = JSON.parse(fsverdict.trim().split('\n').pop());
const wall = Date.now() - t0;

const rec = { w, m, q, tag, rowY, seed, lex, encoding: { vars: meta.vars, clauses: meta.clauses, curves: meta.curves, mode: meta.mode, counter: meta.counter, lex: meta.lex }, solver: 'fastsat.js', maxsec, status: solver.status, conflicts: solver.conflicts, decisions: solver.decisions, solveMs: solver.sec * 1000, wallMs: wall };

if (solver.status === 'SAT') {
  const lits = fs.readFileSync(mdl, 'utf8').trim().split(/\s+/).map(Number);
  const pos = new Set(lits.filter(v => v > 0));
  const stones = [];
  for (let y = 0; y < w; y++) for (let x = 0; x < m; x++) if (pos.has(y * m + x + 1)) stones.push([x, y]);
  const S = require(path.join(DIR, 'scripts/sat.js'));
  const jsv = S.verifyConfig(w, m, q, stones);
  const py = JSON.parse(execFileSync('python3', [`${DIR}/scripts/verify_witness.py`, String(w), String(m), String(q)], { input: JSON.stringify(stones), encoding: 'utf8' }));
  const rows = Array.from({ length: w }, (_, y) => stones.filter(s => s[1] === y).length);
  rec.stones = stones;
  rec.rows = rows;
  rec.nStones = stones.length;
  rec.jsVerify = jsv;
  rec.pyVerify = py;
  rec.deficientRows = rows.map((c, y) => [c, y]).filter(([c]) => c <= q - 2);
  if (!(jsv && jsv.ok && py.ok)) { rec.status = 'VERIFY-FAIL'; }
}
fs.appendFileSync(`${DIR}/results/results.jsonl`, JSON.stringify(rec) + '\n');
fs.rmSync(cnf, { force: true }); fs.rmSync(mdl, { force: true });
console.log(JSON.stringify({ w, m, q, rowY, seed, lex, status: rec.status, n: rec.nStones || null, rows: rec.rows || null, conflicts: rec.conflicts, sec: (rec.wallMs / 1000).toFixed(1), jsOk: rec.jsVerify ? !!rec.jsVerify.ok : null, pyOk: rec.pyVerify ? !!rec.pyVerify.ok : null }));
process.exit(0);
