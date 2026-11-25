// validate.js — exhaustive brute-force ground truth vs every sat2.js encoding variant on small boards.
// Checks: deficient mode, deficient+lex, rowfixed per row, cap mode (tot & seq), cap+lex.
// Requires m >= q for deficient/rowfixed modes (row lines must appear in the census).
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const S = require('./sat.js');
const { dump, toDimacs2 } = require('./sat2.js');

function brute(w, m, q) {
  const { P, n, curves } = S.buildCensus(w, m, q);
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  const full = w * (q - 1);
  const res = { n, full, maximals: 0, minMaximal: Infinity, defMax: 0, minDef: Infinity, defByRow: new Array(w).fill(0) };
  for (let mask = 0; mask < (1 << n); mask++) {
    let ok = true;
    for (const cu of curves) {
      let cnt = 0; for (const p of cu.pts) if (mask >> p & 1) { cnt++; if (cnt >= q) { ok = false; break; } }
      if (!ok) break;
    }
    if (!ok) continue;
    let max = true;
    for (let p = 0; p < n; p++) {
      if (mask >> p & 1) continue;
      let blocked = false;
      for (const ci of through[p]) { const cu = curves[ci]; let cnt = 0; for (const x of cu.pts) if (mask >> x & 1) cnt++; if (cnt >= q - 1) { blocked = true; break; } }
      if (!blocked) { max = false; break; }
    }
    if (!max) continue;
    let size = 0; const rows = new Array(w).fill(0);
    for (let p = 0; p < n; p++) if (mask >> p & 1) { size++; rows[Math.floor(p / m)]++; }
    res.maximals++; res.minMaximal = Math.min(res.minMaximal, size);
    if (size < full) {
      res.defMax++; res.minDef = Math.min(res.minDef, size);
      for (let y = 0; y < w; y++) if (rows[y] <= q - 2) { res.defByRow[y]++; } // any deficient row (existence semantics)
    }
  }
  return res;
}

function kissat(cnfPath, tlim = 120) {
  const kissat = path.join(__dirname, '..', 'kissat-4.0.4-linux-amd64');
  let res;
  try { res = execFileSync(kissat, [cnfPath, '--time=' + tlim], { maxBuffer: 1 << 26, timeout: (tlim + 15) * 1000 }); }
  catch (e) { res = e.stdout || Buffer.alloc(0); }
  const s = res.toString();
  return s.includes('s UNSATISFIABLE') ? 'UNSAT' : s.includes('s SATISFIABLE') ? 'SAT' : 'TIMEOUT';
}

function runEnc(w, m, q, opts) {
  const { enc } = dump(w, m, q, opts);
  const cnf = '/tmp/val_' + Math.floor(Math.random() * 1e9) + '.cnf';
  fs.writeFileSync(cnf, toDimacs2(enc));
  const r = kissat(cnf);
  fs.unlinkSync(cnf);
  return r;
}

function eq(a, b, what) { if (a !== b) { console.log('MISMATCH', what, a, b); process.exitCode = 1; } else console.log('ok', what, '=', a); }

const boards = process.argv.slice(2).map(s => s.split(',').map(Number));
for (const [w, m, q] of boards) {
  console.log('=== board', w, m, q);
  const b = brute(w, m, q);
  console.log('brute:', JSON.stringify(b));
  const defExp = b.defMax > 0 ? 'SAT' : 'UNSAT';
  if (m >= q) {
    eq(runEnc(w, m, q, { mode: 'deficient' }), defExp, 'deficient');
    eq(runEnc(w, m, q, { mode: 'deficient', lex: ['H', 'V', 'HV'] }), defExp, 'deficient+lex');
    for (let y = 0; y < w; y++) {
      const exp = b.defByRow[y] > 0 ? 'SAT' : 'UNSAT';
      eq(runEnc(w, m, q, { mode: 'rowfixed', rowY: y, lex: ['H'] }), exp, 'rowfixed' + y + '+lexH');
    }
  }
  if (b.minMaximal < Infinity) {
    for (const K of [b.minMaximal - 1, b.minMaximal]) {
      const exp = b.minMaximal <= K ? 'SAT' : 'UNSAT';
      eq(runEnc(w, m, q, { mode: 'cap', cap: K, counter: 'tot' }), exp, 'cap' + K + 'tot');
      eq(runEnc(w, m, q, { mode: 'cap', cap: K, counter: 'tot', lex: ['H', 'V', 'HV'] }), exp, 'cap' + K + 'tot+lex');
      eq(runEnc(w, m, q, { mode: 'cap', cap: K, counter: 'seq' }), exp, 'cap' + K + 'seq');
    }
  }
}
console.log(process.exitCode ? 'VALIDATION FAILED' : 'ALL OK');
