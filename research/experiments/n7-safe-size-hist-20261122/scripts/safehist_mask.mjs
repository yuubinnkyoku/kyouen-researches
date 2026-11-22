// safehist_mask.mjs — THIRD independent implementation of the safe-subset size
// histogram Z_n(λ) for the n x n standard kyouen board (q = 4).
//
// Different algorithm from safehist_n7.mjs: NO incremental cov/stInF bookkeeping.
// The current stone set is carried as an explicit bitmask (two 32-bit words),
// and a cell c is placeable iff NO forbidden triple (the other 3 cells of some
// forbidden quartet containing c) is fully contained in the current mask.
// The DFS tree is identical in shape and visits the same nodes; the reachability
// test at every node is computed from scratch by an independent mechanism, so an
// implementation error in either system yields different histograms.
//
// Geometry source: same canonical quartets text (forbidgen det-brute-force
// catalog, sha pinned in the header record).
//
// Usage: node safehist_mask.mjs <n> <quartets.txt> <out.jsonl> [lo:hi]
// Determinism: no randomness, no timing in the output file.

import * as fs from 'node:fs';
import { createHash } from 'node:crypto';

const n = parseInt(process.argv[2], 10);
const quartetsPath = process.argv[3];
const outPath = process.argv[4];
const rangeArg = process.argv[5] ?? null;
let rangeLo = 0, rangeHi = n * n;
if (rangeArg !== null) {
  const m = rangeArg.match(/^(\d+):(\d+)$/);
  if (!m) throw new Error('bad range spec');
  rangeLo = parseInt(m[1], 10); rangeHi = parseInt(m[2], 10);
}
if (!(n >= 3 && n <= 9) || !quartetsPath || !outPath) throw new Error('usage: node safehist_mask.mjs <n> <quartets.txt> <out.jsonl> [lo:hi]');

const N = n * n;
const qt = fs.readFileSync(quartetsPath, 'utf8').split('\n').filter(t => t && !t.startsWith('n='));
const F = qt.length;
const qTextSha = createHash('sha256').update(fs.readFileSync(quartetsPath)).digest('hex');

// forbidQuads: 4 cell indices (ascending) per quartet
const quads = [];
for (let q = 0; q < F; q++) {
  const a = qt[q].split(' ').map(Number);
  if (a.length !== 4 || !(a[0] < a[1] && a[1] < a[2] && a[2] < a[3])) throw new Error('bad row ' + qt[q]);
  quads.push(a);
}

// tripleByCell[c]: for every quartet containing c, the mask of the other three
// cells, stored as TWO Uint32 words (lo = bits 0..31, hi = bits 32..63).
const cellTriples = Array.from({ length: N }, () => ({ los: [], his: [] }));
for (const [a, b, c, d] of quads) {
  for (const e of [a, b, c, d]) {
    let lo = 0, hi = 0;
    for (const o of [a, b, c, d]) if (o !== e) {
      if (o < 32) lo |= (1 << o); else hi |= (1 << (o - 32));
    }
    cellTriples[e].los.push(lo); cellTriples[e].his.push(hi);
  }
}

const hist = new Float64Array(N + 1);

// cur mask words
let curLo = 0, curHi = 0;

function placeable(c) {
  const ts = cellTriples[c];
  const n_ = ts.los.length;
  for (let i = 0; i < n_; i++) {
    const tLo = ts.los[i], tHi = ts.his[i];
    if ((curLo & tLo) === tLo && (curHi & tHi) === tHi) return false;
  }
  return true;
}

function dfs(start, depth) {
  hist[depth]++;
  for (let c = start; c < N; c++) {
    if (!placeable(c)) continue;
    if (c < 32) curLo |= (1 << c); else curHi |= (1 << (c - 32));
    dfs(c + 1, depth + 1);
    if (c < 32) curLo &= ~(1 << c); else curHi &= ~(1 << (c - 32));
  }
}

const t0 = Date.now();

if (rangeLo === 0) hist[0]++;
for (let c = rangeLo; c < rangeHi; c++) {
  if (!placeable(c)) continue;
  if (c < 32) curLo |= (1 << c); else curHi |= (1 << (c - 32));
  dfs(c + 1, 1);
  if (c < 32) curLo &= ~(1 << c); else curHi &= ~(1 << (c - 32));
}

let sum = 0, mx = -1;
const obj = {};
for (let s = 0; s <= N; s++) {
  const v = hist[s];
  if (v > 0) { obj[s] = v; sum += v; mx = s; }
}
const fd = fs.openSync(outPath, 'w');
fs.writeSync(fd, JSON.stringify({ type: 'header', impl: 'mask', n, N, F, quartets_sha256: qTextSha, first_stone_range: [rangeLo, rangeHi] }) + '\n');
fs.writeSync(fd, JSON.stringify({ type: 'safehist', impl: 'mask', histogram: JSON.stringify(obj), total_safe_subsets: sum, max_safe_size: mx }) + '\n');
fs.closeSync(fd);
console.log(JSON.stringify({ n, impl: 'mask', rangeLo, rangeHi, total: sum, maxSafe: mx, elapsedMs: Date.now() - t0 }));
