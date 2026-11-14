'use strict';
const fs = require('fs');
const { buildCurves, minimizeSA, verifyIndependent } = require('/home/user/ky/sa_machine.js');
const OUT = '/home/user/ky/sa_frontier2.jsonl';
// cases: [w,m,q,label,...config cycles] — each entry run until budget
const cases = JSON.parse(process.argv[2]);
const totalMs = Number(process.argv[3]);
const seedBase = Number(process.argv[4] || 1);
const t0 = Date.now();
let ci = 0;
for (const c of cases) {
  const { w, m, q } = c;
  const per = c.perMs || 30000;
  while (Date.now() - t0 < totalMs - per) {
    const seed = seedBase + ci;
    const opts = { fullCapacity: w * (q - 1), T0: 1.0 + (ci % 5) * 1.2, maxRemoveFrac: [0.30, 0.15, 0.45, 0.08, 0.6][ci % 5], sampleK: [24, 40, 12, 60, 8][ci % 5] };
    const ctx = buildCurves(w, m, q);
    const r = minimizeSA(ctx, q, seed, per, opts);
    const rec = { w, m, q, full: w * (q - 1), min: r.bestN, iters: r.iters, ms: r.ms, seed, opts: { T0: opts.T0, maxRemoveFrac: opts.maxRemoveFrac, sampleK: opts.sampleK } };
    if (r.bestN < w * (q - 1)) {
      rec.witness = [...r.best].map(p => [p % m, Math.floor(p / m)]);
      rec.independent = verifyIndependent(w, m, q, rec.witness);
    }
    fs.appendFileSync(OUT, JSON.stringify(rec) + '\n');
    console.log(JSON.stringify({ w, m, q, min: rec.min, full: rec.full, iters: r.iters, seed, found: !!rec.witness, ind: rec.independent ? (rec.independent.safe && rec.independent.maximal) : null }));
    ci++;
    if (rec.witness && rec.independent && rec.independent.safe && rec.independent.maximal) {
      // witness found for this case; move on
      break;
    }
    if (Date.now() - t0 > totalMs) break;
  }
  if (Date.now() - t0 > totalMs - 5000) break;
}
console.log('DONE cases=' + ci + ' ms=' + (Date.now() - t0));
