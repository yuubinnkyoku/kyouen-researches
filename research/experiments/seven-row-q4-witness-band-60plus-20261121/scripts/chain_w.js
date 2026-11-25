// One chain step: width W fresh 2-for-2 from the given frontier (witnesses of W-1).
// Usage: node chain_w.js W INPUT_JSON CAP  (INPUT_JSON: array of stone sets or {kept_stones:[...]})
'use strict';
const fs = require('fs');
const { Board, runCase } = require('./enum_two.js');
const W = Number(process.argv[2]);
const CAP = Number(process.argv[4] || 10);
const sig = b => JSON.stringify(b.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]));
let frontier;
if (W === 61) { const pool = JSON.parse(fs.readFileSync('/home/user/work/pool/chain_pool.json', 'utf8')); frontier = ['w60_a', 'w60_b', 'w60_c', 'w60_d'].map(k => pool[k]); }
else { const raw = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')); frontier = Array.isArray(raw) ? raw : raw.kept_stones; }
const t0 = Date.now(); const stats = []; const next = []; const seen = new Set();
for (const base of frontier) {
  const r = runCase(new Board(W), base, { holes: false, maxWitnesses: 64 });
  stats.push({ base: sig(base), rcc: r.row_capacity_candidates, safe: r.safe_candidates, maximal: r.safe_maximal_row_deficient, ms: Date.now() - t0 });
  for (const w of r.witnesses) { const s = sig(w); if (!seen.has(s)) { seen.add(s); next.push(JSON.parse(s).map(p => [p[0], p[1]])); } }
}
next.sort((a, b) => Math.max(...b.map(p => p[0])) - Math.max(...a.map(p => p[0])));
const kept = next.slice(0, CAP);
fs.writeFileSync(`output/chain/frontier_${W}.json`, JSON.stringify({ width: W, input_bases: frontier.length, found_new: next.length, kept: kept.length, ms: Date.now() - t0, kept_stones: kept }, null, 1));
fs.writeFileSync(`output/chain/stats_${W}.json`, JSON.stringify(stats, null, 1));
fs.writeFileSync(`output/chain/witness_${W}.json`, JSON.stringify({ width: W, count: next.length, witnesses: next }, null, 1));
console.log(JSON.stringify({ width: W, input_bases: frontier.length, found_new: next.length, kept: kept.length, ms: Date.now() - t0 }));
