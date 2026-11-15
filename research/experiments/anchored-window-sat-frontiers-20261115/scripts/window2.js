// window2.js — generic anchored window-SAT for w x m q-point deficient-maximal witnesses.
// Freeze a known witness's cells on a wider board (column offset), leave a set of columns
// free, and solve def-mode CNF + unit clauses with fastsat (pure-JS CDCL).
// SAT  => decoded witness is verified census-free (sat.js verifyConfig) + Python Fraction
//         (verify_witness.py) before being reported/saved.
// UNSAT => rigorous conditional result: no witness with that frozen prefix (checked
//          non-vacuous first: no frozen safety violation, no dead frozen cell).
// Deps: sat.js / sat2.js / fastsat.js / verify_witness.py next to this file
//       (SEVEN_SCRIPTS overrides). Output: OUTDIR or ../output.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const S = require(SC + 'sat.js');
const S2 = require(SC + 'sat2.js');
const OD = process.env.OUTDIR || path.join(__dirname, '..', 'output');
const ROOT = path.join(__dirname, '..');
const resolve = (p) => (p.startsWith('/') ? p : path.join(ROOT, p));

const cnfCache = {};
function baseCNF(w, m, q) {
  const k = w + '/' + m + '/' + q + '/def';
  if (cnfCache[k]) return cnfCache[k];
  const { enc, meta } = S2.dump(w, m, q, { mode: 'deficient', counter: 'seq', lex: [] });
  const txt = S2.toDimacs2(enc);
  return (cnfCache[k] = { txt, ncells: w * m, meta });
}

const throughCache = {};
function censusData(w, m, q) {
  const k = w + '/' + m + '/' + q;
  if (throughCache[k]) return throughCache[k];
  const { P, n, curves } = S.buildCensus(w, m, q);
  const through = Array.from({ length: n }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  return (throughCache[k] = { P, curves, through });
}

function vacuity(w, m, q, frozen, frozenStones) {
  // returns null if the frozen prefix is internally consistent, else a reason
  const { curves, through } = censusData(w, m, q);
  for (let ci = 0; ci < curves.length; ci++) {
    let f = 0;
    for (const p of curves[ci].pts) if (frozenStones.has(p)) f++;
    if (f >= q) return { why: 'frozen-unsafe', ci, f };
  }
  for (const i of frozen) {
    if (frozenStones.has(i)) continue;
    let best = 0, bci = -1;
    for (const ci of through[i]) {
      let f = 0, free = 0;
      for (const p of curves[ci].pts) { if (frozenStones.has(p)) f++; if (!frozen.has(p)) free++; }
      if (f + free > best) { best = f + free; bci = ci; }
    }
    if (best < q - 1) return { why: 'dead-frozen-cell', cell: [i % m, Math.floor(i / m)], best, bci };
  }
  return null;
}

function run(job) {
  const { w, m, q, anchor, off, freeCols, maxsec, tag, vmir = false, hmir = false } = job;
  const aw = JSON.parse(fs.readFileSync(resolve(anchor), 'utf8'));
  const awi = aw.witness || aw;
  let stones = awi.stones.map(([x, y]) => [x, y]);
  if (vmir) stones = stones.map(([x, y]) => [x, w - 1 - y]);
  if (hmir) stones = stones.map(([x, y]) => [awi.m - 1 - x, y]);
  const occ = new Set(stones.map(([x, y]) => y * 1000 + x));
  const free = new Set(freeCols);
  const units = [];
  const frozen = new Set(), frozenStones = new Set();
  for (let bx = 0; bx < m; bx++) {
    if (free.has(bx)) continue;
    const ax = bx - off;
    if (ax < 0 || ax >= awi.m) continue;
    for (let y = 0; y < w; y++) {
      const cell = y * m + bx;
      units.push((occ.has(y * 1000 + ax) ? '' : '-') + (cell + 1));
      frozen.add(cell);
      if (occ.has(y * 1000 + ax)) frozenStones.add(cell);
    }
  }
  const vac = vacuity(w, m, q, frozen, frozenStones);
  if (vac) return { tag, off, freeCols, status: 'VACUOUS', vac, units: units.length };
  const base = baseCNF(w, m, q);
  const cnfFile = path.join(OD, 'win_' + tag + '.cnf');
  fs.writeFileSync(cnfFile, base.txt + '\n' + units.map(u => u + ' 0').join('\n') + '\n');
  const res = spawnSync('node', [SC + 'fastsat.js', cnfFile, '--ncells=' + w * m, '--maxseconds=' + maxsec, '--model=' + path.join(OD, 'win_' + tag + '.model')], { maxBuffer: 1 << 26 });
  const out = JSON.parse(res.stdout.toString().trim());
  const summary = { tag, off, freeCols, nFreeCols: freeCols.length, units: units.length, status: out.status, conflicts: out.conflicts, sec: out.sec };
  if (out.status === 'SAT') {
    const model = fs.readFileSync(path.join(OD, 'win_' + tag + '.model'), 'utf8').trim().split(/\s+/).map(Number);
    const tv = new Set(model.filter(v => v > 0));
    const st = [];
    for (let v = 1; v <= w * m; v++) if (tv.has(v)) { const i = v - 1; st.push([i % m, Math.floor(i / m)]); }
    const vc = S.verifyConfig(w, m, q, st);
    summary.stones = st.length; summary.verify = vc.ok ? 'WITNESS' : vc.why + ' ' + JSON.stringify(vc.cell || vc.co || '');
    if (vc.ok) {
      const rows = Array(w).fill(0); for (const [, y] of st) rows[y]++;
      const rec = { w, m, q, nStones: st.length, rows, stones: st, via: 'window-SAT anchor=' + path.basename(anchor) + (vmir ? '+V' : '') + (hmir ? '+H' : '') + ' off=' + off + ' freeCols=' + JSON.stringify(freeCols), verify: vc };
      const wf = path.join(OD, 'witness_w' + w + 'x' + m + 'q' + q + '_' + tag + '.json');
      fs.writeFileSync(wf, JSON.stringify(rec));
      const py = spawnSync('python3', [SC + 'verify_witness.py', String(w), String(m), String(q)], { input: JSON.stringify(st), maxBuffer: 1 << 24 });
      summary.pyVerify = py.stdout ? py.stdout.toString().trim() : String(py.error);
      summary.saved = 'output/' + path.basename(wf);
    }
  }
  return summary;
}

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
fs.mkdirSync(OD, { recursive: true });
for (const j of jobs) {
  try { console.log(JSON.stringify(run(j))); } catch (e) { console.log(JSON.stringify({ tag: j.tag, error: String(e).slice(0, 300) })); }
}
