const { buildCurves, minimizeSA, verifyIndependent } = require('/home/user/sa/sa_machine.js');
const fs = require('fs');
const [w, m, q, budget, seed, T0, mrf, sK] = process.argv.slice(2).map(Number);
const ctx = buildCurves(w, m, q);
const full = w * (q - 1);
const r = minimizeSA(ctx, q, seed, budget, { fullCapacity: full, T0, maxRemoveFrac: mrf, sampleK: sK });
const witness = [...r.best].map(p => [p % m, Math.floor(p / m)]);
const out = { ts: new Date().toISOString(), case: `${w}x${m}q${q}`, w, m, q, full, min: r.bestN,
  nC: ctx.nC, nCirc: ctx.nCirc, nLines: ctx.nLines, iters: r.iters, ms: r.ms, seed,
  opts: { T0, mrf, sK } };
if (r.bestN < full) { out.witness = witness; out.independent = verifyIndependent(w, m, q, witness); }
fs.appendFileSync('/home/user/sa/results.jsonl', JSON.stringify(out) + '\n');
console.log(JSON.stringify({ min: r.bestN, full, seed, opts: out.opts, found: r.bestN < full }));
