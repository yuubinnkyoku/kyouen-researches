// postprocess.js — parse a finished kissat log, extract + verify SAT models (JS census-free + python independent), write JSON record.
// Usage: node postprocess.js <kout> <w> <m> <q> <prefix> <encArgs> <seconds>
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const S = require('./sat.js');

const [kout, wS, mS, qS, prefix, encArgs, secS] = process.argv.slice(2);
const [w, m, q, sec] = [Number(wS), Number(mS), Number(qS), Number(secS)];
const sout = fs.readFileSync(kout, 'utf8');
const conflicts = Number((sout.match(/conflicts:\s+(\d+)/) || [])[1] || 0);
const decisions = Number((sout.match(/decisions:\s+(\d+)/) || [])[1] || 0);
let result = sout.includes('s UNSATISFIABLE') ? 'UNSAT' : sout.includes('s SATISFIABLE') ? 'SAT' : 'TIMEOUT';
const rec = { w, m, q, encArgs, result, conflicts: conflicts || null, decisions: decisions || null, seconds: sec, date: new Date().toISOString() };
if (result === 'SAT') {
  const lits = [];
  for (const line of sout.split('\n')) if (line.startsWith('v ')) lits.push(...line.slice(2).trim().split(/\s+/).map(Number));
  const n = w * m;
  const modelMap = new Map(); for (const l of lits) modelMap.set(Math.abs(l), l > 0);
  const stones = [];
  for (let i = 0; i < n; i++) if (modelMap.get(i + 1)) stones.push([i % m, Math.floor(i / m)]);
  rec.stones = stones; rec.size = stones.length;
  rec.rows = stones.reduce((a, [x, y]) => (a[y] = (a[y] || 0) + 1, a), {});
  rec.verify_js = S.verifyConfig(w, m, q, stones);
  try {
    const py = execFileSync('python3', [path.join(__dirname, 'verify_input.py'), JSON.stringify({ w, m, q, stones })], { maxBuffer: 1 << 24 }).toString().trim();
    rec.verify_py = JSON.parse(py);
  } catch (e) { rec.verify_py = { error: String(e).slice(0, 200) }; }
  fs.writeFileSync('/tmp/model_' + prefix + '.json', JSON.stringify({ w, m, q, stones }));
}
fs.writeFileSync(path.join(__dirname, '..', 'results', prefix + '.json'), JSON.stringify(rec, null, 1));
console.log(JSON.stringify({ prefix, result: rec.result, conflicts: rec.conflicts, verify_js: rec.verify_js ? rec.verify_js.ok : undefined, verify_py: rec.verify_py ? rec.verify_py.ok : undefined, size: rec.size, rows: rec.rows }));
