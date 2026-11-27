// Chunked resume-safe driver for the seven-row q=4 two-edit sweep (w69 kit
// sweep69run/sweep69hrun procedure, generalized width param). Deterministic
// enumeration; per-base records appended with wall-time bookkeeping only.
// Usage: node sweep_driver.js <width> <fresh|holes> <outfile> <wallBudgetSec>
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const main = () => {
  const W = Number(process.argv[2]);
  const mode = process.argv[3];
  const RES = process.argv[4];
  const budget = Number(process.argv[5] || 180) * 1000;
  const holes = mode === 'holes';
  const bases = JSON.parse(fs.readFileSync('output/w70/bases.json', 'utf8'));
  const done = new Set();
  if (fs.existsSync(RES)) for (const line of fs.readFileSync(RES, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { done.add(JSON.parse(line).sig); } catch (e) {}
  }
  fs.appendFileSync(RES, '');
  const tStart = Date.now();
  let t0 = tStart; let n = 0; let hits = 0;
  for (let i = 0; i < bases.length; i++) {
    if (n > 0 && Date.now() - tStart > budget) break;
    const b = bases[i];
    const sig = JSON.stringify(b.stones.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
    if (done.has(sig)) continue;
    const r = runCase(new Board(W), b.stones, { holes, maxWitnesses: 64 });
    hits += r.safe_maximal_row_deficient;
    fs.appendFileSync(RES, JSON.stringify({ idx: i, tag: b.tag, sig, rcc: r.row_capacity_candidates, safe: r.safe_candidates, shape_errors: r.shape_errors, maximal: r.safe_maximal_row_deficient, ms: Date.now() - t0, witnesses: r.witnesses }) + '\n');
    done.add(sig); n++; t0 = Date.now();
  }
  console.log(JSON.stringify({ width: W, mode, processed: n, witnessHits: hits, totalDone: done.size, ofBases: bases.length }));
};
main();
