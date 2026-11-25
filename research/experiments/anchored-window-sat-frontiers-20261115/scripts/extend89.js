// extend89.js — witness extension/surgery engine for the w=8 q=9 band (M_{8,9} frontier).
// Strategy: a def-mode witness has all rows <= 8 stones (safety) and some row <= 7.
// Appending an EMPTY column keeps safety (a circle with >=9 stoned old points would
// already have been forbidden on the narrower board) and keeps old cells blocked;
// the only cells that can fail are those of the deficient row(s) in the new column,
// which need a blocking circle (exact 8 stones) through them.
// If an extension is not maximal, try 1-stone surgery moves.
// Deps: sat.js / genfast.js next to this file (fastCensus calibrated w8 q9 m9..40).
'use strict';
const fs = require('fs');
const path = require('path');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const OD = process.env.OUTDIR || path.join(__dirname, '..', 'output');
const S = require(SC + 'sat.js');
require(SC + 'genfast.js'); // patches S.buildCensus -> fastCensus (calibrated w8 q9 m9..40)

const W = 8, Q = 9;

// census cache per m: { curves: [{pts:[idx]}], through: [cellIdx -> [curveId]] }
const cens = {};
function census(m) {
  if (cens[m]) return cens[m];
  const { P, curves } = S.buildCensus(W, m, Q);
  const through = Array.from({ length: W * m }, () => []);
  curves.forEach((cu, ci) => { for (const p of cu.pts) through[p].push(ci); });
  return (cens[m] = { P, curves, through });
}

// full analysis of a stone set on 8 x m: safety, blocking, deficiency
function analyze(m, stones) {
  const { P, curves, through } = census(m);
  const occ = new Uint8Array(W * m);
  for (const [x, y] of stones) occ[y * m + x] = 1;
  // safety: no curve with >= Q stones
  const curveCnt = new Int32Array(curves.length);
  for (let ci = 0; ci < curves.length; ci++) {
    let c = 0;
    for (const p of curves[ci].pts) if (occ[p]) c++;
    curveCnt[ci] = c;
    if (c >= Q) return { ok: false, why: 'unsafe', curve: ci, cnt: c };
  }
  // blocking: every empty cell on a curve with >= Q-1 stones
  const unblocked = [];
  for (let i = 0; i < W * m; i++) {
    if (occ[i]) continue;
    let blocked = false;
    for (const ci of through[i]) if (curveCnt[ci] >= Q - 1) { blocked = true; break; }
    if (!blocked) unblocked.push([i % m, Math.floor(i / m)]);
  }
  const rows = Array(W).fill(0);
  for (const [x, y] of stones) rows[y]++;
  const minRow = Math.min(...rows);
  return { ok: unblocked.length === 0 && minRow <= Q - 2, why: unblocked.length === 0 ? (minRow <= Q - 2 ? 'ok' : 'not-deficient') : 'unblocked', unblocked, rows, minRow, curveCnt };
}

const mirror = (stones, m) => stones.map(([x, y]) => [m - 1 - x, y]);

function tryAll(witness, label, log) {
  // returns list of found witnesses: [{m, stones, via}]
  const found = [];
  const bases = [];
  const m0 = witness.m;
  bases.push({ stones: witness.stones, tag: label + ':R' });
  bases.push({ stones: mirror(witness.stones, m0), tag: label + ':L' });
  for (const b of bases) {
    const res = analyze(m0 + 1, b.stones);
    if (res.ok) { found.push({ m: m0 + 1, stones: b.stones, via: 'empty-col ' + b.tag }); continue; }
    if (res.why === 'unsafe') { log('  ' + b.tag + ' unsafe?! ' + JSON.stringify(res.curve)); continue; }
    if (res.why === 'not-deficient') { log('  ' + b.tag + ' not deficient?!'); continue; }
    // surgery: 1-move
    const res1 = surgery1(m0 + 1, b.stones, res.unblocked, log, b.tag);
    if (res1) found.push({ m: m0 + 1, stones: res1.stones, via: 'surgery1 ' + b.tag + ' ' + res1.desc });
  }
  return found;
}

function surgery1(m, stones, unblocked, log, tag) {
  // try moving one stone to/around to fix unblocked cells; verify fully each time
  for (const u of unblocked) {
    for (let si = 0; si < stones.length; si++) {
      const st2 = stones.slice();
      const s = st2[si];
      if (s[0] === u[0] && s[1] === u[1]) continue;
      st2[si] = [u[0], u[1]];
      const r = analyze(m, st2);
      if (r.ok) { log('  surgery1 hit ' + tag + ': move ' + JSON.stringify(s) + ' -> ' + JSON.stringify(u)); return { stones: st2, desc: 'move ' + s + '->' + u }; }
    }
  }
  return null;
}

module.exports = { census, analyze, mirror, tryAll };

if (require.main === module) {
  const files = process.argv.slice(2);
  const log = (s) => console.error(s);
  const all = [];
  for (const f of files) {
    const w = JSON.parse(fs.readFileSync(f, 'utf8'));
    console.error('== ' + f + ' (m=' + w.m + ', rows=' + JSON.stringify(w.rows) + ')');
    const found = tryAll(w, f.replace(/.*\//, '').replace(/\.witness\.json$/, ''), log);
    for (const g of found) { console.error('  FOUND m=' + g.m + ' via ' + g.via); all.push(g); }
  }
  if (all.length) {
    const uniq = [];
    const seen = new Set();
    for (const g of all) {
      const key = g.m + '|' + g.stones.slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]).map(p => p.join(',')).join(';');
      if (seen.has(key)) continue;
      seen.add(key); uniq.push(g);
    }
    for (let i = 0; i < uniq.length; i++) {
      const g = uniq[i];
      const out = { w: W, m: g.m, q: Q, nStones: g.stones.length, rows: analyze(g.m, g.stones).rows, stones: g.stones.slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]), via: g.via };
      const wf = path.join(OD, 'witness-8x' + g.m + 'q9-ext.json');
      fs.writeFileSync(wf, JSON.stringify(out));
      console.error('saved ' + wf);
    }
    console.log(JSON.stringify({ found: uniq.map(g => ({ m: g.m, via: g.via, n: g.stones.length })) }));
  } else {
    console.log(JSON.stringify({ found: [] }));
  }
}
