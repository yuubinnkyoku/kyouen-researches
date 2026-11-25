// diag89.js — diagnose w8q9 witness extension failures: which new cells are unblocked
// after appending empty columns, and which census curves pass through them with how many
// stones (a blocking curve needs exactly 8 = q-1). Usage: node diag89.js witness.json
// Deps: extend89.js next to this file (fastCensus calibrated w8 q9 m9..40).
'use strict';
const fs = require('fs');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const { analyze, census } = require(SC + 'extend89.js');
const W = 8, Q = 9;

const w0 = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const wi = w0.witness || w0;

function diag(m, stones, tag) {
  const r = analyze(m, stones);
  console.log(tag + ' m=' + m + ' why=' + r.why + ' unblocked=' + JSON.stringify(r.unblocked));
  if (r.why !== 'ok' && r.unblocked) {
    const { curves, through } = census(m);
    const occ = new Uint8Array(W * m);
    for (const [x, y] of stones) occ[y * m + x] = 1;
    for (const [ux, uy] of r.unblocked) {
      const i = uy * m + ux;
      const hist = {};
      for (const ci of through[i]) {
        let c = 0; for (const p of curves[ci].pts) if (occ[p]) c++;
        hist[c] = (hist[c] || 0) + 1;
      }
      console.log('  cell (' + ux + ',' + uy + '): curves through=' + through[i].length + ' stone-count hist=' + JSON.stringify(hist));
      const sevens = [];
      for (const ci of through[i]) {
        let c = 0; for (const p of curves[ci].pts) if (occ[p]) c++;
        if (c === Q - 2) sevens.push({ ci, pts: curves[ci].pts.map(p => [p % m, Math.floor(p / m)]), type: curves[ci].type });
      }
      console.log('  curves with 7 stones through cell: ' + sevens.length);
      for (const s7 of sevens.slice(0, 6)) {
        const empty = s7.pts.filter(p => !occ[p[1] * m + p[0]]);
        console.log('    ' + s7.type + ' ci=' + s7.ci + ' pts=' + JSON.stringify(s7.pts) + ' empty=' + JSON.stringify(empty));
      }
    }
  }
  return r;
}

const m0 = wi.m;
// right append (m0+1)
diag(m0 + 1, wi.stones, wi.m + ':R');
// mirror (left append)
diag(m0 + 1, wi.stones.map(([x, y]) => [m0 - 1 - x, y]), wi.m + ':L');
// two empty columns appended right (m0+2)
diag(m0 + 2, wi.stones, wi.m + ':RR');
