// ext_constructive.js — pure column-append/shift constructive extension of a
// deficient-maximal witness base (no solver): board width m' = m_base + dm,
// witness' = base stones shifted right by off (0..dm), verified by sat.js
// verifyConfig (census-free). Mirrors the four-six-row lane 2026-11-14
// constructive-extension records (off=0/1 from m=32 base etc.).
// Usage: node ext_constructive.js W Q BASE.json M_TARGET   (BASE.json = witness json with .stones)
// Prints the first verified {m, off, stones} plus all verified offsets as JSONL on stdout.
'use strict';
const fs = require('fs');
const path = require('path');
const S = require(path.join(__dirname, 'sat.js'));
const [w, q] = [Number(process.argv[2]), Number(process.argv[3])];
const baseFile = process.argv[4];
const mT = Number(process.argv[5]);
const base = JSON.parse(fs.readFileSync(baseFile, 'utf8'));
const stones = (base.witness ?? base).stones ?? base.stones;
const mB = Math.max(...stones.map(s => s[0])) + 1;
const results = [];
for (let off = 0; off <= mT - mB; off++) {
  const shifted = stones.map(([x, y]) => [x + off, y]);
  if (Math.max(...shifted.map(s => s[0])) >= mT) continue;
  const v = S.verifyConfig(w, mT, q, shifted);
  if (v && v.ok) results.push({ m: mT, off, stones: shifted, rows: v.rows, size: v.size });
}
console.log(JSON.stringify({ w, q, mBase: mB, mTarget: mT, verified: results.length, results }));
