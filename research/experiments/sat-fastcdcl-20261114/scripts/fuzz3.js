// cross-check fastsat vs repo CDCL on random 3-SAT, nv 20-40 (both must agree)
const fs = require('fs');
const { execFileSync } = require('child_process');
const mod = require('./row_deficient_sat.js');
let bad = 0, n = 0, agree = 0;
const N = parseInt(process.argv[2] || '60');
for (let iter = 0; iter < N && bad < 3; iter++) {
  const nv = 20 + Math.floor(Math.random() * 21);
  const nc = Math.floor(nv * (3.5 + Math.random() * 2.5));
  const clauses = [];
  for (let c = 0; c < nc; c++) {
    const vs = new Set();
    while (vs.size < 3) vs.add(1 + Math.floor(Math.random() * nv));
    const cl = [];
    for (const v of vs) cl.push(Math.random() < 0.5 ? v : -v);
    clauses.push(cl);
  }
  const t0 = Date.now();
  let ref;
  try { ref = mod.cdcl(nv, clauses.map(c => c.slice()), 300000); } catch (e) { ref = { error: 1 }; }
  const refMs = Date.now() - t0;
  if (ref.timeout || ref.error) continue;
  const lines = ['p cnf ' + nv + ' ' + clauses.length];
  for (const c of clauses) lines.push(c.join(' ') + ' 0');
  fs.writeFileSync('/tmp/fz3.cnf', lines.join('\n') + '\n');
  let out;
  try { out = JSON.parse(execFileSync('node', ['fastsat.js', '/tmp/fz3.cnf', '--maxconflicts=300000', '--model=/tmp/fz3.model'], { encoding: 'utf8' })); }
  catch (e) { out = { status: 'CRASH' }; }
  n++;
  if (out.status === 'SAT') {
    const chk = JSON.parse(execFileSync('node', ['checkmodel.js', '/tmp/fz3.cnf', '/tmp/fz3.model'], { encoding: 'utf8' }));
    if (chk.unsatisfied !== 0) { console.log(iter, 'BAD MODEL'); bad++; continue; }
  }
  const agreeNow = (out.status === 'SAT') === !!ref.sat;
  if (agreeNow) agree++;
  else { console.log(iter, 'DISAGREE fastsat=' + out.status + ' old=' + (ref.sat ? 'SAT' : 'UNSAT') + ' nv=' + nv + ' nc=' + nc); fs.writeFileSync('/tmp/fz3_bad.cnf', lines.join('\n') + '\n'); bad++; }
}
console.log('cross-checked ' + n + ', agree=' + agree + ', bad=' + bad);
