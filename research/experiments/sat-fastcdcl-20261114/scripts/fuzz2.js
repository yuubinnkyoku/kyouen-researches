// fuzz with full enumeration reference (nv<=16), dup literals allowed, plus 3-SAT larger (nv<=30) vs old cdcl
const fs = require('fs');
const { execFileSync } = require('child_process');
const mod = require('./row_deficient_sat.js');
let bad = 0, n = 0;
function brute(nv, clauses) {
  for (let mask = 0; mask < (1 << nv); mask++) {
    let ok = true;
    for (const c of clauses) {
      let sat = false;
      for (const l of c) { const v = Math.abs(l) - 1; const b = (mask >> v & 1) === 1; if ((l > 0) === b) { sat = true; break; } }
      if (!sat) { ok = false; break; }
    }
    if (ok) return true;
  }
  return false;
}
const N = parseInt(process.argv[2] || '300');
for (let iter = 0; iter < N && bad < 3; iter++) {
  const nv = 4 + Math.floor(Math.random() * 12);
  const nc = 2 + Math.floor(Math.random() * (nv * 4));
  const clauses = [];
  for (let c = 0; c < nc; c++) {
    const len = 1 + Math.floor(Math.random() * 4);
    const cl = [];
    for (let l = 0; l < len; l++) {
      const v = 1 + Math.floor(Math.random() * nv);
      cl.push(Math.random() < 0.5 ? v : -v);
    }
    clauses.push(cl);
  }
  const ref = brute(nv, clauses);
  const lines = ['p cnf ' + nv + ' ' + clauses.length];
  for (const c of clauses) lines.push(c.join(' ') + ' 0');
  fs.writeFileSync('/tmp/fz2.cnf', lines.join('\n') + '\n');
  let out;
  try { out = JSON.parse(execFileSync('node', ['fastsat.js', '/tmp/fz2.cnf', '--maxconflicts=500000', '--model=/tmp/fz2.model'], { encoding: 'utf8' })); }
  catch (e) { out = { status: 'CRASH:' + String(e).slice(0, 120) }; }
  n++;
  if (out.status === 'SAT') {
    const chk = JSON.parse(execFileSync('node', ['checkmodel.js', '/tmp/fz2.cnf', '/tmp/fz2.model'], { encoding: 'utf8' }));
    if (chk.unsatisfied !== 0) { console.log(iter, 'BAD MODEL', JSON.stringify(chk)); bad++; continue; }
    if (!ref) { console.log(iter, 'FASTSAT SAT but brute UNSAT nv=' + nv); fs.writeFileSync('/tmp/fz2_bad.cnf', lines.join('\n') + '\n'); bad++; }
  } else if (out.status === 'UNSAT') {
    if (ref) { console.log(iter, 'FASTSAT UNSAT but brute SAT nv=' + nv); fs.writeFileSync('/tmp/fz2_bad.cnf', lines.join('\n') + '\n'); bad++; }
  } else { console.log(iter, 'status', out.status, out.err || ''); if (String(out.status).startsWith('CRASH') || out.status === 'ERROR') bad++; }
}
console.log('checked ' + n + ', bad=' + bad);
