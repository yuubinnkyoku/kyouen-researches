// classify_sat_witnesses.mjs — canonical-form classification (lattice isometry
// D4 x integer translation, same canon logic as research/experiments/s12-s13-upper-witness-20261121/scripts/classify.mjs (K1206)
// of the five SAT-reproduced witnesses against published anchors:
//   K0031 n=7 witness (research/knowledge/items/K0031), K0038 n=10 witness (witnesses.mjs),
//   the k=10 "another ten-stone witness" of K0034 (cells 13 50 56 59 63 68 77 83 85 98),
//   K0320 n=12/n=13 witnesses (classify.mjs anchors).
// Output: canonical keys + pairwise equality vs anchors.
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
  const c = JSON.parse(best);
  const span = `${Math.max(...c.map((p) => p[0])) + 1}x${Math.max(...c.map((p) => p[1])) + 1}`;
  return { canonical: best, span };
}

const cellsOf = (n, ids) => ids.map((v) => [v % n, (v / n) | 0]);
const anchors = {
  'K0031-n7': cellsOf(7, [1, 9, 22, 23, 27, 44, 45]),
  'K0038-n10': [[1,2],[7,2],[1,3],[5,3],[6,3],[6,4],[5,6],[1,8],[9,2],[8,4]],
  'K0034-another-n10': cellsOf(10, [13, 50, 56, 59, 63, 68, 77, 83, 85, 98]),
  'K0320-n12': [[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10],[5,11]],
  'K0320-n13': [[7,0],[3,2],[2,3],[9,3],[10,3],[2,4],[6,4],[11,4],[6,6],[1,10],[2,10],[7,12]],
};

const found = {};
for (const f of ['wit_n7k7', 'wit_n8k8', 'wit_n9k9', 'wit_n10k10', 'wit_n10k10_sh7']) {
  const w = JSON.parse(readFileSync(new URL('../out/' + f + '.json', import.meta.url), 'utf8'));
  found['SAT-' + f] = { n: w.n, cells: w.stones };
}

const keys = {};
for (const [k, v] of Object.entries(anchors)) keys[k] = canonKey(v);
for (const [k, v] of Object.entries(found)) keys[k] = canonKey(v.cells);

const compare = {};
for (const fk of Object.keys(found)) {
  const n = found[fk].n;
  const same = [];
  for (const ak of Object.keys(anchors)) {
    const anchorN = parseInt((ak.match(/n(\d+)/) || [])[1] ?? '0', 10);
    if (anchorN === n) same.push({ anchor: ak, congruent: keys[fk].canonical === keys[ak].canonical });
  }
  compare[fk] = { n, anchors_same_board: same, ...keys[fk] };
}
console.log(JSON.stringify({ canonical_keys: { ...Object.fromEntries(Object.entries(keys).map(([k, v]) => [k, { span: v.span }])), raw: keys }, comparison: compare }, null, 1));
