// Combine two cone dp_result.json files into the full spectrum via the two-cone identity.
'use strict';
const fs = require('fs');
const [,, fileA, fileB, qArg, sArg] = process.argv;
const q = parseInt(qArg), s = parseInt(sArg);
const n = q * q + q + 1;
const A = JSON.parse(fs.readFileSync(fileA, 'utf8'));
const B = JSON.parse(fs.readFileSync(fileB, 'utf8'));
if (A.cone !== 'nc' || B.cone !== 'c') throw new Error('cone roles');
const nlines = q * q + q + 1;
const binom = (nn, k) => { if (k < 0 || k > nn) return 0; if (k === 0) return 1; let r = 1; for (let i = 1; i <= k; i++) r = r * (nn - k + i) / i; return Math.round(r); };
const N3c = nlines * binom(q + 1, 3);
const N3nc = binom(n, 3) - N3c;
const maxm = Math.max(A.maxm, B.maxm);
const tables = {}; const maximalCounts = {}; let total = 0, maxG = 0;
for (let m = 3; m <= maxm; m++) {
  const div = binom(m, 3);
  const row = {};
  const ca = A.counts[m] || []; const cb = B.counts[m] || [];
  for (let g = 0; g < 64; g++) {
    const num = N3nc * (ca[g] || 0) + N3c * (cb[g] || 0);
    if (num === 0) continue;
    if (num % div !== 0) { console.error('FATAL divisibility m=' + m + ' g=' + g); process.exit(4); }
    row[g] = num / div; total += num / div; if (g > maxG) maxG = g;
  }
  tables[m] = row;
  const mm = N3nc * (A.maximal[m] || 0) + N3c * (B.maximal[m] || 0);
  if (mm !== 0) { if (mm % div !== 0) { console.error('FATAL maximal div'); process.exit(5); } maximalCounts[m] = mm / div; }
}
const v3nc = A.gF, v3c = B.gF;
// g of pair {0,1}: children 3-sets on/off the line through 0,1
// on-line children have grundy v3c, off-line v3nc -> mex over {v3c, v3nc}
const childv = {}; childv[v3c] = 1; childv[v3nc] = 1;
let v2 = 0; while (childv[v2]) v2++;
const v1 = v2 === 0 ? 1 : 0;
const v0 = v1 === 0 ? 1 : 0;
const a3 = binom(n, 3);
const a4 = binom(n, 4) - nlines * binom(q + 1, 4);
const a5 = binom(n, 5) - nlines * (binom(q + 1, 4) * (n - (q + 1)) + binom(q + 1, 5));
const out = {
  board: 'PG(2,' + q + ')', points: n, lines: nlines, s,
  cone_noncoll_nodes: A.nodes, cone_coll_nodes: B.nodes,
  layers_noncoll: A.sizes, layers_coll: B.sizes,
  max_size: maxm, grundy_tables: tables, maximal_counts: maximalCounts,
  g_empty: v0, g_single: v1, g_pair: v2, g_triple_noncoll: v3nc, g_triple_coll: v3c,
  raw_cone_noncoll: A.counts, raw_cone_coll: B.counts,
  raw_maximal_noncoll: A.maximal, raw_maximal_coll: B.maximal,
  N3nc, N3c, anchor_totals: { m3: a3, m4: a4, m5: a5 },
  total_positions: total + binom(n, 2) + n + 1,
  max_grundy: maxG,
};
console.log(JSON.stringify(out));
