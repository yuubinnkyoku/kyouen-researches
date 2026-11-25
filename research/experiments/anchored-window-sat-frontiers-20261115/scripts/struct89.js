// struct89.js — structural analysis of known w8q9 witnesses: stone-count histogram over
// all census curves, inventory of blocking (exact 8-stone) circles, and how the
// deficient row's empty cells are covered by them. Usage: node struct89.js w.json...
// Deps: sat.js / genfast.js next to this file (fastCensus calibrated w8 q9 m9..40).
'use strict';
const fs = require('fs');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const { census, analyze } = require(SC + 'extend89.js');
const W = 8, Q = 9;

for (const f of process.argv.slice(2)) {
  const w = JSON.parse(fs.readFileSync(f, 'utf8'));
  const wi = w.witness || w;
  const m = wi.m;
  const { curves, through } = census(m);
  const occ = new Uint8Array(W * m);
  for (const [x, y] of wi.stones) occ[y * m + x] = 1;
  const h = {};
  const blocking = [];
  for (let ci = 0; ci < curves.length; ci++) {
    let c = 0; for (const p of curves[ci].pts) if (occ[p]) c++;
    h[c] = (h[c] || 0) + 1;
    if (c === Q - 1) blocking.push(ci);
  }
  const defRow = wi.rows.indexOf(Math.min(...wi.rows));
  const cover = [];
  for (let x = 0; x < m; x++) {
    const i = defRow * m + x;
    if (occ[i]) continue;
    const bs = through[i].filter(ci => blocking.includes(ci));
    cover.push({ cell: [x, defRow], blockers: bs.length });
  }
  const bhist = {}; for (const c of cover) bhist[c.blockers] = (bhist[c.blockers] || 0) + 1;
  const blkThrough = curves.reduce((t, cu, ci) => t + (cu.pts.some(p => Math.floor(p / m) === defRow) && blocking.includes(ci) ? 1 : 0), 0);
  console.log(f + ' m=' + m + ' defRow=' + defRow + ' stone-hist=' + JSON.stringify(h) + ' blockingCircles=' + blocking.length + ' defRowEmpty=' + cover.length + ' blocker-count-hist=' + JSON.stringify(bhist) + ' blkCirclesThroughDefRow=' + blkThrough);
}
