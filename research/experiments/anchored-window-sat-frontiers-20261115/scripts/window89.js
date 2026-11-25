// window89.js — anchored window-SAT for the (8,9) band frontier m=29.
// Anchors a known m<=28 witness at a column offset on the 8x29 board, freezes all its
// cells up to freezeLimit (inclusive), leaves the right window free, and runs fastsat
// on the m=29 rowY=3 CNF plus unit clauses. Rigorous within the window:
// SAT = verified witness; UNSAT = no m29 witness with that frozen prefix (conditional).
// Base CNF: genfast.js 8 29 9 --rowY=3 (fastCensus calibrated vs q9-sweep m=9..40).
// Deps: sat.js / genfast.js / fastsat.js next to this file (SEVEN_SCRIPTS overrides).
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const OD = process.env.OUTDIR || path.join(__dirname, '..', 'output');
const ROOT = path.join(__dirname, '..');
const resolve = (p) => (p.startsWith('/') ? p : path.join(ROOT, p));
const S = require(SC + 'sat.js');
require(SC + 'genfast.js'); // patches S.buildCensus -> fastCensus (calibrated w8 q9 m9..40)
const { analyze } = require(SC + 'extend89.js');

const M = 29, W = 8;
const base = fs.readFileSync(process.argv[2], 'utf8');

function run(anchorFile, off, freezeLimit, maxsec, tag) {
  const w = JSON.parse(fs.readFileSync(resolve(anchorFile), 'utf8'));
  const wi = w.witness || w;
  const stones = wi.stones;
  const occ = new Set(stones.map(([x, y]) => y * 1000 + x));
  // unit clauses: anchor cell (x,y) -> board col bx = x + off, frozen if bx <= freezeLimit (and bx in [0,M))
  const units = [];
  for (let bx = 0; bx <= freezeLimit && bx < M; bx++) {
    for (let y = 0; y < W; y++) {
      const ax = bx - off;
      if (ax < 0 || ax >= wi.m) continue;
      const v = y * M + bx + 1;
      units.push((occ.has(y * 1000 + ax) ? '' : '-') + v);
    }
  }
  const cnfFile = path.join(OD, 'win89_' + tag + '.cnf');
  fs.writeFileSync(cnfFile, base + units.map(u => u + ' 0').join('\n') + '\n');
  const res = spawnSync('node', [SC + 'fastsat.js', cnfFile, '--ncells=' + W * M, '--maxseconds=' + maxsec, '--model=' + path.join(OD, 'win89_' + tag + '.model')], { maxBuffer: 1 << 26 });
  const out = JSON.parse(res.stdout.toString().trim());
  const summary = { tag, off, freezeLimit, freeCols: M - 1 - freezeLimit, units: units.length, status: out.status, conflicts: out.conflicts, sec: out.sec };
  if (out.status === 'SAT') {
    const model = fs.readFileSync(path.join(OD, 'win89_' + tag + '.model'), 'utf8').trim().split(/\s+/).map(Number);
    const trueVars = new Set(model.filter(v => v > 0));
    const st = [];
    for (let v = 1; v <= W * M; v++) if (trueVars.has(v)) { const i = v - 1; st.push([i % M, Math.floor(i / M)]); }
    const a = analyze(M, st);
    summary.stones = st.length; summary.analyze = a.ok ? 'WITNESS' : a.why + (a.unblocked ? ' ' + a.unblocked.length : '');
    if (a.ok) {
      const rec = { w: 8, m: M, q: 9, nStones: st.length, rows: a.rows, stones: st, via: 'window-SAT anchor=' + tag + ' off=' + off + ' freeze=' + freezeLimit };
      const wf = path.join(OD, 'witness_m29_' + tag + '.json');
      fs.writeFileSync(wf, JSON.stringify(rec));
      summary.saved = 'output/' + path.basename(wf);
    }
  }
  return summary;
}

const jobs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
for (const j of jobs) {
  try { console.log(JSON.stringify(run(j.anchor, j.off, j.freezeLimit, j.maxsec, j.tag))); } catch (e) { console.log(JSON.stringify({ tag: j.tag, error: String(e) })); }
}
