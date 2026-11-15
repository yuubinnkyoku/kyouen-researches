// classsplit.js — deficiency-class decomposition solver for w x m q-point witness-free
// proofs: classes (r, k) = "row r has exactly k stones", r in given canonical rows,
// k in 0..q-2. Mirror (V: y -> w-1-y) soundness: any witness has some deficient row;
// if its index is outside the canonical set, the V-mirror witness is covered.
// All classes UNSAT => witness-free at that (w,m,q) (exhaustive over witnesses whose
// deficient row set intersects the canonical rows after mirroring).
// Deps: sat.js / sat2.js / fastsat.js / verify_witness.py next to this file.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const S = require(SC + 'sat.js');
const S2 = require(SC + 'sat2.js');
const OD = process.env.OUTDIR || path.join(__dirname, '..', 'output');

function solveClass(w, m, q, r, k, maxsec, tag, lex) {
  const { enc, cell, P, n, curves, rowGe } = S2.encodeCore(w, m, q);
  const rowCells = [];
  for (let x = 0; x < m; x++) rowCells.push(cell[r * m + x]);
  // exactly k stones in row r: at-most-k and at-least-k (via negated literals)
  S2.totalizerAtMost(enc, rowCells.slice(), k);
  S2.totalizerAtMost(enc, rowCells.map(v => -v), m - k);
  let lexUsed = [];
  if (lex && lex.length) { for (const nm of lex) { S2.lexLeader(enc, cell, m, w, (x, y) => nm === 'H' ? [m - 1 - x, y] : nm === 'V' ? [x, w - 1 - y] : [m - 1 - x, w - 1 - y]); lexUsed = lex; } }
  const txt = S2.toDimacs2(enc);
  const f = path.join(OD, 'cls_' + tag + '.cnf');
  fs.writeFileSync(f, txt);
  const res = spawnSync('node', [SC + 'fastsat.js', f, '--ncells=' + w * m, '--maxseconds=' + maxsec, '--model=' + path.join(OD, 'cls_' + tag + '.model')], { maxBuffer: 1 << 26 });
  const out = JSON.parse(res.stdout.toString().trim());
  const rec = { tag, w, m, q, r, k, lex: lexUsed, vars: Number(txt.match(/^p cnf (\d+)/m)[1]), status: out.status, conflicts: out.conflicts, sec: out.sec };
  if (out.status === 'SAT') {
    const model = fs.readFileSync(path.join(OD, 'cls_' + tag + '.model'), 'utf8').trim().split(/\s+/).map(Number);
    const tv = new Set(model.filter(v => v > 0));
    const st = [];
    for (let v = 1; v <= w * m; v++) if (tv.has(v)) { const i = v - 1; st.push([i % m, Math.floor(i / m)]); }
    const vc = S.verifyConfig(w, m, q, st);
    rec.stones = st.length; rec.verify = vc.ok ? 'WITNESS' : vc.why;
    if (vc.ok) {
      const rows = Array(w).fill(0); for (const [, y] of st) rows[y]++;
      const wf = path.join(OD, 'witness_w' + w + 'x' + m + 'q' + q + '_' + tag + '.json');
      fs.writeFileSync(wf, JSON.stringify({ w, m, q, nStones: st.length, rows, stones: st, via: 'class-split r=' + r + ' k=' + k, verify: vc }));
      const py = spawnSync('python3', [SC + 'verify_witness.py', String(w), String(m), String(q)], { input: JSON.stringify(st), maxBuffer: 1 << 24 });
      rec.pyVerify = py.stdout ? py.stdout.toString().trim() : String(py.error);
      rec.saved = 'output/' + path.basename(wf);
    }
  }
  return rec;
}

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const j of jobs) {
  try { console.log(JSON.stringify(solveClass(j.w, j.m, j.q, j.r, j.k, j.maxsec, j.tag, j.lex || []))); } catch (e) { console.log(JSON.stringify({ tag: j.tag, error: String(e).slice(0, 300) })); }
}
