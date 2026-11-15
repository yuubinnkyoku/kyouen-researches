// vacuous89.js — check whether a (8,9) window anchor's frozen prefix is already
// contradictory at m=29 (vacuous UNSAT: frozen safety violation or dead frozen cell)
// or genuinely open (real conditional window result). Usage: node vacuous89.js jobs.json
// Deps: extend89.js next to this file (fastCensus calibrated w8 q9 m9..40).
'use strict';
const fs = require('fs');
const path = require('path');
const SC = (process.env.SEVEN_SCRIPTS || __dirname).replace(/\/?$/, '/');
const ROOT = path.join(__dirname, '..');
const resolve = (p) => (p.startsWith('/') ? p : path.join(ROOT, p));
const { census } = require(SC + 'extend89.js');
const M = 29, W = 8, Q = 9;

function check(anchorFile, off, freezeLimit) {
  const raw = JSON.parse(fs.readFileSync(resolve(anchorFile), 'utf8'));
  const w = raw.witness || raw;
  const occ = new Set(w.stones.map(([x, y]) => y * 1000 + x));
  const frozen = new Set(), frozenStones = new Set();
  for (let bx = 0; bx <= freezeLimit && bx < M; bx++) for (let y = 0; y < W; y++) {
    const ax = bx - off; if (ax < 0 || ax >= w.m) continue;
    frozen.add(y * M + bx);
    if (occ.has(y * 1000 + ax)) frozenStones.add(y * M + bx);
  }
  const { curves, through } = census(M);
  const unsafe = [];
  const reach = [];
  for (let ci = 0; ci < curves.length; ci++) {
    let f = 0, free = 0;
    for (const p of curves[ci].pts) { if (frozenStones.has(p)) f++; if (!frozen.has(p)) free++; }
    if (f >= Q) unsafe.push({ ci, f });
    reach[ci] = f + free;
  }
  const dead = [];
  for (const i of frozen) {
    if (frozenStones.has(i)) continue;
    let best = 0, bci = -1;
    for (const ci of through[i]) if (reach[ci] > best) { best = reach[ci]; bci = ci; }
    if (best < Q - 1) dead.push({ cell: [i % M, Math.floor(i / M)], best, bci });
  }
  return { off, freezeLimit, frozenStones: frozenStones.size, unsafeCircles: unsafe.length, deadFrozenCells: dead.length, deadSample: dead.slice(0, 6) };
}

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const j of jobs) console.log(JSON.stringify(check(j.anchor, j.off, j.freezeLimit)));
