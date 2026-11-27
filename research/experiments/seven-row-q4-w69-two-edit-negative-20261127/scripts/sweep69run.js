// Same procedure as published sweep69.js: fresh 2-for-2 at width 69 over all bases, resume-safe.
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const RES = 'output/w69/results.jsonl';
const main = () => {
  const count = Number(process.argv[2] || 10);
  const bases = JSON.parse(fs.readFileSync('output/w69/bases.json', 'utf8'));
  const done = new Set();
  if (fs.existsSync(RES)) for (const line of fs.readFileSync(RES, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { done.add(JSON.parse(line).sig); } catch (e) {}
  }
  fs.appendFileSync(RES, '');
  let t0 = Date.now(); let n = 0; let witnessHits = 0;
  for (let i = 0; i < bases.length && n < count; i++) {
    const b = bases[i];
    const sig = JSON.stringify(b.stones.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
    if (done.has(sig)) continue;
    const r = runCase(new Board(69), b.stones, { holes: false, maxWitnesses: 64 });
    witnessHits += r.safe_maximal_row_deficient;
    fs.appendFileSync(RES, JSON.stringify({ idx: i, tag: b.tag, sig, rcc: r.row_capacity_candidates, safe: r.safe_candidates, shape_errors: r.shape_errors, maximal: r.safe_maximal_row_deficient, ms: Date.now() - t0, witnesses: r.witnesses }) + '\n');
    done.add(sig); n++; t0 = Date.now();
  }
  console.log(JSON.stringify({ processed: n, witnessHits, totalDone: done.size, ofBases: bases.length }));
};
main();
