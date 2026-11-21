// Width-69 HOLES-mode 2-for-2 sweep over all published bases (resume-safe).
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const RES = 'output/w69/results_holes.jsonl';
const main = () => {
  const start = Number(process.argv[2] || 0);
  const count = Number(process.argv[3] || 12);
  const bases = JSON.parse(fs.readFileSync('output/w69/bases.json', 'utf8'));
  const done = new Set();
  if (fs.existsSync(RES)) for (const line of fs.readFileSync(RES, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { done.add(JSON.parse(line).sig); } catch (e) {}
  }
  fs.appendFileSync(RES, '');
  let t0 = Date.now(); let n = 0; let hits = 0;
  for (let i = start; i < bases.length && n < count; i++) {
    const b = bases[i];
    const sig = JSON.stringify(b.stones.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
    if (done.has(sig)) continue;
    const r = runCase(new Board(69), b.stones, { holes: true, maxWitnesses: 64 });
    hits += r.safe_maximal_row_deficient;
    fs.appendFileSync(RES, JSON.stringify({ idx: i, tag: b.tag, sig, rcc: r.row_capacity_candidates, safe: r.safe_candidates, shape_errors: r.shape_errors, maximal: r.safe_maximal_row_deficient, ms: Date.now() - t0, witnesses: r.witnesses }) + '\n');
    done.add(sig); n++; t0 = Date.now();
  }
  console.log(JSON.stringify({ processed: n, witnessHits: hits, totalDone: done.size, ofBases: bases.length }));
};
main();
