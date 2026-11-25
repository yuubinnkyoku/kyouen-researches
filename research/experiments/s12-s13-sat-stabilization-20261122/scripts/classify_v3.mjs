// classify_v3.mjs — classify the v2.1 (v3-run) SAT witnesses against the
// published anchors AND the v2-draft-era witnesses (same canon as classify_sat_witnesses.mjs).
import { readFileSync } from 'node:fs';

function canonKey(cells) {
  let best = null;
  for (const f of [
    (x, y) => [x, y], (x, y) => [-x, y], (x, y) => [x, -y], (x, y) => [-x, -y],
    (x, y) => [y, x], (x, y) => [-y, x], (x, y) => [y, -x], (x, y) => [-y, -x],
  ]) {
    const img = cells.map(([x, y]) => f(x, y));
    const mnx = Math.min(...img.map((c) => c[0])), mny = Math.min(...img.map((c) => c[1]));
    const norm = img.map(([x, y]) => [x - mnx, y - mny]).sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    const key = JSON.stringify(norm);
    if (best === null || key < best) best = key;
  }
  return best;
}
const cellsOf = (n, ids) => ids.map((v) => [v % n, (v / n) | 0]);
const anchors = {
  'K0031-n7': { n: 7, cells: cellsOf(7, [1, 9, 22, 23, 27, 44, 45]) },
  'K0038-n10': { n: 10, cells: [[1,2],[7,2],[1,3],[5,3],[6,3],[6,4],[5,6],[1,8],[9,2],[8,4]] },
  'K0034-another-n10': { n: 10, cells: cellsOf(10, [13, 50, 56, 59, 63, 68, 77, 83, 85, 98]) },
  'K0320-n12': { n: 12, cells: [[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10],[5,11]] },
  'K0320-n13': { n: 13, cells: [[7,0],[3,2],[2,3],[9,3],[10,3],[2,4],[6,4],[11,4],[6,6],[1,10],[2,10],[7,12]] },
};

const sets = {};
for (const f of ['wit_n7k7','wit_n8k8','wit_n9k9','wit_n10k10','wit_n10k10_sh7',
                 'v3wit_n7k7','v3wit_n8k8','v3wit_n9k9','v3wit_n10k10','v3wit_n10k10_sh7']) {
  try {
    const w = JSON.parse(readFileSync(new URL('../out/' + f + '.json', import.meta.url), 'utf8'));
    sets[f] = { n: w.n, key: canonKey(w.stones.map((p) => [p[0], p[1]])) };
  } catch { /* skip if not produced yet */ }
}
const akeys = {};
for (const [k, v] of Object.entries(anchors)) akeys[k] = { n: v.n, key: canonKey(v.cells) };

const out = { anchors: {}, witnesses: {} };
for (const [k, v] of Object.entries(akeys)) out.anchors[k] = v.key;
for (const [f, s] of Object.entries(sets)) {
  const comps = {};
  for (const [k, v] of Object.entries(akeys)) if (v.n === s.n) comps[k] = (v.key === s.key);
  for (const [g, t] of Object.entries(sets)) if (g !== f && t.n === s.n) comps['set:' + g] = (t.key === s.key);
  out.witnesses[f] = { n: s.n, canonical_key: s.key, congruent_with: comps };
}
console.log(JSON.stringify(out, null, 1));
