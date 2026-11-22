// ext_nets.mjs — exhaustive extended-neighborhood scan around a base configuration,
// WITH sit-at adds (the gap found in hunt.mjs localNets/doubleSwapComplete: their
// candidate sets exclude direct stone placement on an uncovered cell, c!==p).
//
// For a seed config S (|S| stones, maximality NOT required) on the n x n board:
//   remove every m-subset of S, then add `a` stones where the add candidates are
//   ALL cells that are not stones of the reduced configuration (full0/full1/full2
//   = add 0/1/2 stones). This includes sit-at adds (candidates are not filtered by
//   the c!==p rule), so the scan is complete for its (remove m, add a) neighborhood.
//
// A checked config is recorded in `found` iff viol==0 && uncovered==0 (safe and
// maximal), tagged with isSeed (identical to the seed stone set) and smaller
// (strictly fewer stones than the seed). bestScore tracks min(viol*1000+uncovered)
// over ALL checked configs (State.score from hunt.mjs), so "no config better than
// the seed" is directly checkable.
//
// Usage:  node ext_nets.mjs <n> <m> <full0|full1|full2> <out.jsonl> [cells.json]
//   cells.json: {"source": "...", "cells": [[x,y], ...]}  (or a bare array)
//   If omitted, uses WITNESSES entry for n from witnesses.mjs.
// Resume: <out>.cp holds the last completed removal index; rerun with the same
// args to resume. Output is JSONL: header / per-removal / done lines (deterministic).
// All arithmetic and control flow are deterministic; reruns are byte-identical.

import { Board, State } from './hunt.mjs';
import { WITNESSES } from './witnesses.mjs';
import * as fs from 'node:fs';

const [nArg, mArg, modeArg, outArg, cellsArg] = process.argv.slice(2);
const n = parseInt(nArg, 10);
const m = parseInt(mArg, 10);
const a = { full0: 0, full1: 1, full2: 2 }[modeArg];
if (!Number.isInteger(n) || !Number.isInteger(m) || a === undefined || !outArg) {
  console.error('usage: node ext_nets.mjs <n> <m> <full0|full1|full2> <out.jsonl> [cells.json]');
  process.exit(2);
}

let seedSpec;
if (cellsArg) {
  const raw = JSON.parse(fs.readFileSync(cellsArg, 'utf8'));
  seedSpec = Array.isArray(raw) ? { source: cellsArg, cells: raw } : { source: raw.source ?? cellsArg, cells: raw.cells };
} else {
  const w = WITNESSES.find((x) => x.n === n);
  if (!w) throw new Error(`no built-in witness for n=${n}; pass cells.json`);
  seedSpec = { source: `WITNESSES:${w.src}`, cells: w.coords };
}

const bd = new Board(n);
const st = new State(bd);
const seedCells = seedSpec.cells.map(([x, y]) => x + n * y);
for (const c of seedCells) st.add(c);
const seedStones = st.size();
const seedScore = st.score();
const seedViol = st.viol;
const seedUncovered = st.uncovered;
if (st.viol !== 0) throw new Error('seed config is not safe');

const cpFile = outArg + '.cp';
let startIdx = 0;
if (fs.existsSync(cpFile)) {
  startIdx = parseInt(fs.readFileSync(cpFile, 'utf8').trim(), 10) + 1;
}
const out = fs.createWriteStream(outArg, { flags: startIdx > 0 ? 'a' : 'w' });
const line = (o) => out.write(JSON.stringify(o) + '\n');
const coordsOf = (cells) => cells.slice().sort((p, q) => p - q).map((p) => [p % n, (p / n) | 0]);

// removal index -> combination of positions in seedCells (lexicographic)
const k = seedCells.length;
const combos = [];
{
  const idx = [];
  const rec = (s) => {
    if (idx.length === m) { combos.push(idx.slice()); return; }
    for (let i = s; i < k; i++) { idx.push(i); rec(i + 1); idx.pop(); }
  };
  if (m > 0) rec(0); else combos.push([]);
}

if (startIdx === 0) line({
  type: 'header', n, m, a, source: seedSpec.source,
  seedCells: coordsOf(seedCells), seedStones, seedScore, seedViol, seedUncovered,
  combos: combos.length, startIdx, argv: process.argv.slice(2).join(' '),
});

const t0 = Date.now();
let totalChecked = 0;
const found = [];
let bestScore = Infinity, bestConfig = null;
let perRemovals = 0;

function checkConfig() {
  totalChecked++;
  const sc = st.score();
  if (sc < bestScore) { bestScore = sc; bestConfig = coordsOf(st.stones); }
  if (st.viol === 0 && st.uncovered === 0) {
    const cs = st.stones.slice().sort((p, q) => p - q);
    const ss = seedCells.slice().sort((p, q) => p - q);
    const isSeed = cs.length === ss.length && cs.every((p, i) => p === ss[i]);
    found.push({
      config: coordsOf(st.stones), stones: st.size(), score: sc,
      smaller: st.size() < seedStones, isSeed,
    });
  }
}

for (let ci = startIdx; ci < combos.length; ci++) {
  const rem = combos[ci].map((i) => seedCells[i]);
  const tr = Date.now();
  for (const c of rem) st.remove(c);
  let checked0 = totalChecked;
  let found0 = found.length;
  if (a === 0) {
    checkConfig();
  } else if (a === 1) {
    for (let c = 0; c < bd.N; c++) {
      if (!st.inS[c]) { st.add(c); checkConfig(); st.remove(c); }
    }
  } else if (a === 2) {
    for (let c1 = 0; c1 < bd.N; c1++) {
      if (st.inS[c1]) continue;
      st.add(c1);
      for (let c2 = c1 + 1; c2 < bd.N; c2++) {
        if (st.inS[c2]) continue;
        st.add(c2); checkConfig(); st.remove(c2);
      }
      st.remove(c1);
    }
  } else throw new Error('a>2 unsupported');
  const row = {
    type: 'removal', idx: ci, removed: coordsOf(rem),
    checked: totalChecked - checked0, foundHere: found.length - found0,
    ms: Date.now() - tr,
  };
  line(row);
  perRemovals++;
  for (const c of rem.slice().reverse()) st.add(c);
  fs.writeFileSync(cpFile, String(ci));
}

line({
  type: 'done', totalChecked, removals: perRemovals,
  found, nonTrivial: found.filter((f) => !f.isSeed).length,
  smallerWitnesses: found.filter((f) => !f.isSeed && f.smaller).length,
  bestScore, bestConfig, ms: Date.now() - t0,
});
out.end();
fs.rmSync(cpFile, { force: true });
